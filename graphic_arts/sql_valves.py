import traceback
import re
from model_new import DI
from model_new import DO
from model_new import ZD as Model
from request_sql import RequestSQL
from general_functions import General_functions

T_DI = 'di'
T_DO = 'do'
T_ZD = 'zd'
TYPE = 'ZD'


class ZD():
    '''Заполнение таблицы.'''
    def __init__(self):
        # self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицы на наличие и заполненость.'''
        modules = [T_DI, T_DO]
        for modul in modules:
            result = self.request.check_table(modul)
            if not result:
                self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица
                                           {modul} отсутсвует''', 2)
                return False
            else:
                if not self.request.check_row_table(modul):
                    self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица
                                               {modul} пустая. Заполни!''', 2)
                    return False

        result = self.request.check_table(T_ZD)
        if not result:
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица zd
                                        отсутсвует''', 2)
            self.request.new_table_orm(Model)
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица zd
                                        добавлена''', 0)
        return True

    def new_list_valves(self):
        '''Состовляем новый список задвижек.'''
        new_zd = []
        where = (DI.name % ('%задвижк%') | DI.name % ('%Задвижк%') |
                 DI.name % ('%клап%') | DI.name % ('%Клап%') |
                 DI.name % ('%клоп%') | DI.name % ('%Клоп%') |
                 DI.name % ('%кран шар%') | DI.name % ('%Кран шар%'))

        list_zd = self.request.select_orm(DI, where, DI.name)
        for zd in list_zd:
            valves = zd.name.split(' - ')[0]
            valves = re.sub(r'(Открыт)|(открыт)|(Закрыт)|(закрыт)', '', valves)
            if 'продувк' not in valves:
                valves = re.sub(r'( Клапан)|( клапан)|(. Клапан)', '', valves)
            new_zd.append(valves)
        for i in sorted(set(new_zd)):
            print(i)

    def entry_to_base(self):
        '''Добавление нового сигнала.'''
        self.request.write_base_orm(self.entry_array, Model)
        self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Добавлен
                                   новый сигнал: {self.count_row}''', 0)

    def add_valves(self):
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise

            old_zd = self.request.non_repea_names(Model, Model.name,
                                                  Model.name)
            self.count_row = len(old_zd)

            self.new_list_valves()

            # for self.uso in data_zd:
            #     # Температура шкафа
            #     self.ai_temp()
            #     # Двери открыты
            #     self.di_door()l
            #     # Остальные сигналы
            #     self.di_all()
            #     self.entry_to_base()

            # self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Работа
            #                            с таблицей завершена''', 1)
            print(f'''SQL. {TYPE}. Работа с таблицей завершена''')
        except Exception:
            print(traceback.format_exc())
            # self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Ошибка
            #                            {traceback.format_exc()}''', 2)


a = ZD()
a.add_valves()