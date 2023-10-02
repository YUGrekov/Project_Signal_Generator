import uuid
import shutil
import os
from models import HardWare
from models import connect
from main_base import General_functions
from lxml.etree import CDATA
from lxml import etree
from enum import Enum
from typing import NamedTuple


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


class NumName(Enum):
    '''Перечисление статических названий.'''
    TYPE_ROOT = 'type'
    PRIVATE = 'private'
    OBJECT = 'object'
    DESIGNED = 'designed'
    INIT = 'init'
    NAME_ATR = 'name'
    D_NAME = 'display-name'
    T_NAME = 'type_name'
    TITLE_NAME = 'title_name'
    VALUE_ATR = 'value'
    UUID = 'uuid'
    DO_ON = 'do-on'
    BODY = 'body'
    WIDTH = 'width'
    T_WIDTH = 't_width'
    HEIGHT = 'height'
    W_WIDTH = 'windowwidth'
    W_HEIGHT = 'windowheight'
    SS_X = 'ss_X'
    RENAME_LINK = 'rename_link'
    LINK_OUT_Y = 'link_out_Y'
    IN_PATH = 'in_path'
    OUT_PATH = 'out_path'
    COOR_Y = (88, 177)


class PT(Enum):
    '''Перечисление статических названий
    и значений по ПТ'''
    WIDTH = '1670'
    HEIGHT = '780'
    W_WIDTH = '1670'
    W_HEIGHT = '780'
    TITLE_WIDTH = '1650'
    SS_X = '950'


class MNS(Enum):
    '''Перечисление статических названий
    и значений по МНС'''
    WIDTH = '1420'
    HEIGHT = '820'
    W_WIDTH = '1420'
    W_HEIGHT = '820'
    TITLE_WIDTH = '1410'
    SS_X = '780'


class DesignedParamsThree(NamedTuple):
    target: str
    value: str
    ver: str


class DesignedParamsTwo(NamedTuple):
    target: str
    ver: str


class DesignedParamsOne(NamedTuple):
    target: str
    ver: str
    ref: str


class USOParams(NamedTuple):
    name_modul: str
    type_modul: str
    uuid_modul: str


class BaseUSO():
    '''Базовый класс шкафа УСО.'''
    params_module = {'MK-516-008A': USOParams(name_modul='AIs',
                                              type_modul='type_MK_516_008(AI8)',
                                              uuid_modul='454fa324-27ee-4c5b-852b-10e43769c2fa'),
                     'MK-514-008': USOParams(name_modul='AOs',
                                             type_modul='type_MK_514_008(AO)',
                                             uuid_modul='e76165af-10c9-4743-b092-8f5dcb3e6e12'),
                     'MK-521-032': USOParams(name_modul='DIs',
                                             type_modul='type_MK_521_032(DI)',
                                             uuid_modul='54337da0-d138-41b0-aefe-20366697201e'),
                     'MK-531-032': USOParams(name_modul='DOs',
                                             type_modul='type_MK_531_032(DO)',
                                             uuid_modul='20cd1522-2d06-49e6-a55d-e0801aeeb4e9'),
                     'MK-545-010': USOParams(name_modul='CNs',
                                             type_modul='type_MK_545_010(CN)',
                                             uuid_modul='c70fe2c3-a605-4c9d-b471-23e410350ddf'),
                     'MK-550-024': USOParams(name_modul='PSUs',
                                             type_modul='type_MK_550_024(PSU)',
                                             uuid_modul='6d539303-1528-4442-bc2e-1f08a49f1567'),
                     'MK-541-002': USOParams(name_modul='RSs',
                                             type_modul='type_MK_541_002(RS)',
                                             uuid_modul='dc2b3d53-089e-4f3f-9ecd-4098cdfa823c')}

    attr_ss = {'1': DesignedParamsThree(target='X', value='5', ver='5'),
               '2': DesignedParamsThree(target='Y', value='5', ver='34'),
               '3': DesignedParamsThree(target='Rotation', value='5', ver='0'),
               '4': DesignedParamsThree(target='Height', value='5', ver='23')}

    attrib_basket = {'1': DesignedParamsThree(target='X', value='70', ver='5'),
                     '2': DesignedParamsThree(target='Y', value='', ver='5'),
                     '3': DesignedParamsThree(target='ZValue', value='0', ver='5'),
                     '4': DesignedParamsThree(target='Rotation', value='0', ver='5'),
                     '5': DesignedParamsThree(target='Scale', value='1', ver='5'),
                     '6': DesignedParamsThree(target='Visible', value='true', ver='5'),
                     '7': DesignedParamsThree(target='Opacity', value='1', ver='5'),
                     '8': DesignedParamsThree(target='Enabled', value='true', ver='5'),
                     '9': DesignedParamsThree(target='Tooltip', value='', ver='5'),
                     '10': DesignedParamsThree(target='Width', value='730', ver='5'),
                     '11': DesignedParamsThree(target='Height', value='160', ver='5'),
                     '12': DesignedParamsThree(target='RoundingRadius', value='0', ver='5'),
                     '13': DesignedParamsThree(target='PenColor', value='4278190080', ver='5'),
                     '14': DesignedParamsThree(target='PenStyle', value='0', ver='5'),
                     '15': DesignedParamsThree(target='PenWidth', value='1', ver='5'),
                     '16': DesignedParamsThree(target='BrushColor', value='4278190080', ver='5'),
                     '17': DesignedParamsThree(target='BrushStyle', value='0', ver='5')}

    attrib_modul = {'1': DesignedParamsThree(target='X', value='', ver='5'),
                    '2': DesignedParamsThree(target='Y', value='0', ver='5'),
                    '3': DesignedParamsThree(target='Rotation', value='0', ver='5'),
                    '4': DesignedParamsThree(target='Width', value='40', ver='5'),
                    '5': DesignedParamsThree(target='Height', value='160', ver='5')}

    attrib_AIs_AOs = {'1': DesignedParamsThree(target='RightPopUp', value='true', ver='5'),
                      '2': DesignedParamsThree(target='DownPopUp_faceplate', value='', ver='5'),
                      '3': DesignedParamsThree(target='UpPopUp_faceplate', value='', ver='5'),
                      '4': DesignedParamsThree(target='_init_path', value='', ver='5')}

    attrib_DIs_DOs = {'1': DesignedParamsThree(target='RightPopUp', value='true', ver='5'),
                      '2': DesignedParamsThree(target='DownPopUp_faceplate', value='true', ver='5'),
                      '3': DesignedParamsThree(target='UpPopUp_faceplate', value='', ver='5'),
                      '4': DesignedParamsThree(target='_init_path', value='', ver='5')}

    attrib_PSUs = {'1': DesignedParamsThree(target='RightPopUp', value='true', ver='5'),
                   '2': DesignedParamsThree(target='DownPopUp_faceplate', value='true', ver='5'),
                   '3': DesignedParamsThree(target='UpPopUp_faceplate', value='', ver='5'),
                   '4': DesignedParamsThree(target='_init_path', value='', ver='5')}

    attrib_RSs = {'1': DesignedParamsThree(target='RightPopUp', value='true', ver='5'),
                  '2': DesignedParamsThree(target= 'DownPopUp_faceplate', value='true', ver='5'),
                  '3': DesignedParamsThree(target='UpPopUp_faceplate', value='', ver='5'),
                  '4': DesignedParamsThree(target= '_init_path', value='', ver='5')}

    attrib_CNs = {'1': DesignedParamsThree(target='_init_path', value='', ver='5'),
                  '2': DesignedParamsThree(target='eth1_animation', value='true', ver='5'),
                  '3': DesignedParamsThree(target='eth2_animation', value='true', ver='5'),
                  '4': DesignedParamsThree(target='RightPopUp', value='true', ver='5'),
                  '5': DesignedParamsThree(target='port1_device', value='', ver='5'),
                  '6': DesignedParamsThree(target='port2_device', value='', ver='5'),
                  '7': DesignedParamsThree(target='DownPopUp_faceplate', value='true', ver='5'),
                  '8': DesignedParamsThree(target='UpPopUp_faceplate', value='', ver='5')}

    attrib_link_input_output = {'1': DesignedParamsThree(target='link_1_is_on', value='true', ver='5'),
                                '2': DesignedParamsThree(target='link_2_is_on', value='true', ver='5'),
                                '3': DesignedParamsThree(target='_init_path_link_1', value='', ver='5'),
                                '4': DesignedParamsThree(target='_init_path_link_2', value='', ver='5'),
                                '5': DesignedParamsThree(target='link_1_inv', value='true', ver='5'),
                                '6': DesignedParamsThree(target='link_2_inv', value='true', ver='5')}

    attrib_link_input_output_d = {'1': DesignedParamsThree(target='X', value='50', ver='5'),
                                  '2': DesignedParamsThree(target='Y', value='60', ver='5'),
                                  '3': DesignedParamsThree(target='Rotation', value='0', ver='5'),
                                  '4': DesignedParamsThree(target='Width', value='70.5', ver='5'),
                                  '5': DesignedParamsThree(target='Height', value='120', ver='5')}

    attrib_point = {'1': DesignedParamsThree(target='X', value='0', ver='5'),
                    '2': DesignedParamsThree(target='Y', value='0', ver='5')}


class AIss(Enum):
    NAME_SS = 'type_analog_srv'
    B_T_ID = 'c5d10192-c8ea-4db8-a5ab-15b09b9b2266'
    SIGN = 'Analogs'


class DIss(Enum):
    NAME_SS = 'type_srv_signal'
    B_T_ID = '72176618-ccac-488c-b1d6-d570e5505e1c'
    SIGN = 'Diskrets'


class ParserFile():
    '''Парсер файла картинки'''
    def __init__(self, new_pic_path: str) -> None:
        parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
        self.tree = etree.parse(new_pic_path, parser)
        self.root = self.tree.getroot()

    def __call__(self):
        return self.root, self.tree

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

    def update_string(self, object: dict, key: str, value: str, new_value: str):
        '''Поиск и обновление строки'''
        try:
            if object[key] == value:
                object[key] = str(new_value)
        except Exception:
            return

    def search_string(self, object: dict, key: str, value: str):
        '''Поиск строки'''
        if object[key] == value:
            return True
        else:
            return False

    def edit_template(self, system: MNS | PT, root, uso_eng: str, uso_rus: str):
        '''Редактирование новой формы под общие для
        всех форм детали и конкретную систему.'''

        for lvl in root.iter(NumName.TYPE_ROOT.value):
            self.update_string(lvl.attrib, NumName.NAME_ATR.value, NumName.T_NAME.value, f'D_{connect.type_system}_{uso_eng}')
            self.update_string(lvl.attrib, NumName.D_NAME.value, NumName.T_NAME.value, f'D_{connect.type_system}_{uso_eng}')
            self.update_string(lvl.attrib, NumName.UUID.value, NumName.UUID.value, str(uuid.uuid1()))

            for lvl_1 in lvl.iter(NumName.DESIGNED.value):
                self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.WIDTH.value, system.WIDTH.value)
                self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.HEIGHT.value, system.HEIGHT.value)
                self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.W_WIDTH.value, system.W_WIDTH.value)
                self.update_string(lvl_1.attrib, NumName.VALUE_ATR.value, NumName.W_HEIGHT.value, system.W_HEIGHT.value)

            for lvl_1 in lvl.iter(NumName.OBJECT.value):
                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 't_uso_title'):

                    for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                        self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.T_WIDTH.value, system.TITLE_WIDTH.value)
                        self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.TITLE_NAME.value, uso_rus)

                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 'r_ss'):
                    for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                        self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.SS_X.value, system.SS_X.value)

                self.update_string(lvl_1.attrib, NumName.NAME_ATR.value, NumName.RENAME_LINK.value, f'_link_D_{connect.type_system}_{uso_eng}_for_enable')
                self.update_string(lvl_1.attrib, NumName.D_NAME.value, NumName.RENAME_LINK.value, f'_link_D_{connect.type_system}_{uso_eng}_for_enable')

            for lvl_1 in lvl.iter(NumName.DO_ON.value):
                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 'Handler_1'):
                    for lvl_2 in lvl_1.iter(NumName.BODY.value):
                        lvl_2.text = CDATA(f'_link_D_{connect.type_system}_{uso_eng}_for_enable.Enabled=false;')

                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 'Handler_2'):
                    for lvl_2 in lvl_1.iter(NumName.BODY.value):
                        lvl_2.text = CDATA(f'_link_D_{connect.type_system}_{uso_eng}_for_enable.Enabled=true;')

    def input_output_name(self, root, max_basket: int,
                          fl_CPU: bool, uso_eng: str, basket: int):
        '''Корректировка названий на входе и выходе корзин'''

        def sign_path(fl_CPU: bool, uso_eng, basket):
            if fl_CPU:
                return f'Diag.MNs.{uso_eng}_A{basket}_01'
            else:
                return f'Diag.CNs.{uso_eng}_A{basket}_01'

        for lvl in root.iter(NumName.TYPE_ROOT.value):

            for lvl_1 in lvl.iter(NumName.OBJECT.value):
                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 't_input_link'):

                    for lvl_2 in lvl_1.iter(NumName.INIT.value):
                        self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.IN_PATH.value,
                                           sign_path(fl_CPU, uso_eng, basket))

                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 't_output_link'):

                    for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                        self.update_string(lvl_2.attrib,
                                           NumName.VALUE_ATR.value,
                                           NumName.LINK_OUT_Y.value,
                                           NumName.COOR_Y.value[0] + (NumName.COOR_Y.value[1] * max_basket))
                    for lvl_2 in lvl_1.iter(NumName.INIT.value):
                        self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.OUT_PATH.value, sign_path)

    def service_signals(self, root, attr_ss, signals):
        '''Добавляем служебные сигналы.'''
        for lvl in root.iter(NumName.TYPE_ROOT.value):

            for lvl_1 in lvl.iter(NumName.OBJECT.value):
                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 'r_ss'):

                    for type_ss in (DIss, AIss):
                        data = signals[0] if type_ss is DIss else signals[1]

                        for i in range(1, len(data)):
                            object = self.new_rows_obj(NewRowsParams(
                                object=NumName.OBJECT.value,
                                access_modifier=NumName.PRIVATE.value,
                                name=f'{type_ss.NAME_SS.value}_{i}',
                                display_name=f'{type_ss.NAME_SS.value}_{i}',
                                uuid=str(uuid.uuid1()),
                                base_type=type_ss.NAME_SS.value,
                                base_type_id=type_ss.B_T_ID.value,
                                ver='5'))
                            lvl_1.append(object)

                            for key, value in attr_ss.items():
                                self.dop_substr(object, (DesignedParamsAttr(
                                    designed=NumName.DESIGNED.value,
                                    target=value[0],
                                    value=value[2],
                                    ver=value[1])))

                            self.dop_substr(object, (DesignedParamsAttr(
                                designed=NumName.INIT.value,
                                target='_init_path',
                                value='word',
                                ver='5')))

                            self.dop_init_substr(object, (InitParamsAttr(
                                init=NumName.INIT.value,
                                target='_init_path',
                                ver='5',
                                ref='unit.Global.global_ApSource')))


class DaignoPicture(BaseUSO):
    def __init__(self):
        self.dop_function = General_functions()

    def cabinet_names(self) -> dict:
        """Получаем название неповторяющихся шкафов.

        Returns:
            dict: Название шкафа на ENG and RUS
        """
        data_value = self.dop_function.connect_by_sql('uso', '''"tag", "name"''')
        return dict(data_value)

    def check_template(self, name_uso: str) -> str:
        '''Проверка шаблона и создание на его основе нового шкафа.'''
        new_picture = f'{connect.path_hmi}\\D_{connect.type_system}_{name_uso}.omobj'

        if os.path.isfile(new_picture):
            os.remove(new_picture)
        shutil.copy2(f'{connect.path_hmi_sample}\\D_USO_Template.omobj',
                     new_picture)

        return new_picture

    def request_ss(self, uso_rus: str):
        """Получаем служебные сигналы."""
        data_value = self.dop_function.connect_by_sql_condition('uso', '*', f'''"name"='{uso_rus}' ''')

        data_AI = self.dop_function.connect_by_sql_condition('ai', "tag_eng", f'''"variable"='{data_value[0][4]}' ''')
        data_DI = []
        for i in range(5, 37):
            value = self.dop_function.connect_by_sql_condition('di', "tag_eng", f'''"variable"='{data_value[0][i]}' ''')
            if len(value) == 0:
                continue
            data_DI.append(value[0][0])
        return data_DI, data_AI

    def filling_pic_uso(self):
        system = MNS if connect.type_system == 'MNS' else PT
        name_uso = self.cabinet_names()
        for eng, rus in name_uso.items():

            path_picture = self.check_template(eng)

            parser = ParserFile(path_picture)
            root, tree = parser()

            parser.edit_template(system, root, eng, rus)

            parser.service_signals(root, self.attr_ss, self.request_ss(rus))

            # parser.input_output_name(root, 3)
            tree.write(path_picture, pretty_print=True, encoding='utf-8')






            # for column in HardWare.select().dicts():
            #     uso = column['uso']

                # if name_uso == uso:
                #     id_basket = column['id']
                #     tag = column['tag']
                #     basket = column['basket']
                #     print(uso)

                #     for modul_column in range(0, 33, 1):
                #         if column[f'type_{modul_column}'] != '' and column[f'type_{modul_column}'] is not None:
                #             print(column[f'type_{modul_column}'])


a = DaignoPicture()
a.filling_pic_uso()