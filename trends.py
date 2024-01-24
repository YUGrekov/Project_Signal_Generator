"""Генерация древа трендов."""
import traceback
from lxml import etree
from main_base import General_functions
from models import connect
from models import AI
from models import TrendsGrp
from datetime import datetime
today = datetime.now()

NAME_FILE = 'AlphaTrends.xml'
CONST_SCRIPT = '<?xml version="1.0" encoding="UTF-8"?>\n<Source Type="NaftaPostgres">\n</Source>'


class TreeTrends():
    def __init__(self):
        self.dop_function = General_functions()

    def count_group_prj(self):
        """Вычисляем кол-во групп из БД."""
        value_bd = self.dop_function.select_orm(AI, None, AI.TrendingGroup)
        data = [grp.TrendingGroup for grp in value_bd if grp.TrendingGroup is not None]
        return sorted(set(data))

    def add_group(self, name_grp):
        """Добавление группы.
        Args:
            name_grp (str): название группы
        Returns:
            object: объект группы
        """
        group = etree.Element('Group')
        group.attrib['Name'] = str(name_grp)

        return group

    def add_signal(self, data, group):
        """Добавление сигнала группы.
        Args:
            data (dict): массив данных.
            group (object): объект группы.
        """
        for signal in data:
            group_tag = etree.Element('Tag')
            group_tag.attrib['Name'] = str(signal.tag)
            group_tag.attrib['Format'] = '%g'
            group_tag.attrib['Description'] = str(signal.name)
            group_tag.attrib['EGU'] = str(signal.Egu)
            group_tag.attrib['Alias'] = str(signal.tag)
            group_tag.attrib['Min'] = str(signal.LoLimEng)
            group_tag.attrib['Max'] = str(signal.HiLimEng)
            group.append(group_tag)

    def collect_tree(self, name_grp, where_sql):
        '''Один метод ля повторяющихся действий.'''
        data_ai = self.dop_function.select_orm(AI,
                                               AI.TrendingGroup == where_sql,
                                               AI.id)
        group = self.add_group(name_grp)
        self.add_signal(data_ai, group)
        return group

    def list_group(self, data_grp):
        '''Распределение списка групп по id и parent_id.'''
        assembly = {}
        for number in data_grp:
            dict_group = []
            grp_id = self.dop_function.select_orm(TrendsGrp, TrendsGrp.id == number, TrendsGrp.id)
            parent_id = self.dop_function.select_orm(TrendsGrp, TrendsGrp.id == grp_id[0].parent_id, TrendsGrp.id)

            if not len(parent_id):
                assembly[grp_id[0].id] = 0
            else:
                groups = self.dop_function.select_orm(TrendsGrp, TrendsGrp.parent_id == parent_id[0].id, TrendsGrp.id)
                for i in groups:
                    dict_group.append(i.id)
                assembly[parent_id[0].id] = dict_group
        return assembly

    def build_tree(self, group_trend, root):
        """Построение дерева трендов.
        Args:
            group_trend (dict): список int c неповторяющимеся группами
            root (object): парсинг
        """
        for lvl_one in root.iter('Source'):
            # Название проекта
            name_prj = self.add_group(connect.name_project)

            for parent, sub in group_trend.items():
                grp_id = self.dop_function.select_orm(TrendsGrp, TrendsGrp.id == parent, TrendsGrp.id)

                group = self.collect_tree(grp_id[0].name_grp, parent)
                if sub:
                    for number in sub:
                        search_subgrp = self.dop_function.select_orm(TrendsGrp, TrendsGrp.id == number, TrendsGrp.id)
                        for sub in search_subgrp:
                            data_ai = self.dop_function.select_orm(AI, AI.TrendingGroup == sub.id, AI.id)
                            if len(data_ai):
                                subgroup = self.collect_tree(sub.name_grp, sub.id)
                                group.append(subgroup)
                name_prj.append(group)
            root.append(name_prj)

    def fill_tree_trends(self):
        '''Обработка заполнения дерева трендов.'''
        msg = {}
        path_file = f'{connect.path_file_txt}\\{NAME_FILE}'
        try:
            # Проверка файла txt на существование и запись шапки
            open_file = self.dop_function.check_file_txt(path_file)
            open_file.write(CONST_SCRIPT)
            open_file.close()
            # Парсинг новой картинки
            root, tree = self.dop_function.xmlParser(path_file)
            # Формирование групп трендов
            data_grp = self.list_group(self.count_group_prj())
            # Построение групп
            self.build_tree(data_grp, root)

            tree.write(path_file, pretty_print=True, encoding='utf-8')
            msg[f'{today} - ВУ. Дерево трендов сформировано'] = 1
            return msg
        except Exception:
            print({traceback.format_exc()})
            msg[f'{today} - ВУ. Дерево трендов. Ошибка {traceback.format_exc()}'] = 2
            return msg