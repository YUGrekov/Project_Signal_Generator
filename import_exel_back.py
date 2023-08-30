import openpyxl as wb
from models import db
from models import connect
from models import Signals
from datetime import datetime
from enum import Enum
import traceback

SHIFT = 1
LIST_MODULE = ['CPU', 'PSU', 'CN', 'MN', 'AI', 'AO', 'DI', 'RS', 'DO']

today = datetime.now()


class NameColumn(Enum):
    '''Перечисление статических столбцов таблицы.'''
    ID = 'id'
    TYPE_SIGNAL = 'type_signal'
    TAG = 'tag'
    NAME = 'description'
    SCHEMA = 'schema'
    KLK = 'klk'
    CONTACT = 'contact'
    BASKET = 'basket'
    MODULE = 'module'
    CHANNEL = 'channel'


class DataExel():
    '''Инициализация файла Exel и его таблиц.
    выдача массива для записи в базу SQL'''
    def __init__(self, exel: str):
        self.exel = exel
        self.connect = wb.load_workbook(self.exel,
                                        read_only=True,
                                        data_only=True)

    def read_table(self) -> list:
        '''Список таблиц Exel.'''
        return [sheet.title for sheet in self.connect.worksheets]

    def max_column(self, uso: str):
        """Читаем выбранную таблицу и получаем макс-ное кол-во столбцов.

        Args:
            uso (str): название шкафа
        """
        self.sheet = self.connect[uso]
        return self.sheet.max_column

    def read_sheet(self, row: int, column: int) -> str:
        '''Чтение ячейки таблицы Exel.'''
        return self.sheet.cell(row=row + 1, column=column + 1).value

    def read_hat_table(self, uso: str, number_row: int,
                       is_tuple: bool,
                       select_column: tuple = None) -> dict | tuple:
        """Список с названиями столбцов.

        Args:
            uso (str): название шкафа
            number_row (int): номер строки с с названиями столбцов
            is_tuple (bool): флаг использования массива tuple
            select_column (tuple, optional): выбранные столбцы с
                                            номерами позиций.

        Returns:
            dict|tuple: либо то либо то
        """
        column = self.max_column(uso)

        if is_tuple:
            hat_tabl = {}
        else:
            hat_tabl = []

        for i in range(int(number_row), int(number_row) + SHIFT):
            for j in range(1, column + SHIFT):
                cell = self.read_sheet(i, j)
                if cell is None:
                    continue

                if is_tuple:
                    for key, value in select_column.items():
                        if value == cell:
                            hat_tabl[key] = j - SHIFT
                else:
                    hat_tabl.append(cell)

        return hat_tabl

    def database_count_row(self):
        '''Вычисляем кол-во строк в таблице Signals в базе SQL.
        Для дальнейшего добавления сигналов в конец таблицы'''
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT COUNT(*) FROM signals''')
            count_row = cursor.fetchall()[0][0]
        except Exception:
            count_row = 0
        return count_row

    def search_type(self, scheme, type_signal):
        '''Дополнительная проверка на тип сигнала.'''
        for value in LIST_MODULE:
            if str(scheme).find(value) != -1:
                type_signal = value
                return type_signal
        return type_signal

    def preparation_import(self, uso: str, number_row: int,
                           select_col: tuple) -> list:
        '''Подготовка таблицы к импорту.'''
        data = []

        count_row = self.database_count_row()

        for row in self.sheet.iter_rows(min_row=(int(number_row) + 1)):

            type_s = row[select_col[NameColumn.TYPE_SIGNAL.value]].value
            schema = row[select_col[NameColumn.SCHEMA.value]].value
            basket = row[select_col[NameColumn.BASKET.value]].value
            module = row[select_col[NameColumn.MODULE.value]].value
            channel = row[select_col[NameColumn.CHANNEL.value]].value

            if (basket or module or channel) is None:
                continue
            count_row += 1

            type_s = self.search_type(schema, type_s)

            data.append(dict(id=count_row,
                             type_signal=type_s,
                             uso=uso,
                             tag=row[select_col[NameColumn.TAG.value]].value,
                             description=row[select_col[NameColumn.NAME.value]].value,
                             schema=schema,
                             klk=row[select_col[NameColumn.KLK.value]].value,
                             contact=row[select_col[NameColumn.CONTACT.value]].value,
                             basket=basket,
                             module=module,
                             channel=channel))
        return data


class Import_in_SQL(DataExel):
    '''Запись и обновление сигналов в базе SQL'''
    def import_for_sql(self, data: dict, uso: str):
        msg = {}
        with db.atomic():
            try:
                Signals.insert_many(data).execute()
                msg[f'{today} - Таблица: signals. Добавлено новое УСО: {uso}'] = 1
            except Exception:
                msg[f'{today} - Таблица: signals, ошибка при заполнении: {traceback.format_exc()}'] = 2
        return msg

    def update_for_sql(self, data, uso):
        msg = {}
        with db.atomic():
            try:
                for row_exel in data:
                    exist_row = Signals.select().where(Signals.uso == uso,
                                                       Signals.basket == str(row_exel[NumberColumn.BASKET.value]),
                                                       Signals.module == str(row_exel[NumberColumn.MODULE.value]),
                                                       Signals.channel == str(row_exel[NumberColumn.CHANNEL.value]))
                    if not bool(exist_row):
                        Signals.create(**row_exel)
                        msg[f'''{today} - Добавлен новый сигнал: id - {row_exel["id"]}, description - {row_exel["description"]},
                                                                basket - {row_exel["basket"]}, module - {row_exel["module"]},
                                                                channel - {row_exel["channel"]}'''] = 0
                        continue

                    else:

                        if str(row_sql['tag']) == str(row_exel['tag']) and \
                            str(row_sql['description']) == str(row_exel['description']) and \
                            str(row_sql['scheme']) == str(row_exel['scheme']) and \
                            str(row_sql['klk']) == str(row_exel['klk']) and \
                            str(row_sql['contact']) == str(row_exel['contact']):

                            continue
                        else:
                            Signals.update(
                                type_signal=row_exel['type_signal'],
                                tag        =row_exel['tag'],
                                description=row_exel['description'],
                                schema     =row_exel['scheme'],
                                klk        =row_exel['klk'],
                                contact    =row_exel['contact'],
                            ).where(Signals.id == row_sql['id']).execute()
                            msg[f'''{today} - Обновление сигнала id = {row_sql["id"]}: Было, 
                                                uso - {row_sql['uso']}, 
                                                type_signal - {row_sql['type_signal']}, 
                                                tag - {row_sql['tag']},                      
                                                description - {row_sql['description']}, 
                                                schema - {row_sql['scheme']}, 
                                                klk - {row_sql['klk']},
                                                contact - {row_sql['contact']} = 
                                                Стало, 
                                                uso - {row_exel['uso']}, 
                                                type_signal - {row_exel['type_signal']}, 
                                                tag - {row_exel['tag']}, 
                                                description - {row_exel['description']}, 
                                                scheme - {row_exel['scheme']}, 
                                                klk - {row_exel['klk']},
                                                contact - {row_exel['contact']}'''] = 3
                            continue
            except Exception:
                msg[f'{today} - Таблица: signals, ошибка при обновлении: {traceback.format_exc()}'] = 2
        return(msg)

    def column_check(self):
        with db:
            list_default = ['id', 'type_signal', 'uso', 'tag', 'description', 'schema', 'klk', 'contact', 'basket', 'module', 'channel']

            self.dop_func = General_functions()
            msg = self.dop_func.column_check(Signals, 'signals', list_default)
        return msg







a = Import_in_SQL(connect.path_to_exel)
a.read_table() # ['МНС.КЦ', 'МНС.УСО.1(1) c БРУ', 'МНС.УСО.1(2)', 'МНС.УСО.1(3)', 'МНС.УСО.2', 'МНС.УСО.3', 'МНС.УСО.4', 'МНС.УСО.5']
a.max_column('МНС.КЦ')
a.read_hat_table('МНС.КЦ', 13, False)
a.read_hat_table('МНС.КЦ', 13, True, {'type_signal': 'Тип сигнала', 'tag': 'Тэг', 'description': 'Наименование'})

c = a.preparation_import('МНС.КЦ', 13, {'type_signal': 0,
                                          'tag': 2,
                                          'description': 3,
                                          'schema': 4,
                                          'klk': 6,
                                          'contact': 7,
                                          'basket': 10,
                                          'module': 11,
                                          'channel': 12})

for i in c:
    print(i)



#print(a.read_hat_table('МНС.КЦ', 13, True, {'type_signal': 'Тип сигнала', 'tag': 'Тэг', 'description': 'Наименование'}))
#a.import_table('МНС.КЦ', 13, {'type_signal': 'Тип сигнала', 'tag': 'Тэг', 'description': 'Наименование'})


# def value_cell(self, uso: str,
#                 number_row: int,
#                 select_column: tuple):
#     '''Вычисляем шапку таблицы или значения ячеек.'''
#     data = []

#     hat_table = self.read_hat_table(uso, number_row, True, select_column)

#     for row in self.sheet.iter_rows(min_row=(int(number_row) + 1)):
#         keys = []
#         values = []
#         for name, number in hat_table.items():
#             keys.append(name)
#             values.append(row[number].value)
#         values.append(uso)
#         array = {k: v for k, v in zip(keys, values)}
#         data.append(array)
#     return data

# def preparation_import(self, data_array: tuple):
#         '''Подготавливаем таблицу к импорту.'''
#         data = []

#         for row in data_array:
#             type_signal = row[NumberColumn.TYPE_SIGNAL.value]
#             scheme = row[NumberColumn.SCHEMA.value]
#             basket = row[NumberColumn.BASKET.value]
#             module = row[NumberColumn.MODULE.value]
#             channel = row[NumberColumn.CHANNEL.value]

#             if (basket or module or channel) is None:
#                 continue

#             type_signal = self.search_type(scheme, type_signal)

#             dict_column = {'type_signal': type_signal,
#                            'uso': row['uso'],
#                            'tag': row['tag'],
#                            'description': row['description'],
#                            'schema': row['schema'],
#                            'klk': row['klk'],
#                            'contact': row['contact'],
#                            'basket': basket,
#                            'module': row['module'],
#                            'channel': row['channel']}
#             data.append(dict_column)
#         return data