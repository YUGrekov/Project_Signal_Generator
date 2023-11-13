import traceback
from model_new import AI
from model_new import DI
from model_new import USO as Model
from model_new import HardWare as HW
from request_sql import RequestSQL
from general_functions import General_functions

T_HW = 'hardware'
T_USO = 'uso'
T_AI = 'ai'
T_DI = 'di'
TYPE = 'USO'


class USO():
    '''Заполнение таблицы.'''
    def __init__(self, logtext):
        self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицы на наличие и заполненость.'''
        modules = [T_HW, T_AI, T_DI]
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

        result = self.request.check_table(T_USO)
        if not result:
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица uso
                                        отсутсвует''', 2)
            self.request.new_table_orm(Model)
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица uso
                                        добавлена''', 0)
        return True

    def add_process(self, data, column, modul, fl_all=False):
        if not len(data):
            return False

        count = 0
        for signal in data:
            if not fl_all:
                self.entry_array[column] = f'{modul}[{signal.id}]'
            else:
                count += 1
                self.entry_array[f'{column}{count}'] = f'{modul}[{signal.id}]'
        return True

    def ai_temp(self):
        '''Поиск температуры в шкафа.'''
        self.count_row += 1
        self.entry_array = {'id': f'{self.count_row}',
                            'variable': f'USO[{self.count_row}]',
                            'name': f'{self.uso.uso}'}

        temp = self.request.select_orm(AI,
                                       ((AI.name % (f'%{self.uso.uso}%')) &
                                        ((AI.tag % ('CST%')) | (AI.tag_eng % ('CST%')))),
                                       AI.name)
        if not self.add_process(temp, 'temperature', 'AI'):
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. {self.uso.uso} -
                                       Температура не найдена''', 2)

    def di_door(self):
        '''Поиск сигнала дверь шкафа открыта.'''
        door = self.request.select_orm(DI,
                                       ((DI.name % (f'%{self.uso.uso}%')) &
                                        ((DI.name % ('%двер%')) | (DI.name % ('%Двер%'))) &
                                        ((DI.tag % ('CSC%')) | (DI.tag_eng % ('CSC%')))),
                                       DI.name)
        if not self.add_process(door, 'door', 'DI'):
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. {self.uso.uso} -
                                       Сигнал "Двери открыты"
                                       не найдено''', 2)

    def di_all(self):
        '''Поиск остальных сигналов диагностики шкафа.'''
        all_di = self.request.select_orm(DI,
                                         ((DI.name % (f'%{self.uso.uso}%')) &
                                          (~((DI.name % ('%двер%')) | (DI.name % ('%Двер%')))) &
                                          ((DI.tag % ('CSC%')) | (DI.tag_eng % ('CSC%')))),
                                         DI.name)
        if not self.add_process(all_di, 'signal_', 'DI', True):
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. {self.uso.uso} -
                                       Сигналы диагностики
                                       шкафа не найдены''', 2)

    def entry_to_base(self):
        '''Добавление нового сигнала.'''
        self.request.write_base_orm(self.entry_array, Model)
        self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Добавлен
                                   новый сигнал: {self.count_row}''', 0)

    def add_uso(self):
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise
            # перед заполнением таблица должна быть пуста
            if self.request.count_row_orm(Model) > 0:
                self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица заполнена.
                                           Перед заполнением необходимо
                                           очистить таблицу''', 2)
                raise
            data_uso = self.request.non_repea_names(HW, HW.uso, HW.uso)
            self.count_row = 0

            for self.uso in data_uso:
                # Температура шкафа
                self.ai_temp()
                # Двери открыты
                self.di_door()
                # Остальные сигналы
                self.di_all()
                self.entry_to_base()
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Работа
                                       с таблицей завершена''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Ошибка
                                       {traceback.format_exc()}''', 2)