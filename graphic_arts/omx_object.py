import traceback
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
    def __init__(self) -> None:
        # self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def path_file(self, text, fl_diag: bool = False):
        '''Формирование пути до файла и очистка перед заполнением.'''
        path_attr = f'Root{tx.prefix_system}'

        root, tree = self.dop_function.xmlParser(tx.path_to_devstudio_omx)
        self.dop_function.clear_omx(path_attr, text, root, fl_diag)

        tree.write(tx.path_to_devstudio_omx, pretty_print=True)
        return root, tree


class Analogs(BaseMethod):
    '''Заполнение объектов файла omx DevStudio.'''
    def write_omx(self):
        try:
            root, tree = self.path_file(ANALOGs)

            data = self.request.select_orm(AI, None, AI.id)

            for row in data:
                row.AnalogGroupId

            # tree.write(tx.path_to_devstudio_omx, pretty_print=True)
            self.logsTextEdit.logs_msg(f'''DevStudio. Map. {ANALOGs} Заполнено''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''DevStudio. Map. {ANALOGs} Ошибка {traceback.format_exc()}''', 2)


a = Analogs()
a.write_omx()