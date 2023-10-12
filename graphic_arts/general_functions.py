import psycopg2
from model_new import db
import traceback


class General_functions():
    '''Общие функции оспользованные при разработке.'''

    def str_find(self, line, array):
        '''Поиск в строке.'''
        for word in array:
            if str(line).find(word) > -1:
                return True

    def all_tables(self):
        '''Получаем список всех таблиц БД.'''
        try:
            cursor = db.cursor()
            cursor.execute("""SELECT table_name
                            FROM information_schema.tables
                            WHERE table_schema='public'""")
            return [name for name in cursor.fetchall()]
        except Exception:
            return ['Нет подключения к БД']

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