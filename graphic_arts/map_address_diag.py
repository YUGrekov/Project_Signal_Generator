import traceback
from map_address import BaseMap
from model_new import connect
from model_new import HardWare


MODBUS = 'ModBus.xml'
RACKSTATE = '.Diag.RackStates.'


class AttribAI():
    '''Атрибуты для заполнения карты адресов модуля AI.'''
    prefix = ['mod_State', 'ch_01', 'ch_02', 'ch_03', 'ch_04', 'ch_05', 'ch_06', 'ch_07', 'ch_08']
    variable = ['diagAI8']
    sign = '.Diag.AIs.'
    design_modul = 'MK-516-008A'
    shift_two = []


class AttribAO():
    '''Атрибуты для заполнения карты адресов модуля AO.'''
    prefix = ['mod_State', 'chHealth', 'ch_01', 'ch_02', 'ch_03', 'ch_04', 'ch_05', 'ch_06', 'ch_07', 'ch_08']
    variable = ['diagAO']
    sign = '.Diag.AOs.'
    design_modul = 'MK-514-008'
    shift_two = []


class AttribDI():
    '''Атрибуты для заполнения карты адресов модуля DI.'''
    prefix = ['mod_State', 'mDI']
    variable = ['diagDI']
    sign = '.Diag.DIs.'
    design_modul = 'MK-521-032'
    shift_two = ['mod_State', 'mDI']


class AttribDO():
    '''Атрибуты для заполнения карты адресов модуля DO.'''
    prefix = ['mod_State', 'mDI']
    variable = ['diagDO']
    sign = '.Diag.DOs.'
    design_modul = 'MK-531-032'
    shift_two = ['mod_State', 'mDI']


class AttribRS():
    '''Атрибуты для заполнения карты адресов модуля RS.'''
    prefix = ['mod_State', 'mod_State_ext']
    variable = ['diagRS']
    sign = '.Diag.RSs.'
    design_modul = 'MK-541-002'
    shift_two = []


class AttribCPU():
    '''Атрибуты для заполнения карты адресов модуля CPU.'''
    prefix = ['mod_State', 'mod_State_ext', 'mod_State_Err',
              'CPUMemFree', 'CPULoad', 'ClcCurr', 'ClcMax', 'RsrCRC32']
    variable = ['diagCPU']
    sign = '.Diag.CPUs.'
    design_modul = 'MK-504-120'
    shift_two = ['CPULoad', 'RsrCRC32', 'ClcCurr', 'ClcMax']


class AttribPSU():
    '''Атрибуты для заполнения карты адресов модуля PSU.'''
    prefix = ['mod_State', 'mod_State_ext', 'SupplyVoltage',
              'CanBusSpeed', 'Can1ErrorCounter', 'Can2ErrorCounter']
    variable = ['diagCPU']
    sign = '.Diag.PSUs.'
    design_modul = 'MK-550-024'
    shift_two = ['SupplyVoltage', 'Can2ErrorCounter']


class AttribCN():
    '''Атрибуты для заполнения карты адресов модуля CN.'''
    prefix = ['mod_State', 'mod_State_ext', 'ports_State', 'pwl_ID']
    variable = ['diagCN']
    sign = '.Diag.CNs.'
    design_modul = 'MK-545-010'
    shift_two = []


class AttribMN():
    '''Атрибуты для заполнения карты адресов модуля MN.'''
    prefix = ['mod_State_ext', 'ports_State']
    variable = ['diagMN']
    sign = '.Diag.MNs.'
    design_modul = 'MK-546-010'
    shift_two = []


class ChoiceType():
    '''Выбор нужного типа модуля.'''
    relation = {'AI': AttribAI,
                'AO': AttribAO,
                'DI': AttribDI,
                'DO': AttribDO,
                'RS': AttribRS,
                'CPU': AttribCPU,
                'PSU': AttribPSU,
                'MN': AttribMN,
                'CN': AttribCN}


class DiagMap(BaseMap, ChoiceType):
    '''Заполнение ModBus карты адресов.'''
    def choice_param(self, type_module):
        '''Выбор базового класса с параметрами.'''
        for used_type, used_cls in self.relation.items():
            if used_type in type_module:
                return used_cls

    def work_file(self, type_module: str):
        '''Запись в файл.'''
        param_m = self.choice_param(type_module)
        self.variable = param_m.variable
        try:
            root, tree, path = self.path_file(MODBUS, param_m.sign)
            list_addrr = self._read_address_mb()
            array_modul = self.get_modul(param_m.design_modul)

            if len(list_addrr) != len(self.variable):
                # self.logsTextEdit.logs_msg(f'''DevStudio. Map {param_m.sign} Ошибка отсутствует
                #                            адрес из списка {self.variable}''', 2)
                raise

            counter = list_addrr[param_m.variable[0]]
            for data in array_modul:
                for i in range(len(param_m.prefix)):
                    name = f'Root{connect.prefix_system}{param_m.sign}{data["string_name"]}.{param_m.prefix[i]}'
                    address = counter
                    # Сдвиг по адресам, если необходимо
                    counter = counter + 2 if param_m.prefix[i] in param_m.shift_two else counter + 1

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {param_m.sign} Заполнено''', 1)
        except Exception:
            print(traceback.format_exc())
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {param_m.sign} Ошибка {traceback.format_exc()}''', 2)


class RackStateMap(BaseMap):
    '''Заполнение ModBus карты адресов.'''
    prefix = ['mBUS', 'mBUSandCh', 'mBUSblink']

    variable = ['mBUS', 'mBUSandCh', 'mBUSblink']

    def _work_file(self):
        '''Запись в файл.'''
        try:
            root, tree, path = self.path_file(MODBUS, RACKSTATE)

            data = self.request.select_orm(HardWare, None, HardWare.id)
            list_addrr = self._read_address_mb()

            if len(list_addrr) != len(self.variable):
                # self.logsTextEdit.logs_msg(f'''DevStudio. Map {RACKSTATE} Ошибка
                #                            отсутствует адрес из списка
                #                            {self.variable}''', 2)
                print(f'''DevStudio. Map {RACKSTATE}
                      Отсутствует адрес из списка
                      {self.variable}''')
                raise

            for row in data:
                for i in range(len(self.prefix)):
                    name = f'Root{connect.prefix_system}{RACKSTATE}rack_{row.id}.{self.prefix[i]}'

                    if 'mBUS' == self.prefix[i]:
                        address = list_addrr['mBUS'] + 2 * (row.id - 1)
                    elif 'mBUSandCh' == self.prefix[i]:
                        address = list_addrr['mBUSandCh'] + 2 * (row.id - 1)
                    elif 'mBUSblink' == self.prefix[i]:
                        address = list_addrr['mBUSblink'] + 2 * (row.id - 1)

                    self.new_element(root, name, address)
            tree.write(path, pretty_print=True)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {RACKSTATE} Заполнено''', 1)
        except Exception:
            print(1)
            # self.logsTextEdit.logs_msg(f'''DevStudio. Map {RACKSTATE} Ошибка
            #                            {traceback.format_exc()}''', 2)