import uuid
import shutil
import os
import sys
import traceback
import math
from enum import Enum
from lxml import etree
from general_functions import General_functions
from typing import NamedTuple
from request_sql import RequestSQL
sys.path.append('../Project_Signal_Generator')
from model_new import connect

CONST_INDEX_FOR = 1
OFFSET_RESET = 43
OFFSET_CLICK = 86


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


class DesignedParamsAttr(NamedTuple):
    designed: str
    target: str
    value: str
    ver: str


class InitParamsAttr(NamedTuple):
    init: str
    target: str
    ver: str
    ref: str


class DesignedParams(NamedTuple):
    target: str
    value: str


class NumName(Enum):
    '''Перечисление статических названий.'''
    TYPE_ROOT = 'type'
    PRIVATE = 'private'
    OBJECT = 'object'
    DESIGNED = 'designed'
    INIT = 'init'
    REF = 'ref'
    LINK_REF = 'link_ref'
    NAME_ATR = 'name'
    APSOURCE = 'ApSource'
    PATH_SERVER = 'path_server'
    D_NAME = 'display-name'
    T_NAME = 'type_name'
    TITLE_NAME = 'title_name'
    VALUE_ATR = 'value'
    UUID = 'uuid'
    WIDTH = 'Width'
    HEIGHT = 'Height'
    W_WIDTH = 'W_Width'
    W_HEIGHT = 'W_Height'
    W_CAPTION = 'W_Caption'
    COOR_Y = 'coord_Y'
    IsKTPRA = 'IsKTPRA'
    VISIBLE = 'Visible'
    RESET_BUT = 'type_reset_all_button_1'
    VER = '5'


class BaseDefenceMap():
    '''Базовый класс карт защит и готовностей.'''
    COLUMN_PUMP = "number_pump_VU"
    COLUMN_LIST = "number_list_VU"
    COLUMN_PROT = "number_protect_VU"
    REQ_ONE_FORM = '''"id", "name", "number_list_VU", "number_protect_VU"'''
    REQ_MANY_FORM = '''"id", "name", "number_list_VU",
                    "number_protect_VU", "number_pump_VU"'''
    TABL_UMPNA = 'umpna'
    COLUMN_NAME = 'name'
    req_1 = '"id_num", "name", "disablemasking"'
    req_path = '"id_num", "number_protect_VU"'
    order = "number_protect_VU"

    attr_top = {1: DesignedParams(target='X', value='1'),
                2: DesignedParams(target='Y', value='39'),
                3: DesignedParams(target='Rotation', value='0'),
                4: DesignedParams(target='Width', value=''),
                5: DesignedParams(target='Height', value='26'),
                6: DesignedParams(target='Visible', value='')}

    attr_row_design = {1: DesignedParams(target='X', value='0'),
                       2: DesignedParams(target='Y', value=''),
                       3: DesignedParams(target='Rotation', value='0'),
                       4: DesignedParams(target='Width', value=''),
                       5: DesignedParams(target='Height', value='26')}

    attr_row_ktpr = {1: DesignedParams(target='_init_group_number', value=''),
                     2: DesignedParams(target='_init_row_number', value=''),
                     3: DesignedParams(target='_def_name', value=''),
                     4: DesignedParams(target='_def_number', value=''),
                     5: DesignedParams(target='_def_number_inarray', value=''),
                     6: DesignedParams(target='NotMasked', value='')}

    attr_row_ktpra = {1: DesignedParams(target='_init_group_number', value=''),
                      2: DesignedParams(target='_init_row_number', value=''),
                      3: DesignedParams(target='_def_name', value=''),
                      4: DesignedParams(target='_def_number', value=''),
                      5: DesignedParams(target='_def_number_inarray', value=''),
                      6: DesignedParams(target='NotMasked', value=''),
                      7: DesignedParams(target='MAnumber', value=''),
                      8: DesignedParams(target='IsKTPRA', value='')}

    attr_row_gmpna = {1: DesignedParams(target='_init_group_number', value=''),
                      2: DesignedParams(target='_init_row_number', value=''),
                      3: DesignedParams(target='_readiness_name', value=''),
                      4: DesignedParams(target='_readiness_number', value=''),
                      5: DesignedParams(target='_readiness_number_inarray', value=''),
                      6: DesignedParams(target='NotMasked', value=''),
                      7: DesignedParams(target='MAnumber', value='')}

    attr_button_design = {1: DesignedParams(target='X', value=''),
                          2: DesignedParams(target='Y', value='2'),
                          3: DesignedParams(target='Rotation', value='0'),
                          4: DesignedParams(target='Width', value='84'),
                          5: DesignedParams(target='Height', value='34')}

    attr_button_init = {1: DesignedParams(target='VisibleObject', value=''),
                        2: DesignedParams(target='_link_init_ApSource_type_defence_button', value=''),
                        3: DesignedParams(target='UnVisibleObject1', value=''),
                        4: DesignedParams(target='UnVisibleObject2', value=''),
                        5: DesignedParams(target='UnVisibleObject3', value=''),
                        6: DesignedParams(target='UnVisibleObject4', value=''),
                        7: DesignedParams(target='UnVisibleObject5', value=''),
                        8: DesignedParams(target='UnVisibleObject6', value=''),
                        9: DesignedParams(target='UnVisibleObject7', value=''),
                        10: DesignedParams(target='UnVisibleObject8', value='')}


class KTPR(BaseDefenceMap):
    '''Отдельный класс для таблицы KTPR.'''
    caption_name = 'Карта общестанционных защит'
    map_name = 'Form_Station_Defences'
    apsoure_name = 'ApSource_form_KTPRs'
    path_server = 'KTPRs'
    link_ref = 'unit.WorkspaceControl.Station_Defences_Control'
    attrib_top = 'type_defence_top'
    attrib_row = 'type_defence_row'
    attrib_click = 'type_defence_button'
    bt_id_top = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
    bt_id_row = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    bt_id_click = '2832c785-46a5-4217-ad3d-c0505077e057'
    target_row = '_link_init_ApSource_type_defence_row'
    width = '1102'
    width_row_top = '1100'
    height = (26, 77)
    isktpra = 'false'
    req_1 = '"id", "name", "disablemasking"'
    req_path = '"id", "number_protect_VU"'
    req_2 = '"number_list_VU" = {}'


class KTPRP(BaseDefenceMap):
    caption_name = 'Карта противопожарных защит'
    map_name = 'Form_Station_Defences'
    apsoure_name = 'ApSource_form_KTPRs'
    path_server = 'KTPRs'
    link_ref = 'unit.WorkspaceControl.Station_Defences_Control'
    attrib_top = 'type_defence_top'
    attrib_row = 'type_defence_row'
    attrib_click = 'type_defence_button'
    bt_id_top = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
    bt_id_row = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    bt_id_click = '2832c785-46a5-4217-ad3d-c0505077e057'
    target_row = '_link_init_ApSource_type_defence_row'
    width = '1102'
    width_row_top = '1100'
    height = (26, 77)
    isktpra = 'false'
    req_1 = '"id", "name", "disablemasking"'
    req_path = '"id", "number_protect_VU"'
    req_2 = '"number_list_VU" = {}'


class KTPRA(BaseDefenceMap):
    caption_name = 'Карта агрегатных защит'
    map_name = 'Form_Defences_MA'
    apsoure_name = 'ApSource_form_KTPRAs_MA'
    path_server = 'KTPRAs.KTPRAs'
    link_ref = 'unit.WorkspaceControl.Defences_Control_NA'
    attrib_top = 'type_defence_top'
    attrib_row = 'type_defence_row'
    attrib_click = 'type_defence_button'
    bt_id_top = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
    bt_id_row = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    bt_id_click = '2832c785-46a5-4217-ad3d-c0505077e057'
    target_row = '_link_init_ApSource_type_defence_row'
    width = '1102'
    width_row_top = '1100'
    height = (26, 77)
    isktpra = 'true'
    req_1 = '"id_num", "name", "disablemasking"'
    req_path = '"id_num", "number_protect_VU"'
    req_2 = '"number_pump_VU" = {} and "number_list_VU" = {}'


class GMPNA(BaseDefenceMap):
    caption_name = 'Карта агрегатных готовностей'
    map_name = 'Form_Readiness_MA'
    apsoure_name = 'ApSource_form_GMPNAs_MA'
    path_server = 'GMPNAs.GMPNAs'
    link_ref = 'unit.WorkspaceControl.Readiness_Control_NA'
    attrib_top = 'type_readiness_top'
    attrib_row = 'type_readiness_row'
    attrib_click = 'type_defence_button'
    bt_id_top = 'b08a935f-b03d-42e0-96c4-dc639b70d499'
    bt_id_row = '48231209-9a9f-42cf-9b38-ef1ef5cc7403'
    bt_id_click = '2832c785-46a5-4217-ad3d-c0505077e057'
    target_row = '_link_init_ApSource_type_readiness_row'
    width = '856'
    width_row_top = '854'
    height = (26, 43, 2)
    isktpra = 'false'
    req_1 = '"id_num", "name", "disablemasking"'
    req_path = '"id_num", "number_protect_VU"'
    req_2 = '"number_pump_VU" = {} and "number_list_VU" = {}'


class BaseFunction():
    '''Дополнительные функции, которые часто используются.'''
    def choice_table(self, table: str) -> bool:
        '''Проверяем принадлежность к таблице KTPR, KTPRP'''
        return True if table in ['KTPR', 'KTPRP'] else False

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
    '''Редактирование шаблона перед запонением.'''
    def __init__(self, *arg):
        self.request = arg[0]
        self.kit = arg[1]
        self.max_prot = arg[2]
        self.root = arg[3]
        self.table = arg[4]

    def update_string(self, object: dict, key: str,
                      value: str, new_value: str):
        '''Поиск и обновление строки'''
        try:
            if object[key] == value:
                object[key] = str(new_value)
        except Exception:
            return

    def select_name(self, pump: int, fl_one_form: bool):
        '''Подбор названий взамисимости от таблицы.'''
        name_caption = self.kit.caption_name
        name_map = self.kit.map_name
        name_ap = self.kit.apsoure_name
        name_path = self.kit.path_server
        link_ref = self.kit.link_ref
        if not fl_one_form:
            name_pump = self.request.where_id_select(self.kit.TABL_UMPNA,
                                                     self.kit.COLUMN_NAME,
                                                     pump)

            name_caption = f'{self.kit.caption_name} {name_pump[0]}'
            name_map = f'{self.kit.map_name}{pump}'
            name_ap = f'{self.kit.apsoure_name}{pump}'
            name_path = f'{self.kit.path_server}_{pump}'
            link_ref = f'{self.kit.link_ref}_{pump}'
        return name_caption, name_map, name_ap, name_path, link_ref

    def size(self, click: bool):
        '''Вычисление размера формы.'''
        if self.kit.path_server == 'GMPNAs.GMPNAs' and not click:
            size_h = str(((self.max_prot + 1) * self.kit.height[0]) + self.kit.height[2])
        else:
            size_h = str(((self.max_prot + 1) * self.kit.height[0]) + self.kit.height[1])

        button_coord_y = str(((self.max_prot + 1) * self.kit.height[0]) + OFFSET_RESET)
        return size_h, button_coord_y

    def upd_settings_form(self, lvl, name, size_h):
        '''Изменение основных настроек формы.'''
        self.update_string(lvl.attrib, NumName.NAME_ATR.value, NumName.T_NAME.value, name[1])
        self.update_string(lvl.attrib, NumName.D_NAME.value, NumName.T_NAME.value, name[1])
        self.update_string(lvl.attrib, NumName.UUID.value, NumName.UUID.value, str(uuid.uuid1()))
        for lvl_1 in lvl.iter(NumName.DESIGNED.value):
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.WIDTH.value, self.kit.width)
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.HEIGHT.value, size_h)
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.W_WIDTH.value, self.kit.width)
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.W_HEIGHT.value, size_h)
            self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.W_CAPTION.value, name[0])

    def upd_apsource(self, lvl, name):
        '''Изменение раздела, где name="ApSource".'''
        for lvl_1 in lvl.iter(NumName.OBJECT.value):
            self.update_string(lvl_1.attrib, NumName.NAME_ATR.value, NumName.APSOURCE.value, name[2])
            self.update_string(lvl_1.attrib, NumName.D_NAME.value, NumName.APSOURCE.value, name[2])
            self.update_string(lvl_1.attrib, NumName.UUID.value, NumName.UUID.value, str(uuid.uuid1()))
            for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.PATH_SERVER.value, name[3])

    def upd_empty_link(self, lvl, name):
        for lvl_1 in lvl.iter(NumName.OBJECT.value):
            self.update_string(lvl_1.attrib, NumName.UUID.value, NumName.UUID.value, str(uuid.uuid1()))

    def upd_basetype_win(self, lvl, name):
        '''Изменение раздела, где name="type_name" и base-type=Window.'''
        for lvl_1 in lvl.iter(NumName.OBJECT.value):
            self.update_string(lvl_1.attrib, NumName.NAME_ATR.value, NumName.T_NAME.value, name[1])
            self.update_string(lvl_1.attrib, NumName.D_NAME.value, NumName.T_NAME.value, name[1])
            self.update_string(lvl_1.attrib, NumName.UUID.value, NumName.UUID.value, str(uuid.uuid1()))
            for lvl_2 in lvl_1.iter(NumName.INIT.value):
                self.update_string(lvl_2.attrib, NumName.REF.value, NumName.LINK_REF.value, name[4])

    def upd_reset_button(self, lvl, coorY):
        '''Изменение раздела, где name="type_reset_all_button_1".'''
        for lvl_1 in lvl.iter(NumName.OBJECT.value):
            if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, NumName.RESET_BUT.value):
                # Обновление UUID
                self.update_string(lvl_1.attrib, NumName.UUID.value, NumName.UUID.value, str(uuid.uuid1()))
                # Для таблицы GMPNA кнопку удаляем
                if self.table == 'GMPNA':
                    self.root.remove(lvl_1)
                    return
                for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                    self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.COOR_Y.value, coorY)
                for lvl_2 in lvl_1.iter(NumName.INIT.value):
                    self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.IsKTPRA.value, self.kit.isktpra)

    def change_template(self, click, name: dict):
        '''Редактирование шаблона формы.'''
        size_h, res_coorY = self.size(click)
        # Type
        for lvl in self.root.iter(NumName.TYPE_ROOT.value):
            self.upd_settings_form(lvl, name, size_h)
            # name="ApSource"
            self.upd_apsource(lvl, name)
            # name="empty_link"
            self.upd_empty_link(lvl, name)
            # base-type=Window
            self.upd_basetype_win(lvl, name)
            # name="type_reset_all_button_1"
            self.upd_reset_button(lvl, res_coorY)


class TopRow(BaseFunction):
    '''Собираем на форме защиты по страницам.'''
    def __init__(self, max_page, root, kit, request, table, num_iter, click):
        self.max_page = max_page
        self.root = root
        self.kit = kit
        self.request = request
        self.table = table
        self.num_iter = num_iter
        self.click = click

    def req_table(self, page):
        '''Запрос к таблице с данными по каждой странице с защитами.'''
        req = f"{self.kit.req_2}".format(self.num_iter, page)

        if self.choice_table(self.table):
            req = f"{self.kit.req_2}".format(page)

        data = self.request.where_select(str(self.table).lower(),
                                         self.kit.req_1, req,
                                         self.kit.order)
        return data

    def choice_list(self):
        '''От таблицы завист набор атрибутов.'''
        if self.choice_table(self.table):
            attr_list = self.kit.attr_row_ktpr
        elif self.table == 'KTPRA':
            attr_list = self.kit.attr_row_ktpra
        else:
            attr_list = self.kit.attr_row_gmpna
        return attr_list

    def choice_value(self, key, id_, num, name, not_mask):
        '''Подставляем значения при определенных условиях.'''
        bit_def = int(id_) % 4
        num_bit_defence = '4' if bit_def == 0 else str(bit_def)
        num_registry = math.ceil(int(id_) / 4)

        if key == 1:
            value = f'Group_{num_registry}'
        elif key == 2:
            value = str(num_bit_defence)
        elif key == 3:
            value = str(name)
        elif key == 4:
            value = str(num)
        elif key == 5:
            value = str(id_)
        elif key == 6:
            value = 'true' if not_mask else 'false'
        elif key == 7:
            value = str(self.num_iter)
        else:
            value = 'true'
        return value

    def filling_page(self, lvl):
        '''Добавляются на форму страницы.'''
        for page in range(1, self.max_page + 1):
            object = self.new_row_obj(lvl,
                                      f'{self.kit.attrib_top}_{page}',
                                      self.kit.attrib_top,
                                      self.kit.bt_id_top)

            visible = 'true' if page == 1 else 'false'
            for key, value in self.kit.attr_top.items():
                if key == 2:
                    atr_val = value[1] if self.click else '1'
                elif key == 4:
                    atr_val = self.kit.width_row_top
                elif key == 6:
                    atr_val = visible
                else:
                    atr_val = value[1]

                self.new_row_designed(object,
                                      NumName.DESIGNED.value,
                                      value[0], atr_val)
            # В страницы добавляются защиты
            self.filling_string_page(lvl, page)

    def filling_string_page(self, lvl, page):
        '''В страницы добавляются защиты.'''
        for lvl_1 in lvl.iter(NumName.OBJECT.value):

            if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, f'{self.kit.attrib_top}_{page}'):

                data = self.req_table(page)
                for i in range(0, len(data)):
                    id_num = data[i][0]
                    name = data[i][1]
                    not_mask = data[i][2]

                    object = self.new_row_obj(lvl_1,
                                              f'{self.kit.attrib_row}_{i + 1}',
                                              self.kit.attrib_row,
                                              self.kit.bt_id_row)

                    coordY = str(self.kit.height[0] * (i + 1))
                    for key, value in self.kit.attr_row_design.items():
                        if key == 2:
                            atr_val = coordY
                        elif key == 4:
                            atr_val = self.kit.width_row_top
                        else:
                            atr_val = value[1]

                        self.new_row_designed(object,
                                              NumName.DESIGNED.value,
                                              value[0], atr_val)

                    if self.choice_table(self.table):
                        ref = self.kit.apsoure_name
                    else:
                        ref = f'{self.kit.apsoure_name}{self.num_iter}'
                    self.new_row_init(object,
                                      NumName.INIT.value,
                                      self.kit.target_row,
                                      ref)

                    attr_used = self.choice_list()
                    for key, value in attr_used.items():
                        self.new_row_designed(object,
                                              NumName.INIT.value,
                                              value[0],
                                              self.choice_value(key, id_num,
                                                                (i + 1), name,
                                                                not_mask))

    def form_assembly(self):
        '''Собираем защиты или готовности для добавления на форму.'''
        # Добавляется страница защиты
        for lvl in self.root.iter(NumName.TYPE_ROOT.value):
            self.filling_page(lvl)


class Button(BaseFunction):
    '''Собираем и добавляем на форму кнопки переключения страниц.'''
    def __init__(self, max_page, root, kit, request, table, num_iter):
        self.max_page = max_page
        self.root = root
        self.kit = kit
        self.request = request
        self.table = table
        self.num_iter = num_iter

    def choice_visible(self, key, page):
        '''Подставляем значения для видимости страниц.'''
        if key == 1:
            value = f'{self.kit.attrib_top}_{page}'
        elif key == 2:
            if self.table == 'KTPR' or self.table == 'KTPRP':
                value = f'{self.kit.apsoure_name}'
            else:
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
                                      f'{self.kit.attrib_click}_{page}',
                                      self.kit.attrib_click,
                                      self.kit.bt_id_click)

            coordX = 1 + (OFFSET_CLICK * (page - 1))
            for key, value in self.kit.attr_button_design.items():
                self.new_row_designed(object,
                                      NumName.DESIGNED.value,
                                      value[0],
                                      str(coordX) if key == 1 else value[1])

            self.new_row_designed(object,
                                  NumName.INIT.value,
                                  'page_number', str(page))

            for key, value in self.kit.attr_button_init.items():
                self.new_row_init(object,
                                  NumName.INIT.value,
                                  value[0],
                                  self.choice_visible(key, page))

            data = self.req_table(page)
            for i in range(1, len(data) + 1):
                self.new_row_designed(object,
                                      NumName.INIT.value,
                                      f'def{i}_path',
                                      self.def_path(data[i - 1][0]))

    def form_assembly(self):
        '''Заполнение кнопкой.'''
        for lvl in self.root.iter(NumName.TYPE_ROOT.value):
            self.filling_button(lvl)


class DefenceMap(BaseFunction):
    '''Запуск генератора карты защит.'''
    def __init__(self, logtext):
        self.logsTextEdit = logtext
        self.dop_function = General_functions()

    def check_template(self, name: str, number: int) -> str:
        '''Проверка шаблона и создание на его основе новой формы.'''
        title = name if self.choice_table(self.table) else f'{name}{number}'
        new_picture = f'{connect.path_hmi}\\{title}.omobj'

        if os.path.isfile(new_picture):
            os.remove(new_picture)
        shutil.copy2(f'{connect.path_hmi_sample}\\Form_Defences_default.omobj',
                     new_picture)
        return new_picture

    def select_kit(self):
        '''Выбор конструктора для заполнения.'''
        if self.table == 'KTPR':
            return KTPR
        elif self.table == 'KTPRP':
            return KTPRP
        elif self.table == 'KTPRA':
            return KTPRA
        elif self.table == 'GMPNA':
            return GMPNA

    def max_condition(self, pump: int):
        '''Вычисляем из БД максимальное кол-во страниц и защит.'''
        if self.choice_table(self.table):
            max_page = self.request.max_value_column(self.table,
                                                     self.kit.COLUMN_LIST)
            max_prot = self.request.max_value_column(self.table,
                                                     self.kit.COLUMN_PROT)
        else:
            max_page = self.request.max_value_column_cond(self.table,
                                                          self.kit.COLUMN_LIST,
                                                          self.kit.COLUMN_PUMP,
                                                          pump)
            max_prot = self.request.max_value_column_cond(self.table,
                                                          self.kit.COLUMN_PROT,
                                                          self.kit.COLUMN_PUMP,
                                                          pump)
        return max_page, max_prot

    def size_for(self, pump):
        '''Max число агрегатов = числу форм для KTPRA и GMPNA. Default to 1
        Если есть number_pump, то цикл работает только по number_pump'''
        start_index = CONST_INDEX_FOR
        end_index = CONST_INDEX_FOR
        if not self.choice_table(self.table):
            end_index = self.request.max_value_column(self.table,
                                                      self.kit.COLUMN_PUMP)
            if pump is not None:
                start_index = pump
                end_index = pump
        return start_index, end_index

    def fill_pic_new(self, table: str, number_pump: int = None):
        """Заполнение новой формы.
        Args:
            list_table (dict): Список таблиц для формирования форм.
            number_pump (int, optional): Номер агрегата, если необходимо.
            Defaults to None.
        """
        try:
            self.table = table
            self.request = RequestSQL()
            # Выделяем конструктор под конкретную таблицу
            self.kit = self.select_kit()

            # Определяем цикл
            start_index, end_index = self.size_for(number_pump)

            # Цикл по каждой форме
            for num_iter in range(start_index, end_index + 1):
                print_tab = self.table if self.choice_table(self.table) else f'{self.table}_{num_iter}'

                # Max кол-во страниц, защит и кнопка переключения на форме
                max_page, max_prot = self.max_condition(num_iter)

                if max_page is None or max_prot is None:
                    self.logsTextEdit.logs_msg(f'''HMI. {print_tab}.
                                               Не определено количество
                                               страниц переключений
                                               или защит''', 2)
                    continue
                self.click = True if max_page > 1 else False

                # На основе шаблона -> новая форма
                new_form = self.check_template(self.kit.map_name, num_iter)
                # Чтение шаблона
                root, tree = self.dop_function.xmlParser(new_form)
                # Изменение шаблона
                template = Template(self.request, self.kit,
                                    max_prot, root, self.table)

                update_data = template.select_name(num_iter, self.choice_table(self.table))
                template.change_template(self.click, update_data)

                # Сборка защит
                defenc_read = TopRow(max_page, root, self.kit, self.request,
                                     self.table, num_iter, self.click)
                defenc_read.form_assembly()
                # Сборка кнопок
                if self.click:
                    button = Button(max_page, root, self.kit,
                                    self.request, self.table, num_iter)
                    button.form_assembly()

                tree.write(new_form, pretty_print=True, encoding='utf-8')
            self.logsTextEdit.logs_msg(f'''HMI. {self.table}.
                                       Picture заполнена''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''HMI. {self.table}. Ошибка:
                                       {traceback.format_exc()}''', 2)