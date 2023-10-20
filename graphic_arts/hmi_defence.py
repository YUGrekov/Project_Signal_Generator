import uuid
import shutil
import os
import sys
import traceback
from enum import Enum
from datetime import datetime
from typing import Any
from lxml import etree
from general_functions import General_functions
from enum import Enum
from typing import NamedTuple
from request_sql import RequestSQL
sys.path.append('../Project_Signal_Generator')
from model_new import connect

CONST_INDEX_FOR = 1
OFFSET_RESET = 13


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

    # T_WIDTH = 't_width'
    # SS_X = 'ss_X'
    # RENAME_LINK = 'rename_link'
    # LINK_OUT_Y = 'link_out_Y'
    # IN_PATH = 'in_path'
    # OUT_PATH = 'out_path'
    # VAL_ATTR_1 = '_init_path'
    # VAL_ATTR_2 = '_link_init_ApSource'
    # VAL_ATTR_3 = 'unit.Global.global_ApSource'
    # VAL_ATTR_4 = '5'
    # COOR_Y = (88, 177)
    # SS_COOR_Y = (5, 27)
    # B_COOR_Y = (-110, 180)
    # M_COOR_X = 40


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

    attr_top = {1: DesignedParams(target='X', value='1'),
                2: DesignedParams(target='Y', value='39'),
                3: DesignedParams(target='Rotation', value='0'),
                4: DesignedParams(target='Width', value='800'),
                5: DesignedParams(target='Height', value='26'),
                6: DesignedParams(target='Visible', value='')}

    attr_row_design = {1: DesignedParams(target='X', value='0'),
                       2: DesignedParams(target='Y', value=''),
                       3: DesignedParams(target='Rotation', value='0'),
                       4: DesignedParams(target='Width', value='800'),
                       5: DesignedParams(target='Height', value='25')}

    attr_row_init = {1: DesignedParams(target='_init_group_number', value=''),
                     2: DesignedParams(target='_init_row_number', value=''),
                     3: DesignedParams(target='_def_name', value=''),
                     4: DesignedParams(target='_def_number', value=''),
                     5: DesignedParams(target='_def_number_inarray', value=''),
                     6: DesignedParams(target='IsKTPRA', value=''),
                     7: DesignedParams(target='NotMasked', value='')}


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
    target_row = '_link_init_ApSource_type_defence_row'
    width = '1102'
    height = (26, 55)
    isktpra = 'false'


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
    target_row = '_link_init_ApSource_type_defence_row'
    width = '1102'
    height = (26, 55)
    isktpra = 'false'


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
    target_row = '_link_init_ApSource_type_defence_row'
    width = '1102'
    height = (26, 55)
    isktpra = 'true'


class GMPNA(BaseDefenceMap):
    caption_name = 'Карта агрегатных готовностей'
    map_name = 'Form_Readiness_MA'
    apsoure_name = 'ApSource_form_GMPNAs_MA'
    path_server = 'GMPNAs.GMPNAs'
    link_ref = 'unit.WorkspaceControl.Readiness_Control_NA'
    attrib_top = 'type_defence_top'
    attrib_row = 'type_defence_row'
    attrib_click = 'type_readiness_button'
    bt_id_top = 'b08a935f-b03d-42e0-96c4-dc639b70d499'
    bt_id_row = '48231209-9a9f-42cf-9b38-ef1ef5cc7403'
    target_row = '_link_init_ApSource_type_readiness_row'
    width = '857'
    height = (26, 55, 2)
    isktpra = 'false'


class Template():
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

    def search_string(self, object: dict, key: str, value: str):
        '''Поиск строки'''
        return True if object[key] == value else False

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
            for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.PATH_SERVER.value, name[3])

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
                # Для таблицы GMPNA кнопку удаляем
                if self.table == 'gmpna':
                    self.root.remove(lvl_1)
                    return
                for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                    self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.COOR_Y.value, coorY)
                for lvl_2 in lvl_1.iter(NumName.INIT.value):
                    self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.IsKTPRA.value, self.kit.isktpra)

    def change_template(self: int, click, name: dict):
        '''Редактирование шаблона формы.'''
        size_h, res_coorY = self.size(click)
        # Type
        for lvl in self.root.iter(NumName.TYPE_ROOT.value):
            self.upd_settings_form(lvl, name, size_h)
            # name="ApSource"
            self.upd_apsource(lvl, name)
            # base-type=Window
            self.upd_basetype_win(lvl, name)
            # name="type_reset_all_button_1"
            self.upd_reset_button(lvl, res_coorY)


class TopRow():
    '''Собираем на форме защиты по страницам.'''
    def __init__(self, max_page, max_prot, root, kit):
        self.max_page = max_page
        self.max_prot = max_prot
        self.root = root
        self.kit = kit

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

    def new_row_obj(self, level, name, kit):
        '''Подготавливаем к созданию новых строк.'''
        object = self.new_rows_obj(NewRowsParams(
            object=NumName.OBJECT.value,
            access_modifier=NumName.PRIVATE.value,
            name=name,
            display_name=name,
            uuid=str(uuid.uuid1()),
            base_type=kit.attrib_top,
            base_type_id=kit.bt_id_top,
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
            ref=ref,)))

    def search_string(self, object: dict, key: str, value: str):
        '''Поиск строки'''
        return True if object[key] == value else False

    def filling_page(self, lvl):
        '''Добавляются на форму страницы.'''
        for page in range(1, self.max_page + 1):
            object = self.new_row_obj(lvl,
                                        f'{self.kit.attrib_top}_{page}',
                                        self.kit)

            visible = 'true' if page == 1 else 'false'
            for key, value in self.kit.attr_top.items():
                self.new_row_designed(object,
                                      NumName.DESIGNED.value,
                                      value[0],
                                      visible if key == 6 else value[1])
            # В страницы добавляются защиты
            self.filling_string_page(lvl, page)

    def filling_string_page(self, lvl, page):
        '''В страницы добавляются защиты.'''
        for lvl_1 in lvl.iter(NumName.OBJECT.value):

            if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, f'{self.kit.attrib_top}_{page}'):

                for i in range(1, 3):
                    object = self.new_row_obj(lvl_1,
                                              f'{self.kit.attrib_row}_{i}',
                                              self.kit)

                    for key, value in self.kit.attr_row_design.items():
                        self.new_row_designed(object,
                                              NumName.DESIGNED.value,
                                              value[0],
                                              value[1])

                    for key, value in self.kit.attr_row_init.items():
                        self.new_row_designed(object,
                                              NumName.INIT.value,
                                              value[0],
                                              value[1])

                    self.new_row_init(object,
                                      NumName.INIT.value,
                                      self.kit.target_row,
                                      self.kit.apsoure_name)

    def form_assembly(self):
        '''Собираем защиты или готовности для добавления на форму.'''
        # Добавляется страница защиты
        for lvl in self.root.iter(NumName.TYPE_ROOT.value):
            self.filling_page(lvl)


class DefenceMap():
    '''Запуск генератора карты защит.'''
    def __init__(self):
        # self.logsTextEdit = logtext
        self.dop_function = General_functions()

    def choise_table(self, table: str) -> bool:
        '''Проверяем принадлежность к таблице KTPR, KTPRP'''
        return True if table in ['KTPR', 'KTPRP'] else False

    def check_template(self, name: str, number: int) -> str:
        '''Проверка шаблона и создание на его основе новой формы.'''
        title = name if self.choise_table(self.table) else f'{name}{number}'
        new_picture = f'{connect.path_hmi}\\{title}.omobj'

        if os.path.isfile(new_picture):
            os.remove(new_picture)
        shutil.copy2(f'{connect.path_hmi_sample}\\Form_Defences_default_new.omobj',
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
        if self.choise_table(self.table):
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
        self.click = True if max_page > 1 else False
        return max_page, max_prot

    def size_for(self, pump):
        '''Max число агрегатов = числу форм для KTPRA и GMPNA. Default to 1
        Если есть number_pump, то цикл работает только по number_pump'''
        start_index = CONST_INDEX_FOR
        end_index = CONST_INDEX_FOR
        if not self.choise_table(self.table):
            end_index = self.request.max_value_column(self.table,
                                                      self.kit.COLUMN_PUMP)
            if pump is not None:
                start_index = pump
                end_index = pump
        return start_index, end_index

    def fill_pic_new(self, list_table: dict,
                     number_pump: int = None):
        """Заполнение новой формы.
        Args:
            list_table (dict): Список таблиц для формирования форм.
            number_pump (int, optional): Номер агрегата, если необходимо.
            Defaults to None.
        """
        try:
            self.request = RequestSQL()
            for self.table in list_table:
                # Выделяем конструктор под конкретную таблицу
                self.kit = self.select_kit()

                # Определяем цикл
                start_index, end_index = self.size_for(number_pump)

                # Цикл по каждой форме
                for page in range(start_index, end_index + 1):
                    new_form = self.check_template(self.kit.map_name, page)

                    # Max кол-во страниц, защит и кнопка переключения на форме
                    max_page, max_prot = self.max_condition(page)

                    if max_page is None or max_prot is None:
                        print(f'''HMI. {self.table}. Не определено количество страниц переключений или защит''')
                        # self.logsTextEdit.logs_msg(f'''HMI. {self.table}.
                        #                            Не определено количество
                        #                            страниц переключений
                        #                            или защит''', 2)
                        continue
                    # Чтение шаблона
                    root, tree = self.dop_function.xmlParser(new_form)
                    # Изменение шаблона
                    template = Template(self.request, self.kit,
                                        max_prot, root, self.table)

                    update_data = template.select_name(page, self.choise_table(self.table))
                    template.change_template(self.click, update_data)

                    # Сборка защит
                    defenc_read = TopRow(max_page, max_prot, root, self.kit)
                    defenc_read.form_assembly()

                    tree.write(new_form, pretty_print=True, encoding='utf-8')

        except Exception:
            print(traceback.format_exc())


a = DefenceMap()
a.fill_pic_new(['KTPR'])
