from typing import Any
from lxml import etree
import uuid
import shutil
import os
from main_base import path_hmi
from main_base import General_functions
from enum import Enum
from typing import NamedTuple

CONST_SIZE_TABLE_OF_FALSE = 61
CONST_SIZE_TABLE_OF_TRUE = 103
CONST_HEIGHT_ROW = 26


class NewRowsParams(NamedTuple):
    """Параметры для функции создания новых строк."""
    object: str
    access_modifier: str
    name: str
    display_name: str
    uuid: str
    base_type: str
    base_type_id: str
    ver: str | None


class NumberColumn(Enum):
    '''Перечисление статических столбцов таблицы.'''
    NUMBER_LIST_VU = 'number_list_VU'
    ORDER_NUMBER_FOR_VU = 'order_number_for_VU'
    TAG = 'tag'
    NAME = 'name'


class DesignedParamsThree(NamedTuple):
    target: str
    value: str
    ver: str


class DesignedParamsTwo(NamedTuple):
    target: str
    ver: str


class BaseAlarmMap():
    '''Базовый класс создания карты табло и сирен.'''
    attrib_uts_row_design = {'1': DesignedParamsThree(target='X', value='0', ver='5'),
                             '2': DesignedParamsThree(target='Y', value=26, ver='5'),
                             '3': DesignedParamsThree(target='Rotation', value='0', ver='5'),
                             '4': DesignedParamsThree(target='Width', value='854', ver='5'),
                             '5': DesignedParamsThree(target='Height', value='26', ver='5')}
    attrib_page_top = {'1': DesignedParamsThree(target='X', value='8', ver='5'),
                       '2': DesignedParamsThree(target='Y', value='53', ver='5'),
                       '3': DesignedParamsThree(target='ZValue', value='0', ver='5'),
                       '4': DesignedParamsThree(target='Rotation', value='0', ver='5'),
                       '5': DesignedParamsThree(target='Scale', value='1', ver='5'),
                       '6': DesignedParamsThree(target='Width', value='854', ver='5'),
                       '7': DesignedParamsThree(target='Height', value='26', ver='5'),
                       '8': DesignedParamsThree(target='Opacity', value='1', ver='5'),
                       '9': DesignedParamsThree(target='Enabled', value='true', ver='5'),
                       '10': DesignedParamsThree(target='Tooltip', value='', ver='5'),
                       '11': DesignedParamsThree(target='RoundingRadius', value='0', ver='5'),
                       '12': DesignedParamsThree(target='PenColor', value='4278190080', ver='5'),
                       '13': DesignedParamsThree(target='PenStyle', value='1', ver='5'),
                       '14': DesignedParamsThree(target='PenWidth', value='1', ver='5'),
                       '15': DesignedParamsThree(target='BrushColor', value='4278190080', ver='5'),
                       '16': DesignedParamsThree(target='BrushStyle', value='0', ver='5'),
                       '17': DesignedParamsThree(target='Visible', value='', ver='5')}
    attrib_row_init_UTS = {'1': DesignedParamsTwo(target='_link_init_ApSource_type_uts_row', ver='5'),
                           '2': DesignedParamsTwo(target='_init_uts_tag', ver='5'),
                           '3': DesignedParamsTwo(target='form_show_verify_on', ver='5'),
                           '4': DesignedParamsTwo(target='form_show_verify_off', ver='5')}
    button_designed = {'1': DesignedParamsThree(target='X', value='8', ver='5'),
                       '2': DesignedParamsThree(target='Y', value='687', ver='5'),
                       '3': DesignedParamsThree(target='Rotation', value='0', ver='5'),
                       '4': DesignedParamsThree(target='Width', value='40', ver='5'),
                       '5': DesignedParamsThree(target='Height', value='30', ver='5')}
    button_init = {'1': DesignedParamsTwo(target='page_number', ver='5'),
                   '2': DesignedParamsTwo(target='VisibleObject', ver='5'),
                   '3': DesignedParamsTwo(target='UnVisibleObject1', ver='5'),
                   '4': DesignedParamsTwo(target='UnVisibleObject2', ver='5'),
                   '5': DesignedParamsTwo(target='UnVisibleObject3', ver='5'),
                   '6': DesignedParamsTwo(target='UnVisibleObject4', ver='5'),
                   '7': DesignedParamsTwo(target='UnVisibleObject5', ver='5'),
                   '8': DesignedParamsTwo(target='UnVisibleObject6', ver='5'),
                   '9': DesignedParamsTwo(target='UnVisibleObject7', ver='5'),
                   '10': DesignedParamsTwo(target='UnVisibleObject8', ver='5'),
                   '11': DesignedParamsTwo(target='_link_init_ApSource_type_uts_button', ver='5')}

    name_title = 'Управление сигнализацией'
    attrib_top_1 = 'page_'
    attrib_top_2 = 'Rectangle'
    attrib_row_1 = 'type_uts_row_'
    attrib_row_2 = 'type_uts_row'
    base_type_id_top = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'
    base_type_id_row = '70e32123-f413-4246-a6d8-6eb96bd1f953'
    coordinate_Width = '870'


class UTS(BaseAlarmMap):
    '''Отдельный класс для таблицы UTS.'''
    text_end = 'Лист табло и сирен'
    attrib_data_1 = 'ApSource_form_UTSs'
    name_form = 'Form_UTS'
    name_apsoure = 'ApSource_form_UTSs'
    designed_path = 'UTSs'


class UPTS(BaseAlarmMap):
    '''Отдельный класс для таблицы UPTS.'''
    text_end = 'Лист пожарных табло и сирен'
    attrib_data_1 = 'ApSource_form_UPTSs'
    name_form = 'Form_UPTS'
    name_apsoure = 'ApSource_form_UPTSs'
    designed_path = 'UPTSs'


class ParserFile():
    '''Парсер файла картинки'''
    def __init__(self, new_pic_path: str) -> None:
        parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
        self.tree = etree.parse(new_pic_path, parser)
        self.root = self.tree.getroot()

    def __call__(self, *args: Any, **kwds: Any):
        return self.root, self.tree

    def modification_list_uts_upts(self, max_value_2: int, path_file: str,
                                   active_tabl: str, button_bool: bool):
        """Модификация шаблона карты сигнализаций

        Args:
            max_value_2 (int): максимальное кол-во защит на листе
            path_file (str): путь новой картинки
            active_tabl (str): активный лист таблицы
            button_bool (bool): флаг показа кнопок
        """
        def update_string(object: dict, key: str, value: str, new_value: str):
            '''Поиск и обновление строки'''
            if object[key] == value:
                object[key] = new_value

        table = UTS() if active_tabl == 'uts' else UPTS()

        for lvl in self.root.iter('type'):
            # type
            update_string(lvl.attrib, 'name', 'name', table.name_form)
            update_string(lvl.attrib, 'display-name', 'name', table.name_form)
            update_string(lvl.attrib, 'uuid', 'uuid', str(uuid.uuid1()))

            for lvl_two in lvl.iter('designed'):
                if lvl_two.attrib['value'] == 'coordinate_H':
                    if button_bool:
                        lvl_two.attrib['value'] = str(((max_value_2 + 1) * CONST_HEIGHT_ROW) + CONST_SIZE_TABLE_OF_TRUE)
                    else:
                        lvl_two.attrib['value'] = str(((max_value_2 + 1) * CONST_HEIGHT_ROW) + CONST_SIZE_TABLE_OF_FALSE)

                update_string(lvl_two.attrib, 'value', 'coordinate_W', table.coordinate_Width)
                update_string(lvl_two.attrib, 'value', 'name_list', table.name_title)

            # 2 level
            for lvl_two in lvl.iter('object'):
                update_string(lvl_two.attrib, 'name', 'ApTemplate', table.name_apsoure)
                update_string(lvl_two.attrib, 'display-name', 'ApTemplate', table.name_apsoure)

                for lvl_three in lvl_two.iter('designed'):
                    update_string(lvl_three.attrib, 'value', 'designed_path', table.designed_path)

                    if lvl_three.attrib['value'] == 'designed_path':
                        lvl_three.attrib['value'] = table.designed_path
        self.tree.write(path_file, pretty_print=True)

    def new_rows(self, params: NewRowsParams):
        """Создаем новые строки."""
        object = etree.Element(params.object)
        object.attrib['access-modifier'] = params.access_modifier
        object.attrib['name'] = params.name
        object.attrib['display-name'] = params.display_name
        object.attrib['uuid'] = params.uuid
        object.attrib['base-type'] = params.base_type
        object.attrib['base-type-id'] = params.base_type_id

        if params.ver:
            object.attrib['ver'] = params.ver

        return object

    def parser_page(self, table: UTS | UPTS, number_list: int, root):
        """Создаем область страницы"""
        object = self.new_rows(NewRowsParams(
            object='object',
            access_modifier='private',
            name=f'{table.attrib_top_1}{str(number_list + 1)}',
            display_name=f'{table.attrib_top_1}{str(number_list + 1)}',
            uuid=str(uuid.uuid1()),
            base_type=table.attrib_top_2,
            base_type_id=table.base_type_id_top,
            ver=None))

        for key, value in table.attrib_page_top.items():
            designed = etree.Element("designed")
            designed.attrib['target'] = value.target
            if (key == '17') and str(number_list + 1) == '1':
                designed.attrib['value'] = 'true'
            elif (key == '17') and str(number_list + 1) != '1':
                designed.attrib['value'] = 'false'
            else:
                designed.attrib['value'] = value.value
            designed.attrib['ver'] = value.ver
            object.append(designed)
        root.append(object)
        return object

    def parser_siren(self, table: UTS | UPTS, object):
        """Парсинг сирены (зуммер)."""
        siren = self.new_rows(NewRowsParams(
            object='object',
            access_modifier='private',
            name='type_siren',
            display_name='type_siren',
            uuid=str(uuid.uuid1()),
            base_type='type_uts_siren',
            base_type_id='9b36c57c-7b17-4397-b329-a35cbb9d5056',
            ver='5'))
        object.append(siren)

        for key, value in table.attrib_uts_row_design.items():
            siren_info = etree.Element("designed")
            siren_info.attrib['target'] = value.target
            if key == '2':
                siren_info.attrib['value'] = "0"
            else:
                siren_info.attrib['value'] = value.value
            siren_info.attrib['ver'] = value.ver
            siren.append(siren_info)

    def parser_uts_signal(self, table: UTS | UPTS, object, count_uts: int,
                          position_on_list: int, uts_tag: str):
        """Добавляем строки из SQL базы

        Args:
            table (UTS | UPTS): выбор таблицы
            object (_type_): объект парсинга
            count_uts (int): счетчик сирены или табло
            position_on_list (int): позиция листа
            uts_tag (str): тег сигнала
        """
        uts = self.new_rows(NewRowsParams(
            object='object',
            access_modifier='private',
            name=f'{table.attrib_row_1}{str(count_uts)}',
            display_name=f'{table.attrib_row_1}{str(count_uts)}',
            uuid=str(uuid.uuid1()),
            base_type=f'{table.attrib_row_2}',
            base_type_id=f'{table.base_type_id_row}',
            ver='5'))

        object.append(uts)
        # Информация внутри каждого модуля
        for key, value in table.attrib_uts_row_design.items():
            uts_info = etree.Element("designed")
            uts_info.attrib['target'] = value.target
            if key == '2':
                coord_Y = value.value * (position_on_list)
                uts_info.attrib['value'] = str(coord_Y)
            else:
                uts_info.attrib['value'] = value.value
            uts_info.attrib['ver'] = value.ver
            uts.append(uts_info)

        for key, value in table.attrib_row_init_UTS.items():
            uts_init = etree.Element("init")
            uts_init.attrib['target'] = value.target
            uts_init.attrib['ver'] = value.ver
            if key == '1':
                uts_init.attrib['ref'] = table.attrib_data_1
            elif key == '2':
                uts_init.attrib['value'] = uts_tag
            else:
                uts_init.attrib['value'] = 'false'
            uts.append(uts_init)

    def adding_button(self, table: UTS | UPTS, path_file: str, root, tree,
                      max_value_1: int, max_value_2: int, page: int,
                      data_inf_button: list, init_1_target: str):
        """Добавление кнопки переключения

        Args:
            table (UTS | UPTS): Таблица из базы
            path_file (str): Путь новой картинки
            root (_type_): парсниг файла
            tree (_type_): парсинг файла
            max_value_1 (int): кол-во страниц
            max_value_2 (int): количество табло и сирен на странице
            page (int): текущая страница
            data_inf_button (list): массив данных для кнопки
            init_1_target (str): данные для кнопки
        """
        for lvl_one in root.iter('type'):
            object = self.new_rows(NewRowsParams(
                object='object',
                access_modifier='private',
                name=f'type_uts_button_{str(page)}',
                display_name=f'type_uts_button_{str(page)}',
                uuid=str(uuid.uuid1()),
                base_type='type_uts_button',
                base_type_id='e9a1de57-5c19-4ad3-98d9-aea8ce2813fe',
                ver='5'))

            for key, value in table.button_designed.items():
                designed = etree.Element("designed")
                designed.attrib['target'] = value.target
                # Координаты по X - 1
                if (key == '1') and (page == 1):
                    designed.attrib['value'] = value.value
                elif (key == '1') and (page > 1):
                    designed.attrib['value'] = str(int(value[1]) + (50 * (page - 1)))
                # по Y - 2
                elif (key == '2'):
                    designed.attrib['value'] = str(((max_value_2) * 26) + 63)
                else:
                    designed.attrib['value'] = value.value
                designed.attrib['ver'] = value.ver
                object.append(designed)

            for key_1, value_1 in table.button_init.items():
                init = etree.Element("init")
                init.attrib['target'] = value_1.target
                init.attrib['ver'] = value_1.ver
                if key_1 == '1':
                    init.attrib['value'] = str(page)
                elif key_1 == '2':
                    init.attrib['ref'] = 'page_' + str(page)
                elif key_1 != str(page + 2) and ((int(key_1) - 2) <= max_value_1):
                    init.attrib['ref'] = 'page_' + str(int(key_1) - 2)
                elif key_1 == '11':
                    init.attrib['ref'] = init_1_target
                else:
                    init.attrib['ref'] = 'empty_link'
                object.append(init)

            for count in range(len(data_inf_button)):
                init_1 = etree.Element("init")
                init_1.attrib['target'] = f'uts{count + 1}_path'
                init_1.attrib['ver'] = '5'
                init_1.attrib['value'] = data_inf_button[count]
                object.append(init_1)
            root.append(object)
        tree.write(path_file, pretty_print=True)


class Alarm_map():
    '''Основной код заполнения формы'''
    def __init__(self, work_tabl: str) -> None:
        """Инициализация класса табло и сирен.

        Args:
            work_tabl (str): Таблица из базы SQL
        """
        self._work_tabl = work_tabl.lower()
        self.filling_template()

    def filling_template(self) -> dict:
        """Заполнение шаблона табло и сирен.
        """
        data_inf_button = []
        msg = {}

        dop_function = General_functions()
        table = UTS() if self._work_tabl == 'uts' else UPTS()
        # Проверим на существование файл
        new_pic_path = f'{path_hmi}\\Form_UTS.omobj' if self._work_tabl == 'uts' else f'{path_hmi}\\Form_UPTS.omobj'

        if os.path.isfile(new_pic_path):
            os.remove(new_pic_path)
        # Копируем шаблон
        shutil.copy2(f'{path_hmi}\\Form_UTS_UPTS_default.omobj', new_pic_path)
        # Счетчик всех табло и сирен в карте
        counter_uts = 0

        # Максимальное число листов, необходимость переключения страниц
        max_value_1 = dop_function.max_value_column(self._work_tabl, NumberColumn.NUMBER_LIST_VU.value, False)
        max_value_2 = dop_function.max_value_column(self._work_tabl, NumberColumn.ORDER_NUMBER_FOR_VU.value, False)
        button_bool = True if int(max_value_1) > 1 else False

        # Начало работы с созданным файлом
        parser = ParserFile(new_pic_path)
        root, tree = parser()

        # Исправляем размеры главного листа
        # Размеры зависят от количества табло и сирен на 1 листе
        parser.modification_list_uts_upts(int(max_value_2), new_pic_path,
                                          self._work_tabl, button_bool)

        data_value = dop_function.connect_by_sql_order(self._work_tabl,
                                f'{NumberColumn.TAG.value}, "{NumberColumn.NUMBER_LIST_VU.value}", "{NumberColumn.ORDER_NUMBER_FOR_VU.value}"',
                                f'"{NumberColumn.NUMBER_LIST_VU.value}", "{NumberColumn.ORDER_NUMBER_FOR_VU.value}"')
        # Цикл по вкладкам табло и сирен,максимум на 240, т.е. 10 листов
        for number_list in range(int(max_value_1)):
            count_uts = 0
            # Уровень первой строчки - type
            for lvl_one in root.iter('type'):

                object = parser.parser_page(table, number_list, root)

                for lvl_two in lvl_one.iter('object'):
                    if lvl_two.attrib['name'] == f'{table.attrib_top_1}{str(number_list + 1)}':

                        if not number_list:
                            parser.parser_siren(table, object)

                        # Ходим ищем текущий активный лист
                        for item in data_value:
                            uts_tag = item[0]
                            active_list_uts = item[1]
                            position_on_list = item[2]

                            if int(active_list_uts) == (number_list + 1):

                                # Информации в кнопке переключения
                                data_inf_button.append(f'{uts_tag}.s_State')

                                counter_uts += 1
                                count_uts += 1

                                parser.parser_uts_signal(table, object,
                                                         count_uts,
                                                         int(position_on_list),
                                                         uts_tag)

                        # Добавляем кнопку переключения
                        if button_bool:
                            init_1_target = f'ApSource_form_{self._work_tabl}s'
                            parser.adding_button(table, new_pic_path, root, tree,
                                                int(max_value_1), int(max_value_2),
                                                (number_list + 1), data_inf_button,
                                                init_1_target)
                        # Массив с данными
                        data_inf_button.clear()

        tree.write(new_pic_path, pretty_print=True)
        return msg
