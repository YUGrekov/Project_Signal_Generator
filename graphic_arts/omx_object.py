import traceback
import uuid
import re
import math
from lxml import etree
from request_sql import RequestSQL
from general_functions import General_functions
from model_new import connect as tx
from model_new import AI
from model_new import DI
from model_new import DO
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
KTPRs = 'KTPRs'
KTPRAs = 'KTPRAs'
GMPNAs = 'GMPNAs'
PIs = 'PIs'
PZs = 'PZs'
Empty = ' '


class BaseMethod():
    '''Базовые методы заполнения.'''
    def __init__(self, *args) -> None:
        self.logsTextEdit = args[0]
        self.dict = args
        self.request = RequestSQL()
        self.dop_function = General_functions()
        self.fl_gmpna = args[1]

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

    def create_object_short(self, name):
        '''Создание объекта DevStudio.'''
        object = etree.Element("{automation.control}object")
        object.attrib['name'] = name
        object.attrib['uuid'] = str(uuid.uuid1())
        return object

    def new_attribute(self, object, type_object, value):
        '''Создание атрибутов объекта DevStudio.'''
        if value is None:
            value = ' '

        attribute = etree.Element('attribute')
        attribute.attrib['type'] = type_object
        attribute.attrib['value'] = str(value)
        object.append(attribute)

    def empty_value(self, value):
        '''Проверка значение на пустоту.'''
        return Empty if value == ' ' or value is None else value


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
    '''Заполнение объектов VS файла omx DevStudio.'''
    t_vs = 'unit.Library.PLC_Types.AuxSystem_PLC'

    def choice_param(self, tag, model):
        '''Поиск тега для контекстного меню'''
        try:
            isdigit = re.findall('\d+', tag)
            row = self.request.select_orm(model, model.id == isdigit, model.id)
            return row[0].tag_eng
        except Exception:
            return Empty

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            el1, tree = self.path_file(VSs)
            data = self.request.select_orm(VS, None, VS.id)

            for row in data:
                short_name = self.empty_value(row.short_name)

                pressure = f'{row.Pressure_is_True}'
                if 'di' in pressure.lower():
                    sensor = self.choice_param(pressure, DI)
                    pc_use = '1'
                elif 'ai' in pressure.lower():
                    sensor = self.choice_param(pressure, AI)
                    pc_use = '2'
                else:
                    sensor = Empty
                    pc_use = '0'

                voltage = self.choice_param(row.Voltage, DI)
                close = self.choice_param(row.OTKL, DO)

                object = self.create_object(f'VS_{row.id}', self.t_vs)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Sign", short_name)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)
                self.new_attribute(object, "unit.Library.Attributes.PC_Use", pc_use)
                self.new_attribute(object, "unit.Library.Attributes.PC_Ref", sensor)
                self.new_attribute(object, "unit.Library.Attributes.DI_ref", voltage)
                self.new_attribute(object, "unit.Library.Attributes.DO_ref", close)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {VSs}. Заполнено''', 1)
        except Exception:
            print(traceback.format_exc())
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {VSs}. Ошибка {traceback.format_exc()}''', 2)


class ZDOmx(BaseMethod):
    '''Заполнение объектов ZD файла omx DevStudio.'''
    t_bt = 'unit.Library.PLC_Types.Valve_PLC'
    t_bt_rs = 'unit.Library.PLC_Types.ex_Valve_PLC'

    def choice_param(self, tag, model):
        '''Поиск тега для контекстного меню'''
        try:
            isdigit = re.findall('\d+', tag)
            row = self.request.select_orm(model, model.id == isdigit, model.id)
            return row[0].tag_eng
        except Exception:
            return Empty

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            el1, tree = self.path_file(ZDs)
            data = self.request.select_orm(ZD, None, ZD.id)

            for row in data:
                short_name = self.empty_value(row.short_name)

                kvo = self.choice_param(row.kvo, DI)
                open_do = self.choice_param(row.open, DO)

                # Наличие мутфа, авария
                isBUR = True if (row.vmmo is None or row.vmmo == '') or (row.vmmz is None or row.vmmz == '') else False
                # Наличие ключа М/Д смотри по двум полям физика или интерфейс
                isDist = True if (row.dist_i is None or row.dist_i != '') or (row.dist is None or row.dist != '') else False

                object = self.create_object(f'ZD_{row.id}', self.t_bt_rs if row.exists_interface is True else self.t_bt)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Sign", short_name)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)
                self.new_attribute(object, "unit.Library.Attributes.BUR", isBUR)
                self.new_attribute(object, "unit.Library.Attributes.RS485", row.exists_interface)
                self.new_attribute(object, "unit.Library.Attributes.Dist_key", isDist)
                self.new_attribute(object, "unit.Library.Attributes.DI_ref", kvo)
                self.new_attribute(object, "unit.Library.Attributes.DO_ref", open_do)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Object. {ZDs}. Заполнено''', 1)
        except Exception:
            print(traceback.format_exc())
            # self.logsTextEdit.logs_msg(f'''DevStudio. Object. {ZDs}. Ошибка {traceback.format_exc()}''', 2)


class NAOmx(BaseMethod):
    '''Заполнение объектов ZD файла omx DevStudio.'''
    t_bt = 'unit.Library.PLC_Types.NA_PLC'

    def choice_param(self, tag, model):
        '''Поиск тега для контекстного меню'''
        try:
            isdigit = re.findall('\d+', tag)
            row = self.request.select_orm(model, model.id == isdigit, model.id)
            return row[0].tag_eng
        except Exception:
            return Empty

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            el1, tree = self.path_file(NAs)
            data = self.request.select_orm(UMPNA, None, UMPNA.id)

            for row in data:
                di_ref = self.choice_param(row.vv_included, DI)
                di_ref1 = self.choice_param(row.vv_double_included, DI)
                do_ref = self.choice_param(row.command_to_turn_off_the_vv_output_1, DO)
                do_ref1 = self.choice_param(row.command_to_turn_off_the_vv_output_2, DO)

                object = self.create_object(f'NA_{row.id}', self.t_bt)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Sign", row.name)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)
                self.new_attribute(object, "unit.Library.Attributes.DI_ref", di_ref)
                self.new_attribute(object, "unit.Library.Attributes.DI_ref1", di_ref1)
                self.new_attribute(object, "unit.Library.Attributes.DO_ref", do_ref)
                self.new_attribute(object, "unit.Library.Attributes.DO_ref1", do_ref1)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {NAs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {NAs}. Ошибка {traceback.format_exc()}''', 2)


class UtsUptsOmx(BaseMethod):
    '''Заполнение объектов UTS or UPTS файла omx DevStudio.'''
    t_bt_uts = 'unit.Library.PLC_Types.UTS_PLC'
    t_bt_upts = 'unit.Library.PLC_Types.UPTS_PLC'

    def choice_system(self):
        '''Выбор системы.'''
        if tx.type_system == 'PT':
            model = UPTS
            sign = UPTSs
            base_type = self.t_bt_upts
        else:
            model = UTS
            sign = UTSs
            base_type = self.t_bt_uts
        return model, sign, base_type

    def choice_param(self, tag, model):
        '''Поиск тега для контекстного меню'''
        try:
            isdigit = re.findall('\d+', tag)
            row = self.request.select_orm(model, model.id == isdigit, model.id)
            return row[0].tag_eng
        except Exception:
            return Empty

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            model, sign, base_type = self.choice_system()

            el1, tree = self.path_file(sign)
            data = self.request.select_orm(model, None, model.id)

            for row in data:
                if row.tag is None:
                    continue

                do_ref = self.choice_param(row.VKL, DO)
                tag = self.dop_function.translate(str(row.tag))
                if row.siren:
                    sign = 'Сирена'
                elif 'газ' in row.name.lower():
                    sign = 'Газ'
                else:
                    sign = ''

                object = self.create_object(tag, base_type)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Sign", sign)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)
                self.new_attribute(object, "unit.Library.Attributes.DO_ref", do_ref)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {sign}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {sign}. Ошибка {traceback.format_exc()}''', 2)


class PIOmx(BaseMethod):
    '''Заполнение объектов PI файла omx DevStudio.'''
    t_bt = 'unit.Library.PLC_Types.PI_PLC'

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            el1, tree = self.path_file(PIs)
            data = self.request.select_orm(PI, None, PI.id)

            for row in data:
                if row.tag is None:
                    continue

                place = self.empty_value(row.location)
                tag = self.dop_function.translate(str(row.tag))

                object = self.create_object(tag, self.t_bt)
                self.new_attribute(object, "unit.Library.Attributes.Sign", row.tag)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Place", place)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {PIs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {PIs}. Ошибка {traceback.format_exc()}''', 2)


class PZOmx(BaseMethod):
    '''Заполнение объектов PZ файла omx DevStudio.'''
    t_bt = 'unit.Library.PLC_Types.PZ_PLC'

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            el1, tree = self.path_file(PZs)
            data = self.request.select_orm(PZ, None, PZ.id)

            for row in data:
                short_name = self.empty_value(row.short_name)

                object = self.create_object(f'PZ_{row.id}', self.t_bt)
                self.new_attribute(object, "unit.Library.Attributes.Sign", short_name)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {PZs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {PZs}. Ошибка {traceback.format_exc()}''', 2)


class PICOmx(BaseMethod):
    '''Заполнение объектов PIC файла omx DevStudio.'''
    t_bt = 'unit.Library.PLC_Types.Picture_PLC'

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            el1, tree = self.path_file(PICTUREs)
            data = self.request.select_orm(PIC, None, PIC.id)

            for row in data:
                if row.frame is None:
                    continue

                object = self.create_object(row.frame, self.t_bt)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Sign", row.name)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {PICTUREs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {PICTUREs}. Ошибка {traceback.format_exc()}''', 2)


class SSOmx(BaseMethod):
    '''Заполнение объектов PIC файла omx DevStudio.'''
    t_bt = 'unit.Library.PLC_Types.SS_PLC'

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            el1, tree = self.path_file(SSs)
            data = self.request.select_orm(SS, None, SS.id)

            for row in data:
                object = self.create_object(f'SS_{row.id}', self.t_bt)
                self.new_attribute(object, "unit.Library.Attributes.Index", row.id)
                self.new_attribute(object, "unit.Library.Attributes.Sign", row.name)
                self.new_attribute(object, "unit.System.Attributes.Description", row.name)

                el1.append(object)

            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {SSs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {SSs}. Ошибка {traceback.format_exc()}''', 2)


class KTPROmx(BaseMethod):
    '''Заполнение объектов PIC файла omx DevStudio.'''
    t_bt = 'unit.Library.PLC_Types.KTPRx_PLC'

    def choice_system(self):
        '''Выбор системы.'''
        return KTPRP if tx.type_system == 'PT' else KTPR

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            model = self.choice_system()
            el1, tree = self.path_file(KTPRs)

            count_row = self.request.count_row_orm(model)
            count_group = math.ceil(count_row / 4)

            for count in range(count_group):
                obj = self.create_object(f'Group_{count + 1}', self.t_bt)
                el1.append(obj)
            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {KTPRs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {KTPRs}. Ошибка {traceback.format_exc()}''', 2)


class KtpraGmpnaOmx(BaseMethod):
    '''Заполнение объектов PIC файла omx DevStudio.'''
    t_bt_ktpra = 'unit.Library.PLC_Types.KTPRx_PLC'
    t_bt_gmpna = 'unit.Library.PLC_Types.GMPNA_PLC'

    def choice_system(self):
        '''Выбор системы.'''
        if self.fl_ktpra:
            model = KTPRA
            sign = KTPRAs
            base_type = self.t_bt_ktpra
        else:
            model = GMPNA
            sign = GMPNAs
            base_type = self.t_bt_gmpna
        return model, sign, base_type

    def write_in_omx(self):
        '''Заполнение структуры.'''
        try:
            model, sign, base_type = self.choice_system()
            el1, tree = self.path_file(sign)

            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {model}, {sign}, {base_type}. Заполнено''', 1)

            count_pumps = self.request.count_row_orm(UMPNA)
            count_row = self.request.count_row_orm(model)
            count_group = math.ceil((count_row / count_pumps) / 4)

            for pumps in range(count_pumps):
                obj = self.create_object_short(f'{sign}_{pumps + 1}')

                for count in range(count_group):
                    group = self.create_object(f'Group_{count + 1}', base_type)
                    obj.append(group)
                el1.append(obj)
            tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {KTPRs}. Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {KTPRs}. Ошибка {traceback.format_exc()}''', 2)


#a = KtpraGmpnaOmx()
# a.write_in_omx()