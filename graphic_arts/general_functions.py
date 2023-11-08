import psycopg2
from lxml import etree


class General_functions():
    '''Общие функции оспользованные при разработке.'''
    def str_find(self, line, array):
        '''Поиск в строке.'''
        for word in array:
            if str(line).find(word) > -1:
                return True

    def translate(self, str):
        if str is None:
            return None

        dict = {".": "_",
                "/": "_",
                "\\": "_",
                ",": "_",
                ":": "_",
                ";": "_",
                "А": "A",
                "В": "B",
                "Е": "E",
                "К": "K",
                "М": "M",
                "Н": "H",
                "О": "O",
                "Р": "P",
                "Т": "T",
                "Ц": "C",
                "Х": "X",
                "а": "a",
                "в": "b",
                "е": "e",
                "к": "k",
                "м": "m",
                "н": "h",
                "о": "o",
                "р": "p",
                "т": "t",
                "ц": "c",
                "х": "x"
                }

        trantab = str.maketrans(dict)
        return str.translate(trantab)

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

    def xmlParser(self, path):
        '''Парсинг файла.'''
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(path, parser)
        root = tree.getroot()
        return root, tree