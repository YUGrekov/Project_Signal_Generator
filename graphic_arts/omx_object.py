import traceback
import uuid
import re
from lxml import etree
from request_sql import RequestSQL
from general_functions import General_functions
from model_new import connect as tx
from model_new import AI
from model_new import DI
from model_new import SS
from model_new import PIC
from model_new import VS
from model_new import ZD
from model_new import UMPNA
from model_new import UTS
from model_new import UPTS
from model_new import KTPR
from model_new import KTPRP
from model_new import KTPRA
from model_new import GMPNA
from model_new import PI
from model_new import PZ
from model_new import HardWare


ANALOGs = 'Analogs'
DISCRETs = 'Diskrets'
PICTUREs = 'Pictures'
UTSs = 'UTSs'
UPTSs = 'UPTSs'
VSs = 'AuxSystems'
ZDs = 'Valves'
NAs = 'NAs'
SSs = 'SSs'
KTPRs = 'KTPRs.'
KTPRAs = 'KTPRAs'
GMPNAs = 'GMPNAs'
PIs = 'PIs'
PZs = 'PZs'


class BaseMethod():
    '''Базовые методы заполнения.'''
    def __init__(self, logtext) -> None:
        self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def path_file(self, text, fl_diag: bool = False):
        '''Формирование пути до файла и очистка перед заполнением.'''
        path_attr = f'Root{tx.prefix_system}'

        root, tree = self.dop_function.xmlParser(tx.path_to_devstudio_omx)
        el1 = self.dop_function.clear_omx(path_attr, text, root, fl_diag)

        tree.write(tx.path_to_devstudio_omx, pretty_print=True)
        return el1, tree

    def create_object(self, name, base_type):
        '''Создание объекта DevStudio.'''
        object = etree.Element("{automation.control}object")
        object.attrib['name'] = name
        object.attrib['uuid'] = str(uuid.uuid1())
        object.attrib['base-type'] = base_type
        object.attrib['aspect'] = 'unit.Library.PLC_Types.PLC'
        return object

    def new_attribute(self, object, type_object, value):
        '''Создание атрибутов объекта DevStudio.'''
        if value is None:
            value = ' '

        attribute = etree.Element('attribute')
        attribute.attrib['type'] = type_object
        attribute.attrib['value'] = str(value)
        object.append(attribute)


class AnalogsOmx(BaseMethod):
    '''Заполнение объектов файла omx DevStudio.'''
    t_ai_lv = 'unit.Library.PLC_Types.lv_Analog_PLC'
    t_ai = 'unit.Library.PLC_Types.Analog_PLC'

    sign_vu = {'объем': 'V',
               'объём': 'V',
               'перепад': 'dP',
               'давлени': 'P',
               'загазованность': 'Газ',
               'вертик': 'Xверт',
               'горизонт': 'Xгор',
               'осевая': 'Xос',
               'попереч': 'Xпоп',
               'осевое': 'Xoc',
               'сила': 'I',
               'температура': 'T',
               'уровень': 'L',
               'утечк': 'L',
               'расход': 'Q',
               'положени': 'Q',
               'затоплен': 'L',
               'частот': 'F',
               'процен': 'Q',
               'заслон': 'Q'}

    def choice_param(self, group_id, name):
        '''Выбор параметров для заполнения.'''
        base_type = self.t_ai_lv if group_id in ('Уровни', 'Аналоговые выходы') else self.t_ai
        sign = next((value for key, value in self.sign_vu.items() if key in name.lower()), ' ')
        return base_type, sign

    def write_in_omx(self):
        '''Заполнение объектами.'''
        try:
            el1, tree = self.path_file(ANALOGs)
            data = self.request.select_orm(AI, None, AI.id)

            for row in data:
                base_type, sign = self.choice_param(row.AnalogGroupId, row.name)

                if row.tag_eng is None or row.tag_eng == ' ':
                    continue

                object = self.create_object(row.tag_eng, base_type)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Sign", sign)
                self.new_attribute(object, "unit.Library.Attributes.EGU_Desc", row.Egu)
                self.new_attribute(object, "unit.Library.Attributes.EGU_Desc_phys", row.PhysicEgu)
                self.new_attribute(object, "unit.Library.Attributes.EGU_Desc_Alt", 'кгс/см2')
                self.new_attribute(object, "unit.Library.Attributes.EGUsChange", row.IsOilPressure)
                self.new_attribute(object, "unit.Library.Attributes.AI_Ref_KZFKP", row.tag)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {ANALOGs}. Заполнено''', 1)
        except Exception:
            print(traceback.format_exc())
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {ANALOGs}. Ошибка {traceback.format_exc()}''', 2)


class DiskretsOmx(BaseMethod):
    '''Заполнение объектов файла omx DevStudio.'''
    t_di = 'unit.Library.PLC_Types.Diskret_PLC'

    sign_vu = {'давлен': 'P',
               'напряж': 'U',
               'уровень': 'L',
               'затоплен': 'L',
               'утечк': 'L',
               'питание': 'U',
               'питание шкафа': 'U'}

    def choice_param(self, name, pNC_AI):
        '''Выбор параметров для заполнения.'''
        sign = next((value for key, value in self.sign_vu.items() if key in name.lower()), ' ')

        ai_id = re.findall('\d+', str(pNC_AI))
        if len(ai_id):
            data_ai = self.request.select_orm(AI, (AI.id == int(ai_id[0])), AI.id)
            for row in data_ai:
                ai_tag = row.tag
                ai_tag_eng = row.tag_eng
        else:
            ai_tag = ' '
            ai_tag_eng = ' '

        return sign, ai_tag, ai_tag_eng

    def write_in_omx(self):
        '''Заполнение объектами.'''
        try:
            el1, tree = self.path_file(DISCRETs)
            data = self.request.select_orm(DI, None, DI.id)

            for row in data:
                sign, ai_tag, ai_tag_eng = self.choice_param(row.name, row.pNC_AI)

                if row.tag_eng is None or row.tag_eng == '':
                    continue

                object = self.create_object(row.tag_eng, self.t_di)
                self.new_attribute(object, 'unit.Library.Attributes.Index', row.id)
                self.new_attribute(object, 'unit.Library.Attributes.Sign', sign)
                self.new_attribute(object, 'unit.System.Attributes.Description', row.name)
                self.new_attribute(object, 'unit.Library.Attributes.AI_Ref', ai_tag_eng)
                self.new_attribute(object, 'unit.Library.Attributes.AI_Ref_KZFKP', ai_tag)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {DISCRETs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {DISCRETs}. Ошибка {traceback.format_exc()}''', 2)


class VSOmx(BaseMethod):
    '''Заполнение объектов файла omx DevStudio.'''
    t_vs = 'unit.Library.PLC_Types.AuxSystem_PLC'

    def choice_param(self, name, pNC_AI):
        '''Выбор параметров для заполнения.'''
        number = re.findall('\d+', str(pNC_AI))
        if len(number):
            data_ai = self.request.select_orm(AI, (AI.id == int(number[0])), AI.id)
            for row in data_ai:
                ai_tag = row.tag
                ai_tag_eng = row.tag_eng
        else:
            ai_tag = ' '
            ai_tag_eng = ' '

        return sign, ai_tag, ai_tag_eng

    def write_in_omx(self):
        '''Заполнение объектами.'''
        try:
            el1, tree = self.path_file(VSs)
            data = self.request.select_orm(VS, None, VS.id)

            for row in data:
                sensor = self.choice_param(row.name, row.Pressure_is_True)
                voltage = self.choice_param(row.name, row.Voltage)
                close = self.choice_param(row.name, row.OTKL)

                object = self.create_object(f'VS_{row.id}', self.t_vs)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Sign", row.short_name)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)
                self.new_attribute(object, "unit.Library.Attributes.PC_Use", pc_use)
                self.new_attribute(object, "unit.Library.Attributes.PC_Ref", sensor)
                self.new_attribute(object, "unit.Library.Attributes.DI_ref", voltage)
                self.new_attribute(object, "unit.Library.Attributes.DO_ref", close)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {VSs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {VSs}. Ошибка {traceback.format_exc()}''', 2)


# a = VSOmx()
# a.write_in_omx()