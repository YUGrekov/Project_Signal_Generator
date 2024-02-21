"""Генерация древа трендов."""
import traceback
from lxml import etree
from model_new import connect
from general_functions import General_functions
from request_sql import RequestSQL
from model_new import AI
from model_new import TrendsGrp


class TreeTrends():
    def __init__(self, logtext):
        self.logsTextEdit = logtext
        self.dop_function = General_functions()

    def count_group_prj(self):
        """Вычисляем кол-во групп из БД."""
        value_bd = self.request.select_orm(AI, None, AI.TrendingGroup)
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

    def add_group_signal(self, data, group):
        """Добавление сигнала группы.
        Args:
            data (dict): массив данных.
            group (object): объект группы.
        """
        for signal in data:
            group_signal = self.add_group(signal.name)

            self.add_signal(signal, group_signal)

            if 'резерв' not in str(signal.name).lower() and signal.module is not None and signal.channel is not None:
                self.add_signal_phisic(signal, group_signal)

            group.append(group_signal)

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
            group_tag.attrib['Description'] = 'Инженерное'
            group_tag.attrib['EGU'] = str(signal.Egu)
            group_tag.attrib['Alias'] = str(signal.tag)
            group_tag.attrib['Min'] = str(signal.LoLimEng)
            group_tag.attrib['Max'] = str(signal.HiLimEng)
            group.append(group_tag)

    def add_signal_phisic(self, signal, group):
        """Добавление дополнительного сигнала группы.
        Args:
            data (dict): массив данных.
            group (object): объект группы.
        """
        group_tag = etree.Element('Tag')
        group_tag.attrib['Name'] = str(f'{signal.tag}_kin')
        group_tag.attrib['Format'] = '%g'
        group_tag.attrib['Description'] = 'Полевое'
        group_tag.attrib['EGU'] = str(signal.PhysicEgu)
        group_tag.attrib['Alias'] = str(f'{signal.tag}_kin')
        group_tag.attrib['Min'] = str(signal.LoLimField)
        group_tag.attrib['Max'] = str(signal.HiLimField)
        group.append(group_tag)

    def collect_tree(self, name_grp, where_sql):
        '''Один метод ля повторяющихся действий.'''
        group = self.add_group(name_grp)
        data_ai = self.request.select_orm(AI, AI.TrendingGroup == where_sql, AI.id)

        self.add_group_signal(data_ai, group)
        return group

    def build_tree(self, group_trend, root):
        """Построение дерева трендов.
        Args:
            group_trend (dict): список int c неповторяющимеся группами
            root (object): парсинг
        """
        for lvl_one in root.iter('Source'):

            # Добавляем название проекта
            name_prj = self.add_group(connect.name_project)

            for number in group_trend:
                grp_id = self.request.select_orm(TrendsGrp, TrendsGrp.id == number, TrendsGrp.id)
                search_subgrp = self.request.select_orm(TrendsGrp, TrendsGrp.parent_id == grp_id[0].id, TrendsGrp.id)

                # Если у группы нет подгруппы и значение parent_id=0
                if (not len(search_subgrp)) and (not grp_id[0].parent_id):
                    group = self.collect_tree(grp_id[0].name_grp, number)
                else:
                    if grp_id[0].parent_id:
                        continue
                    # Родительская группа
                    group = self.collect_tree(grp_id[0].name_grp, grp_id[0].id)
                    # Подгруппа
                    for sub in search_subgrp:
                        subgroup = self.collect_tree(sub.name_grp, sub.id)
                        group.append(subgroup)

                name_prj.append(group)
            root.append(name_prj)

    def fill_tree_trends(self):
        try:
            self.request = RequestSQL()
            # Проверка файла txt на существование
            self.dop_function.check_file_txt(connect.path_file_txt)
            # Парсинг новой картинки
            root, tree = self.dop_function.xmlParser(connect.path_file_txt)
            # Кол-во групп трендов
            data_grp = self. count_group_prj()
            # Построение групп
            self.build_tree(data_grp, root)

            tree.write(connect.path_file_txt, pretty_print=True, encoding='utf-8')
            self.logsTextEdit.logs_msg('''ВУ. Дерево трендов сформировано''', 0)
        except Exception:
            self.logsTextEdit.logs_msg(f'''ВУ. Дерево трендов. Ошибка {traceback.format_exc()}''', 2)