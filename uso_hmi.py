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


class NumName(Enum):
    '''Перечисление статических названий.'''
    TYPE_ROOT = 'type'
    OBJECT = 'object'
    DESIGNED = 'designed'
    NAME_ATR = 'name'
    D_NAME = 'display-name'
    UUID = 'uuid'
    DO_ON = 'do-on'


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

    attrib_ss = {'1': DesignedParamsThree(target='X', value='5', ver='5'),
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

    attrib_t_input_link_d = {'1': DesignedParamsThree(target='X', value='10', ver='5'),
                             '2': DesignedParamsThree(target='Y', value='25', ver='5'),
                             '3': DesignedParamsThree(target='Rotation', value='0', ver='5'),
                             '4': DesignedParamsThree(target='Width', value='220', ver='5'),
                             '5': DesignedParamsThree(target='Height', value='20', ver='5')}

    attrib_t_output_link_d = {'1': DesignedParamsThree(target='X', value='10', ver='5'),
                              '2': DesignedParamsThree(target='Y', value='replace', ver='5'),
                              '3': DesignedParamsThree(target='Rotation', value='0', ver='5'),
                              '4': DesignedParamsThree(target='Width', value='220', ver='5'),
                              '5': DesignedParamsThree(target='Height', value='20', ver='5')}

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


class ParserFile():
    '''Парсер файла картинки'''
    def __init__(self, new_pic_path: str) -> None:
        parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
        self.tree = etree.parse(new_pic_path, parser)
        self.root = self.tree.getroot()

    def __call__(self):
        return self.root, self.tree

    def update_string(object: dict, key: str, value: str, new_value: str):
        '''Поиск и обновление строки'''
        if object[key] == value:
            object[key] = new_value

    def edit_template(self, root, name_uso: str):
        '''Редактирование новой формы под общие для
        всех форм детали и под конкретную систему.'''

        for lvl in root.iter(NumName.TYPE_ROOT.value):
            self.update_string(lvl.attrib, NumName.NAME_ATR.value, NumName.NAME_ATR.value, f'D_{connect.type_system}_{name_uso}')
            self.update_string(lvl.attrib, NumName.D_NAME.value, NumName.NAME_ATR.value, f'D_{connect.type_system}_{name_uso}')
            self.update_string(lvl.attrib, NumName.UUID.value, NumName.UUID.value, str(uuid.uuid1()))




        for lvl_one in root.iter('type'):
            if lvl_one.attrib['name'] == 'name':
                lvl_one.attrib['name'] = f'D_{prefix_system}{tag_cut}'
            if lvl_one.attrib['display-name'] == 'name':
                lvl_one.attrib['display-name'] = f'D_{prefix_system}{tag_cut}'
            if lvl_one.attrib['uuid'] == 'uuid':
                lvl_one.attrib['uuid'] = str(uuid.uuid1())
            if not flag_ASPT:
                for lvl_two in lvl_one.iter('designed'):
                    # Координата Width
                    if lvl_two.attrib['value'] == '1670':
                        lvl_two.attrib['value'] = '1420'

            for lvl_two in lvl_one.iter('object'):
                if lvl_two.attrib['name'] == 't_uso_title':
                    for lvl_three in lvl_two.iter('designed'):
                        if lvl_three.attrib['value'] == 'Rename':
                            lvl_three.attrib['value'] = name_uso

                if not flag_ASPT:
                    if lvl_two.attrib['name'] == 'r_ss':
                        for lvl_three in lvl_two.iter('designed'):
                            if lvl_three.attrib['value'] == '950':
                                lvl_three.attrib['value'] = '780'

                if lvl_two.attrib['name'] == 'Rename_link':
                    lvl_two.attrib['name'] = f'_link_D_{prefix_system}{tag_cut}_for_enable'
                if lvl_two.attrib['display-name'] == 'Rename_link':
                    lvl_two.attrib['display-name'] = f'_link_D_{prefix_system}{tag_cut}_for_enable'

                for lvl_two in lvl_one.iter('do-on'):
                    if lvl_two.attrib['name'] == 'Handler_1':
                        for lvl_three in lvl_two.iter('body'):
                            lvl_three.text = CDATA(f'_link_D_{prefix_system}{tag_cut}_for_enable.Enabled=false;')

                    if lvl_two.attrib['name'] == 'Handler_2':
                        for lvl_three in lvl_two.iter('body'):
                            lvl_three.text = CDATA(f'_link_D_{prefix_system}{tag_cut}_for_enable.Enabled=true;')


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

    def filling_pic_uso(self):
        name_uso = self.cabinet_names()
        for eng, rus in name_uso.items():

            path_picture = self.check_template(eng)

            parser = ParserFile(path_picture)
            root, tree = parser()

            parser.edit_template(root, eng)






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