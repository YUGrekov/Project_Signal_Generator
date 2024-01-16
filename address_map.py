import traceback
import math
from lxml import etree
from datetime import datetime
from main_base import General_functions
from models import connect
from models import AI
from models import DI
from models import SS
from models import PIC
from models import VS
from models import ZD
from models import UMPNA
from models import UTS
from models import UPTS
from models import KTPR
from models import KTPRP
from models import KTPRA
from models import GMPNA
from models import PI
from models import PZ
from models import HardWare
from models import Modbus


today = datetime.now()
MODBUS_503 = 'ModBus503.xml'
MODBUS = 'ModBus.xml'
ANALOGs = 'Analogs.'
DISCRETs = 'Diskrets.'
PICTUREs = 'Pictures.'
UTSs = 'UTSs.'
UPTSs = 'UPTSs.'
VSs = 'AuxSystems.'
ZDs = 'Valves.'
NAs = 'NAs.'
SSs = 'SSs.'
KTPRs = 'KTPRs.'
KTPRAs = 'KTPRAs.'
GMPNAs = 'GMPNAs.'
PIs = 'PIs.'
PZs = 'PZs.'


class BaseMap():
    '''Базовые методы заполнения.'''
    def path_file(self, p_file: str, section: str):
        '''Формирование пути до файла и очистка перед заполнением.'''
        self.gen_funct = General_functions()
        path = f'{connect.path_to_devstudio}\{p_file}'
        root, tree = self.gen_funct.xmlParser(path)
        self.search_clear_section(root, section)
        return root, tree, path

    def _read_address_mb(self):
        '''Чтение адресов ModBus из базы.'''
        modbus = self.gen_funct.select_orm(Modbus, None, Modbus.id)
        start_addrr = {}
        for row in modbus:

            for var in self.variable:

                if var == str(row.variable):
                    start_addrr[var] = row.start_address
                    break

        return start_addrr

    def search_clear_section(self, root, section: str):
        '''Поиск раздела для парсинга карты адресов.'''
        for item in root.iter('node-path'):
            signal = f'Root{connect.prefix_system}.{section}'

            if signal in item.text:
                parent = item.getparent()
                root.remove(parent)

    def new_element(self, root, name: str, addrr: str):
        '''Создание нового элемента в файле.'''
        object = etree.Element('item')
        object.attrib['Binding'] = 'Introduced'
        node_p = etree.Element('node-path')
        node_p.text = str(name)
        object.append(node_p)
        segment = etree.Element('table')
        segment.text = 'Holding Registers'
        object.append(segment)
        address = etree.Element('address')
        address.text = str(addrr)
        object.append(address)
        root.append(object)

    def get_modul(self, type_modul: str):
        '''Собираем данные для дигностики по корзина с выбранным модулем.'''
        modul = []
        count = 0
        for basket in HardWare.select().dicts().order_by(HardWare.id):
            id_ = basket['id']
            tag = basket['tag']
            uso = basket['uso']
            num_basket = basket['basket']

            for key, value in basket.items():
                if value == type_modul:
                    number_modul = str(key).split('_')[1]
                    if int(number_modul) < 10:
                        string_name = f'{tag}_0{number_modul}'
                        modPosition = f'A{num_basket}.0{number_modul}'
                    else:
                        string_name = f'{tag}_{number_modul}'
                        modPosition = f'A{num_basket}.{number_modul}'
                    count += 1
                    modul.append(dict(count=count,
                                      id_=id_,
                                      uso=uso,
                                      string_name=string_name,
                                      num_basket=num_basket,
                                      number_modul=number_modul,
                                      modPosition=modPosition))
        return modul


class AnalogsMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['AIVisualValue', 'AIElValue', 'AIValue', 'AIRealValue',
              'StateAI', 'Range_Bottom', 'Range_Top']

    variable = ['AIVisualValue', 'AIElValue', 'AIValue',
                'AIRealValue', 'StateAI', 'AIParam']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS_503, ANALOGs)

            data = self.gen_funct.select_orm(AI, None, AI.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {ANALOGs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                if not len(row.tag):
                    continue

                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}.{ANALOGs}{row.tag_eng}.{self.prefix[i]}'

                    # Для уровней другой набор префиксов
                    if 'Уровни' not in row.AnalogGroupId and i > 4:
                        break

                    if 'AIVisualValue' == self.prefix[i]:
                        address = list_addrr['AIVisualValue'] + 2 * (row.id - 1)
                    elif 'AIElValue' == self.prefix[i]:
                        address = list_addrr['AIElValue'] + (row.id - 1)
                    elif 'AIValue' == self.prefix[i]:
                        address = list_addrr['AIValue'] + 2 * (row.id - 1)
                    elif 'AIRealValue' == self.prefix[i]:
                        address = list_addrr['AIRealValue'] + 2 * (row.id - 1)
                    elif 'StateAI' == self.prefix[i]:
                        address = list_addrr['StateAI'] + 2 * (row.id - 1)
                    elif 'Range_Bottom' == self.prefix[i]:
                        address = list_addrr['AIParam'] + 2 + 48 * (row.id - 1)
                    elif 'Range_Top' == self.prefix[i]:
                        address = list_addrr['AIParam'] + 4 + 48 * (row.id - 1)

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {ANALOGs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {ANALOGs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class DiskretsMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    variable = ['StateDI']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, DISCRETs)

            data = self.gen_funct.select_orm(DI, None, DI.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {DISCRETs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                name = f'Root{connect.prefix_system}.{DISCRETs}{row.tag_eng}.StateDI'

                address = list_addrr['StateDI'] + (row.id - 1)
                self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {DISCRETs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {DISCRETs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class PicturesMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    variable = ['StatePicture']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, PICTUREs)

            data = self.gen_funct.select_orm(PIC, None, PIC.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {PICTUREs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                if row.frame is None or row.frame == '':
                    continue
                name = f'Root{connect.prefix_system}.{PICTUREs}{row.frame}.StatePicture'

                address = list_addrr['StatePicture'] + (row.id - 1)
                self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {PICTUREs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {PICTUREs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class VSMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['StateAuxSystem', 'StateAux2', 'numOfStart',
              'operatingTimeCurrentMonth',
              'operatingTimeLastMonth',
              'operatingTime']

    variable = ['StateAuxSystem', 'vs_numOfStart', 'vs_operatingTimeCurrentMonth',
                'vs_operatingTimeLastMonth', 'vs_operatingTime']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, VSs)

            data = self.gen_funct.select_orm(VS, None, VS.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {VSs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}.{VSs}VS_{row.id}.{self.prefix[i]}'

                    if 'StateAuxSystem' == self.prefix[i]:
                        address = list_addrr['StateAuxSystem'] + 3 * (row.id - 1)
                    elif 'StateAux2' == self.prefix[i]:
                        address = list_addrr['StateAuxSystem'] + 3 * (row.id - 1) + 1
                    elif 'numOfStart' == self.prefix[i]:
                        address = list_addrr['vs_numOfStart'] + 2 * (row.id - 1)
                    elif 'operatingTimeCurrentMonth' == self.prefix[i]:
                        address = list_addrr['vs_operatingTimeCurrentMonth'] + 2 * (row.id - 1)
                    elif 'operatingTimeLastMonth' == self.prefix[i]:
                        address = list_addrr['vs_operatingTimeLastMonth'] + 2 * (row.id - 1)
                    elif 'operatingTime' == self.prefix[i]:
                        address = list_addrr['vs_operatingTime'] + 2 * (row.id - 1)

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {VSs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {VSs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class ZDMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['StateValve1', 'StateValve2', 'StateValve3',
              'Tm.tmZD', 'NumOfOpenings', 'NumOfClosings']

    variable = ['StateZD', 'numOfOpenings', 'numOfClosings']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, ZDs)

            data = self.gen_funct.select_orm(ZD, None, ZD.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {ZDs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}.{ZDs}ZD_{row.id}.{self.prefix[i]}'

                    if 'StateValve1' == self.prefix[i]:
                        address = list_addrr['StateZD'] + 5 * (row.id - 1)
                    elif 'StateValve2' == self.prefix[i]:
                        address = (list_addrr['StateZD'] + 5 * (row.id - 1) + 1)
                    elif 'StateValve3' == self.prefix[i]:
                        address = (list_addrr['StateZD'] + 5 * (row.id - 1) + 2)
                    elif 'Tm.tmZD' == self.prefix[i]:
                        address = (list_addrr['StateZD'] + 5 * (row.id - 1) + 4)
                    elif 'NumOfOpenings' == self.prefix[i]:
                        address = list_addrr['numOfOpenings'] + 2 * (row.id - 1)
                    elif 'NumOfClosings' == self.prefix[i]:
                        address = list_addrr['numOfClosings'] + 2 * (row.id - 1)

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {ZDs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {ZDs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class PumpsMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['StateNA', 'StateNAEx', 'StateNAStatistic',
              'operatingTimeSinceSwitchingOn',
              'operatingTimeSinceSwitchingOnSet',
              'operatingTimeBeforeOverhaul',
              'operatingTimeBeforeOverhaulSet',
              'numOfStart', 'dateTimeOfStart',
              'dateTimeOfStop', 'operatingTimeCurrentMonth',
              'operatingTimeLastMonth', 'operatingTimeTO',
              'operatingTimeTO1', 'operatingTimeTOSet',
              'operatingTimeMidTO', 'operatingTimeMidTOSet',
              'operatingTimeThisKvart', 'operatingTimeLastKvart',
              'operatingTimeFromBegin', 'operatingTimeED',
              'operatingTimeEDSet', 'numOfStartSet',
              'time24hStart', 'timeFromHotStart',
              'numOfStarts24h', 'OperatingTimeState']

    variable = ['StateNA', 'operatingTimeSinceSwitchingOn',
                'operatingTimeSinceSwitchingOnSet',
                'operatingTimeBeforeOverhaul',
                'operatingTimeBeforeOverhaulSet', 'numOfStarts',
                'numOfStartsSet', 'dateTimeOfStart', 'dateTimeOfStop',
                'operatingTimeCurrentMonth', 'operatingTimeLastMonth',
                'operatingTimeTO', 'operatingTimeTO1',
                'operatingTimeTOSet', 'operatingTimeMidTO',
                'operatingTimeMidTOSet', 'operatingTimeThisKvart',
                'operatingTimeLastKvart', 'operatingTimeFromBegin',
                'operatingTimeED', 'operatingTimeEDSet', 'operatingTimeState']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, NAs)

            data = self.gen_funct.select_orm(UMPNA, None, UMPNA.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {NAs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}.{NAs}NA_{row.id}.{self.prefix[i]}'

                    if 'StateNA' == self.prefix[i]:
                        address = list_addrr['StateNA'] + 11 * (row.id - 1)
                    elif 'StateNAEx' == self.prefix[i]:
                        address = (list_addrr['StateNA'] + 11 * (row.id - 1) + 1)
                    elif 'StateNAStatistic' == self.prefix[i]:
                        address = (list_addrr['StateNA'] + 11 * (row.id - 1) + 2)
                    elif 'operatingTimeSinceSwitchingOn' == self.prefix[i]:
                        address = list_addrr['operatingTimeSinceSwitchingOn'] + 42 * (row.id - 1)
                    elif 'operatingTimeSinceSwitchingOnSet' == self.prefix[i]:
                        address = list_addrr['operatingTimeSinceSwitchingOnSet'] + 42 * (row.id - 1)
                    elif 'operatingTimeBeforeOverhaul' == self.prefix[i]:
                        address = list_addrr['operatingTimeBeforeOverhaul'] + 42 * (row.id - 1)
                    elif 'operatingTimeBeforeOverhaulSet' == self.prefix[i]:
                        address = list_addrr['operatingTimeBeforeOverhaulSet'] + 42 * (row.id - 1)
                    elif 'numOfStart' == self.prefix[i]:
                        address = list_addrr['numOfStarts'] + 42 * (row.id - 1)
                    elif 'numOfStartSet' == self.prefix[i]:
                        address = list_addrr['numOfStartsSet'] + 42 * (row.id - 1)
                    elif 'dateTimeOfStart' == self.prefix[i]:
                        address = list_addrr['dateTimeOfStart'] + 42 * (row.id - 1)
                    elif 'dateTimeOfStop' == self.prefix[i]:
                        address = list_addrr['dateTimeOfStop'] + 42 * (row.id - 1)
                    elif 'operatingTimeCurrentMonth' == self.prefix[i]:
                        address = list_addrr['operatingTimeCurrentMonth'] + 42 * (row.id - 1)
                    elif 'operatingTimeLastMonth' == self.prefix[i]:
                        address = list_addrr['operatingTimeLastMonth'] + 42 * (row.id - 1)
                    elif 'operatingTimeTO' == self.prefix[i]:
                        address = list_addrr['operatingTimeTO'] + 42 * (row.id - 1)
                    elif 'operatingTimeTO1' == self.prefix[i]:
                        address = list_addrr['operatingTimeTO1'] + 42 * (row.id - 1)
                    elif 'operatingTimeTOSet' == self.prefix[i]:
                        address = list_addrr['operatingTimeTOSet'] + 42 * (row.id - 1)
                    elif 'operatingTimeMidTO' == self.prefix[i]:
                        address = list_addrr['operatingTimeMidTO'] + 42 * (row.id - 1)
                    elif 'operatingTimeMidTOSet' == self.prefix[i]:
                        address = list_addrr['operatingTimeMidTOSet'] + 42 * (row.id - 1)
                    elif 'operatingTimeThisKvart' == self.prefix[i]:
                        address = list_addrr['operatingTimeThisKvart'] + 42 * (row.id - 1)
                    elif 'operatingTimeLastKvart' == self.prefix[i]:
                        address = list_addrr['operatingTimeLastKvart'] + 42 * (row.id - 1)
                    elif 'operatingTimeFromBegin' == self.prefix[i]:
                        address = list_addrr['operatingTimeFromBegin'] + 42 * (row.id - 1)
                    elif 'operatingTimeED' == self.prefix[i]:
                        address = list_addrr['operatingTimeED'] + 42 * (row.id - 1)
                    elif 'operatingTimeEDSet' == self.prefix[i]:
                        address = list_addrr['operatingTimeEDSet'] + 42 * (row.id - 1)
                    elif 'operatingTimeState' == self.prefix[i]:
                        address = list_addrr['operatingTimeState'] + 42 * (row.id - 1)
                    else:
                        continue

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {NAs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {NAs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class RelaytedSystemMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    variable = ['SS']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, SSs)

            data = self.gen_funct.select_orm(SS, None, SS.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {SSs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                name = f'Root{connect.prefix_system}.{SSs}SS_{row.id}.StateSS'

                address = list_addrr['SS'] + (row.id - 1)
                self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {SSs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {SSs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class UtsUptsMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    variable = ['StateUTS', 'StateUPTS']

    def system_selection(self, fl_upts):
        '''Выбор таблицы и подписей в зависимости от системы.'''
        self.model = UPTS if fl_upts else UTS
        self.prefix = self.variable[1] if fl_upts else self.variable[0]
        self.sign = UPTSs if fl_upts else UTS

    def work_file(self, fl_upts: bool = False):
        '''Запись в файл.'''
        msg = {}
        self.system_selection(fl_upts)
        try:
            root, tree, path = self.path_file(MODBUS, self.sign)
            list_addrr = self._read_address_mb()

            if not len(list_addrr):
                msg[f'{today} - DevStudio. Map. {self.sign} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            data = self.gen_funct.select_orm(self.model, None, self.model.id)

            for row in data:
                name = f'Root{connect.prefix_system}.{self.sign}{row.tag}.{self.prefix}'

                address = list_addrr[self.prefix] + (row.id - 1)
                self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {self.sign} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {self.sign} Ошибка {traceback.format_exc()}'] = 2
            return msg


class KTPRMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    variable = ['stateKTPRx']

    def system_selection(self, fl_ktprp):
        '''Выбор таблицы и подписей в зависимости от системы.'''
        self.model = KTPRP if fl_ktprp else KTPR

    def work_file(self, fl_ktprp: bool = False):
        '''Запись в файл.'''
        msg = {}
        self.system_selection(fl_ktprp)
        try:
            root, tree, path = self.path_file(MODBUS, KTPRs)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {KTPRs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            count_group = math.ceil(self.gen_funct.count_row_orm(self.model) / 4)
            for group in range(1, count_group + 1):
                name = f'Root{connect.prefix_system}.{KTPRs}Group_{group}.StateKTPRx'

                address = list_addrr['stateKTPRx'] + (group - 1)
                self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {KTPRs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {KTPRs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class KTPRAMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    variable = ['stateKTPRA']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, KTPRAs)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {KTPRAs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            count_na = self.gen_funct.non_repea_names(KTPRA, KTPRA.number_pump_VU, KTPRA.number_pump_VU)
            for na in count_na:
                max_row = self.gen_funct.max_value_column_cond('ktpra', 'id_num', 'number_pump_VU', na.number_pump_VU)
                count_group = math.ceil(max_row / 4)

                for grp in range(1, count_group + 1):
                    name = f'Root{connect.prefix_system}.{KTPRAs}KTPRAs_{na.number_pump_VU}.Group_{grp}.StateKTPRx'

                    address = list_addrr['stateKTPRA'] + (grp - 1) + (na.number_pump_VU - 1) * 48
                    self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {KTPRAs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {KTPRAs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class GMPNAMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    variable = ['stateGMPNA']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, GMPNAs)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {GMPNAs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            count_na = self.gen_funct.non_repea_names(GMPNA, GMPNA.number_pump_VU, GMPNA.number_pump_VU)
            for na in count_na:
                max_row = self.gen_funct.max_value_column_cond('gmpna', 'id_num', 'number_pump_VU', na.number_pump_VU)
                count_group = math.ceil(max_row / 4)

                for grp in range(1, count_group + 1):
                    name = f'Root{connect.prefix_system}.{GMPNAs}GMPNAs_{na.number_pump_VU}.Group_{grp}.StateGMPNA'

                    address = list_addrr['stateGMPNA'] + (grp - 1) + (na.number_pump_VU - 1) * count_group
                    self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {GMPNAs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {GMPNAs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class PIMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    variable = ['StatePI']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, PIs)

            data = self.gen_funct.select_orm(PI, None, PI.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {PIs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                name = f'Root{connect.prefix_system}.{PIs}{row.tag}.StatePI'

                address = list_addrr['StatePI'] + (row.id - 1)
                self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {PIs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {PIs} Ошибка {traceback.format_exc()}'] = 2
            return msg


class PZMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['StatePZ', 'exStatePZ', 'ReadyFlags', 'TimetoNextAttack', 'AttackCounter', 'TimetoEvacuation']

    variable = ['StatePZ']

    def work_file(self):
        '''Запись в файл.'''
        msg = {}
        try:
            root, tree, path = self.path_file(MODBUS, PZs)

            data = self.gen_funct.select_orm(PZ, None, PZ.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                msg[f'{today} - DevStudio. Map. {PZs} Отсутствует адрес из списка {self.variable}'] = 2
                return msg

            for row in data:
                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}.{PZs}PZ_{row.id}.{self.prefix[i]}'
                    address = list_addrr['StatePZ'] + i + (len(self.prefix) * (row.id - 1))

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            msg[f'{today} - DevStudio. Map. {PZs} Заполнено'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. {PZs} Ошибка {traceback.format_exc()}'] = 2
            return msg