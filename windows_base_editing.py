from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from main_base import Editing_table_SQL
import sys

CONST_WIN_SIZE_MAIN_W = 1600
CONST_WIN_SIZE_MAIN_H = 860


class TableWidget(QTableWidget):
    def __init__(self, edit_SQL, table_used, parent=None):
        super(TableWidget, self).__init__(parent)

        self.table_us = table_used
        self.edit_SQL = edit_SQL
        column, row, hat_name, value, msg = self.edit_SQL.editing_sql(self.table_us)

        self.setColumnCount(column)
        self.setRowCount(row)
        self.setHorizontalHeaderLabels(hat_name)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.installEventFilter(self)
        style = "::section {""background-color: #bbbabf; }"
        self.horizontalHeader().setStyleSheet(style)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        for tw_row in range(row):
            for tw_column in range(column):
                if value[tw_row][tw_column] is None:
                    item = QTableWidgetItem('')
                else:
                    item = QTableWidgetItem(str(value[tw_row][tw_column]))
                    # Подсказки к ячейкам
                    self.search_text(str(value[tw_row][tw_column]), "di", item)
                    self.search_text(str(value[tw_row][tw_column]), "do", item)
                    self.search_text(str(value[tw_row][tw_column]), "ai", item)

                if not tw_column:
                    item.setFlags(Qt.ItemIsEnabled)
                self.setItem(tw_row, tw_column, item)

        # Выравнивание по столбцов и строк по наибольшей длине
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        # Events
        self.itemChanged.connect(self.click_position)
        # self.TableWidget.cellClicked.connect(self.click_transfer)
        # self.TableWidget.horizontalScrollBar().valueChanged.connect(self.scrollToColumn)

    def data_cell(self):
        '''Текущая позиция ячейки'''
        return self.currentRow(), self.currentColumn()

    def row_count_tabl(self):
        '''Общее кол-во строк в таблице'''
        return self.rowCount()

    def column_count_tabl(self):
        '''Общее кол-во столбцов в таблице'''
        return self.columnCount()

    def text_cell(self, row: int, column: int) -> str:
        """Значение в текущей ячейке

        Args:
            row (int): Строка ячейки
            column (int): Столбец ячейки

        Returns:
            str: Значение
        """
        return self.item(row, column).text()

    def search_text(self, value_cell: str, what_looking: str, item):
        """Функция поиска описания ячейки

        Args:
            value_cell (str): значчение яччейки
            what_looking (str): что ищем
            item (_type_): элемент qtablewidget
        """
        if value_cell.lower().find(what_looking) != -1:
            name_signal = self.edit_SQL.search_name(what_looking, value_cell)
            item.setToolTip(name_signal)

    def click_position(self):
        '''Отработка события при изменении ячейки'''
        row, column = self.data_cell()

        try:
            value = self.text_cell(row, column)
            value_id = self.text_cell(row, 0)
        except Exception:
            value = None
            value_id = None

        hat_name = self.edit_SQL.column_names(self.table_us)

        msg = self.edit_SQL.update_row_tabl(column, value, value_id,
                                            self.table_us, hat_name)
        # self.logs_msg('default', 1, msg, True)

    def add_row(self):
        '''Добавляем новые строки в объект'''
        rowPos = self.row_count_tabl()

        value = 0
        if rowPos:
            value = self.text_cell(rowPos - 1, 0)

        self.edit_SQL.add_new_row(self.table_us, (rowPos + 1))
        self.insertRow(rowPos)
        self.setItem(rowPos, 0, QTableWidgetItem(f'{int(value) + 1}'))
        # Logs
        # self.logs_msg('В конец таблицы добавлена новая строка', 1)

    def delete_row(self):
        '''Удаляем выбранную строку'''
        row, column = self.data_cell()

        if (row == -1) and (column == -1):
            # self.logs_msg(f'Выбери строку для удаления!', 3)
            return
        value_id = self.text_cell(row, 0)
        self.edit_SQL.delete_row(value_id, self.table_us)
        self.removeRow(row)
        self.selectionModel().clearCurrentIndex()

        # Logs
        # self.logs_msg(f'Таблица: {self.table_used} удалена строка id={value_id}', 3)

    def delete_column(self):
        '''Удаление  выбранного столбца'''
        row, column = self.data_cell()
        self.removeColumn(column)
        hat_name = self.edit_SQL.column_names(self.table_us)
        self.edit_SQL.delete_column(column, hat_name, self.table_us)
        # self.logs_msg(f'Таблица: {self.table_us} удален столбец', 3)

class LogsTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(LogsTextEdit, self).__init__(parent)

        self.setStyleSheet('''border-radius: 4px;
                              border: 1px solid''')
        self.setFont(QFont('Arial', 12))
        self.setReadOnly(True)


class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)

        self.setStyleSheet('''border: 1px solid;
                              border-radius: 4px;
                              font-size: 15px;''')


class PushButton(QPushButton):
    '''Конструктор класса кнопки'''
    def __init__(self, text: str, color, tableWidget, parent=None):
        super(PushButton, self).__init__(parent)
        self.text = text
        self.tableWidget = tableWidget

        self.setText(self.text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("*{border: 1px solid;"
                           "border-radius: 4px;"
                           f"background: {color};"
                           "font-size: 12px;"
                           "padding: 4px 0;}"
                           "*:hover{"f"background:'#707370';""color:'white'}"
                           "*:pressed{background: '#4f45ba'}")

        self.clicked.connect(self.event_handler)

    def event_handler(self):
        if self.text == 'Добавить строку':
            self.tableWidget.add_row()
        elif self.text == 'Удалить строку':
            self.tableWidget.delete_row()
        elif self.text == 'Удалить столбец':
            self.tableWidget.delete_column()


class MainWindow(QMainWindow):
    '''Окно программы с виджетами'''
    def __init__(self, table_used: str):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Редактор базы данных')
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(CONST_WIN_SIZE_MAIN_W, CONST_WIN_SIZE_MAIN_H)

        self.table_us = table_used
        self.editSQL = Editing_table_SQL()
        self.logsTextEdit = LogsTextEdit(self)
        self.tableWidget = TableWidget(self.editSQL, self.table_us)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        # Buttons
        self.b_addrow = PushButton('Добавить строку', '#bfd6bf',
                                   self.tableWidget)
        self.b_delrow = PushButton('Удалить строку', '#d65860',
                                   self.tableWidget)
        # self.b_addcolumn = PushButton('Добавить столбец', '#bfd6bf',
        #                               self.tableWidget)
        self.b_delcolumn = PushButton('Удалить столбец', '#d65860',
                                      self.tableWidget)
        self.b_cleartabl = PushButton('Очистить таблицу', '#bbbabf',
                                      self.tableWidget)
        self.b_deltabl = PushButton('Удалить таблицу', '#bbbabf',
                                    self.tableWidget)
        self.b_links = PushButton('Ссылки', '#faf5cd',
                                  self.tableWidget)
        self.b_apply_query = PushButton('Применить запрос', '#bfd6bf',
                                        self.tableWidget)
        self.b_reset_query = PushButton('Сбросить запрос', '#bbbabf',
                                        self.tableWidget)
        self.b_type_data = PushButton('Тип данных таблицы', '#bfd6bf',
                                      self.tableWidget)
        # self.l_name_col = LineEdit(self,
        #                            placeholderText='Название нового столбца',
        #                            clearButtonEnabled=True)
        self.l_enter_req = LineEdit(self,
                                    placeholderText='Введите запрос',
                                    clearButtonEnabled=True)

        self.layout_g = QGridLayout()
        self.layout_g.addWidget(self.b_addrow, 0, 0)
        self.layout_g.addWidget(self.b_delrow, 1, 0)
        # self.layout_g.addWidget(self.l_name_col, 0, 1, 1, 2)
        # self.layout_g.addWidget(self.b_addcolumn, 1, 1)
        self.layout_g.addWidget(self.b_delcolumn, 1, 2)
        self.layout_g.addWidget(self.b_cleartabl, 0, 3)
        self.layout_g.addWidget(self.b_deltabl, 1, 3)
        self.layout_g.addWidget(self.b_links, 1, 4)
        self.layout_g.addWidget(self.l_enter_req, 0, 5, 1, 3)
        self.layout_g.addWidget(self.b_apply_query, 1, 5)
        self.layout_g.addWidget(self.b_reset_query, 1, 6)
        self.layout_g.addWidget(self.b_type_data, 1, 7)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.tableWidget)
        splitter.addWidget(self.logsTextEdit)
        splitter.setSizes([500, 100])

        self.layout_v = QVBoxLayout(self.centralwidget)
        self.layout_v.addLayout(self.layout_g)
        self.layout_v.addWidget(splitter)


# class Window_update_sql(QWidget):
#     def __init__(self, table_used):
#         super(Window_update_sql, self).__init__()
#         self.setWindowTitle('Редактор базы данных')
#         self.setStyleSheet("background-color: #e1e5e5;")
#         self.setWindowFlags(Qt.WindowCloseButtonHint)
#         self.resize(1600, 860)

#         self.TableWidget = QTableWidget(self)
#         self.TableWidget.setGeometry(10,70,1580,680)
#         self.TableWidget_1 = QTableWidget(self)
#         self.TableWidget_1.move(10,70)
#         self.TableWidget_1.setVisible(False)
#         self.TableWidget.verticalScrollBar().valueChanged.connect(self.__chnge_position)
#         self.TableWidget_1.verticalScrollBar().valueChanged.connect(self.__chnge_position)
#         self.flag_once = True

#         self.logTextBox = QTextEdit(self)
#         self.logTextBox.setGeometry(10,750,1580,100)
#         self.logTextBox.setStyleSheet("border-radius: 4px; border: 1px solid")
#         self.logTextBox.setFont(QFont('Arial', 10))
#         self.logTextBox.setReadOnly(True)

#         self.table_used = table_used
#         self.edit_SQL = Editing_table_SQL()
#         column, row, self.hat_name, value, msg = self.edit_SQL.editing_sql(self.table_used)
#         self.logs_msg('default', 1, msg, True)

#         self.gen_func = General_functions()

#         self.value_tab1  = value
#         self.column_tab1 = column
#         self.row_tab1    = row
#         self.tablew(column, row, self.hat_name, value)

#         new_addrow_Button = QPushButton('Добавить строку', self)
#         new_addrow_Button.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
#         new_addrow_Button.resize(120,25)
#         new_addrow_Button.move(10, 8) 
#         new_addrow_Button.clicked.connect(self.add_row)

#         remoterow_Button = QPushButton('Удалить строку', self)
#         remoterow_Button.setStyleSheet("background: #d65860; border-radius: 4px; border: 1px solid")
#         remoterow_Button.resize(120,25)
#         remoterow_Button.move(10, 40) 
#         remoterow_Button.clicked.connect(self.delete_row)

#         self.namecolumn = QLineEdit(self, placeholderText='Название нового столбца', clearButtonEnabled=True)
#         self.namecolumn.setStyleSheet('border: 1px solid #6f7370; border-radius: 4px; border: 1px solid')
#         self.namecolumn.move(160, 8)
#         self.namecolumn.resize(260,25)
#         new_addcol_Button = QPushButton('Добавить столбец', self)
#         new_addcol_Button.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
#         new_addcol_Button.resize(120,25)
#         new_addcol_Button.move(160, 40) 
#         new_addcol_Button.clicked.connect(self.add_column)

#         remotecolumn_Button = QPushButton('Удалить столбец', self)
#         remotecolumn_Button.setStyleSheet("background: #d65860; border-radius: 4px; border: 1px solid")
#         remotecolumn_Button.resize(120,25)
#         remotecolumn_Button.move(300, 40) 
#         remotecolumn_Button.clicked.connect(self.delete_column)

#         cleartab_Button = QPushButton('Очистить таблицу', self)
#         cleartab_Button.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
#         cleartab_Button.resize(120,25)
#         cleartab_Button.move(470, 8) 
#         cleartab_Button.clicked.connect(self.clear_tabl)

#         droptab_Button = QPushButton('Удалить таблицу', self)
#         droptab_Button.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
#         droptab_Button.resize(120,25)
#         droptab_Button.move(470, 40) 
#         droptab_Button.clicked.connect(self.drop_tabl)

#         link_Button = QPushButton('Ссылки', self)
#         link_Button.setStyleSheet("background: #faf5cd; border-radius: 4px; border: 1px solid")
#         link_Button.resize(120,25)
#         link_Button.move(610, 40) 
#         link_Button.clicked.connect(self.link_tabl)

#         self.req_base = QLineEdit(self, placeholderText='Введите запрос к текущей таблице', clearButtonEnabled=True)
#         self.req_base.setStyleSheet('border: 1px solid #6f7370; border-radius: 4px; border: 1px solid')
#         self.req_base.setToolTip('Значения типа "string" обязательно брать в "ковычки"')
#         self.req_base.move(750, 8)
#         self.req_base.resize(820,25)
#         apply_query_Button = QPushButton('Применить запрос', self)
#         apply_query_Button.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
#         apply_query_Button.resize(120,25)
#         apply_query_Button.move(750, 40) 
#         apply_query_Button.clicked.connect(self.apply_database_query)
#         reset_request_Button = QPushButton('Сбросить запрос', self)
#         reset_request_Button.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
#         reset_request_Button.setToolTip("Если используется выборка из таблицы!")
#         reset_request_Button.resize(120,25)
#         reset_request_Button.move(900, 40) 
#         reset_request_Button.clicked.connect(self.reset_database_query)

#         clickButton_type = QPushButton('Тип данных', self)
#         clickButton_type.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
#         clickButton_type.resize(120,25)
#         clickButton_type.move(1100, 40) 
#         clickButton_type.clicked.connect(self.type_tabl)

#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.logTextBox)
#         self.layout.addWidget(new_addrow_Button)
#         self.layout.addWidget(new_addcol_Button)
#         self.layout.addWidget(remoterow_Button)
#         self.layout.addWidget(cleartab_Button)
#         self.layout.addWidget(self.TableWidget)
#         # Logs
#         self.logs_msg(f'Запущен редактор базы данных. Таблица: {self.table_used}', 1)
#     # Новое окно тип таблицы
#     def type_tabl(self):
#         type_list, msg = self.edit_SQL.type_column(self.table_used)
#         self.type_tabl = Window_type_tabl_sql(type_list)
#         self.type_tabl.show()
#         self.logs_msg('default', 1, msg, True)
#     # Ссылки
#     def link_tabl(self):
#         self.link_tabl = Window_contexmenu_sql()
#         self.link_tabl.show()
#     # Сompletely clear the table
#     def clear_tabl(self):
#         rowcount = self.TableWidget.rowCount()

#         if rowcount == 0: 
#             self.logs_msg(f'Таблица: {self.table_used} пустая', 3)
#             return

#         while rowcount >= 0:
#             self.TableWidget.removeRow(rowcount)
#             rowcount -= 1

#         self.edit_SQL.clear_tabl(self.table_used)
#          # Logs
#         self.logs_msg(f'Таблица: {self.table_used} полностью очищена!', 3)
#     # Drop the table
#     def drop_tabl(self):
#         self.close()
#         self.edit_SQL.drop_tabl(self.table_used)

#     # Adding new lines
#     def add_row(self):  
#         rowPos = self.TableWidget.rowCount()
        
#         if rowPos == 0: 
#             text_cell = 0
#         else:
#             text_cell = self.TableWidget.item(rowPos - 1, 0).text()

#         self.TableWidget.insertRow(rowPos)
#         self.TableWidget.setItem(rowPos, 0, QTableWidgetItem (f'{int(text_cell) + 1}'))

#         self.edit_SQL.add_new_row(self.table_used, (rowPos + 1))
#         # Logs
#         self.logs_msg('В конец таблицы добавлена новая строка', 1)
#     # Removing rows
#     def delete_row(self):
#         row = self.TableWidget.currentRow()
#         if row <= 0: 
#             self.logs_msg('Невозможно удалить строки из пустой таблицы', 2)
#             return
        
#         text_cell_id = self.TableWidget.item(int(row), 0).text()
#         if row > -1: 
#             self.TableWidget.removeRow(row)
#             self.TableWidget.selectionModel().clearCurrentIndex()

#         self.edit_SQL.delete_row(text_cell_id, self.table_used)
#         # Logs
#         self.logs_msg(f'Из таблицы: {self.table_used} удалена строка id={text_cell_id}', 3)
#     # Adding new column
#     def add_column(self):
#         def letters(name):
#             if len(name) == 0: name = 'newcolumn'
#             return name#''.join(filter(str.isalnum, name))
        
#         namecolumn = letters(self.namecolumn.text())
#         hat_name = self.edit_SQL.column_names(self.table_used)
#         if namecolumn in hat_name: 
#             self.logs_msg('Дублирующие название столбца!', 2)
#             return

#         column_count = self.TableWidget.columnCount()
#         self.TableWidget.insertColumn(column_count)

#         self.edit_SQL.add_new_column(self.table_used, namecolumn)

#         hat_name = self.edit_SQL.column_names(self.table_used)
#         self.TableWidget.setHorizontalHeaderLabels(hat_name)
#         # Logs
#         self.logs_msg(f'В таблицу: {self.table_used} добавлен новый столбец: {namecolumn}', 1)
#     # Removing column
#     def delete_column(self):
#         if self.table_used == 'signals': 
#             self.logs_msg(f'Из таблицы: signals нельзя удалять столбцы!', 3)
#             return
#         column = self.TableWidget.currentColumn()
#         self.TableWidget.removeColumn(column)

#         hat_name = self.edit_SQL.column_names(self.table_used)
#         self.edit_SQL.delete_column(column, hat_name, self.table_used)
#         self.logs_msg(f'Из таблицы: {self.table_used} удален столбец', 3)
#     # Changing a table while entering a query
#     def apply_database_query(self):
#         request = self.req_base.text()
#         if request == '': 
#             self.logs_msg(f'Пустой запрос!', 2)
#             return
#         # Под запрос 'select' отдельная функция
#         find = General_functions()
#         if find.str_find(str(request).lower(), {'select'}):
#             column, row, hat_name, value, msg = self.edit_SQL.apply_request_select(request, self.table_used)
#             self.logs_msg('default', 1, msg, True)
#         else:
#             msg = self.edit_SQL.other_requests(request, self.table_used)
#             self.logs_msg('default', 1, msg, True)
#             column, row, hat_name, value, msg = self.edit_SQL.editing_sql(self.table_used)
#             self.logs_msg('default', 1, msg, True)
#         # Если запрос некорректный
#         if column == 'error': return
#         # Clear
#         rowcount = self.TableWidget.rowCount()
#         if rowcount != 0: 
#             while rowcount >= 0:
#                 self.TableWidget.removeRow(rowcount)
#                 rowcount -= 1
#         # Filling
#         self.tablew(column, row, hat_name, value)
#         #SELECT * FROM ai WHERE uso='МНС-2.КЦ' AND basket=3 AND module=3 AND channel=1
#     # Reset a table query
#     def reset_database_query(self):
#         rowcount = self.TableWidget.rowCount()
#         if rowcount != 0: 
#             while rowcount >= 0:
#                 self.TableWidget.removeRow(rowcount)
#                 rowcount -= 1
                
#         self.req_base.clear()

#         column, row, self.hat_name, value, msg = self.edit_SQL.editing_sql(self.table_used)
#         self.logs_msg('default', 1, msg, True)
#         self.tablew(column, row, self.hat_name, value)
#     # Building the selected table
#     def tablew(self, column, row, hat_name, value):
#         # TableW
#         self.TableWidget.setColumnCount(column)
#         self.TableWidget.setRowCount(row)
#         self.TableWidget.setHorizontalHeaderLabels(hat_name)
#         # Color header
#         style = "::section {""background-color: #bbbabf; }"
#         self.TableWidget.horizontalHeader().setStyleSheet(style)
#         self.TableWidget.verticalHeader().setVisible(False)
#         self.TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.TableWidget.installEventFilter(self)

#         for row_t in range(row):
#             for column_t in range(column):
#                 if value[row_t][column_t] is None:
#                     item = QTableWidgetItem('')
#                 else:
#                     item = QTableWidgetItem(str(value[row_t][column_t]))
#                     # Подсказки к ячейкам
#                     if self.gen_func.str_find(str(value[row_t][column_t]).lower(), {'di'}):
#                         name_signal = self.edit_SQL.search_name("di", str(value[row_t][column_t]))
#                         item.setToolTip(name_signal)
#                     elif self.gen_func.str_find(str(value[row_t][column_t]).lower(), {'do'}):
#                         name_signal = self.edit_SQL.search_name("do", str(value[row_t][column_t]))
#                         item.setToolTip(name_signal)
#                     elif self.gen_func.str_find(str(value[row_t][column_t]).lower(), {'ai'}):
#                         name_signal = self.edit_SQL.search_name("ai", str(value[row_t][column_t]))
#                         item.setToolTip(name_signal)
#                     else: item.setToolTip('')
                    
#                 if column_t == 0: item.setFlags(Qt.ItemIsEnabled)
#                 self.TableWidget.setItem(row_t, column_t, item)

#         self.TableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
#         # Выравнивание по столбцов и строк по наибольшей длине
#         self.TableWidget.resizeColumnsToContents()
#         self.TableWidget.resizeRowsToContents()
#         # Events
#         self.TableWidget.itemChanged.connect(self.click_position)
#         self.TableWidget.cellClicked.connect(self.click_transfer)
#         self.TableWidget.horizontalScrollBar().valueChanged.connect(self.scrollToColumn)
    
#     def eventFilter(self, obj: QObject, event: QEvent) -> bool:
#         row = self.TableWidget.currentRow()
#         count_row = self.TableWidget.rowCount()
#         if event.type() == QEvent.KeyPress:
#             if (event.key() == Qt.Key_Up): 
#                 if row > 0: self.setColortoRow(row - 1)
#             elif (event.key() == Qt.Key_Down): 
#                 if row < count_row-1: self.setColortoRow(row + 1)
#         return super().eventFilter(obj, event)
#     # Dubl windows
#     def tablew_1(self, column, row, hat_name, value):
#         # TableW
#         self.TableWidget_1.setColumnCount(column)
#         self.TableWidget_1.setRowCount(row)
#         self.TableWidget_1.setHorizontalHeaderLabels(hat_name)
#         # Color header
#         style = "::section {""background-color: #bbbabf; }"
#         self.TableWidget_1.horizontalHeader().setStyleSheet(style)
#         self.TableWidget_1.verticalHeader().setVisible(False)
#         self.TableWidget_1.setFocusPolicy(Qt.NoFocus)

#         for row_t in range(row):
#             for column_t in range(column):
#                 if value[row_t][column_t] is None:
#                     item = QTableWidgetItem('')
#                 else:
#                     item = QTableWidgetItem(str(value[row_t][column_t]))
#                 # Блокировка изменений столбцов
#                 for i in range(column): 
#                    if column_t == i: item.setFlags(Qt.ItemIsEnabled)
#                 # Выравнивание всех столбцов по общей ширине
#                 self.TableWidget_1.setItem(row_t, column_t, item)
#         # Выравнивание по столбцов и строк по наибольшей длине
#         self.TableWidget_1.resizeColumnsToContents()
#         self.TableWidget_1.resizeRowsToContents()
    
#     def scrollToColumn(self, item):
#         def clear_widget():
#             rowcount = self.TableWidget_1.rowCount()
#             if rowcount != 0: 
#                 while rowcount >= 0:
#                     self.TableWidget_1.removeRow(rowcount)
#                     rowcount -= 1
#         width = 0
#         for i in range(4): width += self.TableWidget.columnWidth(i) 
#         self.TableWidget_1.resize(width, 663)
#         self.TableWidget_1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.TableWidget_1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         currow = self.TableWidget.currentRow()
#         if (item > 0) and self.flag_once and (self.req_base.text() == ''): 
#             clear_widget()
#             column, row, hat_name, value, msg = self.edit_SQL.editing_sql(self.table_used)
#             self.tablew_1(column, row, hat_name, value)
#             self.TableWidget_1.setVisible(True)
#             self.flag_once = False
#             self.logs_msg('default', 1, msg, True)
#             # Выделение в зафиксированных ячейках
#             self.setColortoRow(currow)
#         elif item == 0: 
#             self.TableWidget_1.setVisible(False)
#             self.flag_once = True
    
#     def __chnge_position(self,index):
#         self.TableWidget.verticalScrollBar().setValue(index)
#         self.TableWidget_1.verticalScrollBar().setValue(index)
    
#     def setColortoRow(self, rowIndex):
#         if not self.TableWidget_1.isVisible(): return
#         for i in range(self.TableWidget_1.rowCount()):
#             for j in range(4):
#                 self.TableWidget_1.item(i, j).setBackground(QColor(229, 229, 229))
#                 self.TableWidget_1.item(i, j).setForeground(QColor(0, 0, 0))
#         for j in range(4):
#             self.TableWidget_1.item(rowIndex, j).setBackground(QColor(0, 120, 215))
#             self.TableWidget_1.item(rowIndex, j).setForeground(QColor(255, 255, 255))
    
#     def click_transfer(self):
#         row    = self.TableWidget.currentRow()
#         column = self.TableWidget.currentColumn()
#         # Выделение в зафиксированных ячейках
#         try: self.setColortoRow(row)
#         except: pass

#         try   :  self.link_tabl.parent_click(row, column, self.TableWidget)
#         except: return
#     # Cell change on click
#     def click_position(self):
#         row    = self.TableWidget.currentRow()
#         column = self.TableWidget.currentColumn()

#         if row == 0 and column == 0: return
#         for currentQTableWidgetItem in self.TableWidget.selectedItems():
#             text_cell = self.TableWidget.item(currentQTableWidgetItem.row(), column).text()
#         # На случай, когда нет изменения в ячейке
#         try   : text_cell
#         except: return
        
#         check_cell = self.TableWidget.item(int(row), 0)
#         if check_cell is None: return

#         text_cell_id = self.TableWidget.item(int(row), 0).text()

#         hat_name = self.edit_SQL.column_names(self.table_used)
#         flag_NULL = True if len(text_cell) == 0 else False
#         msg = self.edit_SQL.update_row_tabl(column, text_cell, text_cell_id, self.table_used, hat_name, flag_NULL)
#         self.logs_msg('default', 1, msg, True)
#     # Logging messeges
#     def logs_msg(self, logs=None, number_color=1, buffer_msg=None, msg=False):
#         today = datetime.now()
#         errorFormat   = '<span style="color:red;">{}</span>'
#         warningFormat = '<span style="color:#9ea108;">{}</span>'
#         validFormat   = '<span style="color:black;">{}</span>'
#         newFormat     = '<span style="color:green;">{}</span>'
#         if msg:
#             for string_msg, value in buffer_msg.items():
#                 if   value == 1: 
#                     self.logTextBox.append(validFormat.format(string_msg))
#                 elif value == 2: 
#                     self.logTextBox.append(errorFormat.format(string_msg))
#                 elif value == 3: 
#                     self.logTextBox.append(warningFormat.format(string_msg))
#                 elif value == 0: 
#                     self.logTextBox.append(newFormat.format(string_msg))
#         else:
#             if   number_color == 1: self.logTextBox.append(validFormat.format(f'{today} - {logs}'))
#             elif number_color == 2: self.logTextBox.append(errorFormat.format(f'{today} - {logs}'))
#             elif number_color == 3: self.logTextBox.append(warningFormat.format(f'{today} - {logs}'))
#             elif number_color == 0: self.logTextBox.append(newFormat.format(f'{today} - {logs}'))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow('zd')
    myWin.show()
    sys.exit(app.exec())