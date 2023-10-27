import uuid
import shutil
import os
import traceback
from lxml import etree
from enum import Enum
from typing import NamedTuple
from general_functions import General_functions
from model_new import connect
from request_sql import RequestSQL


SIZE_TABLE_FALSE = 61
SIZE_TABLE_TRUE = 103
HEIGHT_ROW = 26
OFFSET_CLICK_X = 50
OFFSET_CLICK_Y = 63


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


class NumName(Enum):
    '''Перечисление статических столбцов таблицы.'''
    NUM_LIST_VU = 'number_list_VU'
    NUM_SIREN_VU = 'number_siren_VU'
    PATH = 'path'
    NAME = 'name'
    TYPE_ROOT = 'type'
    PRIVATE = 'private'
    OBJECT = 'object'
    DESIGNED = 'designed'
    INIT = 'init'
    REF = 'ref'
    NAME_ATR = 'name'
    APSOURCE = 'ApSource'
    D_NAME = 'display-name'
    T_NAME = 'type_name'
    VALUE_ATR = 'value'
    UUID = 'uuid'
    WIDTH = 'Width'
    HEIGHT = 'Height'
    W_WIDTH = 'W_Width'
    W_HEIGHT = 'W_Height'
    W_CAPTION = 'W_Caption'
    VER = '5'


class DesignedParamsThree(NamedTuple):
    target: str
    value: str
    ver: str


class DesignedParamsTwo(NamedTuple):
    target: str
    ver: str


class DesignedParamsAttr(NamedTuple):
    designed: str
    target: str
    value: str
    ver: str


class DesignedParams(NamedTuple):
    target: str
    value: str


class InitParamsAttr(NamedTuple):
    init: str
    target: str
    ver: str
    ref: str


class BaseAlarmMap():
    '''Базовый класс создания карты табло и сирен.'''
    attr_top = {1: DesignedParams(target='X', value='8'),
                2: DesignedParams(target='Y', value='53'),
                3: DesignedParams(target='ZValue', value='0'),
                4: DesignedParams(target='Rotation', value='0'),
                5: DesignedParams(target='Scale', value='1'),
                6: DesignedParams(target='Width', value='854'),
                7: DesignedParams(target='Height', value='26'),
                8: DesignedParams(target='Opacity', value='1'),
                9: DesignedParams(target='Enabled', value='true'),
                10: DesignedParams(target='Tooltip', value=''),
                11: DesignedParams(target='RoundingRadius', value='0'),
                12: DesignedParams(target='PenColor', value='4278190080'),
                13: DesignedParams(target='PenStyle', value='1'),
                14: DesignedParams(target='PenWidth', value='1'),
                15: DesignedParams(target='BrushColor', value='4278190080'),
                16: DesignedParams(target='BrushStyle', value='0'),
                17: DesignedParams(target='Visible', value='')}
    attr_row_design = {1: DesignedParams(target='X', value='0'),
                       2: DesignedParams(target='Y', value='0'),
                       3: DesignedParams(target='Rotation', value='0'),
                       4: DesignedParams(target='Width', value='910'),
                       5: DesignedParams(target='Height', value='26')}
    attr_row_init = {1: DesignedParams(target='_init_uts_tag', value=''),
                     2: DesignedParams(target='form_show_verify_on', value='false'),
                     3: DesignedParams(target='form_show_verify_off', value='false'),
                     4: DesignedParams(target='IsBlock', value='')}
    attr_button_design = {1: DesignedParams(target='X', value=''),
                          2: DesignedParams(target='Y', value=''),
                          3: DesignedParams(target='Rotation', value='0'),
                          4: DesignedParams(target='Width', value='40'),
                          5: DesignedParams(target='Height', value='30')}
    attr_button_init = {'1': DesignedParamsTwo(target='page_number', ver='5'),
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
    attrib_top_1 = 'page'
    attrib_top_2 = 'Rectangle'
    attrib_row = 'type_uts_row'
    bt_id_top = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'
    bt_id_row = '70e32123-f413-4246-a6d8-6eb96bd1f953'
    width = '870'
    req_1 = '"tag"'
    req_2 = '"number_list_VU" = {}'
    order = "number_siren_VU"
    init_target = '_link_init_ApSource_type_uts_row'
    type_zum = 'type_siren'
    bt_zum = 'type_uts_siren'
    bt_id_zum = '9b36c57c-7b17-4397-b329-a35cbb9d5056'
    click = 'type_uts_button'
    bt_id_click = 'e9a1de57-5c19-4ad3-98d9-aea8ce2813fe'


class UTS(BaseAlarmMap):
    '''Отдельный класс для таблицы UTS.'''
    text_end = 'Лист табло и сирен'
    name_form = 'Form_UTS'
    name_apsoure = 'ApSource_form_UTSs'
    designed_path = 'UTSs'


class UPTS(BaseAlarmMap):
    '''Отдельный класс для таблицы UPTS.'''
    text_end = 'Лист пожарных табло и сирен'
    name_form = 'Form_UPTS'
    name_apsoure = 'ApSource_form_UPTSs'
    designed_path = 'UPTSs'


class BaseFunction():
    '''Дополнительные функции, которые часто используются.'''
    def search_string(self, object: dict, key: str, value: str):
        '''Поиск строки'''
        return True if object[key] == value else False

    def new_rows_obj(self, params: NewRowsParams):
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

    def new_row_obj(self, level, name, b_t, b_t_id):
        '''Подготавливаем к созданию новых строк.'''
        object = self.new_rows_obj(NewRowsParams(
            object=NumName.OBJECT.value,
            access_modifier=NumName.PRIVATE.value,
            name=name,
            display_name=name,
            uuid=str(uuid.uuid1()),
            base_type=b_t,
            base_type_id=b_t_id,
            ver=NumName.VER.value))
        level.append(object)
        return object

    def dop_substr(self, object, params: DesignedParamsAttr):
        """Создаем новые строки."""
        dop = etree.Element(params.designed)
        dop.attrib['target'] = params.target
        dop.attrib['value'] = params.value
        dop.attrib['ver'] = params.ver
        object.append(dop)

    def dop_init_substr(self, object, params: InitParamsAttr):
        """Создаем новые строки."""
        dop = etree.Element(params.init)
        dop.attrib['target'] = params.target
        dop.attrib['ver'] = params.ver
        dop.attrib['ref'] = params.ref
        object.append(dop)

    def new_row_designed(self, object, designed, target, value):
        self.dop_substr(object, (DesignedParamsAttr(
            designed=designed,
            target=target,
            value=value,
            ver=NumName.VER.value)))

    def new_row_init(self, object, init, target, ref):
        self.dop_init_substr(object, (InitParamsAttr(
            init=init,
            target=target,
            ver=NumName.VER.value,
            ref=ref)))


class Template(BaseFunction):
    '''Редактирование шаблона перед заполнением.'''
    def __init__(self, *arg):
        self.request = arg[0]
        self.kit = arg[1]
        self.max_siren = arg[2]
        self.root = arg[3]
        self.table = arg[4]

    def update_string(self, object: dict, key: str,
                      value: str, new_value: str):
        '''Поиск и обновление строки.'''
        try:
            if object[key] == value:
                object[key] = str(new_value)
        except Exception:
            return

    def size(self, click: bool):
        '''Вычисление размера формы.'''
        if click:
            size = str(((self.max_siren + 1) * HEIGHT_ROW) + SIZE_TABLE_TRUE)
        else:
            size = str(((self.max_siren + 1) * HEIGHT_ROW) + SIZE_TABLE_FALSE)
        return size

    def upd_settings_form(self, lvl, size_h):
        '''Изменение основных настроек формы.'''
        self.update_string(lvl.attrib, NumName.NAME_ATR.value, NumName.T_NAME.value, self.kit.name_form)
        self.update_string(lvl.attrib, NumName.D_NAME.value, NumName.T_NAME.value, self.kit.name_form)
        self.update_string(lvl.attrib, NumName.UUID.value, NumName.UUID.value, str(uuid.uuid1()))

        for lvl_1 in lvl.iter(NumName.DESIGNED.value):
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.WIDTH.value, self.kit.width)
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.HEIGHT.value, size_h)
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.W_WIDTH.value, self.kit.width)
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.W_HEIGHT.value, size_h)
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.W_CAPTION.value, self.kit.name_title)

    def upd_apsource(self, lvl):
        '''Изменение раздела, где name="ApSource".'''
        for lvl_1 in lvl.iter(NumName.OBJECT.value):
            self.update_string(lvl_1.attrib, NumName.NAME_ATR.value, NumName.APSOURCE.value, self.kit.name_apsoure)
            self.update_string(lvl_1.attrib, NumName.D_NAME.value, NumName.APSOURCE.value, self.kit.name_apsoure)

            for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.PATH.value, self.kit.designed_path)

    def change_template(self, click: bool):
        '''Редактирование шаблона формы.'''
        size_h = self.size(click)
        # Type
        for lvl in self.root.iter(NumName.TYPE_ROOT.value):
            self.upd_settings_form(lvl, size_h)
            # name="ApSource"
            self.upd_apsource(lvl)


class TopRow(BaseFunction):
    '''Собираем на форме сирены по страницам.'''
    def __init__(self, max_page, root, kit, request, table, click):
        self.max_page = max_page
        self.root = root
        self.kit = kit
        self.request = request
        self.table = table
        self.click = click

    def req_table(self, page):
        '''Запрос к таблице с данными по каждой странице с защитами.'''
        req = f"{self.kit.req_2}".format(page)

        data = self.request.where_select(str(self.table).lower(),
                                         self.kit.req_1, req,
                                         self.kit.order)
        return data

    def filling_page(self, lvl):
        '''Добавляются на форму страницы.'''
        for page in range(1, self.max_page + 1):
            object = self.new_row_obj(lvl,
                                      f'{self.kit.attrib_top_1}_{page}',
                                      self.kit.attrib_top_2,
                                      self.kit.bt_id_top)

            visible = 'true' if page == 1 else 'false'
            for key, value in self.kit.attr_top.items():
                atr_val = visible if key == 17 else value[1]
                self.new_row_designed(object,
                                      NumName.DESIGNED.value,
                                      value[0], atr_val)
            # В страницы добавляются защиты
            # На первую страницу добавляем зуммер, затем остальные сирены
            if page == 1:
                self.filling_zummer(lvl, page)
            self.filling_string_page(lvl, page)

    def filling_zummer(self, lvl, page):
        '''Добавляется на форму страницы зуммер.'''
        for lvl_1 in lvl.iter(NumName.OBJECT.value):
            if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, f'{self.kit.attrib_top_1}_{page}'):

                object = self.new_row_obj(lvl_1,
                                          f'{self.kit.type_zum}',
                                          self.kit.bt_zum,
                                          self.kit.bt_id_zum)

                for key, value in self.kit.attr_row_design.items():
                    self.new_row_designed(object,
                                          NumName.DESIGNED.value,
                                          value[0], value[1])

    def filling_string_page(self, lvl, page):
        '''В страницы добавляются защиты.'''
        for lvl_1 in lvl.iter(NumName.OBJECT.value):
            if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, f'{self.kit.attrib_top_1}_{page}'):

                data = self.req_table(page)
                for i in range(1, len(data) + 1):
                    tag = data[i - 1][0]

                    object = self.new_row_obj(lvl_1,
                                              f'{self.kit.attrib_row}_{i}',
                                              self.kit.attrib_row,
                                              self.kit.bt_id_row)

                    coordY = str(HEIGHT_ROW * i)
                    for key, value in self.kit.attr_row_design.items():
                        atr_val = coordY if key == 2 else value[1]

                        self.new_row_designed(object,
                                              NumName.DESIGNED.value,
                                              value[0], atr_val)

                    for key, value in self.kit.attr_row_init.items():
                        if key == 1:
                            init_val = tag
                        elif key == 4:
                            if i == 1:
                                init_val = 'true'
                            else:
                                continue
                        else:
                            init_val = value[1]

                        self.new_row_designed(object,
                                              NumName.INIT.value,
                                              value[0], init_val)

                    self.new_row_init(object,
                                      NumName.INIT.value,
                                      self.kit.init_target,
                                      self.kit.name_apsoure)

    def form_assembly(self):
        '''Собираем сирены для добавления на форму.'''
        # Добавляется страница защиты
        for lvl in self.root.iter(NumName.TYPE_ROOT.value):
            self.filling_page(lvl)


class Button(BaseFunction):
    '''Собираем и добавляем на форму кнопки переключения страниц.'''
    def __init__(self, max_page, max_siren, root, kit, request, table):
        self.max_page = max_page
        self.max_siren = max_siren
        self.root = root
        self.kit = kit
        self.request = request
        self.table = table

    def choice_visible(self, key, page):
        '''Подставляем значения для видимости страниц.'''
        if key == 1:
            value = f'{self.kit.attrib_top}_{page}'
        elif key == 2:
            value = f'{self.kit.apsoure_name}{self.num_iter}'
        elif key > 2:
            for i in range(key, 11):
                if key == i and page == (key - 2) and self.max_page >= (key - 2):
                    value = 'empty_link'
                    break
                elif self.max_page >= (key - 2):
                    value = f'{self.kit.attrib_top}_{key - 2}'
                    break
                else:
                    value = 'empty_link'
                    break
        return value

    def req_table(self, page):
        '''Запрос к таблице с данными по каждой странице с защитами.'''
        req = f"{self.kit.req_2}".format(self.num_iter, page)

        if self.choice_table(self.table):
            req = f"{self.kit.req_2}".format(page)

        data = self.request.where_select(str(self.table).lower(),
                                         self.kit.req_path, req,
                                         self.kit.order)
        return data

    def def_path(self, id_num):
        '''Указываем группы для подсветки кнопки.'''
        bit_def = int(id_num) % 4
        num_bit_defence = '4' if bit_def == 0 else str(bit_def)
        num_registry = math.ceil(int(id_num) / 4)

        return f'Group_{num_registry}.4' if num_bit_defence == 0 else f'Group_{num_registry}.{num_bit_defence}'

    def filling_button(self, lvl):
        '''Добавляется на форму кнопка.'''
        for page in range(1, self.max_page + 1):
            object = self.new_row_obj(lvl,
                                      f'{self.kit.click}_{page}',
                                      self.kit.click,
                                      self.kit.bt_id_click)

            coordX = 8 + (OFFSET_CLICK_X * (page - 1))
            coordY = (self.max_siren * HEIGHT_ROW) + OFFSET_CLICK_Y
            for key, value in self.kit.attr_button_design.items():
                if key == 1:
                    atr_val = coordX
                elif key == 2:
                    atr_val = coordY
                else:
                    atr_val = value[1]
                self.new_row_designed(object,
                                      NumName.DESIGNED.value,
                                      value[0], str(atr_val))

            self.new_row_designed(object, NumName.INIT.value,
                                  'page_number', str(page))

            # for key, value in self.kit.attr_button_init.items():
            #     self.new_row_init(object,
            #                       NumName.INIT.value,
            #                       value[0],
            #                       self.choice_visible(key, page))

            # data = self.req_table(page)
            # for i in range(1, len(data) + 1):
            #     self.new_row_init(object,
            #                       NumName.INIT.value,
            #                       f'def{i}_path',
            #                       self.def_path(data[i - 1][0]))

    def form_assembly(self):
        '''Заполнение кнопкой.'''
        for lvl in self.root.iter(NumName.TYPE_ROOT.value):
            self.filling_button(lvl)


class Alarm_map():
    '''Заполнение карт табло и сирен.'''
    def __init__(self, table):
        # self.logsTextEdit = logtext
        self.dop_function = General_functions()
        self.table = table

    def check_template(self, name: str) -> str:
        '''Проверка шаблона и создание на его основе новой формы.'''
        new_picture = f'{connect.path_hmi}\\{name}.omobj'

        if os.path.isfile(new_picture):
            os.remove(new_picture)
        shutil.copy2(f'{connect.path_hmi_sample}\\Form_UTS_UPTS_default.omobj',
                     new_picture)
        return new_picture

    def max_condition(self):
        '''Вычисляем из БД максимальное кол-во страниц и сирен.'''
        max_page = self.request.max_value_column(self.table,
                                                 NumName.NUM_LIST_VU.value)
        max_siren = self.request.max_value_column(self.table,
                                                  NumName.NUM_SIREN_VU.value)
        return int(max_page), int(max_siren)

    def filling_template(self):
        """Заполнение шаблона табло и сирен."""
        try:
            self.kit = UTS() if self.table == 'UTS' else UPTS()
            self.request = RequestSQL()
            # self.logsTextEdit.logs_msg(f'''HMI. {self.table}. Заполнение формы''', 1)

            # Max кол-во страниц, защит и кнопка переключения на форме
            max_page, max_siren = self.max_condition()
            if max_page is None or max_siren is None:
                # self.logsTextEdit.logs_msg(f'''HMI. {self.table}.
                #                             Не определено количество
                #                             страниц переключений
                #                             или сирен''', 2)
                return
            self.click = True if max_page > 1 else False

            # На основе шаблона -> новая форма
            new_form = self.check_template(self.kit.name_form)
            # Чтение шаблона
            root, tree = self.dop_function.xmlParser(new_form)
            # Изменение шаблона
            template = Template(self.request, self.kit,
                                max_siren, root, self.table)
            template.change_template(self.click)
            # Сборка сирен
            siren = TopRow(max_page, root, self.kit, self.request,
                           self.table, self.click)
            siren.form_assembly()
            # Добавление кнопок переключения
            if self.click:
                button = Button(max_page, max_siren, root, self.kit,
                                self.request, self.table)
                button.form_assembly()

            tree.write(new_form, pretty_print=True, encoding='utf-8')
            # self.logsTextEdit.logs_msg(f'''HMI. {self.table}.
            #                            Picture заполнена''', 1)
        except Exception:
            print(f'Генерация picture .omobj {traceback.format_exc()}')


a = Alarm_map('UTS')
a.filling_template()
