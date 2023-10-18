from model_new import db


class RequestSQL():
    '''Отдельный класс с запросами к БД.'''
    def __init__(self):
        self.cursor = db.cursor()

    def information_schema(self, table: str):
        '''Получаем тип столбцов таблицы.'''
        self.cursor.execute(f"""SELECT column_name, data_type
                                FROM information_schema.columns
                                WHERE table_schema = 'public' AND
                                      table_name = '{table}'""")
        return self.cursor.fetchall()

    def where_id_select(self, table: str, column: str, value_id: int):
        '''Запрос на выборку данных с условием по id.'''
        self.cursor.execute(f"""SELECT "{column}"
                                FROM "{table}"
                                WHERE id = {value_id}""")
        return self.cursor.fetchone()

    def all_select_table(self, table: str):
        '''Запрос на получение полных данных о
        таблице сортированные по столбцу id.'''
        self.cursor.execute(f'SELECT * FROM "{table}" ORDER BY id')
        return self.cursor.description, self.cursor.fetchall()

    def not_all_select_table(self, table: str, column):
        '''Запрос на получение частичных данных о
        таблице сортированные по столбцу id.'''
        self.cursor.execute(f'SELECT {column} FROM "{table}" ORDER BY id')
        return self.cursor.fetchall()

    def update_row(self, table: str, column, id_cell, change_value):
        '''Запрос на обновление ячейки строки.'''
        if change_value == 'NULL':
            string = f'SET "{column}"= NULL'
        else:
            string = f'''SET "{column}"= '{change_value}' '''

        self.cursor.execute(f"""UPDATE "{table}"
                                {string}
                                WHERE id={id_cell}""")

    def new_row(self, table: str, row: int):
        '''Запрос на добавление новой строки.'''
        self.cursor.execute(f'''INSERT INTO "{table}" (id)
                                VALUES ({row});''')

    def delete_row(self, id_cell: str, table: str):
        '''Запрос на удаление выбранной строки.'''
        self.cursor.execute(f'''DELETE FROM "{table}"
                                WHERE id={id_cell}''')

    def delete_table(self, table: str):
        '''Запрос на удаление таблицы.'''
        self.cursor.execute(f'DROP TABLE "{table}"')

    def clear_table(self, table: str):
        '''Запрос на очистку таблицы.'''
        self.cursor.execute(f'DELETE FROM "{table}"')

    def new_table(self, models):
        '''Создание новой таблицы по модели.'''
        with db.atomic():
            db.create_tables([models])

    def get_tabl(self):
        '''Сбор таблиц базы'''
        return db.get_tables()

    def max_value_column(self, table: str, column):
        '''Нахождение максимального знач-ния в столбце.'''
        self.cursor.execute(f'''SELECT MAX("{column}")
                                FROM "{table}"''')
        a = map(int, self.cursor.fetchall())
        return self.cursor.fetchall()[0][0]

    def max_value_column_cond(self):
        '''Нахождение максимального знач-ния в столбце с условием.'''
        cursor = db.cursor()
            if condition is False: cursor.execute(f'''SELECT MAX("{column}") FROM "{table_used}"''')
            else                 : cursor.execute(f'''SELECT MAX("{column}") FROM "{table_used}" WHERE "{args[0]}"={args[1]}''')
        except Exception:
            return 
        return cursor.fetchall()[0][0]