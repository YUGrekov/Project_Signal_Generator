from peewee import *
from playhouse.migrate import *

# from gen_gui import MainWin
# from PyQt5.QtWidgets import QApplication
# app = QApplication([])

# win_ = MainWin()
# path_prj = win_.launch()

path_to_exel = f'D:\\Development\\New_SQL_generator\\Working_draft_SQL\\sqllite_database\\П3 - КЗФКП Аксинино-2_MK500_20230405.xlsx'
path_to_base = f'D:\\Development\\New_SQL_generator\\Working_draft_SQL\\sqllite_database\\asutp.db'

path_to_exel = 'D:\\Development\\New_SQL_generator\\Working_draft_SQL\\sqllite_database\\П3 - КЗФКП Аксинино-2_MK500_20230405.xlsx'
path_sample  = 'D:\Development\Generation_msg\Sample\\'
path_location_file = 'D:\Development\Generation_msg\Script\\'
name_project = 'Тест'
prefix_system = ''
path_to_devstudio = 'D:\Проекты\НПС-Бисер\project\\typical_prj\\'
path_su = 'D:\Development\Generation_msg\SU\\'
path_rest = ''
path_hmi = 'D:\\Development\\Generation_msg\\HMI'
path_hmi_sample = 'D:\\Development\\Generation_msg\\HMI'

database_msg = 'asutp_temp'
user_msg = 'postgres'
password_msg = 'postgres'
host_msg = 'localhost'
port_msg = '5432'

database_prj = 'asutp'
user_prj = 'postgres'
password_prj = 'postgres'
host_prj = 'localhost'
port_prj = '5432'

# with open(path_prj) as paths:
#     for string in paths:
#         split_str = string.strip().split(': ')
#         if split_str[0] == 'path_to_kzfkp':
#             path_to_exel = split_str[1]
#         if split_str[0] == 'path_sample':
#             path_sample = split_str[1]
#         if split_str[0] == 'path_location_file':
#             path_location_file = split_str[1]
#         if split_str[0] == 'name_project':
#             name_project = split_str[1]
#         if split_str[0] == 'prefix_system':
#             prefix_system = split_str[1]
#         if split_str[0] == 'path_to_devstudio':
#             path_to_devstudio = split_str[1]
#         if split_str[0] == 'path_su':
#             path_su = split_str[1]
#         if split_str[0] == 'path_rest:':
#             path_rest = split_str[1]

#         if split_str[0] == 'database_msg':
#             database_msg = split_str[1]
#         if split_str[0] == 'user_msg':
#             user_msg = split_str[1]
#         if split_str[0] == 'password_msg':
#             password_msg = split_str[1]
#         if split_str[0] == 'host_msg':
#             host_msg = split_str[1]
#         if split_str[0] == 'port_msg':
#             port_msg = split_str[1]
        
#         if split_str[0] == 'database':
#             database_prj = split_str[1]
#         if split_str[0] == 'user':
#             user_prj = split_str[1]
#         if split_str[0] == 'password':
#             password_prj = split_str[1]
#         if split_str[0] == 'host':
#             host_prj = split_str[1]
#         if split_str[0] == 'port':
#             port_prj = split_str[1]


db = PostgresqlDatabase(database_msg, user=user_msg, password=password_msg, host=host_msg, port=port_msg)
db_prj = PostgresqlDatabase(database_prj, user=user_prj, password=password_prj, host=host_prj, port=port_prj)

migrator = SqliteMigrator(db)


class BaseModel(Model):
    class Meta:
        database = db
        order_by = id

rus_list = {'signals': {'id':'№', 'type_signal':'Тип сигнала', 'uso':'Шкаф', 'tag':'Идентификатор', 'description':'Наименование', 
                        'schema':'Схема', 'klk':'Клеммник', 'contact':'Контакт', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'di': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                   'pValue':'Ссылка на входное\nзначение сигнала', 'pHealth':'Ссылка на исправность\nканала','Inv':'Инвертировать\nвходное значение',
                   'ErrValue':'Значение, выставляемое в stateDI[..].Value\nпри неиcправности канала',
                   'priority_0':'Приоритет при 0', 'priority_1':'Приоритет при 1', 'Msg':'Выдавать сообщения\nпо изменению сигнала',
                   'isDI_NC':'isDI_NC', 'isAI_Warn':'isAI_Warn', 'isAI_Avar':'isAI_Avar',
                   'pNC_AI':'pNC_AI', 'TS_ID':'TS ID для быстрых сигналов', 'isModuleNC':'isModuleNC', 'Pic':'Pic', 
                   'tabl_msg':'Таблица сообщений',
                   'group_diskrets':'Группа дискретов.\nГруппировка в архивном журнале', 'msg_priority_0':'Приоритет\nсообщения при 0', 
                   'msg_priority_1':'Приоритет\nсообщения при 1', 'short_title':'Короткое название', 
                   'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'do': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'pValue':'Ссылка на входное\nзначение сигнала', 
                   'pHealth':'Ссылка на исправность\nканала', 'short_title':'Короткое название', 'tabl_msg':'Таблица сообщений',
                   'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},

            'rs': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'array_number_modul':'№ модуля в\nмассиве mRS', 
                   'pValue':'Ссылка на входное\nзначение сигнала', 'pHealth':'Ссылка на исправность\nканала', 'Pic':'Pic',
                   'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'hardware': {'id':'№', 'variable':'Переменная', 'tag':'Идентификатор\n(не генерится!)', 'uso':'Шкаф', 'basket':'Корзина',
                         'type_0':'Тип модуля 0',   'variable_0':'Переменная модуля 0',   'type_1':'Тип модуля 1',   'variable_1':'Переменная модуля 1',  
                         'type_2':'Тип модуля 2',   'variable_2':'Переменная модуля 2',   'type_3':'Тип модуля 3',   'variable_3':'Переменная модуля 3',  
                         'type_4':'Тип модуля 4',   'variable_4':'Переменная модуля 4',   'type_5':'Тип модуля 5',   'variable_5':'Переменная модуля 5',
                         'type_6':'Тип модуля 6',   'variable_6':'Переменная модуля 6',   'type_7':'Тип модуля 7',   'variable_7':'Переменная модуля 7',  
                         'type_8':'Тип модуля 8',   'variable_8':'Переменная модуля 8',   'type_9':'Тип модуля 9',   'variable_9':'Переменная модуля 9',  
                         'type_10':'Тип модуля 10', 'variable_10':'Переменная модуля 10', 'type_11':'Тип модуля 11', 'variable_11':'Переменная модуля 11',
                         'type_12':'Тип модуля 12', 'variable_12':'Переменная модуля 12', 'type_13':'Тип модуля 13', 'variable_13':'Переменная модуля 13', 
                         'type_14':'Тип модуля 14', 'variable_14':'Переменная модуля 14', 'type_15':'Тип модуля 15', 'variable_15':'Переменная модуля 15', 
                         'type_16':'Тип модуля 16', 'variable_16':'Переменная модуля 16', 'type_17':'Тип модуля 17', 'variable_17':'Переменная модуля 17',
                         'type_18':'Тип модуля 18', 'variable_18':'Переменная модуля 18', 'type_19':'Тип модуля 19', 'variable_19':'Переменная модуля 19', 
                         'type_20':'Тип модуля 20', 'variable_20':'Переменная модуля 20', 'type_21':'Тип модуля 21', 'variable_21':'Переменная модуля 21', 
                         'type_22':'Тип модуля 22', 'variable_22':'Переменная модуля 22', 'type_23':'Тип модуля 23', 'variable_23':'Переменная модуля 23',
                         'type_24':'Тип модуля 24', 'variable_24':'Переменная модуля 24', 'type_25':'Тип модуля 25', 'variable_25':'Переменная модуля 25', 
                         'type_26':'Тип модуля 26', 'variable_26':'Переменная модуля 26', 'type_27':'Тип модуля 27', 'variable_27':'Переменная модуля 27', 
                         'type_28':'Тип модуля 28', 'variable_28':'Переменная модуля 28', 'type_29':'Тип модуля 29', 'variable_29':'Переменная модуля 29',
                         'type_30':'Тип модуля 30', 'variable_30':'Переменная модуля 30', 'type_31':'Тип модуля 31', 'variable_31':'Переменная модуля 31', 
                         'type_32':'Тип модуля 32', 'variable_32':'Переменная модуля 32'},
            
            'uso': {'id':'№','variable':'Переменная', 'name':'Название', 'temperature':'Температура\nшкафа', 'door':'Двери открыты', 
                         'signal_1':'Сигнал 1', 'signal_2':'Сигнал 2', 'signal_3':'Сигнал 3', 'signal_4':'Сигнал 4', 'signal_5':'Сигнал 5', 
                         'signal_6':'Сигнал 6', 'signal_7':'Сигнал 7', 'signal_8':'Сигнал 8', 'signal_9':'Сигнал 9', 'signal_10':'Сигнал 10', 
                         'signal_11':'Сигнал 11', 'signal_12':'Сигнал 12', 'signal_13':'Сигнал 13', 'signal_14':'Сигнал 14', 'signal_15':'Сигнал 15', 
                         'signal_16':'Сигнал 16', 'signal_17':'Сигнал 17', 'signal_18':'Сигнал 18', 'signal_19':'Сигнал 19', 'signal_20':'Сигнал 20', 
                         'signal_21':'Сигнал 21', 'signal_22':'Сигнал 22', 'signal_23':'Сигнал 23', 'signal_24':'Сигнал 24', 'signal_25':'Сигнал 25', 
                         'signal_26':'Сигнал 26', 'signal_27':'Сигнал 27', 'signal_28':'Сигнал 28', 'signal_29':'Сигнал 29', 'signal_30':'Сигнал 30', 
                         'signal_31':'Сигнал 31', 'signal_32':'Сигнал 32'},
            
            'ao': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'pValue':'Ссылка на входное значение сигнала',
                   'pHealth':'Ссылка на исправность канала', 'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'ai': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'pValue':'Ссылка на входное\nзначение сигнала',
                   'pHealth':'Ссылка на исправность\nканала','AnalogGroupId':'Группа аналогов',
                   'SetpointGroupId':'Группа уставок\nаналогов', 'Egu':'Единица измерения', 'sign_VU':'Подпись для ВУ', 
                   'IsOilPressure':'Давление нефти/нефтепродукта\n(флаг для пересчета в кгс/см2)', 'number_NA_or_aux':'Номер НА или вспом.', 
                   'IsPumpVibration':'Вибрация насоса', 'vibration_motor':'Вибрация ЭД', 'current_motor':'Ток ЭД НА', 
                   'aux_outlet_pressure':'Давление на вых. вспом.', 'number_ust_min_avar':'№ уставки мин. авар.', 
                   'number_ust_min_pred':'№ уставки мин. пред.', 'number_ust_max_pred':'№ уставки макс. пред.', 'number_ust_max_avar':'№ уставки макс. авар.', 
                   'LoLimField':'Пол. мин.', 'HiLimField':'Пол. макс.', 'LoLimEng':'Инж. Мин.', 'HiLimEng':'Инж. Макс.', 'LoLim':'Достоверность мин.', 
                   'HiLim':'Достоверность макс.', 'Histeresis':'Гистерезис', 'TimeFilter':'Фильтрация', 
                   'Min6':'Мин.6', 'Min5':'Мин.5', 'Min4':'Мин.4', 'Min3':'Мин.3', 'Min2':'Мин.2', 'Min1':'Мин.', 
                   'Max1':'Макс.', 'Max2':'Макс.2', 'Max3':'Макс.3', 'Max4':'Макс.4', 'Max5':'Макс.5', 'Max6':'Макс.6', 
                   'MsgMask':'''Настройки уставок, Сообщение\nДвоичная маска, порядок следования битов: 15-резерв, 14-ВПД, 13-Макс6, 12-Макс5, 11-Макс4,\n10-Макс3, 9-Макс2, 8-Макс1, 7-Норма, 6-Мин1, 5-Мин2, 4-Мин3, 3-Мин4, 2-Мин5, 1-Мин6, 0-НПД''', 
                   'SigMask':'''Настройки уставок, Сигнализация\nДвоичная маска, порядок следования битов: 15-резерв, 14-ВПД, 13-Макс6, 12-Макс5, 11-Макс4,\n10-Макс3, 9-Макс2, 8-Макс1, 7-Норма, 6-Мин1, 5-Мин2, 4-Мин3, 3-Мин4, 2-Мин5, 1-Мин6, 0-НПД''', 
                    'CtrlMask':'''Маска контроля уставок при имитации\nМаска 16 бит. Порядок следования битов уставок: 15-13-резерв, 12-Недостоверность, 11-Макс6,\n10-Макс5, 9-Макс4, 8-Макс3, 7-Макс2, 6-Макс1, 5-Мин1, 4-Мин2, 3-Мин3, 2-Мин4, 1-Мин5, 0-Мин6''',
                   'Precision':'Отображаемая точность\nзначения', 'Pic':'Pic', 
                   'TrendingGroup':'Группа сброса трендов', 'DeltaT':'Гистерезис ТИ', 'PhysicEgu':'Единица измерения физической\nвеличины (АЦП)',
                   'RuleName':'Правило для карты\nуставок', 'fuse':'Предохранитель',
                   'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},

            'ktprp': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название',
                      'Number_PZ':'Номер PZ', 'Type':'Тип\n1 - авт., 2 - АПУ, 3 - с АРМ', 'Pic':'Pic', 
                      'number_list_VU':'Номер листа\n(для ВУ)', 'number_protect_VU':'Номер защиты\n(для ВУ)'},
            
            'ktpr': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название',
                     'avar_parameter':'Аварийный параметр\n(pInput)', 'DisableMasking':'Запрет маскирования\n(1 - запрет)', 
                     'auto_unlock_protection':'Автоматическая деблокировка \nзащиты (1 - разрешена)', 
                     'shutdown_PNS_a_time_delay_up_5s_after_turning':'Откл. ПНС с выдержкой времени до 5с\nпосле откл. всех МНА',
                     'bitmask_protection_group_membership':'Битовая маска принадлежности защиты группе\n(1 в N бите - разрешение сраб. данной защиты на N группе (плече))', 
                     'stop_type_NA':'Тип остановки НА:\n0-None, 1-ManageStop, 2-ElectricStop, 3-ManageStopOffVV\n4-ChRPAlarmStop, 5-StopAuto, 6-StopAuto2, 7-PovtorOtkl',
                     
                     'pump_station_stop_type':'''Тип остановки насосной станции:
                     1 - StopAllInShoulder - одновремменная остановка всех НА в плече, 2 - StopOneByOneInShoulder - последовательная остановка всех НА в плече, 
                     3 - StopFirstNextInShoulder - отключение первого по потоку нефти НА, и отключения следующего при сохранении авар. параметра, 
                     4 - StopOnlyirstInShoulder - отключение первого по потоку нефти НА, 5 - StopAllInSubShoulder - одновреммення остановка всех ПН в подплече''',

                     'closing_gate_valves_at_the_inlet_NPS':'Закрытие задвижек\nна входе НПС', 
                     'closing_gate_valves_at_the_outlet_NPS':'Закрытие задвижек\nна выходе НПС', 
                     'closing_gate_valves_between_PNS_and_MNS':'Закрытие задвижек\nмежду ПНС и МНС', 
                     'closing_gate_valves_between_RP_and_PNS':'Закрытие задвижек\nмежду РП и ПНС', 
                     'closing_valves_inlet_and_outlet_MNS':'Закрытие задвижек на\nвходе и выходе МНС', 
                     'closing_valves_inlet_and_outlet_PNS':'Закрытие задвижек на\nвходе и выходе ПНС', 
                     'closing_valves_inlet_and_outlet_MNA':'Закрытие задвижек на\nвходе и выходе МНА', 
                     'closing_valves_inlet_and_outlet_PNA':'Закрытие задвижек на\nвходе и выходе ПНА', 
                     'closing_valves_inlet_RD':'Закрытие задвижек на\nвходе узла РД', 
                     'closing_valves_outlet_RD':'Закрытие задвижек на\nвыходе узла РД', 
                     'closing_valves_inlet_SSVD':'Закрытие задвижек на\nвходе ССВД', 
                     'closing_valves_inlet_FGU':'Закрытие задвижек на\nвходе ФГУ', 
                     'closing_secant_valve_connection_unit__oil_production_oil':'Закрытие секущей задвижки узла\nподключения объекта нефтедобычи',
                     'closing_valves_inlet_RP':'Закрытие задвижек на\nвходе РП', 
                     'reserve_protect_14':'Резерв(14 бит)', 
                     'reserve_protect_15':'Резерв(15 бит)',

                     'shutdown_oil_pumps':'Отключение\nмаслонасосов', 
                     'shutdown_oil_pumps_after_signal_stopped_NA':'Отключение маслонасосов\nпосле сигнала "остановлен" НА', 
                     'shutdown_circulating_water_pumps':'Отключение насосов\nоборотного водоснабжения', 
                     'shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS':'Отключение насосов откачки\nиз емкостей сбора утечек МНС', 
                     'shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS':'Отключение насосов откачки\nиз емкостей сбора утечек ПНС', 
                     'shutdown_pumps_pumping_out_from_tanks_SSVD':'Отключение насосов откачки\nиз емкостей ССВД',
                     'switching_off_the_electric_room_fans':'Отключение беспромвальных\nвентиляторов электрозала', 
                     'shutdown_of_booster_fans_ED':'Отключение подпорных\nвентиляторов ЭД', 
                     'shutdown_of_retaining_fans_of_the_electrical_room':'Отключение подпорных\nвентиляторов электрозала', 
                     'shutdown_of_ED_air_compressors':'Отключение компрессоров\nподпора воздуха ЭД', 
                     'shutdown_pumps_providing_oil':'Отключение насосов, обеспечивающих\nподкачку нефти от объектов нефтедобычи', 
                     'disabling_pumps_for_pumping_oil_oil_products_through_BIC':'Отключение насосов прокачки\nнефти через БИК', 
                     'shutdown_domestic_and_drinking_water_pumps':'Отключение насосов\nхоз-питьевого водоснабжения', 
                     'shutdown_of_art_well_pumps':'Отключение насосов\nартскважин', 
                     'AVO_shutdown':'Отключение АВО', 
                     'shutdown_of_water_cooling_fans_circulating_water_supply_system':'Отключение вентиляторов водоохлаждения\nсистемы оборотного водоснабжения', 
                    
                     'shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS':'Отключение вытяжных\nвентиляторов насосного зала МНС', 
                     'shutdown_of_exhaust_fans_of_the_pumping_room_PNS':'Отключение вытяжных\nвентиляторов насосного зала ПНС', 
                     'shutdown_of_exhaust_fans_in_the_centralized_oil_system_room':'Отключение вытяжных вентиляторов\nв помещении централизованной маслосистемы', 
                     'shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room':'Отключение вытяжных вентиляторов\nмаслоприямка в электрозале', 
                     'shutdown_of_exhaust_fans_in_the_RD_room':'Отключение вытяжных\nвентиляторов в помещении РД', 
                     'shutdown_of_exhaust_fans_in_the_SSVD_room':'Отключение вытяжных\nвентиляторов в помещении ССВД', 
                     'shutdown_of_the_roof_fans_of_the_MNS_pump_room':'Отключение крышных\nвентиляторов насосного зала МНС', 
                     'shutdown_of_the_roof_fans_of_the_PNS_pump_room':'Отключение крышных\nвентиляторов насосного зала ПНС', 
                     'switching_off_the_supply_fans_pumping_room_of_the_MNS':'Отключение приточных вентиляторов\nнасосного зала МНС и закрытие\nогнезадерживающих клапанов', 
                     'switching_off_the_supply_fans_pumping_room_of_the_PNS':'Отключение приточных вентиляторов\nнасосного зала ПНС и закрытие\nогнезадерживающих клапанов', 
                     'switch_off_the_supply_fans_in_the_centralized_oil':'Отключение приточных вентиляторов\nв помещении централизованной маслосистемы и\nзакрытие огнезадерживающих клапанов', 
                     'switching_off_the_supply_fan_of_the_RD_room':'Отключение приточного\nвентилятора помещения РД', 
                     'switching_off_the_supply_fan_of_the_SSVD_room':'Отключение приточного\nвентилятора помещения ССВД', 
                     'switching_off_the_supply_fans_of_the_ED_air_compressor':'Отключение приточных вентиляторов\nпомещения компрессорной подпора воздуха ЭД\nи закрытие огнезадерживающих клапанов', 
                     'switching_off_the_supply_fan_of_the_BIK_room':'Отключение приточного\nвентилятора помещения БИК', 
                     'switching_off_the_supply_fan_of_the_SIKN_room':'Отключение приточного\nвентилятора помещения СИКН', 

                     'closing_the_air_valves_louvered_grilles_of_the_pump_room':'Закрытие воздушных клапанов\n(жалюзийных решёток) насосного зала', 
                     'closing_of_air_valves_louvered_grilles_of_the_compressor_room':'Закрытие воздушных клапанов\n(жалюзийных решёток) помещения компрессорной\nподпора воздуха ЭД', 
                     'shutdown_of_electric_oil_heaters':'Отключение электронагревателей\nмасла', 
                     'shutdown_of_the_electric_heaters_of_the_leakage_collection_MNS':'Отключение электронагревателей\nемкости сбора утечек МНС', 
                     'shutdown_of_the_electric_heaters_of_the_leakage_collection_PNS':'Отключение электронагревателей\nемкости сбора утечек ПНС', 
                     'shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank':'Отключение электронагревателей\nемкости сбора утечек СИКН', 
                     'shutdown_of_air_coolers_of_the_locking_system_MNA':'Отключение воздушных охладителей\nсистемы запирания торцовых уплотнений\nвсех МНА', 
                     'shutdown_of_air_coolers_of_the_locking_system_disc_NA':'Отключение воздушных охладителей\nсистемы запирания торцовых уплотнений\nотключенных НА', 
                     'shutdown_of_the_external_cooling_circuit_ChRP_MNA':'Отключение внешнего контура\nохлаждения ЧРП МНА', 
                     'shutdown_of_the_external_cooling_circuit_ChRP_PNA':'Отключение внешнего контура\nохлаждения ЧРП ПНА', 
                     'shutdown_of_locking_system_pumps':'Отключение насосов\nсистемы запирания',
                     'shutdown_of_pumps_for_pumping_oil_oil_products_through':'Отключение насосов прокачки нефти\nчерез оперативный БИК', 
                     'shutdown_of_pumping_pumps_from_leakage_collection_tanks':'Отключение насосов откачки из\nемкостей сбора утечек всех СИКН', 
                     'shutdown_of_anticondensation_electric_heaters_ED':'Отключение антиконденсационных\nэлектронагревателей ЭД', 
                     'fire_protection':'Защита по пожару', 
                     'reserve_aux_15':'Резерв(15 бит)', 

                     'value_ust':'Временная уставка', 
                     'Pic':'Pic',
                     'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок', 'number_list_VU':'Номер листа (для ВУ)', 'number_protect_VU':'Номер защиты (для ВУ)'},
            
            'ktpra': {'id':'№', 'id_num':'Номер защиты', 'variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'NA':'Имя НА', 'avar_parameter':'Аварийный параметр', 
                    'stop_type':'''Тип остановки(0 - None,\n1 - ManageStop,\n2 - ElectricStop,\n3 - ManageStopOffVV,\n4 - ChRPAlarmStop,\n5 - StopAuto,\n6 - StopAuto2,\n7 - PovtorOtkl1)''',  
                    'AVR':'Флаг необходимости АВР\nНА при срабатывании защиты' , 'close_valves':'Флаг необходимости закрытия\nагрегатных задвижек НА\nпри срабатывании защиты', 
                    'DisableMasking':'Флаг запрета маскирования', 'value_ust':'Временная уставка', 
                    'Pic':'Pic', 'group_ust':'Группа уставок', 
                    'rule_map_ust':'Правило для карты уставок', 
                    'number_list_VU':'Номер листа (для ВУ)', 'number_protect_VU':'Номер защиты (для ВУ)', 'number_pump_VU':'Номер агрегата (для ВУ)'},
            
            'ktprs': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название',
                       'drawdown':'Сработка', 'reference_to_value':'Ссылка на значение', 'priority_msg_0':'Приоритет сообщ. при 0', 
                       'priority_msg_1':'Приоритет сообщ. при 1',
                       'prohibition_issuing_msg':'Запрет выдачи сообщений', 
                       'Pic':'Номера листов на которых данный сигнал участвует в формировании рамки квитирования'},
            
            'gmpna': {'id':'№', 'id_num':'Номер защиты', 'variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'name_for_Chrp_in_local_mode':'Название для ЧРП в местном режиме', 'NA':'Имя НА', 'used_time_ust':'Использовать временную уставку', 
                      'value_ust':'Уставка', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок', 
                      'number_list_VU':'Номер листа (для ВУ)', 'number_protect_VU':'Номер защиты (для ВУ)', 'number_pump_VU':'Номер агрегата (для ВУ)'},
            
            'umpna':{'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'vv_included':'ВВ Включен', 'vv_double_included':'ВВ Включен дубль', 'vv_disabled':'ВВ отключен', 'vv_double_disabled':'ВВ отключен дубль', 
                     'current_greater_than_noload_setting':'Сила тока > уставки\nхолостого хода', 'serviceability_of_circuits_of_inclusion_of_VV':'Исправность цепей\nвключения ВВ',
                     'serviceability_of_circuits_of_shutdown_of_VV':'Исправность цепей\nотключения ВВ', 'serviceability_of_circuits_of_shutdown_of_VV_double':'Исправность цепей\nотключения ВВ дубль', 'stop_1':'Стоп 1', 
                     'stop_2':'Стоп 2', 'stop_3':'Стоп 3', 'stop_4':'Стоп 4', 
                     'monitoring_the_presence_of_voltage_in_the_control_current':'Сигнал «Контроль наличия напряжения\nв цепях оперативного тока»', 
                     'voltage_presence_flag_in_the_ZRU_motor_cell':'Флаг наличия напряжения\nв двигательной ячейке ЗРУ', 'vv_trolley_rolled_out':'Тележка ВВ выкачена', 
                     'remote_control_mode_of_the_RZiA_controller':'Дистанционный режим управления\nконтроллера РЗиА', 
                     'availability_of_communication_with_the_RZiA_controller':'Наличие связи с\nконтроллером РЗиА', 
                     'the_state_of_the_causative_agent_of_ED':'Состояние возбудителя ЭД', 'engine_prepurge_end_flag':'Флаг окончания предпуск.\nпродувки двигателя', 
                     'flag_for_the_presence_of_safe_air_boost_pressure_in_the_en':'Флаг наличия безопасного давления подпора\nвоздуха в корпусе двигателя', 
                     'flag_for_the_presence_of_safe_air_boost_pressure_in_the_ex':'Флаг наличия безопасного давления подпора\nвоздуха в корпусе возбудителя', 
                     'engine_purge_valve_closed_flag':'Флаг закрытого положения\nклапана продувки двигателя', 
                     'oil_system_oil_temperature_flag_is_above_10_at_the_cooler_ou':'Флаг темп. масла маслосистемы выше 10гр.С\nна выходе охладителя (для индивид. маслосистемы)', 
                     'flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_indiv':'Флаг предельного мин. уровня масла\nв маслобаке (для индивид. маслосистемы)', 
                     'flag_for_the_presence_of_the_minimum_level_of_the_barrier':'Флаг наличия мин. уровня запирающей\nжидкости в баке системы запирания',
                     'generalized_flag_for_the_presence_of_barrier_fluid_pressure':'Обобщенный флаг наличия давления запирающей\nжидкости к торцевому уплотнению', 
                     'command_to_turn_on_the_vv_only_for_UMPNA':'Команда на включение ВВ (только для UMPNA)', 
                     'command_to_turn_off_the_vv_output_1':'Команда на отключение ВВ (выход 1)',
                     'command_to_turn_off_the_vv_output_2':'Команда на отключение ВВ (выход 2)', 'NA_Chrp':'НА с ЧРП', 'type_NA_MNA':'Тип НА - МНА\n(1 - МНА, 0 - ПНА)', 'pump_type_NM':'Насос типа НМ(1 - НМ)', 
                     'parametr_KTPRAS_1':'Параметр для KTPRAS_1', 
                     'number_of_delay_scans_of_the_analysis_of_the_health_of_the':'Количество сканов задержки анализа\nисправности цепей управления ВВ НА', 
                     'unit_number_of_the_auxiliary_system_start_up_oil_pump':'Номер агрегата вспомсистемы\n"пуско-резервный маслонасос" (для индивид. маслосистемы)', 
                     'NPS_number_1_or_2_which_the_AT_belongs':'Номер НПС (1 или 2), к которой относится НА', 
                     'achr_protection_number_in_the_array_of_station_protections':'Номер защиты АЧР\nв массиве станционных защит', 
                     'saon_protection_number_in_the_array_of_station_protections':'Номер защиты САОН\nв массиве станционных защит', 
                     'gmpna_49':'GMPNA_[49]', 'gmpna_50':'GMPNA_[50]', 'gmpna_51':'GMPNA_[51]', 'gmpna_52':'GMPNA_[52]', 'gmpna_53':'GMPNA_[53]', 'gmpna_54':'GMPNA_[54]',
                     'gmpna_55':'GMPNA_[55]', 'gmpna_56':'GMPNA_[56]', 'gmpna_57':'GMPNA_[57]', 'gmpna_58':'GMPNA_[58]', 'gmpna_59':'GMPNA_[59]', 'gmpna_60':'GMPNA_[60]', 
                     'gmpna_61':'GMPNA_[61]', 'gmpna_62':'GMPNA_[62]', 'gmpna_63':'GMPNA_[63]', 'gmpna_64':'GMPNA_[64]', 
                     'Pic':'Pic', 'tabl_msg':'Шаблон сообщений',
                     'replacement_uso_signal_vv_1':'Замена %1 - УСО сигналов ВВ 1\n(Строка для замены %1 в сообщениях)', 
                     'replacement_uso_signal_vv_2':'Замена %2 - УСО сигналов ВВ 2\n(Строка для замены %2 в сообщениях)'},
            
            'umpna_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},
            
            'umpna_narab_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},
                       
            'zd': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'short_name':'Короткое название', 'exists_interface':'Наличие ИНТЕРФЕЙСА', 'KVO':'КВО', 'KVZ':'КВЗ', 'MPO':'МПО', 
                   'MPZ':'МПЗ', 'Dist':'Дист_ф', 'Mufta':'Муфта', 'Drive_failure':'Авария привода', 'Open':'Открыть', 'Close':'Закрыть', 'Stop':'Остановить', 'Opening_stop':'Открытие остановить', 
                   'Closeing_stop':'Закрытие остановить', 'KVO_i':'КВО_и', 'KVZ_i':'КВЗ_и', 'MPO_i':'МПО_и', 'MPZ_i':'МПЗ_и', 'Dist_i':'Дист_и', 'Mufta_i':'Муфта_и','Drive_failure_i':'Авария привода_и', 
                   'Open_i':'Открыть_и', 'Close_i':'Закрыть_и', 'Stop_i':'Остановить_и', 'Opening_stop_i':'Открытие остановить_и','Closeing_stop_i':'Закрытие остановить_и', 'No_connection':'Отсутствие связи', 
                   'Close_BRU':'Закрыть с БРУ', 'Stop_BRU':'Стоп с БРУ', 'Voltage':'Напряжение', 'Voltage_CHSU':'Напряжение ЩСУ', 'Voltage_in_signaling_circuits':'Напряжение в цепях\nсигнализации', 
                   'Serviceability_opening_circuits':'Исправность цепей открытия', 'Serviceability_closening_circuits':'Исправность цепей закрытия', 'VMMO':'ВММО', 'VMMZ':'ВММЗ', 
                   'Freeze_on_suspicious_change':'Замораживать при\nподозрительном изм', 'Is_klapan':'Это клапан', 'Opening_percent':'Процент открытия', 'Pic':'Pic', 'Type_BUR_ZD':'Тип БУР задвижки', 
                   'tabl_msg':'Шаблон для сообщений', 'AlphaHMI':'AlphaHMI', 'AlphaHMI_PIC1':'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont':'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2':'AlphaHMI_PIC2',
                   'AlphaHMI_PIC2_Number_kont':'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3':'AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont':'AlphaHMI_PIC3_Number_kont', 
                   'AlphaHMI_PIC4':'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont':'AlphaHMI_PIC4_Number_kont'},

            'zd_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'zd_type': {'id':'№', 'type_bur':'Тип БУР','manufacturer':'Производитель','heating_on':'Включен подогрев','operating_mode_stop':'Режим работы "Стоп"',
                        'ready_for_technological_operations':'Готова к технологическим операциям','operation_time_current_protect':'Срабатывание время токовой защиты',
                        'protect_kz':'Защита от тока КЗ','engine_overheating':'Перегрев двигателя','undervoltage_input_network':'Пониженое напряжение входной сети',
                        'interruption_phase_connection_ED':'Обрыв фазы подключения к ЭД','loss_phases_input_mains':'Обрыв фаз входной питающей сети',
                        'lack_of_movement':'Отсутствие движения','power_input_overvoltage':'Перенапряжение на силовом входе',
                        'critical_supply_voltage_drop':'Критическое снижение напряжения питания',
                        'wrong_phase_sequence_network_power_input_unit':'Неправильное чередование фаз сети на силовом входе блока',
                        'wrong_direction_travel':'Неправильное направление движения','position_sensor_setting_defect':'Дефект настройки датчика положения',
                        'device_defect':'Дефект устройства','battery_discharge':'Разряд элемента питания',
                        'overheating_power_converter_module':'Перегрев модуля силового преобразователя','hypothermia':'Переохлаждение',
                        'current_load_moment':'Текущий момент нагрузки','service_phase_defect':'Дефект служебной фазы',
                        'digital_input_overvoltage':'Перенапряжение на дискретном входе','insulation_resistance_05_om':'Сопротивление изоляции < 0,5 МОм',
                        'insulation_resistance_1_om':'Сопротивление изоляции < 1 МОм','no_connection_motor':'Отсутствие подключения к электродвигателю',
                        'dc_bus_undervoltage':'Пониженное напряжение на шине постоянного тока','defect_parameters_groups_b_d':'Дефект параметров групп B,D',
                        'defect_parameters_groups_g':'Дефект параметров группы G'},

            'vs': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'short_name':'Короткое\nназвание', 'group':'Группа', 'number_in_group':'Номер в группе', 'MP':'МП', 'Pressure_is_True':'Давление норма', 
                   'Voltage':'Напряжение', 'Voltage_Sch':'Напряжение на СШ', 'Serviceability_of_circuits_of_inclusion':'Исправность цепей\nвключения', 'External_alarm':'Внешняя авария', 'Pressure_sensor_defective':'Датчик давления неисправен', 
                   'VKL':'Включить', 'OTKL':'Отключить', 'Not_APV':'АПВ не требуется', 'Pic':'Pic', 'tabl_msg':'Таблица сообщений', 'Is_klapana_interface_auxsystem':'Это клапан/интерфейсная вспомсистема',
                   'AlphaHMI':'AlphaHMI', 'AlphaHMI_PIC1':'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont':'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2':'AlphaHMI_PIC2',
                   'AlphaHMI_PIC2_Number_kont':'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3':'AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont':'AlphaHMI_PIC3_Number_kont', 
                   'AlphaHMI_PIC4':'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont':'AlphaHMI_PIC4_Number_kont'},

            'vs_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'vsgrp': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'fire_or_watering':'Пож или водоорош', 'count_auxsys_in_group':'Количество вспомсистем в группе', 
                      'WarnOff_flag_if_one_auxsystem_in_the_group_is_running':'Требуется выставлять флаг WarnOff\nесли работает одна вспомсистема в группе', 'additional_steps_required':'Требуется выполнять дополнительные действия\nперед пуском/остановом вспомсистем в группе'},

            'vsgrp_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'uts': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'short_name':'Короткое\nназвание', 'location':'Место установки', 'VKL':'Включить', 'Serviceability_of_circuits_of_inclusion':'Исправность цепей\nвключения', 'siren':'Сирена', 
                    'Does_not_require_autoshutdown':'Не требует\nавтоотключения', 'Examination':'Проверка', 'Kvit':'Квитирование', 
                    'Pic':'Pic', 'number_list_VU':'Номер листа для ВУ', 'order_number_for_VU':'Номер порядка для ВУ', 
                    'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'upts': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'short_name':'Короткое\nназвание', 'location':'Место установки', 'VKL':'Включить', 'Serviceability_of_circuits_of_inclusion':'Исправность цепей\nвключения', 
                     'siren':'Сирена', 'Does_not_require_autoshutdown':'Не требует\nавтоотключения', 'Examination':'Проверка', 'Kvit':'Квитирование', 
                    'Pic':'Pic', 'number_list_VU':'Номер листа для ВУ', 'order_number_for_VU':'Номер порядка для ВУ', 
                    'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},

            'uts_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'vv': {'id':'№','variable':'Переменная', 'name':'Название', 'VV_vkl':'Высоковольтный выключатель включен', 'VV_otkl':'Высоковольтный выключатель отключен', 'Pic':'Pic'},
            
            'pi': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'Type_PI':'Тип ПИ:\n1 - пламени, 2 - тепловой,\n3 - дымовой, 4 - АПУ, 5 - тепловой аналог.', 
                   'Fire_0':'Пожар 0', 'Attention_1':'Внимание 1', 'Fault_1_glass_pollution_broken_2':'Неисправность 1\nзагрязнение стекла обрыв 2', 'Fault_2_fault_KZ_3':'Неисправность 2\nнеисправность КЗ 3', 
                   'Yes_connection_4':'Есть связь 4', 'Frequency_generator_failure_5':'Неисправность генератора частоты 5','Parameter_loading_error_6':'Ошибка загрузки параметров 6', 
                   'Communication_error_module_IPP_7':'Ошибка связи с модулем ИПП 7', 'Supply_voltage_fault_8':'Неисправность напряжения\nпитания 8', 'Optics_contamination_9':'Загрязнение оптики 9',
                   'IK_channel_failure_10':'Неисправность ИК канала 10', 'UF_channel_failure_11':'Неисправность УФ канала 11', 'Loading_12':'Загрузка 12', 'Test_13':'Тест 13', 'Reserve_14':'Резерв 14',
                   'Reset_Link':'Сброс ссылка', 'Reset_Request':'Сброс запроса', 'Through_loop_number_for_interface':'Сквозной номер шлейфа\nдля интерфейсных', 'location':'Место установки', 'Pic':'Pic','Normal':'Норма'}, 
                
            'pz_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'dps': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'control':'Контроль', 'deblock':'Деблокировка', 
                      'actuation':'Срабатывание', 'actuation_transmitter':'Срабатывание\n(трансмиттер)', 'malfunction':'Неисправность', 'voltage':'Напряжение'},
            
            'tm_dp': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'link_to_link_signal':'Ссылка на сигнал\nналичия связи', 'link_to_timeout':'Ссылка на таймаут по умолчанию\ntmCommon.CSPA_t1'},
            
            'tm_ts': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'function_ASDU':'Функция ASDU', 'addr_object':'Адрес объекта', 'link_value':'Ссылка на значение'},
            
            'tm_ti4': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'function_ASDU':'Функция ASDU', 'addr_object':'Адрес объекта', 'variable_value':'Переменная - значение', 'variable_status':'Переменная - статус',
                      'variable_Aiparam':'Переменная - Aiparam'},

            'tm_ti2': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'function_ASDU':'Функция ASDU', 'addr_object':'Адрес объекта', 'variable_value':'Переменная - значение', 'variable_status':'Переменная - статус'},

            'tm_tii': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'function_ASDU':'Функция ASDU', 'addr_object':'Адрес объекта', 'variable_value':'Переменная - значение', 'variable_status':'Переменная - статус'},

            'tm_tu': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'function_ASDU':'Функция ASDU', 'addr_object':'Адрес объекта', 'variable_change':'Изменяемая переменная', 'change_bit':'Изменяемый бит',
                      'descriptionTU':'descriptionTU\nне более 32 символа латиницы'},

            'tm_tr4': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'function_ASDU':'Функция ASDU', 'addr_object':'Адрес объекта', 'variable_change':'Изменяемая переменная', 'descriptionTR4':'descriptionTR4\nне более 32 символа латиницы'},
            
            'tm_tr2': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'function_ASDU':'Функция ASDU', 'addr_object':'Адрес объекта', 'variable_change':'Изменяемая переменная', 'descriptionTR4':'descriptionTR4\nне более 32 символа латиницы'},
            
            'pz': {'id':'№', 'variable':'Переменная', 'tag'   :'Идентификатор', 'name':'Название',
                   'type_zone':'Тип\n0 - без тушения, -1 - пенотушение,\n>=1 - водотушение, -2 - АГП',
                   'max_number_foam_attacks' :'Максимальное количество пенных атак\nЕсли нет доп. требований: зона с пенотушением 3,\nзона с водоохлаждением 65535',
                   'flag_stop_extinguishing_end_foam_attacks':'Флаг остановки тушения после окончания пенных атак\nЕсли нет доп требований: зона с пенотушением - 1\nзона с водоохлаждением - 0',
                   'foam_pump_group_number'  :'Номер группы\nнасосов пенотушения', 'cooling_pump_group_number'   :'Номер группы\nнасосов водоохлаждения',
                   "nPI_1" :'Номера ПИ зоны - 1', "nPI_2" :'Номера ПИ зоны - 2', "nPI_3" :'Номера ПИ зоны - 3', "nPI_4" :'Номера ПИ зоны - 4',
                   "nPI_5" :'Номера ПИ зоны - 5',"nPI_6" :'Номера ПИ зоны - 6',"nPI_7" :'Номера ПИ зоны - 7',"nPI_8" :'Номера ПИ зоны - 8',
                   "nPI_9" :'Номера ПИ зоны - 9',"nPI_10":'Номера ПИ зоны - 10',"nPI_11":'Номера ПИ зоны - 11',
                   "nPI_12":'Номера ПИ зоны - 12',"nPI_13":'Номера ПИ зоны - 13',"nPI_14":'Номера ПИ зоны - 14',"nPI_15":'Номера ПИ зоны - 15',
                   "nPI_16":'Номера ПИ зоны - 16',"nPI_17":'Номера ПИ зоны - 17',"nPI_18":'Номера ПИ зоны - 18',"nPI_19":'Номера ПИ зоны - 19',"nPI_20":'Номера ПИ зоны - 20',
                   "nPI_21":'Номера ПИ зоны - 21',"nPI_22":'Номера ПИ зоны - 22',"nPI_23":'Номера ПИ зоны - 23',"nPI_24":'Номера ПИ зоны - 24',"nPI_25":'Номера ПИ зоны - 25',
                   "nPI_26":'Номера ПИ зоны - 26',"nPI_27":'Номера ПИ зоны - 27',"nPI_28":'Номера ПИ зоны - 28',"nPI_29":'Номера ПИ зоны - 29',"nPI_30":'Номера ПИ зоны - 30',
                   "nPI_31":'Номера ПИ зоны - 31',"nPI_32":'Номера ПИ зоны - 32',
                   "nUTSFire_1":'Номера табло и\nсирен "Пена", "Пожар" - 1',"nUTSFire_2":'Номера табло и\nсирен "Пена", "Пожар" - 2',
                   "nUTSFire_3":'Номера табло и\nсирен "Пена", "Пожар" - 3',"nUTSFire_4":'Номера табло и\nсирен "Пена", "Пожар" - 4',
                   "nUTSFire_5":'Номера табло и\nсирен "Пена", "Пожар" - 5',"nUTSFire_6":'Номера табло и\nсирен "Пена", "Пожар" - 6',
                   "nUTSFire_7":'Номера табло и\nсирен "Пена", "Пожар" - 7',"nUTSFire_8":'Номера табло и\nсирен "Пена", "Пожар" - 8',
                   "nUTSFire_9":'Номера табло и\nсирен "Пена", "Пожар" - 9',"nUTSFire_10":'Номера табло и\nсирен "Пена", "Пожар" - 10',
                   "nUTSFire_11":'Номера табло и\nсирен "Пена", "Пожар" - 11',"nUTSFire_12":'Номера табло и\nсирен "Пена", "Пожар" - 12',
                   "nUTSFire_13":'Номера табло и\nсирен "Пена", "Пожар" - 13',"nUTSFire_14":'Номера табло и\nсирен "Пена", "Пожар" - 14',
                   "nUTSFire_15":'Номера табло и\nсирен "Пена", "Пожар" - 15', "nUTSFire_16":'Номера табло и\nсирен "Пена", "Пожар" - 16',
                   "nUTSFire_17":'Номера табло и\nсирен "Пена", "Пожар" - 17', "nUTSFire_18":'Номера табло и\nсирен "Пена", "Пожар" - 18',
                   "nUTSFire_19":'Номера табло и\nсирен "Пена", "Пожар" - 19',"nUTSFire_20":'Номера табло и\nсирен "Пена", "Пожар" - 20',
                   "nUTSPTOff_1":'Номера табло "Автоматическое\nпожаротушение отключено" - 1',  "nUTSPTOff_2":'Номера табло "Автоматическое\nпожаротушение отключено" - 2',
                   "nUTSPTOff_3":'Номера табло "Автоматическое\nпожаротушение отключено" - 3', "nUTSPTOff_4":'Номера табло "Автоматическое\nпожаротушение отключено" - 4',
                    "nZD_1":'Номера\nзадвижек - 1',"nZD_2":'Номера\nзадвижек - 2',"nZD_3":'Номера\nзадвижек - 3',
                    "nZD_4":'Номера\nзадвижек - 4',"nZD_5":'Номера\nзадвижек - 5',"nZD_6":'Номера\nзадвижек - 6',
                    "nZD_7":'Номера\nзадвижек - 7',"nZD_8":'Номера\nзадвижек - 8',
                "nZD_SM_1":'Номера доп\nзадвижек - 1', "nZD_SM_2":'Номера доп\nзадвижек - 1 - 2',"nZD_SM_3":'Номера доп\nзадвижек - 1 - 3',
                "nZD_SM_4":'Номера доп\nзадвижек - 1 - 4',"nZD_SM_5":'Номера доп\nзадвижек - 1 - 5', "nZD_SM_6":'Номера доп\nзадвижек - 1 - 6',
                "nZD_SM_7":'Номера доп\nзадвижек - 1 - 7',"nZD_SM_8":'Номера доп\nзадвижек - 1 - 8',"nZD_SM_9":'Номера доп\nзадвижек - 1 - 9',
                "nZD_SM_10":'Номера доп\nзадвижек - 1 - 10',"nZD_SM_11":'Номера доп\nзадвижек - 1 - 11',"nZD_SM_12":'Номера доп\nзадвижек - 1 - 12',
                'auxsystem_enable':'Необх. кол-во для тушения\nВспомсистем включить','bd_open':'Необх. кол-во для тушения\nБаков-дозаторов открыть',
                'number_group_bd':'Номер группы баков-дозаторов','censor' :'Необх кол-во исправных для готовности\nДатчиков',
                'auxsystem':'Необх кол-во исправных для готовности\nВспомсистем','bd'  :'Необх кол-во исправных для готовности\nБаков-дозаторов',
                'g_1' :'Г_1','g_2' :'Г_2','g_3' :'Г_3','g_4' :'Г_4','g_5' :'Г_5', 'g_6' :'Г_6', 'g_7' :'Г_7','g_8' :'Г_8','g_9' :'Г_9','g_10':'Г_10',
                'g_11':'Г_11','g_12':'Г_12','g_13':'Г_13','g_14':'Г_14','g_15':'Г_15',
                'readiness':'Готовности', 'start_pumps_opening_all_valves_direction':'Запускать насосы после открытия\nвсех задвижек по направлению',
                "pDoorClosed_1" :'Дверь закрыта (АГТ)_1', "pDoorClosed_2" :'Дверь закрыта (АГТ)_2',"pDoorClosed_3" :'Дверь закрыта (АГТ)_3',
                "pDoorClosed_4" :'Дверь закрыта (АГТ)_4',"automatic_fire_extinguishing_mode_enabled_AGT" :'Режим автоматического\nпожаротушения включен (АГТ)',
                "cancellation_launch_OTV_AGT":'Отмена пуска ОТВ (АГТ)', "OTV_output_control_AGP":'Контроль выхода ОТВ (АГП)',
                "start_OTV_AGT" :'Пуск ОТВ (АГТ)', "shutdown_ventilation_and_air_conditioning_by_fire_AGT" :'Отключение вентиляции и\n кондиционирования по пожару (АГТ)',
                "serviceability_connecting_lines_signal_Start_OTV_AGT":'Исправность соединительных линий\n сигнала Пуск ОТВ (АГТ)',
                "the_presence_pressure_cylinders_OTV_AGT":'Наличие давления в\nбаллонах ОТВ (АГТ)','short_name': 'Подпись на мнемокадре' },
        
            'ai_fuse':{'id':'№','tag':'Идентификатор','name_group_fuse':'Имя группы предохранителя','control_result':'Контрольное значение','reliability_control':'Значение проверочное'},
        
            'ai_grp':{'id':'№', 'name':'Название','Min6':'Мин.6', 'Min5':'Мин.5', 'Min4':'Мин.4', 'Min3':'Мин.3', 'Min2':'Мин.2', 'Min1':'Мин.', 
                    'Max1':'Макс.', 'Max2':'Макс.2', 'Max3':'Макс.3', 'Max4':'Макс.4', 'Max5':'Макс.5', 'Max6':'Макс.6','tabl_msg':'Таблица сообщений'}}

class Signals(BaseModel):
    type_signal = CharField(null = True)
    uso         = CharField(null = True)
    tag         = CharField(null = True)
    description = CharField(null = True)
    schema      = CharField(null = True)
    klk         = CharField(null = True)
    contact     = CharField(null = True)
    basket      = IntegerField(null = True)
    module      = IntegerField(null = True)
    channel     = IntegerField(null = True)

    class Meta:
        table_name = 'signals'
class HardWare(BaseModel):
    variable     = CharField(null = True)
    tag          = CharField(null = True)
    uso          = CharField(null = True)
    basket       = IntegerField(null = True)
    powerLink_ID = CharField(null = True)
    Pic          = CharField(null = True)
    type_0       = CharField(null = True)
    variable_0   = CharField(null = True)
    type_1       = CharField(null = True)
    variable_1   = CharField(null = True)
    type_2       = CharField(null = True)
    variable_2   = CharField(null = True)
    type_3       = CharField(null = True)
    variable_3   = CharField(null = True)
    type_4       = CharField(null = True)
    variable_4   = CharField(null = True)
    type_5       = CharField(null = True)
    variable_5   = CharField(null = True)
    type_6       = CharField(null = True)
    variable_6   = CharField(null = True)
    type_7       = CharField(null = True)
    variable_7   = CharField(null = True)
    type_8       = CharField(null = True)
    variable_8   = CharField(null = True)
    type_9       = CharField(null = True)
    variable_9   = CharField(null = True)
    type_10      = CharField(null = True)
    variable_10  = CharField(null = True)
    type_11      = CharField(null = True)
    variable_11  = CharField(null = True)
    type_12      = CharField(null = True)
    variable_12  = CharField(null = True)
    type_13      = CharField(null = True)
    variable_13  = CharField(null = True)
    type_14      = CharField(null = True)
    variable_14  = CharField(null = True)
    type_15      = CharField(null = True)
    variable_15  = CharField(null = True)
    type_16      = CharField(null = True)
    variable_16  = CharField(null = True)
    type_17      = CharField(null = True)
    variable_17  = CharField(null = True)
    type_18      = CharField(null = True)
    variable_18  = CharField(null = True)
    type_19      = CharField(null = True)
    variable_19  = CharField(null = True)
    type_20      = CharField(null = True)
    variable_20  = CharField(null = True)
    type_21      = CharField(null = True)
    variable_21  = CharField(null = True)
    type_22      = CharField(null = True)
    variable_22  = CharField(null = True)
    type_23      = CharField(null = True)
    variable_23  = CharField(null = True)
    type_24      = CharField(null = True)
    variable_24  = CharField(null = True)
    type_25      = CharField(null = True)
    variable_25  = CharField(null = True)
    type_26      = CharField(null = True)
    variable_26  = CharField(null = True)
    type_27      = CharField(null = True)
    variable_27  = CharField(null = True)
    type_28      = CharField(null = True)
    variable_28  = CharField(null = True)
    type_29      = CharField(null = True)
    variable_29  = CharField(null = True)
    type_30      = CharField(null = True)
    variable_30  = CharField(null = True)
    type_31      = CharField(null = True)
    variable_31  = CharField(null = True)
    type_32      = CharField(null = True) 
    variable_32  = CharField(null = True)

    class Meta:
        table_name = 'hardware'
class AI(BaseModel):
    variable         = CharField(null = True)
    tag              = CharField(null = True)
    name             = CharField(null = True)
    pValue           = CharField(null = True)
    pHealth          = CharField(null = True)
    AnalogGroupId    = CharField(null = True)
    SetpointGroupId = CharField(null = True)
    Egu             = CharField(null = True)
    sign_VU          = CharField(null = True)
    IsOilPressure  = BooleanField(null = True)

    number_NA_or_aux = IntegerField(null = True)
    IsPumpVibration  = IntegerField(null = True)
    vibration_motor  = IntegerField(null = True)
    current_motor    = IntegerField(null = True)
    aux_outlet_pressure = IntegerField(null = True)

    number_ust_min_avar = IntegerField(null = True)
    number_ust_min_pred = IntegerField(null = True)
    number_ust_max_pred = IntegerField(null = True)
    number_ust_max_avar = IntegerField(null = True)

    LoLimField = DoubleField(null = True)
    HiLimField = DoubleField(null = True)
    LoLimEng = DoubleField(null = True)
    HiLimEng = DoubleField(null = True)
    LoLim = DoubleField(null = True)
    HiLim = DoubleField(null = True)
    Histeresis = DoubleField(null = True)
    TimeFilter = DoubleField(null = True)

    Min6 = DoubleField(null = True)
    Min5 = DoubleField(null = True)
    Min4 = DoubleField(null = True)
    Min3 = DoubleField(null = True)
    Min2 = DoubleField(null = True)
    Min1 = DoubleField(null = True)
    Max1 = DoubleField(null = True)
    Max2 = DoubleField(null = True)
    Max3 = DoubleField(null = True)
    Max4 = DoubleField(null = True)
    Max5 = DoubleField(null = True)
    Max6 = DoubleField(null = True)

    SigMask = CharField(null = True)
    MsgMask = CharField(null = True)
    CtrlMask = CharField(null = True)

    Precision = IntegerField(null = True)
    Pic = CharField(null = True)
    TrendingGroup = IntegerField(null = True)
    DeltaT = DoubleField(null = True)
    PhysicEgu = CharField(null = True)
    RuleName = CharField(null = True)
    fuse = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)
    tag_eng = CharField(null = True)

    AlphaHMI = CharField(null = True)
    AlphaHMI_PIC1 = CharField(null = True)
    AlphaHMI_PIC1_Number_kont = CharField(null = True)
    AlphaHMI_PIC2 = CharField(null = True)
    AlphaHMI_PIC2_Number_kont = CharField(null = True)
    AlphaHMI_PIC3 = CharField(null = True)
    AlphaHMI_PIC3_Number_kont = CharField(null = True)
    AlphaHMI_PIC4 = CharField(null = True)
    AlphaHMI_PIC4_Number_kont = CharField(null = True)

    class Meta:
        table_name = 'ai'
class AO(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    pValue  = CharField(null = True)
    pHealth = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)
    tag_eng = CharField(null = True)

    class Meta:
        table_name = 'ao'
class DI(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    pValue  = CharField(null = True)
    pHealth = CharField(null = True)

    Inv = IntegerField(null = True)
    ErrValue = IntegerField(null = True)
    priority_0 = IntegerField(null = True)
    priority_1 = IntegerField(null = True)
    Msg = IntegerField(null = True)
    isDI_NC = CharField(null = True)
    isAI_Warn = CharField(null = True)
    isAI_Avar = CharField(null = True)
    pNC_AI = CharField(null = True)
    TS_ID = CharField(null = True)
    isModuleNC = CharField(null = True)
    Pic = CharField(null = True)
    tabl_msg = CharField(null = True)
    group_diskrets = CharField(null = True)
    msg_priority_0 = CharField(null = True)
    msg_priority_1 = CharField(null = True)
    short_title = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)
    tag_eng = CharField(null = True)

    AlphaHMI = CharField(null = True)
    AlphaHMI_PIC1 = CharField(null = True)
    AlphaHMI_PIC1_Number_kont = CharField(null = True)
    AlphaHMI_PIC2 = CharField(null = True)
    AlphaHMI_PIC2_Number_kont = CharField(null = True)
    AlphaHMI_PIC3 = CharField(null = True)
    AlphaHMI_PIC3_Number_kont = CharField(null = True)
    AlphaHMI_PIC4 = CharField(null = True)
    AlphaHMI_PIC4_Number_kont = CharField(null = True)
    
    class Meta:
        table_name = 'di'
class DO(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    pValue  = CharField(null = True)
    pHealth = CharField(null = True)
    short_title = CharField(null = True)
    tabl_msg = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)
    tag_eng = CharField(null = True)

    AlphaHMI = CharField(null = True)
    AlphaHMI_PIC1 = CharField(null = True)
    AlphaHMI_PIC1_Number_kont = CharField(null = True)
    AlphaHMI_PIC2 = CharField(null = True)
    AlphaHMI_PIC2_Number_kont = CharField(null = True)
    AlphaHMI_PIC3 = CharField(null = True)
    AlphaHMI_PIC3_Number_kont = CharField(null = True)
    AlphaHMI_PIC4 = CharField(null = True)
    AlphaHMI_PIC4_Number_kont = CharField(null = True)
    
    class Meta:
        table_name = 'do'
class RS(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    array_number_modul  = IntegerField(null = True)
    pValue  = CharField(null = True)
    pHealth = CharField(null = True)
    Pic = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)
    
    class Meta:
        table_name = 'rs'
class USO(BaseModel):
    variable = CharField(null = True)
    name = CharField(null = True)
    temperature  = CharField(null = True)
    door = CharField(null = True)
    signal_1 = CharField(null = True)
    signal_2 = CharField(null = True)
    signal_3 = CharField(null = True)
    signal_4 = CharField(null = True)
    signal_5 = CharField(null = True)
    signal_6 = CharField(null = True)
    signal_7 = CharField(null = True)
    signal_8 = CharField(null = True)
    signal_9 = CharField(null = True)
    signal_10 = CharField(null = True)
    signal_11 = CharField(null = True)
    signal_12 = CharField(null = True)
    signal_13 = CharField(null = True)
    signal_14 = CharField(null = True)
    signal_15 = CharField(null = True)
    signal_16 = CharField(null = True)
    signal_17 = CharField(null = True)
    signal_18 = CharField(null = True)
    signal_19 = CharField(null = True)
    signal_20 = CharField(null = True)
    signal_21 = CharField(null = True)
    signal_22 = CharField(null = True)
    signal_23 = CharField(null = True)
    signal_24 = CharField(null = True)
    signal_25 = CharField(null = True)
    signal_26 = CharField(null = True)
    signal_27 = CharField(null = True)
    signal_28 = CharField(null = True)
    signal_29 = CharField(null = True)
    signal_30 = CharField(null = True)
    signal_31 = CharField(null = True)
    signal_32 = CharField(null = True)

    class Meta:
        table_name = 'uso'
class KTPRP(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)

    Number_PZ = CharField(null = True)
    Type = CharField(null = True)
    Pic = CharField(null = True)

    number_list_VU = IntegerField(null = True)
    number_protect_VU = IntegerField(null = True)
    
    class Meta:
        table_name = 'ktprp'
class KTPR(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)

    avar_parameter = CharField(null = True)
    DisableMasking = IntegerField(null = True)
    auto_unlock_protection = IntegerField(null = True)
    shutdown_PNS_a_time_delay_up_5s_after_turning = IntegerField(null = True)
    bitmask_protection_group_membership = IntegerField(null = True)
    stop_type_NA = IntegerField(null = True)
    pump_station_stop_type = IntegerField(null = True)
    
    closing_gate_valves_at_the_inlet_NPS = IntegerField(null = True)
    closing_gate_valves_at_the_outlet_NPS = IntegerField(null = True)
    closing_gate_valves_between_PNS_and_MNS = IntegerField(null = True)
    closing_gate_valves_between_RP_and_PNS = IntegerField(null = True)
    closing_valves_inlet_and_outlet_MNS = IntegerField(null = True)
    closing_valves_inlet_and_outlet_PNS = IntegerField(null = True)
    closing_valves_inlet_and_outlet_MNA = IntegerField(null = True)
    closing_valves_inlet_and_outlet_PNA = IntegerField(null = True)
    closing_valves_inlet_RD = IntegerField(null = True)
    closing_valves_outlet_RD = IntegerField(null = True)
    closing_valves_inlet_SSVD = IntegerField(null = True)
    closing_valves_inlet_FGU = IntegerField(null = True)
    closing_secant_valve_connection_unit__oil_production_oil = IntegerField(null = True)
    closing_valves_inlet_RP = IntegerField(null = True)
    reserve_protect_14 = IntegerField(null = True)
    reserve_protect_15 = IntegerField(null = True)

    shutdown_oil_pumps = IntegerField(null = True)
    shutdown_oil_pumps_after_signal_stopped_NA = IntegerField(null = True)
    shutdown_circulating_water_pumps = IntegerField(null = True)
    shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS = IntegerField(null = True)
    shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS = IntegerField(null = True)
    shutdown_pumps_pumping_out_from_tanks_SSVD = IntegerField(null = True)
    switching_off_the_electric_room_fans = IntegerField(null = True)
    shutdown_of_booster_fans_ED = IntegerField(null = True)
    shutdown_of_retaining_fans_of_the_electrical_room = IntegerField(null = True)
    shutdown_of_ED_air_compressors = IntegerField(null = True)
    shutdown_pumps_providing_oil = IntegerField(null = True)
    disabling_pumps_for_pumping_oil_oil_products_through_BIC = IntegerField(null = True)
    shutdown_domestic_and_drinking_water_pumps = IntegerField(null = True)
    shutdown_of_art_well_pumps = IntegerField(null = True)
    AVO_shutdown = IntegerField(null = True)
    shutdown_of_water_cooling_fans_circulating_water_supply_system = IntegerField(null = True)

    shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS = IntegerField(null = True)
    shutdown_of_exhaust_fans_of_the_pumping_room_PNS = IntegerField(null = True)
    shutdown_of_exhaust_fans_in_the_centralized_oil_system_room = IntegerField(null = True)
    shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room = IntegerField(null = True)
    shutdown_of_exhaust_fans_in_the_RD_room = IntegerField(null = True)
    shutdown_of_exhaust_fans_in_the_SSVD_room = IntegerField(null = True)
    shutdown_of_the_roof_fans_of_the_MNS_pump_room = IntegerField(null = True)
    shutdown_of_the_roof_fans_of_the_PNS_pump_room = IntegerField(null = True)
    switching_off_the_supply_fans_pumping_room_of_the_MNS = IntegerField(null = True)
    switching_off_the_supply_fans_pumping_room_of_the_PNS = IntegerField(null = True)
    switch_off_the_supply_fans_in_the_centralized_oil = IntegerField(null = True)
    switching_off_the_supply_fan_of_the_RD_room = IntegerField(null = True)
    switching_off_the_supply_fan_of_the_SSVD_room = IntegerField(null = True)
    switching_off_the_supply_fans_of_the_ED_air_compressor = IntegerField(null = True)
    switching_off_the_supply_fan_of_the_BIK_room = IntegerField(null = True)
    switching_off_the_supply_fan_of_the_SIKN_room = IntegerField(null = True)
    
    closing_the_air_valves_louvered_grilles_of_the_pump_room = IntegerField(null = True)
    closing_of_air_valves_louvered_grilles_of_the_compressor_room = IntegerField(null = True)
    shutdown_of_electric_oil_heaters = IntegerField(null = True)
    shutdown_of_the_electric_heaters_of_the_leakage_collection_MNS = IntegerField(null = True)
    shutdown_of_the_electric_heaters_of_the_leakage_collection_PNS = IntegerField(null = True)
    shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank = IntegerField(null = True)
    shutdown_of_air_coolers_of_the_locking_system_MNA = IntegerField(null = True)
    shutdown_of_air_coolers_of_the_locking_system_disc_NA = IntegerField(null = True)
    shutdown_of_the_external_cooling_circuit_ChRP_MNA = IntegerField(null = True)
    shutdown_of_the_external_cooling_circuit_ChRP_PNA = IntegerField(null = True)
    shutdown_of_locking_system_pumps = IntegerField(null = True)
    shutdown_of_pumps_for_pumping_oil_oil_products_through = IntegerField(null = True)
    shutdown_of_pumping_pumps_from_leakage_collection_tanks = IntegerField(null = True)
    shutdown_of_anticondensation_electric_heaters_ED = IntegerField(null = True)
    fire_protection = IntegerField(null = True)
    reserve_aux_15 = IntegerField(null = True)

    value_ust = IntegerField(null = True)
    Pic = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    number_list_VU = IntegerField(null = True)
    number_protect_VU = IntegerField(null = True)
    
    class Meta:
        table_name = 'ktpr'
class KTPRA(BaseModel):
    id_num = IntegerField(null = True)
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    NA = CharField(null = True)
    avar_parameter = CharField(null = True)
    stop_type = IntegerField(null = True)
    AVR = IntegerField(null = True)
    close_valves = IntegerField(null = True)
    DisableMasking = IntegerField(null = True)
    value_ust = IntegerField(null = True)
    Pic = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    number_list_VU = IntegerField(null = True)
    number_protect_VU = IntegerField(null = True)
    number_pump_VU = IntegerField(null = True)
    
    class Meta:
        table_name = 'ktpra'      
class KTPRS(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    drawdown = CharField(null = True)
    reference_to_value = CharField(null = True)
    priority_msg_0 = IntegerField(null = True)
    priority_msg_1 = IntegerField(null = True)
    prohibition_issuing_msg = BooleanField(null = True)
    Pic = CharField(null = True)
    
    class Meta:
        table_name = 'ktprs'
class GMPNA(BaseModel):
    id_num = IntegerField(null = True)
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    name_for_Chrp_in_local_mode = CharField(null = True)
    NA = CharField(null = True)
    used_time_ust = BooleanField(null = True)
    value_ust = IntegerField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    number_list_VU = IntegerField(null = True)
    number_protect_VU = IntegerField(null = True)
    number_pump_VU = IntegerField(null = True)
    
    class Meta:
        table_name = 'gmpna'
class tmNA_UMPNA(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = BooleanField(null = True)
    value_ust = IntegerField(null = True)
    value_real_ust = DoubleField(null = True)
    minimum = IntegerField(null = True)
    maximum = IntegerField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'umpna_tm'
class tmNA_UMPNA_narab(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = BooleanField(null = True)
    value_ust = IntegerField(null = True)
    minimum = IntegerField(null = True)
    maximum = IntegerField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'umpna_narab_tm'
class UMPNA(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)

    vv_included = CharField(null = True)
    vv_double_included = CharField(null = True)
    vv_disabled = CharField(null = True)
    vv_double_disabled = CharField(null = True)
    current_greater_than_noload_setting = CharField(null = True)
    serviceability_of_circuits_of_inclusion_of_VV = CharField(null = True)
    serviceability_of_circuits_of_shutdown_of_VV = CharField(null = True)
    serviceability_of_circuits_of_shutdown_of_VV_double = CharField(null = True)

    stop_1 = CharField(null = True)
    stop_2 = CharField(null = True)
    stop_3 = CharField(null = True)
    stop_4 = CharField(null = True)

    monitoring_the_presence_of_voltage_in_the_control_current = CharField(null = True)
    voltage_presence_flag_in_the_ZRU_motor_cell = CharField(null = True)
    vv_trolley_rolled_out = CharField(null = True)
    remote_control_mode_of_the_RZiA_controller = CharField(null = True)
    availability_of_communication_with_the_RZiA_controller = CharField(null = True)
    the_state_of_the_causative_agent_of_ED = CharField(null = True)
    engine_prepurge_end_flag = CharField(null = True)
    flag_for_the_presence_of_safe_air_boost_pressure_in_the_en = CharField(null = True)
    flag_for_the_presence_of_safe_air_boost_pressure_in_the_ex = CharField(null = True)
    engine_purge_valve_closed_flag = CharField(null = True)
    oil_system_oil_temperature_flag_is_above_10_at_the_cooler_ou = CharField(null = True)
    flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_indiv = CharField(null = True)
    flag_for_the_presence_of_the_minimum_level_of_the_barrier = CharField(null = True)
    generalized_flag_for_the_presence_of_barrier_fluid_pressure = CharField(null = True)
    command_to_turn_on_the_vv_only_for_UMPNA = CharField(null = True)
    command_to_turn_off_the_vv_output_1 = CharField(null = True)
    command_to_turn_off_the_vv_output_2 = CharField(null = True)
    NA_Chrp = CharField(null = True)
    type_NA_MNA = CharField(null = True)
    pump_type_NM = CharField(null = True)
    parametr_KTPRAS_1 = CharField(null = True)
    number_of_delay_scans_of_the_analysis_of_the_health_of_the = CharField(null = True)
    unit_number_of_the_auxiliary_system_start_up_oil_pump = CharField(null = True)
    NPS_number_1_or_2_which_the_AT_belongs = CharField(null = True)
    achr_protection_number_in_the_array_of_station_protections = CharField(null = True)
    saon_protection_number_in_the_array_of_station_protections = CharField(null = True)

    gmpna_49 = CharField(null = True)
    gmpna_50 = CharField(null = True)
    gmpna_51 = CharField(null = True)
    gmpna_52 = CharField(null = True)
    gmpna_53 = CharField(null = True)
    gmpna_54 = CharField(null = True)
    gmpna_55 = CharField(null = True)
    gmpna_56 = CharField(null = True)
    gmpna_57 = CharField(null = True)
    gmpna_58 = CharField(null = True)
    gmpna_59 = CharField(null = True)
    gmpna_60 = CharField(null = True)
    gmpna_61 = CharField(null = True)
    gmpna_62 = CharField(null = True)
    gmpna_63 = CharField(null = True)
    gmpna_64 = CharField(null = True)

    Pic = CharField(null = True)
    tabl_msg = CharField(null = True)
    replacement_uso_signal_vv_1 = CharField(null = True)
    replacement_uso_signal_vv_2 = CharField(null = True)

    class Meta:
        table_name = 'umpna'
class ZD(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    short_name = CharField(null = True)
    exists_interface = BooleanField(null = True)

    KVO = CharField(null = True)
    KVZ = CharField(null = True)
    MPO = CharField(null = True)
    MPZ = CharField(null = True)
    Dist = CharField(null = True)
    Mufta = CharField(null = True)
    Drive_failure = CharField(null = True)
    Open = CharField(null = True)
    Close = CharField(null = True)
    Stop = CharField(null = True)
    Opening_stop = CharField(null = True)
    Closeing_stop = CharField(null = True)

    KVO_i = CharField(null = True)
    KVZ_i  = CharField(null = True)
    MPO_i  = CharField(null = True)
    MPZ_i  = CharField(null = True)
    Dist_i  = CharField(null = True)
    Mufta_i  = CharField(null = True)
    Drive_failure_i  = CharField(null = True)
    Open_i  = CharField(null = True)
    Close_i  = CharField(null = True)
    Stop_i  = CharField(null = True)
    Opening_stop_i  = CharField(null = True)
    Closeing_stop_i  = CharField(null = True)
    
    No_connection = CharField(null = True)
    Close_BRU = CharField(null = True)
    Stop_BRU = CharField(null = True)
    Voltage = CharField(null = True)
    Voltage_CHSU= CharField(null = True)
    Voltage_in_signaling_circuits = CharField(null = True)
    Serviceability_opening_circuits = CharField(null = True)
    Serviceability_closening_circuits = CharField(null = True)
    VMMO = CharField(null = True)
    VMMZ = CharField(null = True)
    Freeze_on_suspicious_change = CharField(null = True)
    Is_klapan = IntegerField(null = True)
    Opening_percent = CharField(null = True)
    Pic = CharField(null = True)
    Type_BUR_ZD = CharField(null = True)
    tabl_msg = CharField(null = True)

    AlphaHMI = CharField(null = True)
    AlphaHMI_PIC1 = CharField(null = True)
    AlphaHMI_PIC1_Number_kont = CharField(null = True)
    AlphaHMI_PIC2 = CharField(null = True)
    AlphaHMI_PIC2_Number_kont = CharField(null = True)
    AlphaHMI_PIC3 = CharField(null = True)
    AlphaHMI_PIC3_Number_kont = CharField(null = True)
    AlphaHMI_PIC4 = CharField(null = True)
    AlphaHMI_PIC4_Number_kont = CharField(null = True)

    class Meta:
        table_name = 'zd'
class ZD_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = BooleanField(null = True)
    value_ust = IntegerField(null = True)
    minimum = IntegerField(null = True)
    maximum = IntegerField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'zd_tm'
class VS(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    short_name = CharField(null = True)
    group = IntegerField(null = True)
    number_in_group = IntegerField(null = True)
    MP = CharField(null = True)
    Pressure_is_True = CharField(null = True)
    Voltage = CharField(null = True)
    Voltage_Sch = CharField(null = True)
    Serviceability_of_circuits_of_inclusion = CharField(null = True)
    External_alarm = CharField(null = True)
    Pressure_sensor_defective = CharField(null = True)
    VKL = CharField(null = True)
    OTKL = CharField(null = True)
    Not_APV = IntegerField(null = True)
    Pic = CharField(null = True)
    tabl_msg = CharField(null = True)
    Is_klapana_interface_auxsystem = CharField(null = True)
    
    AlphaHMI = CharField(null = True)
    AlphaHMI_PIC1 = CharField(null = True)
    AlphaHMI_PIC1_Number_kont = CharField(null = True)
    AlphaHMI_PIC2 = CharField(null = True)
    AlphaHMI_PIC2_Number_kont = CharField(null = True)
    AlphaHMI_PIC3 = CharField(null = True)
    AlphaHMI_PIC3_Number_kont = CharField(null = True)
    AlphaHMI_PIC4 = CharField(null = True)
    AlphaHMI_PIC4_Number_kont = CharField(null = True)

    class Meta:
        table_name = 'vs'
class VS_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = BooleanField(null = True)
    value_ust = IntegerField(null = True)
    minimum = IntegerField(null = True)
    maximum = IntegerField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'vs_tm'   
class VSGRP(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    fire_or_watering = BooleanField(null = True)
    count_auxsys_in_group = IntegerField(null = True)
    WarnOff_flag_if_one_auxsystem_in_the_group_is_running = BooleanField(null = True)
    additional_steps_required = BooleanField(null = True)

    class Meta:
        table_name = 'vsgrp'
class VSGRP_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = BooleanField(null = True)
    value_ust = IntegerField(null = True)
    minimum = IntegerField(null = True)
    maximum = IntegerField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'vsgrp_tm'
class UTS(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    short_name = CharField(null = True)
    location = CharField(null = True)
    VKL = CharField(null = True)
    Serviceability_of_circuits_of_inclusion = CharField(null = True)
    siren = IntegerField(null = True)
    Does_not_require_autoshutdown = CharField(null = True)
    Examination = CharField(null = True)
    Kvit = CharField(null = True)
    Pic = CharField(null = True)
    number_list_VU = CharField(null = True)
    order_number_for_VU = CharField(null = True)
    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)

    class Meta:
        table_name = 'uts'
class UPTS(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    short_name = CharField(null = True)
    location = CharField(null = True)
    VKL = CharField(null = True)
    Serviceability_of_circuits_of_inclusion = CharField(null = True)
    siren = BooleanField(null = True)
    Does_not_require_autoshutdown = CharField(null = True)
    Examination = CharField(null = True)
    Kvit = CharField(null = True)
    Pic = CharField(null = True)
    number_list_VU = CharField(null = True)
    order_number_for_VU = CharField(null = True)
    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)

    class Meta:
        table_name = 'upts'
class UTS_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = BooleanField(null = True)
    value_ust = IntegerField(null = True)
    minimum = IntegerField(null = True)
    maximum = IntegerField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'uts_tm'
class VV(BaseModel):
    variable = CharField(null = True)
    name = CharField(null = True)
    VV_vkl = CharField(null = True)
    VV_otkl = CharField(null = True)
    Pic = CharField(null = True)

    class Meta:
        table_name = 'vv'   
class PI(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    Type_PI = CharField(null = True)
    Fire_0 = CharField(null = True)
    Attention_1 = CharField(null = True)
    Fault_1_glass_pollution_broken_2 = CharField(null = True)
    Fault_2_fault_KZ_3 = CharField(null = True)
    Yes_connection_4 = CharField(null = True)
    Frequency_generator_failure_5 = CharField(null = True)
    Parameter_loading_error_6 = CharField(null = True)
    Communication_error_module_IPP_7 = CharField(null = True)
    Supply_voltage_fault_8 = CharField(null = True)
    Optics_contamination_9 = CharField(null = True)
    IK_channel_failure_10 = CharField(null = True)
    UF_channel_failure_11 = CharField(null = True)
    Loading_12 = CharField(null = True)
    Test_13 = CharField(null = True)
    Reserve_14 = CharField(null = True)
    Reset_Link = CharField(null = True)
    Reset_Request = CharField(null = True)
    Through_loop_number_for_interface = CharField(null = True)
    location = CharField(null = True)
    Pic = CharField(null = True)
    Normal = CharField(null = True)

    class Meta:
        table_name = 'pi'  
class PZ_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = BooleanField(null = True)
    value_ust = IntegerField(null = True)
    minimum = IntegerField(null = True)
    maximum = IntegerField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'pz_tm'
class DPS(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    control = CharField(null = True)
    deblock = CharField(null = True)
    actuation = CharField(null = True)
    actuation_transmitter = CharField(null = True)
    malfunction = CharField(null = True)
    voltage = CharField(null = True)

    class Meta:
        table_name = 'dps'
class TM_DP(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    link_to_link_signal = CharField(null = True)
    link_to_timeout = CharField(null = True)
    Pic = CharField(null = True)

    class Meta:
        table_name = 'tm_dp'
class TM_TS(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    function_ASDU = CharField(null = True)
    addr_object = IntegerField(null = True)
    link_value = CharField(null = True)

    class Meta:
        table_name = 'tm_ts'
class TM_TI4(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    function_ASDU = CharField(null = True)
    addr_object = IntegerField(null = True)
    variable_value = CharField(null = True)
    variable_status = CharField(null = True)
    variable_Aiparam = CharField(null = True)
    class Meta:
        table_name = 'tm_ti4'
class TM_TI2(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    function_ASDU = CharField(null = True)
    addr_object = IntegerField(null = True)
    variable_value = CharField(null = True)
    variable_status = CharField(null = True)
    class Meta:
        table_name = 'tm_ti2'
class TM_TII(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    function_ASDU = CharField(null = True)
    addr_object = IntegerField(null = True)
    variable_value = CharField(null = True)
    variable_status = CharField(null = True)
    class Meta:
        table_name = 'tm_tii'
class TM_TU(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    function_ASDU = CharField(null = True)
    addr_object = IntegerField(null = True)
    variable_change = CharField(null = True)
    change_bit = IntegerField(null = True)
    descriptionTU = CharField(null = True)
    class Meta:
        table_name = 'tm_tu'
class TM_TR4(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    function_ASDU = CharField(null = True)
    addr_object = IntegerField(null = True)
    variable_change = CharField(null = True)
    descriptionTR4 = CharField(null = True)
    class Meta:
        table_name = 'tm_tr4'
class TM_TR2(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    function_ASDU = CharField(null = True)
    addr_object = IntegerField(null = True)
    variable_change = CharField(null = True)
    descriptionTR4 = CharField(null = True)
    class Meta:
        table_name = 'tm_tr2'


