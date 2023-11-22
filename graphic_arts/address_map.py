import traceback
from lxml import etree
from request_sql import RequestSQL
from general_functions import General_functions
from model_new import connect
from model_new import AI
from model_new import DI
from model_new import PIC
from model_new import VS
from model_new import ZD
from model_new import UMPNA
from model_new import Modbus


MODBUS_503 = 'ModBus503.xml'
MODBUS = 'ModBus.xml'
ANALOGs = '.Analogs.'
DISCRETs = '.Diskrets.'
PICTUREs = '.Pictures.'
VSs = '.AuxSystems.'
ZDs = '.Valves.'
NAs = '.NAs.'


class BaseMap():
    '''Базовые методы заполнения.'''
    def __init__(self) -> None:
        self.request = RequestSQL()
        self.gen_funct = General_functions()

    def path_file(self, p_file: str, section: str):
        '''Формирование пути до файла и очистка перед заполнением.'''
        path = f'{connect.path_to_devstudio}\{p_file}'
        root, tree = self.gen_funct.xmlParser(path)
        self.search_clear_section(root, section)
        return root, tree, path

    def search_clear_section(self, root, section: str):
        '''Поиск раздела для парсинга карты адресов.'''
        for item in root.iter('node-path'):
            signal = f'Root{connect.prefix_system}{section}'

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


class AnalogsMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['AIVisualValue', 'AIElValue',
              'AIValue', 'AIRealValue',
              'StateAI', 'Range_Bottom', 'Range_Top']

    def _read_address_mb(self):
        '''Чтение адресов ModBus из базы.'''
        modbus = self.request.select_orm(Modbus, None, Modbus.id)
        for row in modbus:
            if 'AIVisualValue' in str(row.variable):
                AIVV = row.start_address
            if 'AIElValue' in str(row.variable):
                AIElV = row.start_address
            if 'AIValue' in str(row.variable):
                AIV = row.start_address
            if 'AIRealValue' in str(row.variable):
                AIRV = row.start_address
            if 'StateAI' in str(row.variable):
                StateAI = row.start_address
            if 'AIParam' in str(row.variable):
                AIP = row.start_address

        return [AIVV, AIElV, AIV, AIRV, StateAI, AIP]

    def _work_file(self):
        '''Запись в файл.'''
        root, tree, path = self.path_file(MODBUS_503, ANALOGs)

        data = self.request.select_orm(AI, None, AI.id)
        list_addrr = self._read_address_mb()

        for row in data:
            for i in range(len(self.prefix)):
                name = f'Root{connect.prefix_system}{ANALOGs}{row.tag_eng}.{self.prefix[i]}'
                # Для уровней другой набор префиксов
                if 'Уровни' in str(row.AnalogGroupId):
                    if i > 4:
                        break

                if 'AIVisualValue' in self.prefix[i]:
                    address = list_addrr[0] + 2 * (row.id - 1)
                elif 'AIElValue' in self.prefix[i]:
                    address = list_addrr[1] + (row.id - 1)
                elif 'AIValue' in self.prefix[i]:
                    address = list_addrr[2] + 2 * (row.id - 1)
                elif 'AIRealValue' in self.prefix[i]:
                    address = list_addrr[3] + 2 * (row.id - 1)
                elif 'StateAI' in self.prefix[i]:
                    address = list_addrr[4] + 2 * (row.id - 1)
                elif 'Range_Bottom' in self.prefix[i]:
                    address = list_addrr[5] + 4 + 46 * (row.id - 1)
                elif 'Range_Top' in self.prefix[i]:
                    address = list_addrr[5] + 2 + 46 * (row.id - 1)

                self.new_element(root, name, address)
        tree.write(path, pretty_print=True)


class DiskretsMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    def _read_address_mb(self):
        '''Чтение адресов ModBus из базы.'''
        modbus = self.request.select_orm(Modbus, None, Modbus.id)
        for row in modbus:
            if 'StateDI' in str(row.variable):
                return row.start_address

    def _work_file(self):
        '''Запись в файл.'''
        try:
            root, tree, path = self.path_file(MODBUS, DISCRETs)

            data = self.request.select_orm(DI, None, DI.id)
            list_addrr = self._read_address_mb()

            for row in data:
                name = f'Root{connect.prefix_system}{DISCRETs}{row.tag_eng}.StateDI'

                address = list_addrr + (row.id - 1)
                self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {DISCRETs}
            #                            Заполнено''', 1)
        except Exception:
            print(1)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {DISCRETs} Ошибка
            #                            {traceback.format_exc()}''', 2)


class PicturesMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    def _read_address_mb(self):
        '''Чтение адресов ModBus из базы.'''
        modbus = self.request.select_orm(Modbus, None, Modbus.id)
        for row in modbus:
            if 'StatePicture' in str(row.variable):
                return row.start_address

    def _work_file(self):
        '''Запись в файл.'''
        try:
            root, tree, path = self.path_file(MODBUS, PICTUREs)

            data = self.request.select_orm(PIC, None, PIC.id)
            list_addrr = self._read_address_mb()

            for row in data:
                if row.frame is None or row.frame == '':
                    continue
                name = f'Root{connect.prefix_system}{PICTUREs}{row.frame}.StatePicture'

                address = list_addrr + (row.id - 1)
                self.new_element(root, name, address)

            tree.write(path, pretty_print=True)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {PICTUREs} Заполнено''', 1)
        except Exception:
            print(1)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {PICTUREs} Ошибка
            #                            {traceback.format_exc()}''', 2)


class VSMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['StateAuxSystem', 'numOfStart',
              'operatingTimeCurrentMonth',
              'operatingTimeLastMonth',
              'operatingTime']

    def _read_address_mb(self):
        '''Чтение адресов ModBus из базы.'''
        modbus = self.request.select_orm(Modbus, None, Modbus.id)
        for row in modbus:
            if 'StateAuxSystem' in str(row.variable):
                stateVS = row.start_address
            if 'vs_numOfStart' in str(row.variable):
                numOfStart = row.start_address
            if 'vs_operatingTimeCurrentMonth' in str(row.variable):
                operTCM = row.start_address
            if 'vs_operatingTimeLastMonth' in str(row.variable):
                operTLM = row.start_address
            if 'vs_operatingTime' in str(row.variable):
                operTime = row.start_address

        return [stateVS, numOfStart, operTCM, operTLM, operTime]

    def _work_file(self):
        '''Запись в файл.'''
        try:
            root, tree, path = self.path_file(MODBUS, VSs)

            data = self.request.select_orm(VS, None, VS.id)
            list_addrr = self._read_address_mb()

            for row in data:
                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}{VSs}VS_{row.id}.{self.prefix[i]}'

                    if 'StateAuxSystem' in self.prefix[i]:
                        address = list_addrr[0] + 3 * (row.id - 1)
                    elif 'numOfStart' in self.prefix[i]:
                        address = list_addrr[1] + 2 * (row.id - 1)
                    elif 'operatingTimeCurrentMonth' in self.prefix[i]:
                        address = list_addrr[2] + 2 * (row.id - 1)
                    elif 'operatingTimeLastMonth' in self.prefix[i]:
                        address = list_addrr[3] + 2 * (row.id - 1)
                    elif 'operatingTime' in self.prefix[i]:
                        address = list_addrr[4] + 2 * (row.id - 1)

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {VSs} Заполнено''', 1)
        except Exception:
            print(1)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {VSs} Ошибка
            #                            {traceback.format_exc()}''', 2)


class ZDMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['StateValve1', 'StateValve2',
              'StateValve3', 'Tm.tmZD',
              'NumOfOpenings', 'NumOfClosings']

    def _read_address_mb(self):
        '''Чтение адресов ModBus из базы.'''
        modbus = self.request.select_orm(Modbus, None, Modbus.id)
        for row in modbus:
            if 'StateZD' in str(row.variable):
                state = row.start_address
            if 'numOfOpenings' in str(row.variable):
                n_of_open = row.start_address
            if 'numOfClosings' in str(row.variable):
                n_of_close = row.start_address

        return [state, n_of_open, n_of_close]

    def _work_file(self):
        '''Запись в файл.'''
        try:
            root, tree, path = self.path_file(MODBUS, ZDs)

            data = self.request.select_orm(ZD, None, ZD.id)
            list_addrr = self._read_address_mb()

            for row in data:
                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}{ZDs}ZD_{row.id}.{self.prefix[i]}'

                    if 'StateValve1' in self.prefix[i]:
                        address = list_addrr[0] + 5 * (row.id - 1)
                    elif 'StateValve2' in self.prefix[i]:
                        address = (list_addrr[0] + 5 * (row.id - 1) + 1)
                    elif 'StateValve3' in self.prefix[i]:
                        address = (list_addrr[0] + 5 * (row.id - 1) + 2)
                    elif 'Tm.tmZD' in self.prefix[i]:
                        address = (list_addrr[0] + 5 * (row.id - 1) + 4)
                    elif 'NumOfOpenings' in self.prefix[i]:
                        address = list_addrr[1] + 2 * (row.id - 1)
                    elif 'NumOfClosings' in self.prefix[i]:
                        address = list_addrr[2] + 2 * (row.id - 1)

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {ZDs} Заполнено''', 1)
        except Exception:
            print(1)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {ZDs} Ошибка
            #                            {traceback.format_exc()}''', 2)


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

    def _read_address_mb(self):
        '''Чтение адресов ModBus из базы.'''
        modbus = self.request.select_orm(Modbus, None, Modbus.id)
        start_addrr = {}
        for row in modbus:

            for var in self.variable:

                if var == str(row.variable):
                    start_addrr[var] = row.start_address
                    break

        return start_addrr

    def _work_file(self):
        '''Запись в файл.'''
        try:
            root, tree, path = self.path_file(MODBUS, NAs)

            data = self.request.select_orm(UMPNA, None, UMPNA.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                # self.logsTextEdit.logs_msg(f'''DevStudio. Map {NAs} Ошибка
                #                            отсутствует адрес из списка
                #                            {self.variable}''', 2)
                print(f'''DevStudio. Map {NAs}
                      Отсутствует адрес из списка
                      {self.variable}''')
                raise

            for row in data:
                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}{NAs}NA_{row.id}.{self.prefix[i]}'

                    if 'StateNA' in self.prefix[i]:
                        address = list_addrr['StateNA'] + 11 * (row.id - 1)
                    elif 'StateNAEx' in self.prefix[i]:
                        address = (list_addrr['StateNA'] + 11 * (row.id - 1) + 1)
                    elif 'StateNAStatistic' in self.prefix[i]:
                        address = (list_addrr['StateNA'] + 11 * (row.id - 1) + 2)
                    elif 'operatingTimeSinceSwitchingOn' in self.prefix[i]:
                        address = list_addrr['operatingTimeSinceSwitchingOn'] + 42 * (row.id - 1)
                    elif 'operatingTimeSinceSwitchingOnSet' in self.prefix[i]:
                        address = list_addrr['operatingTimeSinceSwitchingOnSet'] + 42 * (row.id - 1)
                    elif 'operatingTimeBeforeOverhaul' in self.prefix[i]:
                        address = list_addrr['operatingTimeBeforeOverhaul'] + 42 * (row.id - 1)
                    elif 'operatingTimeBeforeOverhaulSet' in self.prefix[i]:
                        address = list_addrr['operatingTimeBeforeOverhaulSet'] + 42 * (row.id - 1)
                    elif 'numOfStart' in self.prefix[i]:
                        address = list_addrr['numOfStart'] + 42 * (row.id - 1)
                    elif 'numOfStartSet' in self.prefix[i]:
                        address = list_addrr['numOfStartSet'] + 42 * (row.id - 1)
                    elif 'dateTimeOfStart' in self.prefix[i]:
                        address = list_addrr['dateTimeOfStart'] + 42 * (row.id - 1)
                    elif 'dateTimeOfStop' in self.prefix[i]:
                        address = list_addrr['dateTimeOfStop'] + 42 * (row.id - 1)
                    elif 'operatingTimeCurrentMonth' in self.prefix[i]:
                        address = list_addrr['operatingTimeCurrentMonth'] + 42 * (row.id - 1)
                    elif 'operatingTimeLastMonth' in self.prefix[i]:
                        address = list_addrr['operatingTimeLastMonth'] + 42 * (row.id - 1)
                    elif 'operatingTimeTO' in self.prefix[i]:
                        address = list_addrr['operatingTimeTO'] + 42 * (row.id - 1)
                    elif 'operatingTimeTO1' in self.prefix[i]:
                        address = list_addrr['operatingTimeTO1'] + 42 * (row.id - 1)
                    elif 'operatingTimeTOSet' in self.prefix[i]:
                        address = list_addrr['operatingTimeTOSet'] + 42 * (row.id - 1)
                    elif 'operatingTimeMidTO' in self.prefix[i]:
                        address = list_addrr['operatingTimeMidTO'] + 42 * (row.id - 1)
                    elif 'operatingTimeMidTOSet' in self.prefix[i]:
                        address = list_addrr['operatingTimeMidTOSet'] + 42 * (row.id - 1)
                    elif 'operatingTimeThisKvart' in self.prefix[i]:
                        address = list_addrr['operatingTimeThisKvart'] + 42 * (row.id - 1)
                    elif 'operatingTimeLastKvart' in self.prefix[i]:
                        address = list_addrr['operatingTimeLastKvart'] + 42 * (row.id - 1)
                    elif 'operatingTimeFromBegin' in self.prefix[i]:
                        address = list_addrr['operatingTimeFromBegin'] + 42 * (row.id - 1)
                    elif 'operatingTimeED' in self.prefix[i]:
                        address = list_addrr['operatingTimeED'] + 42 * (row.id - 1)
                    elif 'operatingTimeEDSet' in self.prefix[i]:
                        address = list_addrr['operatingTimeEDSet'] + 42 * (row.id - 1)
                    elif 'OperatingTimeState' in self.prefix[i]:
                        address = list_addrr['OperatingTimeState'] + 42 * (row.id - 1)

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {NAs} Заполнено''', 1)
        except Exception:
            print(1)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {NAs} Ошибка
            #                            {traceback.format_exc()}''', 2)


a = PumpsMap()
a._work_file()