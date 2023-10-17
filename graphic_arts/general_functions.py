import psycopg2
import traceback


class General_functions():
    '''Общие функции оспользованные при разработке.'''

    def str_find(self, line, array):
        '''Поиск в строке.'''
        for word in array:
            if str(line).find(word) > -1:
                return True

    def exist_check_db(self, dbname, user, password, host, port):
        '''Проверка на существование БД'''
        try:
            db_connect = psycopg2.connect(f"""dbname={dbname}
                                              user={user}
                                              host={host}
                                              password={password}
                                              port={port}
                                              connect_timeout=1""")
            db_connect.close()
            return True
        except Exception:
            return False

    def check_in_table(self, table: str, array_table: dict):
        '''Проверка на существование таблицы в БД.'''
        return True if table in array_table else False