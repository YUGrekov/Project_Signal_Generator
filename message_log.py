"""Генерация древа архивных сообщений."""
import traceback
from lxml import etree
from main_base import General_functions
from models import connect
from models import Msg
from models import MsgCat
from models import AI
from models import ZD
from models import VS
from models import UTS
from models import UPTS
from models import UMPNA
from models import PZ
from models import PI
from models import DPS
from models import BD
from datetime import datetime
today = datetime.now()

NAME_FILE = 'Categories.xml'
CONST_SCRIPT = '<?xml version="1.0" encoding="utf-8"?>\n<Groups>\n</Groups>'
EQUALITY = {AI: ['аналогов'],
            ZD: ['задвижк'],
            VS: ['вспомсистем'],
            UMPNA: ['насосн', 'агрега'],
            PZ: ['пожарн', 'зоны'],
            PI: ['пожарн', 'извещатель'],
            DPS: ['поточных', 'устройств'],
            BD: ['бак', 'дозатор']
            }


class TreeJornal():
    def __init__(self):
        self.dop_function = General_functions()

    def add_group(self, name, code):
        """Добавление группы.
        Args:
            name (str): название группы.
            code (str): коды сообщений.
        Returns:
            object: объект группы
        """
        group = etree.Element('Group')
        group.attrib['Name'] = str(name)
        group.attrib['FilterField'] = 'Code'
        etree.SubElement(group, 'Value').text = f'{code}'
        return group

    def add_atrib_group(self, name_grp, value):
        """Добавление подгруппы.
        Args:
            name_grp (str): название группы
            value(str): код сообщения объекта.
        Returns:
            object: объект группы
        """
        group = etree.Element('Group')
        group.attrib['Name'] = str(name_grp)
        group.attrib['FilterField'] = 'Code'
        group.text = value
        return group

    def collect_signal(self, model_bd, count_msg: int, start_msg: int, group):
        """Запись подгруппы.
        Args:
            model_bd (object): Модель БД.
            count_msg (int): Кол-во сообщений на 1 сигнал.
            start_msg (int): Стартовый адрес сообщений.
        """
        data = self.dop_function.select_orm(model_bd, None, model_bd.id)
        for row in data:
            begin_code_row = start_msg + count_msg * (row.id - 1)
            end_code_row = begin_code_row + (count_msg - 1)
            code_row = f'{begin_code_row}, {end_code_row}'

            subgroup = self.add_atrib_group(row.name, code_row)
            group.append(subgroup)

    def fill_subgroup(self, category, group):
        for model, point in EQUALITY.items():
            check_len = 0
            for word in point:
                if word in category.lower():
                    check_len += 1

            if check_len == len(point):
                msg = self.dop_function.select_orm(Msg,
                                                   Msg.tag == model.__name__,
                                                   Msg.id)
                if len(msg):
                    self.collect_signal(model, msg[0].count, msg[0].index, group)

    def build_tree(self, root):
        """Построение дерева.
        Args:
            root (object): парсинг
        """
        for lvl_one in root.iter('Groups'):
            msg_cat = self.dop_function.select_orm(MsgCat, None, MsgCat.id)

            for row in msg_cat:
                category = row.category
                code = row.list_code_category

                # Категория сообщений
                group = self.add_group(category, code)
                # Поиск подгруппы
                self.fill_subgroup(category, group)

                root.append(group)

    def fill_tree_jornal(self):
        '''Обработка заполнения дерева журнала.'''
        msg = {}
        path_file = f'{connect.path_file_txt}\\{NAME_FILE}'
        try:
            # Проверка файла на существование и запись шапки
            open_file = self.dop_function.check_file_txt(path_file)
            open_file.write(CONST_SCRIPT)
            open_file.close()
            # Парсинг новой картинки
            root, tree = self.dop_function.xmlParser(path_file)
            # Заполнение
            self.build_tree(root)

            tree.write(path_file, pretty_print=True, encoding='utf-8')
            msg[f'{today} - ВУ. Категории архивного журнала заполнены'] = 1
            return msg
        except Exception:
            print({traceback.format_exc()})
            msg[f'{today} - ВУ. Категории архивного журнала. Ошибка {traceback.format_exc()}'] = 2
            return msg


a = TreeJornal()
a.fill_tree_jornal()