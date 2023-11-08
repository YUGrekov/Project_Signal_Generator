import re
import traceback
from model_new import DI
from model_new import Signals
from request_sql import RequestSQL
from general_functions import General_functions

T_SIGNALS = 'signals'
T_HW = 'hardware'


class Diskrets():
    '''Заполнение таблицы.'''
    di_count = 0

    def __init__(self):
        # self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицу signals на наличие и заполненость.'''
        result = self.request.check_table(T_SIGNALS)
        if not result:
            print('''SQL. AI. Таблица signals отсутсвует или не заполнена''')
            # self.logsTextEdit.logs_msg('''SQL. DI. Таблица
            #                            signals отсутсвует
            #                            или не заполнена''', 2)
            return False
        return True

    def module_calc(self, uso, basket, module):
        '''Вычисление сквозного номера модуля для
        заполнения pValue, pHealth из таблицы HW.'''
        try:
            hw = self.request.where_select(T_HW, f'variable_{module}, tag',
                                           f'''"uso"='{uso}' and "basket"='{basket}' ''', 'id')
            if len(hw) > 1:
                print(f'SQL. DI. {uso}.A{basket}_{module}, при вычислении номера для pValue и pHealth обнаружено несколько модулей!')
                # self.logsTextEdit.logs_msg(f'''SQL. DI.
                #                            {uso}.A{basket}_{module},
                #                            при вычислении номера
                #                            для pValue и pHealth обнаружено
                #                            несколько модулей!''', 2)
                return 'NULL'
            return re.findall('\d+', hw[0][0])[0], hw[0][1]
        except Exception:
            print(f'SQL. DI. {uso}.A{basket}_{module}, номер модуля pValue и pHealth не найден!')
            # self.logsTextEdit.logs_msg(f'''SQL. DI. {uso}.A{basket}_{module},
            #                            номер модуля pValue и
            #                            pHealth не найден!''', 1)
            return 'NULL', None

    def process_request(self):
        '''Обработка нескольких запросов.'''
        where_1 = (Signals.tag % ('CSC%'))
        where_2 = (Signals.schema % ('DI%')) & (~(Signals.tag % ('CSC%')))
        where_3 = (Signals.schema % ('DM%')) & (Signals.type_signal % ('DI%'))
        where = [where_1, where_2, where_3]

        fl_empty = False if self.request.count_row_orm(DI) > 1 else True

        for order in range(3):
            data = self.request.select_orm(Signals, where[order],
                                           Signals.description)
            count_rez = 0 if order == 2 else int(len(data) * 0.3)
            # Проверяем, обновляем или добавляем сигнал
            self.check_signal(data)
            # Добавляем резервы
            if count_rez and fl_empty:
                self.add_empty_row(count_rez)

    def check_signal(self, data):
        '''Проверка сигнала на существование в таблице DI.
        По УСО, корзине, модулю и каналу.'''
        for signal in data:
            Diskrets.di_count += 1
            uso = signal.uso
            basket = signal.basket
            module = signal.module
            channel = signal.channel
            coinc = self.request.select_orm(DI,
                                            (DI.uso == uso) &
                                            (DI.basket == basket) &
                                            (DI.module == module) &
                                            (DI.channel == channel),
                                            DI.basket)
            for i in coinc:
                self.msg_id = i.id

            if bool(coinc):
                self.update_table(signal)
            else:
                num_through, tag = self.module_calc(signal.uso,
                                                    signal.basket,
                                                    signal.module)
                self.add_new_signal(signal, num_through, tag)

    def add_new_signal(self, signal, num_through, tag):
        '''Добавление нового сигнала.'''
        num = f'0{signal.module}' if signal.module < 10 else f'{signal.module}'
        try:
            if 'CSC' in signal.tag:
                group_di = 'Диагностика'
            elif 'EC' in signal.tag:
                group_di = 'Электроснабжение'
            else:
                group_di = 'Общие'
        except Exception:
            group_di = ''
        short_title = re.sub(r'\sшкаф.+[МНСПТРПСАР].+[0-9)КЦБРУ]', '', signal.description)

        list_DI = dict(id=Diskrets.di_count,
                       variable=f'DI[{Diskrets.di_count}]',
                       tag=signal.tag,
                       name=signal.description,
                       pValue=f'{tag}_{num}_DI[{signal.channel}]',
                       pHealth=f'mDI_HEALTH[{str(num_through)}]',
                       Inv=0,
                       ErrValue=0,
                       priority_0=1,
                       priority_1=1,
                       Msg=1,
                       tabl_msg='TblDiscretes',
                       group_diskrets=group_di,
                       msg_priority_0=1,
                       msg_priority_1=1,
                       short_title=short_title,
                       tag_eng=self.dop_function.translate(signal.tag),
                       uso=signal.uso,
                       basket=signal.basket,
                       module=signal.module,
                       channel=signal.channel)

        self.request.write_base_orm(list_DI, DI)
        print(f'SQL. DI. Добавлен новый сигнал: {Diskrets.di_count}')
        # self.logsTextEdit.logs_msg(f'''SQL. AI. Добавлен новый
        #                            сигнал: {AIParam.ai_count}''', 0)

    def add_empty_row(self, count_rez):
        '''Добавляем пустые строки для резерва.'''
        for i in range(Diskrets.di_count + 1, Diskrets.di_count + count_rez + 1):
            empty_row = dict(id=i,
                             variable=f'DI[{i}]',
                             tag=f'LOGIC_DI_{i}',
                             name='Переменная зарезервирована для логически формируемого сигнала',
                             tabl_msg='TblDiscretes',
                             group_diskrets='Общие')
            self.request.write_base_orm(empty_row, DI)
        Diskrets.di_count = Diskrets.di_count + count_rez

    def update_table(self, signal):
        '''Обновление тега и названия сигнала в таблице.'''
        coinc = self.request.select_orm(DI,
                                        (DI.tag == signal.tag) &
                                        (DI.name == signal.description),
                                        DI.basket)
        if not bool(coinc):
            self.request.update_base_orm(DI,
                                         {'tag': signal.tag,
                                          'name': signal.description},
                                         (DI.uso == signal.uso) &
                                         (DI.basket == signal.basket) &
                                         (DI.module == signal.module) &
                                         (DI.channel == signal.channel))
            print(f'SQL. DI. Строка обновлена: {self.msg_id}')
            # self.logsTextEdit.logs_msg(f'''SQL. DI.
            #                            Строка обновлена:
            #                            {self.msg_id}''', 0)

    def add_diskrets(self):
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise

            self.process_request()

            print('SQL. DI. Работа с таблицей завершена')
            # self.logsTextEdit.logs_msg('''SQL. DI. Работа
            #                            с таблицей завершена''', 1)
        except Exception:
            print({traceback.format_exc()})
            # self.logsTextEdit.logs_msg(f'''SQL. DI. Ошибка
            #                            {traceback.format_exc()}''', 2)