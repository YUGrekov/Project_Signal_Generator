"""Генерация древа трендов."""
import traceback
from lxml import etree
from main_base import General_functions
from models import connect
from models import AI
from models import TrendsGrp
from datetime import datetime
today = datetime.now()


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
        group = self.add_group(name_grp)
        data_ai = self.dop_function.select_orm(AI, AI.TrendingGroup == where_sql, AI.id)
        self.add_signal(data_ai, group)
        return group

    def build_tree(self, group_trend, root):
        """Построение дерева трендов.
        Args:
            group_trend (dict): список int c неповторяющимеся группами
            root (object): парсинг
        """
        save_grp = []
        for lvl_one in root.iter('Source'):

            # Добавляем название проекта
            name_prj = self.add_group(connect.name_project)

            for number in group_trend:
                grp_id = self.dop_function.select_orm(TrendsGrp,
                                                      TrendsGrp.id == number,
                                                      TrendsGrp.id)

                # Если у группы нет подгруппы
                if not grp_id[0].parent_id:
                    group = self.collect_tree(grp_id[0].name_grp, number)
                else:
                    # Родительская группа
                    parent_group = self.dop_function.select_orm(TrendsGrp,
                                                                TrendsGrp.id == grp_id[0].parent_id,
                                                                TrendsGrp.id)

                    if parent_group[0].name_grp not in save_grp:
                        group = self.collect_tree(parent_group[0].name_grp, parent_group[0].id)
                        save_grp.append(parent_group[0].name_grp)

                    # Подгруппа
                    search_subgrp = self.dop_function.select_orm(TrendsGrp,
                                                                 TrendsGrp.id == number,
                                                                 TrendsGrp.id)
                    for sub in search_subgrp:
                        subgroup = self.collect_tree(sub.name_grp, sub.id)
                        group.append(subgroup)

                name_prj.append(group)
            root.append(name_prj)

    def fill_tree_trends(self):
        '''Обработка заполнения дерева трендов.'''
        msg = {}
        try:
            # Проверка файла txt на существование
            self.dop_function.check_file_txt(connect.path_file_txt)
            # Парсинг новой картинки
            root, tree = self.dop_function.xmlParser(connect.path_file_txt)
            # Кол-во групп трендов
            data_grp = self.count_group_prj()
            # Построение групп
            self.build_tree(data_grp, root)

            tree.write(connect.path_file_txt, pretty_print=True, encoding='utf-8')
            msg[f'{today} - ВУ. Дерево трендов сформировано'] = 1
            return msg
        except Exception:
            msg[f'{today} - ВУ. Дерево трендов. Ошибка {traceback.format_exc()}'] = 2
            return msg