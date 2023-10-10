
class Editing_table_SQL():
    '''Редактирование базы SQL'''
    def __init__(self):
        self.cursor = db.cursor()
        self.dop_function = General_functions()

    def editing_sql(self, table_sql: str):
        '''Сбор данных для построения(столбцы, значения ячеек)'''
        try:
            eng_name_column = self.column_names(table_sql)
            
            dict_rus = self.exist_check_array(self.read_json(), table_sql)
            rus_eng_name = self.russian_name_column(dict_rus, eng_name_column)

            count_column = self.exist_check_int(self.read_json(), table_sql)

            value = self.cursor.fetchall()
            return len(eng_name_column), len(value), rus_eng_name, value, count_column
        except Exception:
            return 0, 0, 0, 0, 0

    def read_json(self) -> tuple:
        '''Русификация шапки таблицы из файла .json.'''

        with open(connect.path_rus_text, "r", encoding='utf-8') as outfile:
            return json.load(outfile)

    def russian_name_column(self, dict_rus, name_column):
        '''Расшифровка с английского на русский'''
        return [dict_rus[eng_t] if eng_t in dict_rus.keys() else eng_t for eng_t in name_column]

    def exist_check_array(self, array: dict, table: str):
        '''Проверка на существование данных столбцов из файла'''
        try:
            return array[table]
        except Exception:
            return {}

    def exist_check_int(self, array: dict, table: str):
        '''Проверка на существование данных для
          видимости столбцов левой таблицы в params_visible_column'''
        try:
            value = array['params_visible_column']
            return value[table]
        except Exception:
            return 4

    def search_name(self, tabl, value):
        '''Поиск подписи к ячейке'''
        try:
            isdigit_num = re.findall('\d+', str(value))
            self.cursor.execute(f"""SELECT name 
                                    FROM "{tabl}"
                                    WHERE id = {int(isdigit_num[0])}""")
            name_row = self.cursor.fetchall()[0][0]
            return name_row
        except Exception:
            return ''

    def column_names(self, table_used):
        '''Собираем название колонок'''
        self.cursor.execute(f'SELECT * FROM "{table_used}" ORDER BY id')
        return next(zip(*self.cursor.description))

    def apply_request_select(self, request, table_used: str, logging):
        try:
            self.cursor.execute(f'''{request}''')
            query_table = Parser(f'''{request}''').tables
            name_column = next(zip(*self.cursor.description))
            table_used = query_table[0]

            eng_name_column = self.column_names(table_used)

            dict_rus = self.exist_check_array(self.read_json(), table_used)
            rus_eng_name = self.russian_name_column(dict_rus, eng_name_column)

            c_col = self.exist_check_int(self.read_json(), table_used)

            value = self.cursor.fetchall()

            count_column = len(name_column)
            count_row = len(value)
            return table_used, count_column, count_row, rus_eng_name, value, c_col
        except Exception:
            logging.logs_msg(f'Таблица: {table_used} некорректный запрос: {traceback.format_exc()}', 2)
            return 'error', 'error', 'error', 'error', 'error', 'error'

    def update_row_tabl(self, column: int, text_cell: str, text_cell_id: int, 
                        table_used: str, hat_name: list, logging):
        active_column = list(hat_name)[column]
        try:
            if text_cell is None:
                self.cursor.execute(f"""UPDATE "{table_used}" 
                                        SET "{active_column}"= NULL
                                        WHERE id={text_cell_id}""")
            else:
                self.cursor.execute(f"""UPDATE "{table_used}" 
                                        SET "{active_column}"='{text_cell}'
                                        WHERE id={text_cell_id}""")
            return 
        except Exception:
            logging.logs_msg(f'Таблица: {table_used}, ошибка при изменении ячейки: {traceback.format_exc()}', 2)
            return

    def add_new_row(self, table_used: str, row: int) -> None:
        '''Добавление новой строки'''
        self.cursor.execute(f'''INSERT INTO "{table_used}" (id)
                                VALUES ({row});''')

    def delete_row(self, text_cell_id: str, table_used: str) -> None:
        '''Удаление выбранной строки'''
        self.cursor.execute(f'''DELETE FROM "{table_used}"
                                WHERE id={text_cell_id}''')

    def clear_tabl(self, table_used: str) -> None:
        '''Очистка таблицы'''
        self.cursor.execute(f'''DELETE FROM "{table_used}"''')

    def drop_tabl(self, table_used: str) -> None:
        '''Удаление таблицы'''
        self.cursor.execute(f'''DROP TABLE "{table_used}"''')

    def get_tabl(self):
        '''Сбор таблиц базы'''
        return db.get_tables()

    def type_column(self, table_used: str, logging):
        '''Собираем тип столбцов, и названия на рус и англ'''
        type_list = []
        try:
            self.cursor.execute(f"""SELECT column_name, data_type
                                    FROM information_schema.columns
                                    WHERE table_schema = 'public' AND 
                                        table_name = '{table_used}'""")
            
            dict_rus = self.exist_check_array(self.read_json(), table_used)

            for i in self.cursor.fetchall():
                column_name = i[0]
                data_type = i[1]
                try:
                    list_a = [column_name,  dict_rus[column_name], data_type]
                except Exception:
                    list_a = [column_name,  '', data_type]
                type_list.append(list_a)

        except Exception:
            logging.logs_msg(f'Окно тип данных: ошибка: {traceback.format_exc()}', 2)

        return type_list

    def dop_window_signal(self, table_used):
        type_list = []
        try:
            if table_used == 'ktpra':
                self.cursor.execute(f"""SELECT id, variable, name
                                        FROM "{table_used}"
                                        ORDER BY id""")
            else:
                self.cursor.execute(f"""SELECT id, tag, name 
                                        FROM "{table_used}" 
                                        ORDER BY id""")
            for i in self.cursor.fetchall():
                id_ = i[0]
                tag = i[1]
                name = i[2]

                list_a = [id_, tag, name]
                type_list.append(list_a)
            msg = ' Таблица открыта '
            color = '#6bdb84'
        except Exception:
            msg = ' Для типа сигнала нет таблицы '
            color = 'yellow'

        return type_list, msg, color

    def filter_text(self, text, list_signal):
        '''Поиск сигналов в окне ссылки'''
        list_request = []
        for i in list_signal:
            id_ = i[0]
            tag = i[1]
            name = i[2]

            if self.dop_function.str_find(str(name).lower(), {text}):
                list_temp = [id_, tag, name]
                list_request.append(list_temp)
        return list_request