from lxml import etree
import uuid, math, os, shutil
from main_base import *

reset_button_designed = {'1' : ['X'       , '901', '2'],
                         '2' : ['Y'       , ''   , '2'],
                         '3' : ['Rotation', '0'  , '2'],
                         '4' : ['Width'   , '200', '2'],
                         '5' : ['Height'  , '30' , '2'],

}
reset_button_init_KTPR = {'2' : ['IsKTPRA'                           , ''  , '4'],
}
reset_button_init_KTPRA= {'2' : ['IsKTPRA'                           , ''  , '4'],
                          '3' : ['MAnumber'                          , ''  , '4'],
}

attrib_defence_top = {'1' : ['X'       , '1'  , '4'],
                      '2' : ['Y'       , '1'  , '4'],
                      '3' : ['Rotation', '0'  , '4'],
                      '4' : ['Width'   , '800', '4'],
                      '5' : ['Height'  , '26' , '4'],
                      '6' : ['Visible' , ''   , '4']
}
attrib_defence_row_design = {'1' : ['X'       , '0'  , '4'],
                             '2' : ['Y'       , 26   , '4'],
                             '3' : ['Rotation', '0'  , '4'],
                             '4' : ['Width'   , '800', '4'],
                             '5' : ['Height'  , '25' , '4'],
}

attrib_row_init_KTPR = {'1' : ['_link_init_ApSource_type_defence_row'    , '4'],
                        '2' : ['_init_group_number'                      , '4'],
                        '3' : ['_init_row_number'                        , '4'],
                        '4' : ['_def_name'                               , '4'],
                        '5' : ['_def_number'                             , '4'],
                        #'6' : ['_link_init_ApSource_type_defence_row_cmd', '4'],
                        '7' : ['_def_number_inarray'                     , '4'],
                        '8' : ['IsKTPRA'                                 , '4'],
}
attrib_row_init_KTPRA = {'1' : ['_link_init_ApSource_type_defence_row'    , '4'],
                         '2' : ['_init_group_number'                      , '4'],
                         '3' : ['_init_row_number'                        , '4'],
                         '4' : ['_def_name'                               , '4'],
                         '5' : ['_def_number'                             , '4'],
                         #'6' : ['_link_init_ApSource_type_defence_row_cmd', '4'],
                         '7' : ['_def_number_inarray'                     , '4'],
                         '8' : ['IsKTPRA'                                 , '4'],
                         '9' : ['MAnumber'                                , '4']
}
attrib_row_init_GMPNA = {'1' : ['_link_init_ApSource_type_readiness_row'    , '4'],
                         '2' : ['_init_group_number'                        , '4'],
                         '3' : ['_init_row_number'                          , '4'],
                         '4' : ['_readiness_name'                           , '4'],
                         '5' : ['_readiness_number'                         , '4'],
                         #'6' : ['_link_init_ApSource_type_readiness_row_cmd', '4'],
                         '7' : ['_readiness_number_inarray'                 , '4'],
                         '9' : ['MAnumber'                                  , '4']
}

button_designed = {'1' : ['X'       , '1'  , '4'],
                   '2' : ['Y'       , '657', '4'],
                   '3' : ['Rotation', '0'  , '4'],
                   '4' : ['Width'   , '46' , '4'],
                   '5' : ['Height'  , '36' , '4'],
}
button_init = {'1' : ['page_number'     , '4'],
               '2' : ['VisibleObject'   , '4'],
               '3' : ['UnVisibleObject1', '4'],
               '4' : ['UnVisibleObject2', '4'],
               '5' : ['UnVisibleObject3', '4'],
               '6' : ['UnVisibleObject4', '4'],
               '7' : ['UnVisibleObject5', '4'],
               '8' : ['UnVisibleObject6', '4'],
               '9' : ['UnVisibleObject7', '4'],
               '10': ['UnVisibleObject8', '4'],
               '11': ['_link_init_ApSource_type_defence_button', '4']
}

# Добавление кнопок переключения страниц с защитами
def button_click(path_file, root, tree, max_value_list, max_value_list_1, num_item,
                 data_inf_button, init_1_target, attrib_top_1, attrib_button):
    count = 0
    for lvl_one in root.iter('type'):
        object = etree.Element('object')
        object.attrib['access-modifier'] = 'private'
        object.attrib['name'] = attrib_top_1 + str(num_item)
        object.attrib['display-name'] = attrib_top_1 + str(num_item)
        object.attrib['uuid'] = str(uuid.uuid1())
        object.attrib['base-type'] = attrib_button
        if attrib_button == 'type_readiness_button':
            object.attrib['base-type-id'] = '3b23edfd-8b38-49af-b25b-94bd39dac56f'
        else:
            object.attrib['base-type-id'] = '2832c785-46a5-4217-ad3d-c0505077e057'
        object.attrib['ver'] = '4'

        for key, value in button_designed.items():
            designed = etree.Element("designed")
            designed.attrib['target'] = value[0]
            # Координаты по X - 1
            if (key == '1') and (num_item == 1):
                designed.attrib['value'] = value[1]
            elif (key == '1') and (num_item > 1):
                designed.attrib['value'] = str(int(value[1]) + (56 * (num_item - 1)))
            # по Y - 2
            elif (key == '2'):
                designed.attrib['value'] = str(((max_value_list_1 + 1) * 26) + 10)
            else:
                designed.attrib['value'] = value[1]
            designed.attrib['ver'] = value[2]
            object.append(designed)

        for key_1, value_1 in button_init.items():
            init = etree.Element("init")
            init.attrib['target'] = value_1[0]
            init.attrib['ver'] = value_1[1]
            if key_1 == '1':
                init.attrib['value'] = str(num_item)
            elif key_1 == '2':
                init.attrib['ref'] = attrib_top_1 + str(num_item)
            elif key_1 != str(num_item + 2) and ((int(key_1) - 2) <= max_value_list):
                init.attrib['ref'] = attrib_top_1 + str(int(key_1) - 2)
            elif key_1 == '11':
                if attrib_button == 'type_readiness_button':
                    init.attrib['target'] = '_link_init_ApSource_type_readiness_button'
                else:
                    init.attrib['target'] = '_link_init_ApSource_type_defence_button'
                init.attrib['ref'] = init_1_target
            else:
                init.attrib['ref'] = 'empty_link'
            object.append(init)
        for item in data_inf_button:
            count += 1
            init_1 = etree.Element("init")
            init_1.attrib['target'] = 'def' + str(count) + '_path'
            init_1.attrib['ver'] = '4'
            init_1.attrib['value'] = item
            object.append(init_1)
        root.append(object)
    tree.write(path_file, pretty_print=True)
# Внесение изменения в шаблон
def modification_list_defence(max_value_2, path_file, root, tree, list_active, pump, button_bool, str_pumps):
    if list_active == 'ktpr':
        name_title        = 'Карта общестанционных защит'
        name_defence      = 'Form_Station_Defences'
        name_apsoure      = 'ApSource_form_KTPRs'
        designed_path     = 'KTPRs'
        name_windows      = 'Form_Station_Defences'
        init_ref          = 'unit.WorkspaceControl.Station_Defences_Control'
        is_IsKTPRA        = 'false'
        reset_button      = reset_button_init_KTPR
        coordinate_Width  = '1102'
    elif list_active == 'ktprp':
        name_title        = 'Карта противопожарных защит'
        name_defence      = 'Form_Station_Defences'
        name_apsoure      = 'ApSource_form_KTPRs'
        designed_path     = 'KTPRs'
        name_windows      = 'Form_Station_Defences'
        init_ref          = 'unit.WorkspaceControl.Station_Defences_Control'
        is_IsKTPRA        = 'false'
        reset_button      = reset_button_init_KTPR
        coordinate_Width  = '1102'
    elif list_active == 'ktpra':
        name_title        = 'Карта агрегатных защит ' + str_pumps
        name_defence      = 'Form_MA' + str(pump) + '_Defences'
        name_apsoure      = 'ApSource_form_KTPRAs_MA' + str(pump)
        designed_path     = 'KTPRAs.KTPRAs_' + str(pump)
        name_windows      = 'Form_MA' + str(pump) + '_Defences'
        init_ref          = 'unit.WorkspaceControl.NA_' + str(pump) + '_Defences_Control'
        is_IsKTPRA        = 'true'
        reset_button      = reset_button_init_KTPRA
        coordinate_Width  = '1102'
    elif list_active == 'gmpna':
        name_title        = 'Карта агрегатных готовностей ' + str_pumps
        name_defence      = 'Form_MA' + str(pump) + '_Readiness'
        name_apsoure      = 'ApSource_form_GMPNAs_MA' + str(pump)
        name_windows      = 'Form_MA' + str(pump) + '_Readiness'
        init_ref          = 'unit.WorkspaceControl.NA_' + str(pump) +  '_Readiness_Control'
        designed_path     = 'GMPNAs.GMPNAs_' + str(pump)
        coordinate_Width  = '857'

    for lvl_one in root.iter('type'):
        # type
        if lvl_one.attrib['name'] == 'name':
            lvl_one.attrib['name'] = name_defence
        if lvl_one.attrib['display-name'] == 'name':
            lvl_one.attrib['display-name'] = name_defence
        if lvl_one.attrib['uuid'] == 'uuid':
            lvl_one.attrib['uuid'] = str(uuid.uuid1())
        for lvl_two in lvl_one.iter('designed'):
            if lvl_two.attrib['value'] == 'coordinate_H':
                if (list_active == 'gmpna') and (button_bool == False):
                    lvl_two.attrib['value'] = str(((max_value_2 + 1) * 26) + 2)
                else:
                    lvl_two.attrib['value'] = str(((max_value_2 + 1) * 26) + 55)

            if lvl_two.attrib['value'] == 'coordinate_W':
                lvl_two.attrib['value'] = coordinate_Width
            if lvl_two.attrib['value'] == 'name_list':
                lvl_two.attrib['value'] = name_title
        # 2 level
        for lvl_two in lvl_one.iter('object'):
            #1
            if lvl_two.attrib['name'] == 'defences':
                lvl_two.attrib['name'] = name_apsoure
            if lvl_two.attrib['display-name'] == 'defences':
                lvl_two.attrib['display-name'] = name_apsoure
            for lvl_three in lvl_two.iter('designed'):
                if lvl_three.attrib['value'] == 'designed_path':
                    lvl_three.attrib['value'] = designed_path
            #2
            if lvl_two.attrib['name'] == 'name':
                lvl_two.attrib['name'] = name_windows
            if lvl_two.attrib['display-name'] == 'name':
                lvl_two.attrib['display-name'] = name_windows
            for lvl_three in lvl_two.iter('init'):
                if lvl_three.attrib['ref'] == '_Control':
                    lvl_three.attrib['ref'] = init_ref
        #3
        # Для готовностей кнопка Деблокировать ВСЕ не нужна
        if list_active != 'gmpna':
            object = etree.Element('object')
            object.attrib['access-modifier'] = 'private'
            object.attrib['name'] = 'type_reset_all_button_1'
            object.attrib['display-name'] = 'type_reset_all_button_1'
            object.attrib['uuid'] = str(uuid.uuid1())
            object.attrib['base-type'] = 'type_reset_all_button'
            object.attrib['base-type-id'] = '63a525da-c1a1-4436-ac7a-4031350c94e2'
            object.attrib['ver'] = '2'
            for key, value in reset_button_designed.items():
                designed = etree.Element("designed")
                designed.attrib['target'] = value[0]
                if key == '2':
                    designed.attrib['value']  = str(((max_value_2 + 1) * 26) + 13)
                else:
                    designed.attrib['value']  = value[1]
                designed.attrib['ver']    = value[2]
                object.append(designed)
            for key, value in reset_button.items():
                    init = etree.Element("init")
                    init.attrib['target'] = value[0]
                    init.attrib['ver'] = value[2]
                    if key == '2':
                        init.attrib['value'] = is_IsKTPRA
                    elif key == '3':
                        init.attrib['value'] = str(pump)
                    object.append(init)
            root.append(object)
    tree.write(path_file, pretty_print=True)

def gen_station_defence(work_tabl, pump_def):
    data_inf_button = []
    msg             = {}
    dop_function = General_functions()
    # Номера столбцов выбранной таблицы
    if   work_tabl == 'ktpr' :
        name_tabl               = 'KTPR'
        attrib_data_1           = 'ApSource_form_KTPRs'
        attrib_IsKTPRA          = 'false'
        attrib_top_1            = 'type_defence_top_'
        attrib_top_2            = 'type_defence_top'
        attrib_row_1            = 'type_defence_row_'
        attrib_row_2            = 'type_defence_row'
        attrib_button           = 'type_defence_button'
        attrib_init_row         = attrib_row_init_KTPR
        base_type_id_top        = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
        base_type_id_row        = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    elif work_tabl == 'ktprp':
        name_tabl               = 'KTPR'
        attrib_data_1           = 'ApSource_form_KTPRs'
        attrib_IsKTPRA          = 'false'
        attrib_top_1            = 'type_defence_top_'
        attrib_top_2            = 'type_defence_top'
        attrib_row_1            = 'type_defence_row_'
        attrib_row_2            = 'type_defence_row'
        attrib_button           = 'type_defence_button'
        attrib_init_row         = attrib_row_init_KTPR
        base_type_id_top        = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
        base_type_id_row        = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    elif work_tabl == 'ktpra':
        name_tabl               = 'KTPRA'
        attrib_data_1           = 'ApSource_form_KTPRAs_MA'
        attrib_IsKTPRA          = 'true'
        attrib_top_1            = 'type_defence_top_'
        attrib_top_2            = 'type_defence_top'
        attrib_row_1            = 'type_defence_row_'
        attrib_row_2            = 'type_defence_row'
        attrib_button           = 'type_defence_button'
        attrib_init_row         = attrib_row_init_KTPRA
        base_type_id_top        = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
        base_type_id_row        = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    elif work_tabl == 'gmpna':
        name_tabl               = 'GMPNA'
        attrib_data_1           = 'ApSource_form_GMPNAs_MA'
        attrib_top_1            = 'type_readiness_top_'
        attrib_top_2            = 'type_readiness_top'
        attrib_row_1            = 'type_readiness_row_'
        attrib_row_2            = 'type_readiness_row'
        attrib_button           = 'type_readiness_button'
        attrib_init_row         = attrib_row_init_GMPNA
        base_type_id_top        = 'b08a935f-b03d-42e0-96c4-dc639b70d499'
        base_type_id_row        = '48231209-9a9f-42cf-9b38-ef1ef5cc7403'
    try:
        # Максимальное число агрегатов
        max_value_pump = dop_function.max_value_column(work_tabl, "number_pump_VU", False) if pump_def is True else 1

        # Цикл по агрегатныи защитам и готовностям. Для общестанционных цикл = 1
        for pump in range(max_value_pump):
            str_pumps     = ''
            pump_plus_one = pump + 1
        
            # Проверим на существование файл, если есть то удалим
            if   work_tabl == 'ktpr' : new_pic_path = f'{path_hmi}\\Form_Station_Defences.omobj'
            elif work_tabl == 'ktprp': new_pic_path = f'{path_hmi}\\Form_Station_Defences.omobj'
            elif work_tabl == 'ktpra': new_pic_path = f'{path_hmi}\\Form_MA{str(pump_plus_one)}_Defences.omobj'
            elif work_tabl == 'gmpna': new_pic_path = f'{path_hmi}\\Form_MA{str(pump_plus_one)}_Readiness.omobj'
            
            if os.path.isfile(new_pic_path): os.remove(new_pic_path)
            # В любом случае создадим новый
            shutil.copy2(f'{path_hmi}\\Form_Defences_default.omobj', new_pic_path)

            # Счетчик всех защит в карте
            counter_defence = 0
            # Максимальное число листов, необходимость переключения страниц,
            if pump_def is False:
                max_value_1 = dop_function.max_value_column(work_tabl, "number_list_VU", False)
                max_value_2 = dop_function.max_value_column(work_tabl, "number_protect_VU", False)
            else:
                max_value_1 = dop_function.max_value_column(work_tabl, "number_list_VU", True, "number_pump_VU", pump_plus_one)
                max_value_2 = dop_function.max_value_column(work_tabl, "number_protect_VU", True, "number_pump_VU", pump_plus_one)
            button_bool = True if max_value_1 > 1 else False

            # Начало работы с созданным файлом
            parser = etree.XMLParser(remove_blank_text=True)
            tree   = etree.parse(new_pic_path, parser)
            root   = tree.getroot()
            # Узнаем название агрегата агрегатных защит и готовностей
            if pump_def is True: 
                str_pumps = dop_function.connect_by_sql_condition(f'umpna', f'"name"', f'id={pump_plus_one}')
                str_pumps = str_pumps[0][0]
            
            if pump_def is True: msg[f'{today} - Генерация picture .omobj {work_tabl}. {str_pumps}'] = 1
            else               : msg[f'{today} - Генерация picture .omobj {work_tabl}'] = 1
            # Исправляем координаты кнопки деблокировки и главного листа
            # Координаты зависят от количества защит на 1 листе
            modification_list_defence(max_value_2, new_pic_path, root, tree, work_tabl, pump_plus_one, button_bool, str_pumps)

            if pump_def is True: 
                data_value = dop_function.connect_by_sql_order(f'{work_tabl}', f'"id", "name", "number_list_VU", "number_protect_VU", "number_pump_VU"', '''"number_pump_VU", "number_list_VU", "number_protect_VU"''')
            else: 
                data_value = dop_function.connect_by_sql_order(f'{work_tabl}', f'"id", "name", "number_list_VU", "number_protect_VU"', '''"number_list_VU", "number_protect_VU"''')
    
            # Цикл по вкладкам защит,максимум на 240, т.е. 10 листов
            for number_list in range(max_value_1):
                # Счетчики
                count_row = 0
                count_defence_list = 0
                #Уровень первой строчки - type
                for lvl_one in root.iter('type'):
                    # Уровень второй, добавляем уровень TOP
                    object = etree.Element('object')
                    object.attrib['access-modifier'] = 'private'
                    object.attrib['name'] = attrib_top_1 + str(number_list + 1)
                    object.attrib['display-name'] = attrib_top_1 + str(number_list + 1)
                    object.attrib['uuid'] = str(uuid.uuid1())
                    object.attrib['base-type'] = attrib_top_2
                    object.attrib['base-type-id'] = base_type_id_top
                    for key, value in attrib_defence_top.items():
                        designed = etree.Element("designed")
                        designed.attrib['target'] = value[0]
                        if (key == '6') and str(number_list + 1) == '1':
                            #esigned.attrib['value'] = 'true'
                            continue
                        if (key == '6') and str(number_list + 1) != '1':
                            designed.attrib['value'] = 'false'
                        else:
                            designed.attrib['value'] = value[1]
                        designed.attrib['ver'] = value[2]
                        object.append(designed)
                    root.append(object)
                    # Добавление защит на каждую вкладку
                    for lvl_two in lvl_one.iter('object'):
                        if lvl_two.attrib['name'] == attrib_top_1 + str(number_list + 1):

                            if pump_def is True: init_1_target = f'ApSource_form_{name_tabl}s_MA{str(pump_plus_one)}'
                            else               : init_1_target = f'ApSource_form_{name_tabl}s'

                            for item in data_value:
                                number_defence      = item[0]
                                description_defence = item[1]
                                active_list_defence = item[2]
                                number_list_defence = item[3]

                                if active_list_defence is None or number_list_defence is None: continue

                                # Номере бита в регистре, т.к. берем остаток, и если остаток = 0, нам надо 4
                                bit_defence_old = int(number_defence) % 4
                                if bit_defence_old == 0: num_bit_defence = '4'
                                else                   : num_bit_defence = str(bit_defence_old)
                                # Номер регистра
                                num_registry = math.ceil(int(number_defence) / 4)

                                # Разные условия для листов защит
                                if pump_def is False:
                                    if active_list_defence == number_list + 1:
                                        # Массив данных для информации в кнопке переключения
                                        # Т.к. бит 0 будет, когда не будет остатка, т.е. по факту это 4 защита
                                        if num_bit_defence == 0: data_inf_button.append(f'Group_{num_registry}.4')
                                        else                   : data_inf_button.append(f'Group_{num_registry}.{num_bit_defence}')
                                        # Увеличиваем номера защит и счетчик всех защит
                                        counter_defence += 1
                                        count_defence_list += 1
                                        # Уровень второй, строчки - object
                                        defence = etree.Element('object')
                                        defence.attrib['access-modifier'] = 'private'
                                        defence.attrib['name']            = f'{attrib_row_1}{count_defence_list}'
                                        defence.attrib['display-name']    = f'{attrib_row_1}{count_defence_list}'
                                        defence.attrib['uuid']            = f'{uuid.uuid1()}'
                                        defence.attrib['base-type']       = attrib_row_2
                                        defence.attrib['base-type-id']    = base_type_id_row
                                        defence.attrib['ver']             = '4'
                                        object.append(defence)
                                        # Информация внутри каждого модуля
                                        for key, value in attrib_defence_row_design.items():
                                            defence_info = etree.Element("designed")
                                            defence_info.attrib['target'] = value[0]
                                            if key == '2':
                                                coord_Y = value[1] * (count_defence_list)
                                                defence_info.attrib['value'] = str(coord_Y)
                                            else:
                                                defence_info.attrib['value'] = value[1]
                                            defence_info.attrib['ver'] = value[2]
                                            defence.append(defence_info)

                                        for key, value in attrib_init_row.items():
                                            defence_init = etree.Element("init")
                                            defence_init.attrib['target'] = value[0]
                                            defence_init.attrib['ver'] = value[1]
                                            if   key == '1': defence_init.attrib['ref']   = attrib_data_1
                                            elif key == '2': defence_init.attrib['value'] = f'Group_{num_registry}'
                                            elif key == '3': defence_init.attrib['value'] = str(num_bit_defence)
                                            elif key == '4': defence_init.attrib['value'] = str(description_defence)
                                            elif key == '5': defence_init.attrib['value'] = str(counter_defence)
                                            elif key == '7': defence_init.attrib['value'] = str(number_defence)
                                            elif key == '8': defence_init.attrib['value'] = attrib_IsKTPRA
                                            defence.append(defence_init)
                                else:
                                    number_pumps = item[4]
                                    if number_pumps == pump_plus_one and active_list_defence == number_list + 1:
                                        # Массив данных для информации в кнопке переключения
                                        # Т.к. бит 0 будет, когда не будет остатка, т.е. по факту это 4 защита
                                        if num_bit_defence == 0: data_inf_button.append(f'Group_{num_registry}.4')
                                        else                   : data_inf_button.append(f'Group_{num_registry}.{num_bit_defence}')
                                        # Увеличиваем номера защит и счетчик всех защит
                                        counter_defence += 1
                                        count_defence_list += 1
                                        # Уровень второй, строчки - object
                                        defence = etree.Element('object')
                                        defence.attrib['access-modifier'] = 'private'
                                        defence.attrib['name'] = attrib_row_1 + str(count_defence_list)
                                        defence.attrib['display-name'] = attrib_row_1 + str(count_defence_list)
                                        defence.attrib['uuid'] = str(uuid.uuid1())
                                        defence.attrib['base-type'] = attrib_row_2
                                        defence.attrib['base-type-id'] = base_type_id_row
                                        defence.attrib['ver'] = '4'
                                        object.append(defence)
                                        # Информация внутри каждого модуля
                                        for key, value in attrib_defence_row_design.items():
                                            defence_info = etree.Element("designed")
                                            defence_info.attrib['target'] = value[0]
                                            if key == '2':
                                                coord_Y = value[1] * (count_defence_list)
                                                defence_info.attrib['value'] = str(coord_Y)
                                            else:
                                                defence_info.attrib['value'] = value[1]
                                            defence_info.attrib['ver'] = value[2]
                                            defence.append(defence_info)

                                        for key, value in attrib_init_row.items():
                                            defence_init = etree.Element("init")
                                            defence_init.attrib['target'] = value[0]
                                            defence_init.attrib['ver'] = value[1]
                                            if   key == '1': defence_init.attrib['ref']   = attrib_data_1 + str(pump_plus_one)
                                            elif key == '2': defence_init.attrib['value'] = 'Group_' + str(num_registry)
                                            elif key == '3': defence_init.attrib['value'] = str(num_bit_defence)
                                            elif key == '4': defence_init.attrib['value'] = str(description_defence)
                                            elif key == '5': defence_init.attrib['value'] = str(counter_defence)
                                            elif key == '6': defence_init.attrib['ref']   = attrib_data_1 + str(pump_plus_one) + '_Cmd'
                                            elif key == '7': defence_init.attrib['value'] = str(number_defence)
                                            elif key == '8': defence_init.attrib['value'] = attrib_IsKTPRA
                                            elif key == '9': defence_init.attrib['value'] = str(pump_plus_one)
                                            defence.append(defence_init)
                            # Добавляем кнопку переключения
                            if button_bool == True: button_click(new_pic_path, root, tree, max_value_1, max_value_2,
                                                                number_list + 1, data_inf_button, init_1_target, attrib_top_1, attrib_button)
                            # Массив с данными
                            data_inf_button.clear()
            tree.write(new_pic_path, pretty_print=True)
        msg[f'{today} - Генерация picture .omobj {work_tabl}: Выполнено'] = 1
        return msg
    except Exception:
        msg[f'{today} - Генерация picture .omobj {work_tabl}: {traceback.format_exc()}'] = 2
        return msg