'''Заполнение готовностей PZ в файл AttributesMapDescription.'''
from datetime import datetime
from models import PZ
from main_base import General_functions
from models import connect
import traceback
today = datetime.now()

PATH = f'{connect.path_to_devstudio}\\AttributesMapDescription.xml'


class ReadyMap():
    def __init__(self):
        self.dop_function = General_functions()

    def fill_map_ready(self):
        msg = {}

        root, tree = self.dop_function.xmlParser(PATH)
        self.dop_function.clear_map_attrib(root, '.PZs.')

        data = self.dop_function.select_orm(PZ, None, PZ.id)

        try:
            for zone in data:
                for i in range(1, 16):
                    value = eval(f'zone.g_{i}')
                    value = ' ' if value is None else value
                    name = f'Root{connect.prefix_system}.PZs.PZ_{zone.id}.s_ReadyFlags.Ready{i}'

                    self.dop_function.map_new_attrib(root, name, value)

            tree.write(PATH, pretty_print=True, encoding='utf-8')
            msg[f'{today} - DevStudio. Map. PZs AttributesMapDescription заполнен'] = 1
            return msg
        except Exception:
            msg[f'{today} - DevStudio. Map. PZs AttributesMapDescription ошибка {traceback.format_exc()}'] = 2
            return msg