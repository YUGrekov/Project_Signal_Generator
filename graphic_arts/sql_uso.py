import traceback
from model_new import AI
from model_new import DI
from model_new import USO as Model
from model_new import HardWare as HW
from request_sql import RequestSQL
from general_functions import General_functions

T_HW = 'hardware'
T_AI = 'ai'
T_DI = 'di'
TYPE = 'USO'


class USO():
    '''Заполнение таблицы.'''
    def __init__(self):
        # self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицы на наличие и заполненость.'''
        modules = [T_HW, T_AI, T_DI]
        for modul in modules:
            result = self.request.check_table(modul)
            if not result:
                # self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица
                #                            {modul} отсутсвует''', 2)
                print(f'''SQL. {TYPE}. Таблица {modul} отсутсвует. Добавь!''')
                return False
            else:
                if not self.request.check_row_table(modul):
                    # self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица
                    #                            {modul} пустая. Заполни!''', 2)
                    print(f'SQL. {TYPE}. Таблица {modul} пустая. Заполни!')
                    return False
        return True

    def add_process(self, data, column, modul):
        if not len(data):
            return False

        for signal in data:
            self.entry_array[column] = f'{modul}[{signal.id}]'
        return True

    def ai_temp(self):
        '''Поиск температуры в шкафа.'''
        self.count_row += 1
        self.entry_array = {'id': f'{self.count_row}',
                            'variable': f'USO[{self.count_row}]',
                            'name': f'{self.uso.uso}'}

        temp = self.request.select_orm(AI,
                                       ((AI.name % (f'%{self.uso.uso}%')) &
                                        ((AI.tag % ('CST%')) | (AI.tag_eng % ('CST%')))),
                                       AI.name)
        if not self.add_process(temp, 'temperature', 'AI'):
            print(f'SQL. {TYPE}. {self.uso.uso} - Температура не найдена')
            # self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. {self.uso.uso} -
            #                            Температура не найдена''', 2)

    def entry_to_base(self, signal, tag):
        '''Добавление нового сигнала.'''
        num = f'0{signal.module}' if signal.module < 10 else f'{signal.module}'

        list_RS = dict(id=self.count_row,
                       variable=f'RS[{self.count_row}]',
                       name=signal.description,
                       pValue=f'{tag}_{num}.COM_CH[{signal.channel}]',
                       uso=signal.uso,
                       basket=signal.basket,
                       module=signal.module,
                       channel=signal.channel)

        self.request.write_base_orm(list_RS, Model)
        self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Добавлен
                                   новый сигнал: {self.count_row}''', 0)

    def add_uso(self):
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise
            # перед заполнением таблица должна быть пуста
            if self.request.count_row_orm(Model) > 0:
                print(f'SQL. {TYPE}. Таблица заполнена. Перед заполнением необходимо очистить таблицу')
                # self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица заполнена.
                #                            Перед заполнением необходимо
                #                            очистить таблицу''', 2)
                raise
            data_uso = self.request.non_repea_names(HW, HW.uso, HW.uso)
            self.count_row = 0

            for self.uso in data_uso:
                # Температура шкафа
                self.ai_temp()
                # Двери открыты
                # self.di_door(uso.uso)
                # Остальные сигналы
                # self.di_all(uso.uso)

                # self.entry_to_base()

            # self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Работа
            #                            с таблицей завершена''', 1)
        except Exception:
            print(traceback.format_exc())
            # self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Ошибка
            #                            {traceback.format_exc()}''', 2)


a = USO()
a.add_uso()