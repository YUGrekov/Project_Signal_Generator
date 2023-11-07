import re
import traceback
from model_new import DI
from model_new import Signals
from request_sql import RequestSQL
from general_functions import General_functions

T_SIGNALS = 'signals'
T_HW = 'hardware'


class Diskrets():
    '''Заполнение таблицы.'''

    def __init__(self) -> None:
        # self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицу signals на наличие и заполненость.'''
        result = self.request.check_table(T_SIGNALS)
        if not result:
            print('''SQL. AI. Таблица signals отсутсвует или не заполнена''')
            # self.logsTextEdit.logs_msg('''SQL. DI. Таблица
            #                            signals отсутсвует
            #                            или не заполнена''', 2)
            return False
        return True

    def add_diskrets(self):
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise

            data = self.request.select_orm(Signals,
                                           (Signals.type_signal.contains('DI')) |
                                           (Signals.schema.contains('DI')),
                                           Signals.description)
            for signal in data:
                pass

            print('SQL. AI. Работа с таблицей завершена')
            # self.logsTextEdit.logs_msg('''SQL. DI. Работа
            #                            с таблицей завершена''', 1)
        except Exception:
            print({traceback.format_exc()})
            # self.logsTextEdit.logs_msg(f'''SQL. DI. Ошибка
            #                            {traceback.format_exc()}''', 2)