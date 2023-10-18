import uuid
import shutil
import os
import traceback
from datetime import datetime
from typing import Any
from lxml import etree
from main_base import General_functions
from main_base import connect
from enum import Enum
from typing import NamedTuple
from request_sql import RequestSQL


class BaseDefenceMap():
    '''Базовый класс карты защит.'''
    "number_pump_VU"
    "number_list_VU"
    "number_protect_VU"


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


class KTPRA(BaseDefenceMap):
    caption_name = 'Карта агрегатных защит'
    map_name = 'Form_Defences_MA'
    apsoure_name = 'ApSource_form_KTPRAs_MA'
    path_server = 'KTPRAs.KTPRAs'
    link_ref = 'unit.WorkspaceControl.Defences_Control.NA'
    attrib_top = 'type_defence_top'
    attrib_row = 'type_defence_row'
    attrib_click = 'type_defence_button'
    bt_id_top = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
    bt_id_row = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'


class GMPNA(BaseDefenceMap):
    caption_name = 'Карта агрегатных готовностей'
    map_name = 'Form_Readiness_MA'
    apsoure_name = 'ApSource_form_GMPNAs_MA'
    path_server = 'GMPNAs.GMPNAs'
    link_ref = 'unit.WorkspaceControl.Readiness_Control.NA'
    attrib_top = 'type_defence_top'
    attrib_row = 'type_defence_row'
    attrib_click = 'type_readiness_button'
    bt_id_top = 'b08a935f-b03d-42e0-96c4-dc639b70d499'
    bt_id_row = '48231209-9a9f-42cf-9b38-ef1ef5cc7403'


class DefenceMap():
    '''Запуск генератора карты защит.'''
    def __init__(self):
        # self.logsTextEdit = logtext
        self.dop_function = General_functions()

    def check_template(self, name_uso: str) -> str:
        '''Проверка шаблона и создание на его основе нового шкафа.'''
        new_picture = f'{connect.path_hmi}\\D_{connect.type_system}_{name_uso}.omobj'

        if os.path.isfile(new_picture):
            os.remove(new_picture)
        shutil.copy2(f'{connect.path_hmi_sample}\\D_USO_Template.omobj',
                     new_picture)
        return new_picture

    def select_kit(self, table: str):
        '''Выбор конструктора для заполнения.'''
        if table == 'KTPR':
            return KTPR
        elif table == 'KTPRP':
            return KTPRP
        elif table == 'KTPRA':
            return KTPRA
        elif table == 'GMPNA':
            return GMPNA

    def fill_pic_new(self, list_table: dict, fl_one_pic: bool,
                     number_pump: int = None):
        """Заполнение новой формы.
        Args:
            list_table (dict): Список таблиц для формирования форм.
            fl_one_pic (bool): Флаг для KTPR и KTPRP, где всегда 1 форма.
            number_pump (int, optional): Номер агрегата, если необходимо.
            Defaults to None.
        """
        request = RequestSQL()
        for table in list_table:
            # Выделяем конструктор под конкретную таблицу
            kit = self.select_kit(list_table)
            # Max число агрегатов = числу форм для KTPRA и GMPNA. Default to 1
            max_value = 1
            if not fl_one_pic:
                max_value = request.max_value_column(table, "number_pump_VU")
                # max_value = self.dop_function.max_value_column(table, "number_pump_VU", False)
            


a = DefenceMap()
a.fill_pic_new(('KTPR'), True)
