import traceback
from model_new import HardWare
from model_new import connect
from request_sql import RequestSQL
from general_functions import General_functions


T_SIGNALS = 'signals'
C_USO = 'uso'


class HW():
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

    def add_const_row(self, uso):
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
        self.request.write_base_orm(const_row, HardWare)

    def add_kk_row(self, uso, count: int):
        '''Добавление в базу KK по необходимости.'''
        const_row = [
            {'id': f'{count}', 'uso': uso,
             'variable': f'countsErrDiag[{count}]', 'basket': f'{count}',
             'type_0': 'MK-550-024', 'variable_0': 'PSU',
             'type_1': 'MK-544-040', 'variable_1': 'EthEx;3',
             'type_2': 'MK-504-120', 'variable_2': 'CPU;7'},
            {'id': f'{count}', 'uso': uso,
             'variable': f'countsErrDiag[{count}]', 'basket': f'{count}',
             'type_0': 'MK-550-024', 'variable_0': 'PSU',
             'type_1': 'MK-544-040', 'variable_1': 'EthEx;3',
             'type_2': 'MK-504-120', 'variable_2': 'CPU;7'}
        ]
        self.request.write_base_orm(const_row, HardWare)
    
    def fill_hw(self, isflag: bool):
        '''Заполнение таблицы.'''
        fl_kc = False
        countsErrDiag = 2
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise
            # Находим названия неповторяющихся шкафов
            all_uso = self.request.non_repeating_names(T_SIGNALS, C_USO, C_USO)
            for uso in all_uso:
                # Добавляем один раз, постоянные строки - контроллеры
                if not fl_kc:
                    self.add_const_row(uso[0])
                    fl_kc = True
                if isflag:
                    self.add_const_row(uso[0])



            print('SQL. Hardware. Таблица заполнена')
            # self.logsTextEdit.logs_msg('''SQL. Hardware.
            #                            Таблица заполнена''', 1)
        except Exception:
            print({traceback.format_exc()})
            # self.logsTextEdit.logs_msg(f'''SQL. Hardware. Ошибка
            #                            {traceback.format_exc()}''', 2) 


# a = HW()
# a.fill_hw()
name = ['МНА032', 'НА', 'на', 'sdaf']
for i in name:
    if 'НА' in i:
        print(i)









# def getting_modul(self, kk_is_True):
#     msg = {}
#     list_type = {'CPU': 'MK-504-120', 'PSU': 'MK-550-024', 'CN': 'MK-545-010', 'MN' : 'MK-546-010', 'AI'    : 'MK-516-008A',
#                     'AO' : 'MK-514-008', 'DI' : 'MK-521-032', 'RS': 'MK-541-002', 'DO' : 'MK-531-032', 'EthEx' : 'MK-544-040'}
#     with db:
#         try:
#             if self.dop_function.empty_table('signals'): 
#                 msg[f'{today} - Таблица: signals пустая! Заполни таблицу!'] = 2
#                 return msg

#             self.cursor.execute(f'''SELECT DISTINCT uso 
#                                     FROM signals
#                                     ORDER BY uso''')
#             list_uso = self.cursor.fetchall()

#             temp_flag    = False
#             test_s       = []
#             count_basket = 0
#             count_AI, count_AO, count_EthEx = 0, 0, 0
#             count_DI, count_DO, count_RS = 0, 0, 0 
#             for uso in list_uso:
#                 self.cursor.execute(f"""SELECT DISTINCT basket 
#                                         FROM signals
#                                         WHERE uso='{uso[0]}'
#                                         ORDER BY basket""")
#                 list_basket = self.cursor.fetchall()

#                 # ЦК в количестве 2 - ONE!
#                 if temp_flag is False:
#                     for i in range(2):
#                         uso_kk = uso[0]
#                         test_s.append(dict(uso = uso[0], variable = f'countsErrDiag[{i + 1}]', tag = '',
#                                             basket  = i + 1, powerLink_ID ='', Pic = '',
#                                             type_0  = f'MK-550-024', variable_0 = f'PSU',   type_1 = f'MK-546-010', variable_1 = f'MN;3',
#                                             type_2  = f'MK-504-120', variable_2 = f'CPU;7', type_3 = f'',           variable_3 = f'',
#                                             type_4  = f'',           variable_4 = f'',      type_5 = f'',           variable_5 = f'',
#                                             type_6  = f'',           variable_6 = f'',      type_7 = f'',           variable_7 = f'',
#                                             type_8  = f'',           variable_8 = f'',      type_9 = f'',           variable_9 = f'',
#                                             type_10 = f'',           variable_10= f'',      type_11= f'',           variable_11= f'',
#                                             type_12 = f'',           variable_12= f'',      type_13= f'',           variable_13= f'',
#                                             type_14 = f'',           variable_14= f'',      type_15= f'',           variable_15= f'',
#                                             type_16 = f'',           variable_16= f'',      type_17= f'',           variable_17= f'',
#                                             type_18 = f'',           variable_18= f'',      type_19= f'',           variable_19= f'',
#                                             type_20 = f'',           variable_20= f'',      type_21= f'',           variable_21= f'',
#                                             type_22 = f'',           variable_22= f'',      type_23= f'',           variable_23= f'',
#                                             type_24 = f'',           variable_24= f'',      type_25= f'',           variable_25= f'',
#                                             type_26 = f'',           variable_26= f'',      type_27= f'',           variable_27= f'',
#                                             type_28 = f'',           variable_28= f'',      type_29= f'',           variable_29= f'',
#                                             type_30 = f'',           variable_30= f'',      type_31= f'',           variable_31= f'',
#                                             type_32 = f'',           variable_32= f''))
#                     temp_flag = True
#                 for basket in list_basket:
#                     count_basket     += 1
#                     list_hw           = {}
#                     list_hw['uso']    = uso[0]    
#                     list_hw['basket'] = basket[0] 

#                     # Если в проекте есть КК
#                     if kk_is_True and count_basket == 3:
#                         for i in range(4, 6, 1):
#                             test_s.append(dict(uso        = uso_kk,
#                                                 variable   = f'countsErrDiag[{i + 1}]',
#                                                 tag        = '',
#                                                 basket     = i + 1,
#                                                 type_0     = 'MK-550-024',
#                                                 variable_0 = f'PSU',
#                                                 type_1     = f'MK-544-040',
#                                                 variable_1 = f'EthEx;3',
#                                                 type_2     = f'MK-504-120',
#                                                 variable_2 = f'CPU;7'))

#                     self.cursor.execute(f"""SELECT DISTINCT module, type_signal 
#                                             FROM signals
#                                             WHERE uso='{uso[0]}' AND basket={basket[0]}
#                                             ORDER BY module""")
#                     req_modul = self.cursor.fetchall()
#                     for i in req_modul:
#                         if i[1] is None or i[1] == '' or i[1] == ' ': 
#                             type_kod = 'Неопределен!'
#                             type_mod = 'Неопределен!'
#                             msg[f'{today} - Таблица: Hardware. {uso[0]}.A{basket[0]}.{i[0]} тип не определен!'] = 2
#                         else:
#                             for key, value in list_type.items():
#                                 if str(i[1]).find(key) != -1: 
#                                     if key == 'AI': 
#                                         count_AI += 1
#                                         type_mod = f'{key}[{count_AI}]'
#                                     elif key == 'AO': 
#                                         count_AO += 1
#                                         type_mod = f'{key}[{count_AO}]'
#                                     elif key == 'DI': 
#                                         count_DI += 1
#                                         type_mod = f'{key}[{count_DI}]'
#                                     elif key == 'DO': 
#                                         count_DO += 1
#                                         type_mod = f'{key}[{count_DO}]'
#                                     elif key == 'RS': 
#                                         count_RS += 1
#                                         type_mod = f'RS[{count_RS}];3'
#                                     elif key == 'EthEx': 
#                                         count_EthEx += 1
#                                         type_mod = f'{key}[{count_EthEx}]'
#                                     else:
#                                         type_mod = key
#                                     type_kod = value

#                         if   kk_is_True and (count_basket == 1 or count_basket == 2):
#                             list_hw['id'] = count_basket + 2
#                         else:
#                             list_hw['id'] = count_basket + 4
                        
#                         list_hw['variable']        = f'countsErrDiag[]'
#                         list_hw['tag']             = ''
#                         list_hw['powerLink_ID']    = count_basket
#                         list_hw['type_0']          = 'MK-550-024'
#                         list_hw['variable_0']      = 'PSU'
#                         list_hw['type_1']          = 'MK-545-010'
#                         list_hw['variable_1']      = 'CN;3'
#                         list_hw[f'type_{i[0]}']     = type_kod
#                         list_hw[f'variable_{i[0]}'] = type_mod
#                     test_s.append(list_hw)

#             # Checking for the existence of a database
#             HardWare.insert_many(test_s).execute()
#             msg[f'{today} - Таблица: hardware заполнена'] = 1
#         except Exception:
#             msg[f'{today} - Таблица: hardware, ошибка при заполнении: {traceback.format_exc()}'] = 2
#         msg[f'{today} - Таблица: hardware, выполнение кода завершено!'] = 1
#     return(msg)