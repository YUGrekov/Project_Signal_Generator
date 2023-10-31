import traceback
from model_new import Signals
from request_sql import RequestSQL
from general_functions import General_functions

T_SIGNALS = 'signals'


class AI():
    name_m = 'AI[{}]'
    type_m = 'MK-516-008A'

    def counter(self, num):
        if AI.count == 0:
            a = AI.count + 1
        else:
            a = self.num
        return a

    def save_num(self, num):
        self.num = num


class AO():
    name_m = 'AO[{}]'
    type_m = 'MK-514-008'
    count = 0

    def counter(self):
        if AO.count == 0:
            a = AO.count + 1
        else:
            a = self.num
        return a

    def save_num(self, num):
        self.num = num


class DI():
    name_m = 'DI[{}]'
    type_m = 'MK-521-032'
    count = 0

    def counter(self):
        if DI.count == 0:
            a = DI.count + 1
        else:
            a = self.num
        return a

    def save_num(self, num):
        self.num = num


class DO():
    name_m = 'DO[{}]'
    type_m = 'MK-531-032'
    count = 0

    def counter(self):
        if DO.count == 0:
            a = DO.count + 1
        else:
            a = self.num
        return a

    def save_num(self, num):
        self.num = num


class RS():
    name_m = 'RS[{}];3'
    type_m = 'MK-541-002'
    count = 0

    def counter(self):
        if RS.count == 0:
            a = RS.count + 1
        else:
            a = self.num
        return a

    def save_num(self, num):
        self.num = num


class BaseUSO():
    '''Описания атрибутов и ссылки на классы.'''
    PARAM_MODULE = {'ai': AI,
                    'ao': AO,
                    'di': DI,
                    'do': DO,
                    'rs': RS
                    }


class HW(BaseUSO):
    '''Таблица Hardware.'''
    def __init__(self):
        # self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицу signals на наличие и заполненость.'''
        all_tables = self.request.get_tabl()
        if not self.dop_function.check_in_table(T_SIGNALS, all_tables):
            print('''SQL. Hardware. Таблица signals отсутсвует''')
            # self.logsTextEdit.logs_msg('''SQL. Hardware. Таблица
            #                            signals отсутсвует''', 2)
            return False
        if self.request.empty_table_check(T_SIGNALS):
            print('''SQL. Hardware. Таблица signals не заполнена''')
            # self.logsTextEdit.logs_msg('''SQL. Hardware. Таблица
            #                            signals не заполнена''', 2)
            return False
        return True

    def add_kc_row(self, uso):
        '''Добавление в базу ОСН и РЕЗ КЦ.'''
        const_row = [
            {'id': '1', 'uso': uso, 'variable': 'countsErrDiag[1]',
             'basket': '1',
             'type_0': 'MK-550-024', 'variable_0': 'PSU',
             'type_1': 'MK-546-010', 'variable_1': 'MN;3',
             'type_2': 'MK-504-120', 'variable_2': 'CPU;7'},
            {'id': '2', 'uso': uso, 'variable': 'countsErrDiag[2]',
             'basket': '2',
             'type_0': 'MK-550-024', 'variable_0': 'PSU',
             'type_1': 'MK-546-010', 'variable_1': 'MN;3',
             'type_2': 'MK-504-120', 'variable_2': 'CPU;7'}
        ]
        # self.request.write_base_orm(const_row, HardWare)

    def add_kk_row(self, uso, query):
        list_basket = [i.basket for i in query]
        count = max(list_basket) + 1
        '''Добавление в базу KK по необходимости.'''
        const_row = [
            {'id': f'{count}', 'uso': uso,
             'variable': f'countsErrDiag[{count}]', 'basket': f'{count}',
             'type_0': 'MK-550-024', 'variable_0': 'PSU',
             'type_1': 'MK-544-040', 'variable_1': 'EthEx;3',
             'type_2': 'MK-504-120', 'variable_2': 'CPU;7'},
            {'id': f'{count + 1}', 'uso': uso,
             'variable': f'countsErrDiag[{count + 1}]',
             'basket': f'{count + 1}',
             'type_0': 'MK-550-024', 'variable_0': 'PSU',
             'type_1': 'MK-544-040', 'variable_1': 'EthEx;3',
             'type_2': 'MK-504-120', 'variable_2': 'CPU;7'}
        ]
        # self.request.write_base_orm(const_row, HardWare)
        return min(list_basket) - 1, max(list_basket)

    def assembly_row(self, countsErr: int, pwl_id: int):
        """Повторное значение в строке.
        Args:
            countsErr (int): Счетчик ошибок для СУ.
            pwl_id (int): PowerLink_ID для СУ.

        Returns:
            dict: Словарь строки для добавления
        """
        return {'id': countsErr,
                'variable': countsErr,
                'powerLink_ID': pwl_id,
                'type_0': 'MK-550-024',
                'variable_0': 'PSU',
                'type_1': 'MK-545-010',
                'variable_1': 'CN;3',
                }

    def value_module(self):
        '''Выбираем корректное название,
        тип модуля и порядковый номер.'''
        for key, value in list_type.items():
            if str(i[1]).find(key) != -1: 
                if key == 'AI': 
                    count_AI += 1
                    type_mod = f'{key}[{count_AI}]'
                elif key == 'AO': 
                    count_AO += 1
                    type_mod = f'{key}[{count_AO}]'
                elif key == 'DI': 
                    count_DI += 1
                    type_mod = f'{key}[{count_DI}]'
                elif key == 'DO': 
                    count_DO += 1
                    type_mod = f'{key}[{count_DO}]'
                elif key == 'RS': 
                    count_RS += 1
                    type_mod = f'RS[{count_RS}];3'
                elif key == 'EthEx': 
                    count_EthEx += 1
                    type_mod = f'{key}[{count_EthEx}]'
                else:
                    type_mod = key
                type_kod = value

    def fill_hw(self, kk_flag: bool):
        """Заполнение таблицы.
        Args:
            kk_flag (bool): Нужен ли КК
        """
        temp_flag = False
        powerLink_ID = 0
        counts_uso = 0
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise
            # Находим названия неповторяющихся шкафов
            all_uso = self.request.non_repea_names(Signals,
                                                   Signals.uso,
                                                   Signals.uso)
            for name in all_uso:
                counts_uso += 1
                # Кол-во корзин в УСО
                count_b = self.request.non_repea_cond(Signals, Signals.basket,
                                                      Signals.uso == name.uso,
                                                      Signals.basket)
                # Один раз, постоянные строки-КЦ, КК
                if not temp_flag:
                    self.add_kc_row(name.uso)
                    if kk_flag:
                        min_b, max_b = self.add_kk_row(name.uso, count_b)
                    temp_flag = True
                    countsErr_one = min_b
                    countsErr_new = max_b + 2

                if counts_uso <= 2:
                    countsErr = countsErr_one if counts_uso == 1 else countsErr_new

                for number in count_b:
                    powerLink_ID += 1
                    countsErr += 1

                    data_basket = self.request.non_repea_cond(Signals,
                                                              Signals.module,
                                                              (Signals.uso == number.uso) & (Signals.basket == number.basket),
                                                              Signals.module)

                    write_array = self.assembly_row(countsErr, powerLink_ID)
                    for data in data_basket:
                        module_s = data.module
                        type_s = data.type_signal

                        for type_m, variable_m in self.PARAM_MODULE.items():

                            if (str(type_s).lower() in type_m):
                                n = variable_m.counter(self)
                                variable_m.save_num(self, n)

                                print(n)

                                write_array[f'type_{module_s}'] = variable_m.type_m
                                write_array[f'variable_{module_s}'] = f'{variable_m.name_m}'.format(countsErr)
                    print(write_array)

            print('SQL. Hardware. Таблица заполнена')
            # self.logsTextEdit.logs_msg('''SQL. Hardware.
            #                            Таблица заполнена''', 1)
        except Exception:
            print({traceback.format_exc()})
            # self.logsTextEdit.logs_msg(f'''SQL. Hardware. Ошибка
            #                            {traceback.format_exc()}''', 2)


a = HW()
a.fill_hw(True)