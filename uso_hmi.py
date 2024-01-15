import uuid
import shutil
import os
import traceback
from datetime import datetime
from models import HardWare
from models import connect
from main_base import General_functions
from lxml.etree import CDATA
from lxml import etree
from enum import Enum
from typing import NamedTuple
today = datetime.now()


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


class DesignedParamsThree(NamedTuple):
    target: str
    value: str


class AIs(Enum):
    NAME = 'AIs'
    TYPE = 'type_MK_516_008(AI8)'
    B_T = 'type_MK_516_008(AI8)'
    B_T_ID = '454fa324-27ee-4c5b-852b-10e43769c2fa'


class AOs(Enum):
    NAME = 'AOs'
    TYPE = 'type_MK_514_008(AO)'
    B_T = 'type_MK_514_008(AO)'
    B_T_ID = 'e76165af-10c9-4743-b092-8f5dcb3e6e12'


class DIs(Enum):
    NAME = 'DIs'
    TYPE = 'type_MK_521_032(DI)'
    B_T = 'type_MK_521_032(DI)'
    B_T_ID = '54337da0-d138-41b0-aefe-20366697201e'


class DOs(Enum):
    NAME = 'DOs'
    TYPE = 'type_MK_531_032(DO)'
    B_T = 'type_MK_531_032(DO)'
    B_T_ID = '20cd1522-2d06-49e6-a55d-e0801aeeb4e9'


class CNs(Enum):
    NAME = 'CNs'
    TYPE = 'type_MK_545_010(CN)'
    B_T = 'type_MK_545_010(CN)'
    B_T_ID = 'c70fe2c3-a605-4c9d-b471-23e410350ddf'


class PSUs(Enum):
    NAME = 'PSUs'
    TYPE = 'type_MK_550_024(PSU)'
    B_T = 'type_MK_550_024(PSU)'
    B_T_ID = '6d539303-1528-4442-bc2e-1f08a49f1567'


class RSs(Enum):
    NAME = 'RSs'
    TYPE = 'type_MK_541_002(RS)'
    B_T = 'type_MK_541_002(RS)'
    B_T_ID = 'dc2b3d53-089e-4f3f-9ecd-4098cdfa823c'


class Emptys(Enum):
    NAME = 'Emptys'
    TYPE = 'type_MK_500_001(empty)'
    B_T = 'type_MK_500_001(empty)'
    B_T_ID = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'


class InputLine(Enum):
    NAME = 'l_input_to_A'
    TYPE = 'l_input_to_A'
    B_T = 'type_line_for_connect'
    B_T_ID = '9ce8edc0-9c10-4a3b-9263-da44abb267e1'
    COOR_X = 50
    COOR_Y = (60, 180)
    COOR_WIDTH = (70.5, 70.5, 70.5, 70.5)
    COOR_HEIGHT = (120, 103, 103, 103)


class OutputLine(Enum):
    NAME = 'l_output_to_A'
    TYPE = 'l_output_to_A'
    B_T = 'type_line_for_connect'
    B_T_ID = '9ce8edc0-9c10-4a3b-9263-da44abb267e1'
    COOR_X = 120.5
    COOR_Y = (207, 180)
    COOR_WIDTH = (70.5, 70.5, 70.5, 70.5)
    COOR_HEIGHT = (50, 50, 50, 50)


class InputPoint(Enum):
    NAME = 'Point_'
    TYPE = 'Point'
    B_T = 'Point'
    B_T_ID = '467f1af0-7bb4-4a61-b6fb-06e7bfd530d6'
    COOR_X = (0, 0, 70.5)
    COOR_Y = (0, 120, 120)


class OutputPoint(Enum):
    NAME = 'Point_'
    TYPE = 'Point'
    B_T = 'Point'
    B_T_ID = '467f1af0-7bb4-4a61-b6fb-06e7bfd530d6'
    COOR_X = (0, -70.5, -70.5)
    COOR_Y = (0, 0, 50)


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
    VAL_ATTR_1 = '_init_path'
    VAL_ATTR_2 = '_link_init_ApSource'
    VAL_ATTR_3 = 'unit.Global.global_ApSource'
    VAL_ATTR_4 = '5'
    COOR_Y = (88, 177)
    SS_COOR_Y = (5, 27)
    B_COOR_Y = (-110, 180)
    M_COOR_X = 40


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


class BaseUSO():
    '''Базовый класс для формирования шкафа УСО.
    Описания атрибутов и их значения'''
    params_module = {'MK-516-008A': AIs,
                     'MK-514-008': AOs,
                     'MK-521-032': DIs,
                     'MK-531-032': DOs,
                     'MK-545-010': CNs,
                     'MK-550-024': PSUs,
                     'MK-541-002': RSs,
                     'MK-500-001': Emptys}

    attr_ss = {'1': DesignedParamsThree(target='X', value='5'),
               '2': DesignedParamsThree(target='Y', value=''),
               '3': DesignedParamsThree(target='Rotation', value='0'),
               '4': DesignedParamsThree(target='Height', value='23')}

    attr_basket = {'1': DesignedParamsThree(target='X', value='70'),
                   '2': DesignedParamsThree(target='Y', value=''),
                   '3': DesignedParamsThree(target='ZValue', value='0'),
                   '4': DesignedParamsThree(target='Rotation', value='0'),
                   '5': DesignedParamsThree(target='Scale', value='1'),
                   '6': DesignedParamsThree(target='Visible', value='true'),
                   '7': DesignedParamsThree(target='Opacity', value='1'),
                   '8': DesignedParamsThree(target='Enabled', value='true'),
                   '9': DesignedParamsThree(target='Tooltip', value=''),
                   '10': DesignedParamsThree(target='Width', value='730'),
                   '11': DesignedParamsThree(target='Height', value='160'),
                   '12': DesignedParamsThree(target='RoundingRadius', value='0'),
                   '13': DesignedParamsThree(target='PenColor', value='4278190080'),
                   '14': DesignedParamsThree(target='PenStyle', value='0'),
                   '15': DesignedParamsThree(target='PenWidth', value='1'),
                   '16': DesignedParamsThree(target='BrushColor', value='4278190080'),
                   '17': DesignedParamsThree(target='BrushStyle', value='0')}

    attr_modul = {'1': DesignedParamsThree(target='X', value=''),
                  '2': DesignedParamsThree(target='Y', value='0'),
                  '3': DesignedParamsThree(target='Rotation', value='0'),
                  '4': DesignedParamsThree(target='Width', value='40'),
                  '5': DesignedParamsThree(target='Height', value='160')}

    attr_set_mod = {'1': DesignedParamsThree(target='RightPopUp', value='true'),
                    '2': DesignedParamsThree(target='UpPopUp_faceplate', value=''),
                    '3': DesignedParamsThree(target='DownPopUp_faceplate', value='')}

    attr_CNs = {'1': DesignedParamsThree(target='RightPopUp', value='true'),
                '2': DesignedParamsThree(target='UpPopUp_faceplate', value=''),
                '3': DesignedParamsThree(target='DownPopUp_faceplate', value=''),
                '4': DesignedParamsThree(target='eth1_animation', value='true'),
                '5': DesignedParamsThree(target='eth2_animation', value='true'),
                '6': DesignedParamsThree(target='port1_device', value=''),
                '7': DesignedParamsThree(target='port2_device', value='')}

    attr_init_in_out = {'1': DesignedParamsThree(target='link_1_is_on', value='true'),
                        '2': DesignedParamsThree(target='link_2_is_on', value='true'),
                        '3': DesignedParamsThree(target='link_1_inv', value='true'),
                        '4': DesignedParamsThree(target='link_2_inv', value='true'),
                        '5': DesignedParamsThree(target='_init_path_link_1', value=''),
                        '6': DesignedParamsThree(target='_init_path_link_2', value='')}

    attr_obj_in_out = {'1': DesignedParamsThree(target='X', value='50'),
                       '2': DesignedParamsThree(target='Y', value='60'),
                       '3': DesignedParamsThree(target='Width', value='70.5'),
                       '4': DesignedParamsThree(target='Height', value='120'),
                       '5': DesignedParamsThree(target='Rotation', value='0')}

    attr_point = {'1': DesignedParamsThree(target='X', value=''),
                  '2': DesignedParamsThree(target='Y', value='')}


class AIss(Enum):
    NAME_SS = 'type_analog_srv'
    B_T = 'type_analog_srv'
    B_T_ID = 'c5d10192-c8ea-4db8-a5ab-15b09b9b2266'
    SIGN = 'Analogs'


class DIss(Enum):
    NAME_SS = 'type_srv_signal'
    B_T = 'type_srv_signal'
    B_T_ID = '72176618-ccac-488c-b1d6-d570e5505e1c'
    SIGN = 'Diskrets'


class BASKET(Enum):
    NAME_SS = 'r_basket'
    B_T = 'Rectangle'
    B_T_ID = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'
    SIGN = ''


class ParserFile(BaseUSO):
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

    def new_row_obj(self, level, name: str, attr):
        object = self.new_rows_obj(NewRowsParams(
            object=NumName.OBJECT.value,
            access_modifier=NumName.PRIVATE.value,
            name=name,
            display_name=name,
            uuid=str(uuid.uuid1()),
            base_type=attr.B_T.value,
            base_type_id=attr.B_T_ID.value,
            ver=NumName.VAL_ATTR_4.value))
        level.append(object)
        return object

    def new_row_designed(self, object, designed, target, value):
        self.dop_substr(object, (DesignedParamsAttr(
            designed=designed,
            target=target,
            value=value,
            ver=NumName.VAL_ATTR_4.value)))

    def new_row_init(self, object, init, target, ref):
        self.dop_init_substr(object, (InitParamsAttr(
            init=init,
            target=target,
            ver=NumName.VAL_ATTR_4.value,
            ref=ref,)))

    def update_string(self, object: dict, key: str, value: str, new_value: str):
        '''Поиск и обновление строки'''
        try:
            if object[key] == value:
                object[key] = str(new_value)
        except Exception:
            return

    def search_string(self, object: dict, key: str, value: str):
        '''Поиск строки'''
        return True if object[key] == value else False

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

    def in_out_name(self, root, data_value: dict, fl_not_link: bool):
        '''Корректировка названий на входе и выходе корзин'''
        def sign_path(uso: str):
            if 'KC' in uso:
                return f'Diag.MNs.{uso}_01'
            else:
                return f'Diag.CNs.{uso}_01'

        def delete_in_out(root, lvl_1):
            '''Удаляем линию если необходимо'''
            root.remove(lvl_1)

        len_data = len(data_value)
        for lvl in root.iter(NumName.TYPE_ROOT.value):

            for lvl_1 in lvl.iter(NumName.OBJECT.value):

                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 't_input_link'):

                    if fl_not_link:
                        delete_in_out(root, lvl_1)
                        continue

                    for lvl_2 in lvl_1.iter(NumName.INIT.value):
                        self.update_string(lvl_2.attrib, NumName.VALUE_ATR.value, NumName.IN_PATH.value,
                                           sign_path(data_value[0]['net'][0][5].split(';')[0]))

                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 't_output_link'):

                    if fl_not_link:
                        delete_in_out(root, lvl_1)
                        return

                    for lvl_2 in lvl_1.iter(NumName.DESIGNED.value):
                        self.update_string(lvl_2.attrib,
                                           NumName.VALUE_ATR.value,
                                           NumName.LINK_OUT_Y.value,
                                           NumName.COOR_Y.value[0] + (NumName.COOR_Y.value[1] * len_data))
                    for lvl_2 in lvl_1.iter(NumName.INIT.value):
                        self.update_string(lvl_2.attrib,
                                           NumName.VALUE_ATR.value,
                                           NumName.OUT_PATH.value,
                                           sign_path(data_value[len_data - 1]['net'][len_data - 1][6].split(';')[0]))

    def service_signals(self, root, signals):
        '''Добавляем служебные сигналы.'''
        for lvl in root.iter(NumName.TYPE_ROOT.value):
            for lvl_1 in lvl.iter(NumName.OBJECT.value):
                if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, 'r_ss'):
                    counter = 1
                    for type_ss in (DIss, AIss):
                        data = signals[0] if type_ss is DIss else signals[1]

                        if data == 0:
                            continue

                        for i in range(1, len(data) + 1):
                            if len(data) > 1:
                                name = f'{type_ss.NAME_SS.value}_{i}'
                            else:
                                name = type_ss.NAME_SS.value
                            coord_Y = str(NumName.SS_COOR_Y.value[0] + (NumName.SS_COOR_Y.value[1] * counter))
                            counter += 1

                            object = self.new_row_obj(lvl_1, name, type_ss)

                            for key, value in self.attr_ss.items():
                                self.new_row_designed(object,
                                                      NumName.DESIGNED.value,
                                                      value[0],
                                                      coord_Y if key == '2' else value[1])

                            self.new_row_designed(object,
                                                  NumName.INIT.value,
                                                  NumName.VAL_ATTR_1.value,
                                                  f'{type_ss.SIGN.value}.{data[i - 1]}')

                            self.new_row_init(object,
                                              NumName.INIT.value,
                                              NumName.VAL_ATTR_2.value,
                                              NumName.VAL_ATTR_3.value)

    def edit_basket(self, root, data_basket: dict):
        '''Добавляем корзины на форму.'''
        for lvl in root.iter(NumName.TYPE_ROOT.value):

            for basket in data_basket:
                number = basket['basket']
                object = self.new_row_obj(lvl,
                                          f'r_basket_{number}',
                                          BASKET)

                coord_Y = str(NumName.B_COOR_Y.value[0] + (NumName.B_COOR_Y.value[1] * number))
                for key, value in self.attr_basket.items():
                    self.new_row_designed(object,
                                          NumName.DESIGNED.value,
                                          value[0],
                                          coord_Y if key == '2' else value[1])

    def edit_modul(self, root, data_basket: dict, uso_eng: str, uso_rus: str):
        '''Заполняем модулями корзину.'''
        for lvl in root.iter(NumName.TYPE_ROOT.value):
            for lvl_1 in lvl.iter(NumName.OBJECT.value):

                for basket in data_basket:
                    count_AIs = 0
                    count_AOs = 0
                    count_DIs = 0
                    count_DOs = 0
                    count_PSUs = 0
                    count_RSs = 0
                    count_Empts = 0
                    m_number = 0

                    b_number = basket['basket']
                    if self.search_string(lvl_1.attrib, NumName.NAME_ATR.value, f'r_basket_{b_number}'):

                        for modul in basket['data']:
                            try:
                                name = self.params_module[modul]
                                new_name = name.TYPE.value
                                if name == AIs:
                                    count_AIs += 1
                                    new_name = f'{name.TYPE.value}_{count_AIs}'
                                elif name == AOs:
                                    count_AOs += 1
                                    new_name = f'{name.TYPE.value}_{count_AOs}'
                                elif name == DIs:
                                    count_DIs += 1
                                    new_name = f'{name.TYPE.value}_{count_DIs}'
                                elif name == DOs:
                                    count_DOs += 1
                                    new_name = f'{name.TYPE.value}_{count_DOs}'
                                elif name == PSUs:
                                    count_PSUs += 1
                                    new_name = f'{name.TYPE.value}_{count_PSUs}'
                                elif name == RSs:
                                    count_RSs += 1
                                    new_name = f'{name.TYPE.value}_{count_RSs}'
                                elif name == Emptys:
                                    count_Empts += 1
                                    new_name = f'{name.TYPE.value}_{count_Empts}'

                                object = self.new_row_obj(lvl_1, new_name, name)

                                coord_X = str(NumName.M_COOR_X.value * m_number)
                                for key, value in self.attr_modul.items():
                                    self.new_row_designed(object,
                                                          NumName.DESIGNED.value,
                                                          value[0],
                                                          coord_X if key == '1' else value[1])

                                self.settings_modul(object,
                                                    name,
                                                    uso_eng, uso_rus,
                                                    b_number, m_number,
                                                    basket['net'])
                                m_number += 1
                            except Exception:
                                continue

    def settings_modul(self, object, t_modul, uso_eng: str, uso_rus: str,
                       b_number: int, m_number: int, net_data: dict):
        '''Дополнительные настройки модуля.'''
        try:
            m_number = f'0{m_number}' if m_number < 10 else m_number
            attribut = self.attr_CNs if t_modul.NAME.value == 'CNs' else self.attr_set_mod
            faceplate = ('true', 'false') if b_number >= 2 else ('false', 'true')
            for net in net_data:
                if net[4] == b_number:
                    net_link_in = str(net[5]).split(';')
                    net_link_out = str(net[6]).split(';')

            for key, value in attribut.items():
                if key == '2':
                    attr_value = faceplate[0]
                elif key == '3':
                    attr_value = faceplate[1]
                elif key == '6':
                    try:
                        attr_value = f'{net_link_in[2]} корзина {net_link_in[1]}'
                    except Exception:
                        attr_value = ''
                elif key == '7':
                    try:
                        attr_value = f'{net_link_out[2]} корзина {net_link_out[1]}'
                    except Exception:
                        attr_value = ''
                else:
                    attr_value = value[1]

                self.new_row_designed(object,
                                      NumName.INIT.value,
                                      value[0],
                                      attr_value)

            self.new_row_designed(object,
                                  NumName.INIT.value,
                                  NumName.VAL_ATTR_1.value,
                                  f'Diag.{t_modul.NAME.value}.{uso_eng}_A{b_number}_{m_number}')

            self.new_row_init(object,
                              NumName.INIT.value,
                              NumName.VAL_ATTR_2.value,
                              NumName.VAL_ATTR_3.value)
        except Exception:
            print({traceback.format_exc()})

    def line_in_out(self, root, data_basket: dict, uso_eng: str,
                    input_line: bool = True):
        """Добавление на форму линий связи корзины.

        Args:
            root (_type_): объект иттерирования
            data_basket (dict): данные корзины
            uso_eng (str): название шкафа на ENG
            input_line (bool, optional): Входная линия. Defaults to True.
        """
        def attr_value(attr_number: int, def_value: str, b_number: int):
            '''Координаты подсчитать невозможно,
            поэтому используем статические.'''
            if attr_number == 1:
                value_attr = attr_line.COOR_X.value
            elif attr_number == 2:
                value_attr = attr_line.COOR_Y.value[0] + attr_line.COOR_Y.value[1] * (b_number - 1)
            elif attr_number == 3:
                value_attr = attr_line.COOR_WIDTH.value[b_number - 1]
            elif attr_number == 4:
                value_attr = attr_line.COOR_HEIGHT.value[b_number - 1]
            else:
                value_attr = def_value
            return str(value_attr)

        def init_value(attr_number: int, def_value: str, uso_eng: str,
                       net_uso, b_number: int, flag_in: bool):
            '''Формируем значения входной и выходной линии.'''
            for net in net_uso:
                if net[4] == b_number:
                    basket = net[4]
                    in_basket = net[5].split(';')
                    out_basket = net[6].split(';')
                    line = in_basket if flag_in else out_basket
                    sign_in_out = 'MNs' if 'KC' in line[0] else 'CNs'
                    sign_current = 'MNs' if 'KC' in uso_eng else 'CNs'
                    if flag_in:
                        if attr_number == 5:
                            value_attr = f'Diag.{sign_in_out}.{line[0]}_01.ch_CN_02.ePNotLink'
                        elif attr_number == 6:
                            value_attr = f'Diag.{sign_current}.{uso_eng}_A{basket}_01.ch_CN_01.ePNotLink'
                        else:
                            value_attr = def_value
                    else:
                        if attr_number == 5:
                            value_attr = f'Diag.{sign_current}.{uso_eng}_A{basket}_01.ch_CN_02.ePNotLink'
                        elif attr_number == 6:
                            value_attr = f'Diag.{sign_in_out}.{line[0]}_01.ch_CN_01.ePNotLink'
                        else:
                            value_attr = def_value
                    return value_attr

        attr_line = InputLine if input_line else OutputLine
        for lvl in root.iter(NumName.TYPE_ROOT.value):
            for basket in data_basket:
                number = basket['basket']
                net = basket['net']

                object = self.new_row_obj(lvl,
                                          f'{attr_line.NAME.value}{number}',
                                          attr_line)

                for key, value in self.attr_obj_in_out.items():
                    self.new_row_designed(object,
                                          NumName.DESIGNED.value,
                                          value[0],
                                          attr_value(int(key),
                                                     value[1], number))
                for key, value in self.attr_init_in_out.items():
                    self.new_row_designed(object,
                                          NumName.INIT.value,
                                          value[0],
                                          init_value(int(key), value[1],
                                                     uso_eng, net, number,
                                                     input_line))
                self.new_row_init(object,
                                  NumName.INIT.value,
                                  NumName.VAL_ATTR_2.value,
                                  NumName.VAL_ATTR_3.value)

    def edit_point(self, root, data_basket: dict, input_line: bool = True):
        '''Добавление на форму точек для отображения линии.'''
        def attr_value(attr_number: int, count_point: int):
            '''Координаты подсчитать невозможно,
            поэтому используем статические.'''
            if attr_number == 1:
                value_attr = attr_line.COOR_X.value[count_point - 1]
            elif attr_number == 2:
                value_attr = attr_line.COOR_Y.value[count_point - 1]
            return str(value_attr)

        attr_line = InputPoint if input_line else OutputPoint
        sign = InputLine if input_line else OutputLine

        for lvl in root.iter(NumName.TYPE_ROOT.value):
            for lvl_1 in lvl.iter(NumName.OBJECT.value):

                for basket in data_basket:
                    b_number = basket['basket']
                    if self.search_string(lvl_1.attrib,
                                          NumName.NAME_ATR.value,
                                          f'{sign.NAME.value}{b_number}'):

                        for i in range(1, 4):
                            object = self.new_row_obj(lvl_1,
                                                      f'{attr_line.NAME.value}{i}',
                                                      attr_line)

                            for key, value in self.attr_point.items():
                                self.new_row_designed(object,
                                                      NumName.DESIGNED.value,
                                                      value[0],
                                                      attr_value(int(key), i))


class DaignoPicture():
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
        try:
            data_AI[0]
            return data_DI, data_AI[0]
        except Exception:
            return data_DI, 0

    def request_basket(self, uso_rus: str):
        '''Собираем данные по каждому шкафу.'''
        data = []

        net_value = self.dop_function.connect_by_sql_condition('net', '*', f'''"name"='{uso_rus}' ''')
        fl_not_link = True if not len(net_value) else False
        for column in HardWare.select().order_by(HardWare.id).dicts():
            uso = column['uso']
            if uso_rus == uso:
                tag = column['tag']
                basket = column['basket']

                data_b = [column[f'type_{modul_column}'] for modul_column in range(0, 33, 1)]

                for i in range(len(data_b), 0, -1):
                    if data_b[i - 1] is None:
                        data_b.pop(i - 1)
                    else:
                        break

                data.append(dict(tag=tag,
                                 basket=basket,
                                 data=data_b,
                                 net=net_value))
        return data, fl_not_link

    def filling_pic_uso(self):
        msg = {}
        system = MNS if connect.type_system == 'MNS' else PT
        try:
            name_uso = self.cabinet_names()
            for eng, rus in name_uso.items():
                # Корзина КЦ не нужна
                if 'KC' in eng:
                    continue
                # Проверка шаблона и создание новой картинки
                path_picture = self.check_template(eng)
                # Парсинг новой картинки
                parser = ParserFile(path_picture)
                root, tree = parser()
                # Правка шаблона
                parser.edit_template(system, root, eng, rus)
                # Добавление служебных сигналов
                parser.service_signals(root, self.request_ss(rus))
                # Собираем корзины
                data, fl_not_link = self.request_basket(rus)
                # Заполняем форму
                parser.edit_basket(root, data)
                parser.edit_modul(root, data, eng, rus)
                # Добавляем подписи к линиям
                parser.in_out_name(root, data, fl_not_link)
                # Если есть связь между корзинами
                if not fl_not_link:
                    # Добавляем линии корзины
                    parser.line_in_out(root, data, eng)
                    parser.line_in_out(root, data, eng, False)
                    # Добавляем точки к линиям
                    parser.edit_point(root, data)
                    parser.edit_point(root, data, False)

                tree.write(path_picture, pretty_print=True, encoding='utf-8')
            return msg
        except Exception:
            msg[f'{today} - HMI. USO. Ошибка {traceback.format_exc()}'] = 2
            return msg