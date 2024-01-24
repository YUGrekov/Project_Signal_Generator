"""Генерация древа для поиска сигналов."""
import traceback
from main_base import General_functions
from models import connect
from models import Signals
from models import USO
from datetime import datetime
today = datetime.now()

NAME_FILE = 'AlphaSearch.xml'
CONST_SCRIPT = ('CREATE SCHEMA IF NOT EXISTS signals;\n'
                'CREATE TABLE IF NOT EXISTS signals.allsignals(\n'
                '\ttag VARCHAR(32),           \n'
                '\tdescription VARCHAR(1024), \n'
                '\tklk VARCHAR(32),           \n'
                '\tkont VARCHAR(32),          \n'
                '\tinitpath VARCHAR(1024),    \n'
                '\tposition VARCHAR(32),      \n'
                '\tcabinet VARCHAR(32),       \n'
                '\track VARCHAR(32),          \n'
                '\tmodule VARCHAR(32)         \n'
                ');\n'
                'DELETE FROM signals.allsignals ;\n')


class SearchSignal():
    def __init__(self):
        self.dop_function = General_functions()

    def check_none(self, value):
        '''Проверка пустой ячейки.'''
        return '' if value is None else value

    def array_uso(self):
        '''Список имен шкафа.'''
        data = self.dop_function.select_orm(USO, None, USO.id)
        name_uso = {}
        for uso in data:
            name_uso[uso.name] = uso.tag
        return name_uso

    def fill_search_signal(self):
        msg = {}
        path_file = f'{connect.path_file_txt}\\{NAME_FILE}'

        try:
            # Проверка файла txt на существование
            open_file = self.dop_function.check_file_txt(path_file)
            # Запись шапки
            open_file.write(CONST_SCRIPT)
            # Массив данных таблицы signals
            data = self.dop_function.select_orm(Signals, None, Signals.id)

            # Список имен шкафа
            name_uso = self.array_uso()

            for row in data:
                if row.tag is None:
                    continue

                klk = self.check_none(row.klk)
                contact = self.check_none(row.contact)
                tag = self.dop_function.translate(row.tag)

                module = f'0{row.module}' if row.module < 10 else row.module
                initPath = f'Diag.{row.type_signal}s.{name_uso[row.uso]}_A{row.basket}_{module}'

                sql_request = f"INSERT INTO signals.allsignals VALUES('" \
                              f"{tag}','{row.description}','{klk}','{contact}','{initPath}','" \
                              f"{row.channel}','{row.uso}','{row.basket}','{row.module}');\n"
                open_file.write(sql_request)
            open_file.close()

            msg[f'{today} - ВУ. Скрипт поиска сигналов собран'] = 1
            return msg
        except Exception:
            msg[f'{today} - ВУ. Скрипт поиска сигналов. Ошибка {traceback.format_exc()}'] = 2
            return msg