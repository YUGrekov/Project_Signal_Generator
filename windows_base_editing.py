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
from PyQt5.QtWidgets import QHeaderView
from main_base import Editing_table_SQL
import sys

CONST_WIN_SIZE_MAIN_W = 1600
CONST_WIN_SIZE_MAIN_H = 860
CONST_WIN_SIZE_TYPETABLE_W = 500
CONST_WIN_SIZE_TYPETABLE_H = 600
CONST_WIDTH_BORDER = 11
CONST_COUNT_ONE = 1


class WindowContexMenuSQL(QMainWindow):
    def __init__(self):
        super(WindowContexMenuSQL, self).__init__()
        self.setWindowTitle('Ссылки')
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(800, 675)

#         self.edit_SQL = Editing_table_SQL()
#         self.write_text_cell = ''
        
#         # Выбор таблицы
#         self.combo = QComboBox(self)
#         self.combo.setStyleSheet("border-radius: 4px; border: 1px solid")
#         self.combo.resize(120,25)
#         self.combo.move(5, 5)
#         self.combo.setFont(QFont('Arial', 10))
#         self.tuple_tabl = {'AI':'ai', 'AO':'ao', 'DI':'di', 'DO':'do', 'ctrlDO':'do', 'NA':'umpna', 'ZD':'zd', 'VS':'vs', 'VSGRP':'vsgrp',
#                            'BUF':'buf', 'RSreq':'rsreq', 'KTPR':'ktpr', 'KTPRA':'ktpra', 'KTPRS':'ktprs', 'NPS':'nps', 'AIVisualValue':'ai', 
#                            'ctrlAO':'ao', 'Facility':'', 'BUFr':'bufr', 'PI':'pi', 'UTS':'uts', 'UPTS':'upts'}
#         for key, tabl in self.tuple_tabl.items():
#            self.combo.addItem(str(key))
#         # Кнопка открыть таблицу
#         open_Button = QPushButton('Открыть таблицу', self)
#         open_Button.setStyleSheet("background: #faf5cd;border-radius: 4px; border: 1px solid")
#         open_Button.move(130, 5)
#         open_Button.resize(120,25)
#         open_Button.clicked.connect(self.open_tabl)
#         # Тип
#         self.combo_type = QComboBox(self)
#         self.combo_type.setStyleSheet("border-radius: 4px; border: 1px solid")
#         self.combo_type.resize(200,25)
#         self.combo_type.move(270, 5)
#         self.combo_type.setFont(QFont('Arial', 10))
#         self.combo_type.activated.connect(self.do_something)
#         # Строка ввода сигнала для поиска
#         self.req_base = QLineEdit(self, placeholderText='Поиск сигнала', clearButtonEnabled=True)
#         self.req_base.setStyleSheet("border-radius: 4px; border: 1px solid")
#         self.req_base.move(500, 5)
#         self.req_base.resize(292,25)
#         self.req_base.textChanged.connect(self.request)
#         # Подтвердить выбранный сигнал
#         confirm_Button = QPushButton('Добавить', self)
#         confirm_Button.setStyleSheet("background: #bfd6bf;border-radius: 4px; border: 1px solid")
#         confirm_Button.move(672, 645)
#         confirm_Button.resize(120,25)
#         confirm_Button.clicked.connect(self.new_text_cell)
#         # Значение ссылки
#         self.link_value = QLineEdit(self, placeholderText='Значение ссылки', clearButtonEnabled=True)
#         self.link_value.setStyleSheet("border-radius: 4px; border: 1px solid")
#         self.link_value.move(315, 645)
#         self.link_value.resize(350,25)
#         # Результат загрузки таблицы
#         self.load = QLabel('', self)
#         self.load.move(10, 643)
#         self.load.resize(200,25)

#         self.TableWidget = QTableWidget(self)
#         self.TableWidget.setGeometry(5,40,790,600)
#         self.TableWidget.verticalHeader().setVisible(False)
#         self.TableWidget.horizontalHeader().setStretchLastSection(True) 
#         self.TableWidget.setColumnCount(3)
#         tabl = ['№', 'Тэг', 'Название']
#         self.TableWidget.setHorizontalHeaderLabels(tabl)
#         # Color header
#         style = "::section {""background-color: #bbbabf; }"
#         self.TableWidget.horizontalHeader().setStyleSheet(style)
#         self.TableWidget.cellClicked.connect(self.click_position)

#     def parent_click(self, row, column, qtablew):
#         self.row_parent = row
#         self.column_parent = column
#         self.tablew_parent = qtablew

#     def build(self, table_list):
#         self.list_signal = table_list
#         self.launch_windows(self.list_signal)

#     def launch_windows(self, table_list):
#         self.TableWidget.setRowCount(len(table_list))
#         for row_t in range(len(table_list)):
#             for column_t in range(3):
#                 if column_t == 0: value = table_list[row_t][column_t]
#                 if column_t == 1: value = table_list[row_t][column_t]
#                 if column_t == 2: value = table_list[row_t][column_t]

#                 if value is None:
#                     item = QTableWidgetItem('')
#                 else:
#                     item = QTableWidgetItem(str(value))
#                 item.setFlags(Qt.ItemIsEnabled)
#                 self.TableWidget.setItem(row_t, column_t, item)

#     def request(self):
#         request = self.req_base.text()
#         if request == '': return
#         # Clear
#         rowcount = self.TableWidget.rowCount()
#         if rowcount != 0: 
#             while rowcount >= 0:
#                 self.TableWidget.removeRow(rowcount)
#                 rowcount -= 1

#         list_filter = self.edit_SQL.filter_text(request, self.list_signal)
#         self.launch_windows(list_filter) 

#     def setColortoRow(self, rowIndex):
#         for i in range(self.TableWidget.rowCount()):
#             for j in range(self.TableWidget.columnCount()):
#                 self.TableWidget.item(i, j).setBackground(QColor(229, 229, 229))

#         for j in range(self.TableWidget.columnCount()):
#             self.TableWidget.item(rowIndex, j).setBackground(QColor(107, 219, 132))

#     def new_text_cell(self):
#         try:
#             self.cell_value
#             self.tablew_parent.setItem(self.row_parent, self.column_parent, QTableWidgetItem(self.write_text_cell))
#         except: return

#     def open_tabl(self):
#         name_table = self.combo.currentText()
#         for key, tab_value in self.tuple_tabl.items():
#             if key == name_table:
#                 need_open = tab_value
#         # Clear
#         rowcount = self.TableWidget.rowCount()
#         if rowcount != 0: 
#             while rowcount >= 0:
#                 self.TableWidget.removeRow(rowcount)
#                 rowcount -= 1
#         list_signal, msg, color = self.edit_SQL.dop_window_signal(need_open)
#         self.load.setText(msg)
#         self.load.setStyleSheet(f"background-color: {color}")
#         self.build(list_signal)

#         list_type = {'AI':['Norm','Warn','Avar','Ndv','LTMin','MTMax','Min6','Min5','Min4','Min3_IsMT10Perc','Min2_IsNdv2ndParam','Min1_IsHighVibStat',
#                            'Max1_IsHighVibStatNMNWR', 'Max2_IsHighVibNoStat', 'Max3_IsAvarVibStat', 'Max4_IsAvarVibStatNMNWR', 'Max5_IsAvarVibNoStat', 
#                            'Max6_IsAvar2Vib', 'Status'],
#                      'DI':['Value', 'Break', 'KZ', 'NC'],
#                      'BUF':['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'],
#                      'RSreq':['ok'],
#                      'ZD':['State_1_Opening','State_2_Opened','State_3_Middle','State_4_Closing','State_5_Closed','Dist','Imit','NOT_EC','Open','Close','Stop',
#                            'StopClose','KVO','KVZ','MPO','MPZ','CorrCO','CorrCZ','VMMO','VMMZ','NOT_ZD_EC_KTP','Local','Mufta','Avar_BUR','CorrCOCorrCZ','ErrMPO',
#                            'ErrMPZ','EC','RS_OK','Blink','Neisprav','NeispravVU','Close_Fail','Open_Fail','Stop_Fail','Unpromted_Open',
#                            'Unpromted_Close','Avar','Diff','WarnClose','ECsign'],
#                      'VSGRP':['REZ_EXIST','REM','OTKL'],
#                      'VS':['State_1_VKL','State_2_OTKL','State_3_ZAPUSK','State_4_OSTANOV','Mode_1_OSN','Mode_2_REZ','Mode_3_RUCH','Mode_4_REM','NEISPRAV','SEC_EC',
#                            'EC','MP','Imit','BLOCK_WORK_IS_ACTIVE','BLOCK_STOP_IS_ACTIVE','WAITING_FOR_FUTURE_PUSK','WAITING_FOR_APV','STARTED_AS_DOP','REORDER_REZ',
#                            'PC','WarnOff','PC_FALL','PC_NOT_UP','MPC_CONTROL','PC_CONTROL','MPC_CEPI_OTKL','MPC_CEPI_VKL','EC_CONTROL','EC_FALL','MPC_FALL','MPC_NOT_FALL',
#                            'MPC_CONTROL_RUCH','PC_CONTROL_RUCH','EC_CONTROL_RUCH','MPC_NOT_UP','EXTERNAL'],
#                      'NA':['MainState_1_VKL','MainState_2_OTKL','MainState_3_PUSK','MainState_4_OSTANOV','SubState_1_GP','SubState_2_GORREZ','SubState_3_PP','SubState_4_PO',
#                               'Mode_1_OSN','Mode_2_TU','Mode_3_REZ','Mode_4_REM','KTPRA_P','SimAgr','Prog_1','Prog_2','HIGHVIB','HIGHVIBNas','QF3A','QF1A','BBon','BBoff',
#                               'KTPRA_FNM','KTPRA_M','GMPNA_M','BBErrOtkl_All','BBErrOtkl','BBErrOtkl1','BBErrVkl','SAR_Ramp','StartWork','StopWork','StopNoCmd_1','StopNoCmd_2',
#                               'StartNoCmd','StateAlarm','StateAlarm_ChRP','StateAlarm_All','ChRPRegError','LogicalChRPCrash','StateAlarm_VV','StopErr','StopErr2','StopErr_All',
#                               'StartErr','StartErr2','StartErr3','StartErr_All','KKCAlarm1','KKCAlarm2','KKCAlarm3','KKCAlarm4','InputPath','OutputPath','OIPVib','GMPNA_F',
#                               'GMPNA_P','KTPR_ACHR','KTPR_SAON','ZD_Unprompted_Close','needRez','needOverhaul','ED_IsMT10Perc','ED_IsNdv2ndParam','ED_IsHighVibStat',
#                               'ED_IsHighVibNoStat','ED_IsAvarVibStat','ED_IsAvarVibNoStat','ED_IsAvar2Vib','Pump_IsMT10Perc','Pump_IsNdv2ndParam','Pump_IsHighVibStat',
#                               'Pump_IsHighVibStatNMNWR','Pump_IsHighVibNoStat','Pump_IsAvarVibStat','Pump_IsAvarVibStatNMNWR','Pump_IsAvarVibNoStat','Pump_IsAvar2Vib'],
#                      'KTPR':['P','F','M','NP'],
#                      'KTPRA':['P','F','M','NP'],
#                      'KTPRS':['P','F','M','NP'],
#                      'NPS':['ModeNPSDst','MNSInWork','IsMNSOff','IsNPSModePsl','IsPressureReady','NeNomFeedInterval','OIPHighPressure','KTPR_P','KTPR_M','CSPAWorkDeny',
#                             'TSstopped','stopDisp','stopCSPA','stopARM','CSPAlinkOK'],
#                      'Facility':['ndv2Gas','gasKTPR','activeGas','startExcessHeat','stopExcessHeat','warnGasPoint1','warnGasPoint2','warnGasPoint3','warnGasPoint4',
#                                  'warnGasPoint5','warnGasPoint6','warnGasPoint7','warnGasPoint8','longGasPoint1','longGasPoint2','longGasPoint3','longGasPoint4',
#                                  'longGasPoint5','longGasPoint6','longGasPoint7','longGasPoint8'],
#                      'DO':['Value'],
#                      'ctrlDO':[''],
#                      'ctrlAO':[''],
#                      'AO':[''],
#                      'BUFr':[''],
#                      'AIVisualValue':['']}
        
#         self.combo_type.clear()
#         for key, value in list_type.items():
#             if key == name_table:
#                 for i in value:
#                     self.combo_type.addItem(str(i))

#     def do_something(self):
#         self.update_str()

#     def click_position(self):
#         row = self.TableWidget.currentRow()
#         self.setColortoRow(row)
#         self.cell_value = self.TableWidget.item(row, 0).text()
#         self.cell_value_ktpra = self.TableWidget.item(row, 1).text()
#         self.update_str() 

#     def update_str(self):
#         column = self.TableWidget.currentColumn()
#         row    = self.TableWidget.currentRow()
#         try:
#             if column == 0:
#                 self.link_value.setText(str(row + 1))
#                 self.write_text_cell = str(row + 1)
#             else:
#                 if self.combo.currentText() in  ['ctrlDO', 'AO', 'AIVisualValue', 'ctrlAO', 'BUFr']: 
#                     self.link_value.setText(f'{self.combo.currentText()}[{self.cell_value}]')
#                     self.write_text_cell = f'{self.combo.currentText()}[{self.cell_value}]'
#                 elif self.combo.currentText() == 'Facility': 
#                     self.link_value.setText(f'{self.combo.currentText()}[].{self.combo_type.currentText()}')
#                     self.load.setText('Добавь индекс вручную!')
#                     self.load.setStyleSheet("background-color: red")
#                     self.write_text_cell = f'{self.combo.currentText()}[].{self.combo_type.currentText()}'
#                 elif self.combo.currentText() == 'KTPRA': 
#                     self.link_value.setText(f'{self.cell_value_ktpra}.{self.combo_type.currentText()}')
#                     self.write_text_cell = f'{self.cell_value_ktpra}.{self.combo_type.currentText()}'
#                 else:
#                     self.link_value.setText(f'{self.combo.currentText()}[{self.cell_value}].{self.combo_type.currentText()}')
#                     self.write_text_cell = f'{self.combo.currentText()}[{self.cell_value}].{self.combo_type.currentText()}'
#         except: return


class WindowTypeTableSQL(QMainWindow):
    """Отдельно окно с типами столбов, применяемое для запроса"""
    def __init__(self, table_list):
        super(WindowTypeTableSQL, self).__init__()

        self.setWindowTitle('Тип столбцов таблицы')
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(CONST_WIN_SIZE_TYPETABLE_W, CONST_WIN_SIZE_TYPETABLE_H)

        self.t_w = QTableWidget(self)
        self.t_w.verticalHeader().setVisible(False)
        self.t_w.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.t_w.setColumnCount(3)
        self.t_w.setFocusPolicy(Qt.NoFocus)
        self.t_w.setRowCount(len(table_list))
        column = ['Имя_eng', 'Имя_rus', 'Тип']
        self.t_w.setHorizontalHeaderLabels(column)
        style = "::section {""background-color: #bbbabf; }"
        self.t_w.horizontalHeader().setStyleSheet(style)

        for row_t in range(len(table_list)):
            for column_t in range(3):
                item = QTableWidgetItem(table_list[row_t][column_t])
                item.setFlags(Qt.ItemIsEnabled)
                self.t_w.setItem(row_t, column_t, item)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.layout_v = QVBoxLayout(self.centralwidget)
        self.layout_v.addWidget(self.t_w)


class TableWidget(QTableWidget):
    def __init__(self, edit_SQL, table_used,
                 tw_dub: bool = False, parent=None):
        super(TableWidget, self).__init__(parent)

        self.table_us = table_used
        self.tw_dub = tw_dub
        self.edit_SQL = edit_SQL
        column, row, hat_name, value, msg = self.object_data_table()

        self.init_table(column, row, hat_name, value)

    def object_data_table(self) -> tuple:
        '''Данные из базы SQL для построения таблицы'''
        column, row, hat_name, value, msg = self.edit_SQL.editing_sql(self.table_us)
        return column, row, hat_name, value, msg

    def init_table(self, column: int, row: int, hat_name: list, value: list):
        """Построение таблицы с данными

        Args:
            column (int): кол-во столбцов
            row (int): кол-во строк
            hat_name (list): заголовки столбцов
            value (list): значения ячеек
        """
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
        # Видимость столбцов
        if not self.tw_dub:
            [self.setColumnHidden(idx, True) for idx in range(0, 4)]
        else:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.blockSignals(False)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        # Events
        self.itemChanged.connect(self.click_position)

    def width_column(self) -> int:
        '''Получаем значение ширины 4 колонок'''
        width = 0
        for i in range(4):
            width += self.columnWidth(i)
        return width + CONST_WIDTH_BORDER

    def tw_clear_lines(self, rowcount: int):
        """Очистка таблицы виджета QTableWidget

        Args:
            rowcount (int): кол-во строк
        """
        if not rowcount:
            while rowcount >= 0:
                self.removeRow(rowcount)
                rowcount -= 1

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
    def __init__(self, text: str, color: str, parent=None):
        super(PushButton, self).__init__(parent)

        self.text = text

        self.setText(self.text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("*{border: 1px solid;"
                           "border-radius: 4px;"
                           f"background: {color};"
                           "font-size: 12px;"
                           "padding: 4px 0;}"
                           "*:hover{"f"background:'#707370';""color:'white'}"
                           "*:pressed{background: '#4f45ba'}")


class MainWindow(QMainWindow):
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
        self.tableWidget_dub = TableWidget(self.editSQL, self.table_us, True)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.l_enter_req = LineEdit(self,
                                    placeholderText='Введите запрос',
                                    clearButtonEnabled=True)
        b_addrow = PushButton('Добавить строку', '#bfd6bf')
        b_delrow = PushButton('Удалить строку', '#d65860')
        b_cleartabl = PushButton('Очистить таблицу', '#bbbabf')
        b_deltabl = PushButton('Удалить таблицу', '#bbbabf')
        b_apply_query = PushButton('Применить запрос', '#bfd6bf')
        b_reset_query = PushButton('Сбросить запрос', '#bbbabf')
        b_type_data = PushButton('Тип данных таблицы', '#bfd6bf')
        b_links = PushButton('Ссылки', '#faf5cd')

        # Events
        self.fl_actives_windows = 0
        b_addrow.clicked.connect(self.add_row)
        b_delrow.clicked.connect(self.delete_row)
        b_cleartabl.clicked.connect(self.clear_tabl)
        b_deltabl.clicked.connect(self.clear_tabl)
        b_apply_query.clicked.connect(self.apply_query)
        b_reset_query.clicked.connect(self.reset_query)
        b_type_data.clicked.connect(self.type_tabl)
        b_links.clicked.connect(self.link_tabl)
        self.tableWidget.selectionModel().selectionChanged.connect(self.on_Change_one)
        self.tableWidget_dub.selectionModel().selectionChanged.connect(self.on_Change_two)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.synh_position)
        self.tableWidget_dub.verticalScrollBar().valueChanged.connect(self.synh_position)

        # Position
        self.layout_g = QGridLayout()
        self.layout_g.addWidget(b_addrow, 0, 0)
        self.layout_g.addWidget(b_delrow, 1, 0)
        self.layout_g.addWidget(b_cleartabl, 0, 3)
        self.layout_g.addWidget(b_deltabl, 1, 3)
        self.layout_g.addWidget(b_links, 1, 4)
        self.layout_g.addWidget(self.l_enter_req, 0, 5, 1, 3)
        self.layout_g.addWidget(b_apply_query, 1, 5)
        self.layout_g.addWidget(b_reset_query, 1, 6)
        self.layout_g.addWidget(b_type_data, 1, 7)

        splitter_h = QSplitter(Qt.Horizontal)
        splitter_h.addWidget(self.tableWidget_dub)
        splitter_h.addWidget(self.tableWidget)
        width = self.tableWidget_dub.width_column()
        splitter_h.setSizes([width, CONST_WIN_SIZE_MAIN_W - width])

        splitter_v = QSplitter(Qt.Vertical)
        splitter_v.addWidget(splitter_h)
        splitter_v.addWidget(self.logsTextEdit)
        splitter_v.setSizes([500, 100])

        self.layout_v = QVBoxLayout(self.centralwidget)
        self.layout_v.addLayout(self.layout_g)
        self.layout_v.addWidget(splitter_v)

    def on_Change_one(self):
        '''Активность окна 1'''
        self.fl_actives_windows = 1

    def on_Change_two(self):
        '''Активность окна 2'''
        self.fl_actives_windows = 2

    def type_tabl(self):
        '''Запуск нового окна для просмотра типа столбцов'''
        type_list, msg = self.editSQL.type_column(self.table_us)
        self.type_tabl = WindowTypeTableSQL(type_list)
        self.type_tabl.show()
        # self.logs_msg('default', 1, msg, True)

    def link_tabl(self):
        self.link_tabl = WindowContexMenuSQL()
        self.link_tabl.show()

    def synh_position(self, index):
        '''Синхронное перелистывание текста по вертикали'''
        self.tableWidget.verticalScrollBar().setValue(index)
        self.tableWidget_dub.verticalScrollBar().setValue(index)

    def add_row(self):
        '''Добавляем новые строки в объекты'''
        rowcount = self.tableWidget.row_count_tabl()

        value = 0
        if rowcount:
            value = self.tableWidget.text_cell(rowcount - 1, 0)

        self.editSQL.add_new_row(self.table_us, (rowcount + 1))
        self.tableWidget.insertRow(rowcount)
        self.tableWidget.setItem(rowcount, 0, QTableWidgetItem(f'{int(value) + CONST_COUNT_ONE}'))
        self.tableWidget_dub.insertRow(rowcount)
        self.tableWidget_dub.setItem(rowcount, 0, QTableWidgetItem(f'{int(value) + CONST_COUNT_ONE}'))
        # Logs
        # self.logs_msg('В конец таблицы добавлена новая строка', 1)

    def delete_row(self):
        '''Удаляем выбранную строку'''
        if self.fl_actives_windows == 1:
            row, column = self.tableWidget.data_cell()
        else:
            row, column = self.tableWidget_dub.data_cell()

        if (row == -1) and (column == -1):
            # self.logs_msg(f'Выбери строку для удаления!', 3)
            return
        if self.fl_actives_windows == 1:
            value_id = self.tableWidget.text_cell(row, 0)
        else:
            value_id = self.tableWidget_dub.text_cell(row, 0)
        self.editSQL.delete_row(value_id, self.table_us)
        self.tableWidget.removeRow(row)
        self.tableWidget.selectionModel().clearCurrentIndex()
        self.tableWidget_dub.removeRow(row)
        self.tableWidget_dub.selectionModel().clearCurrentIndex()
        # self.logs_msg(f'Таблица: {self.table_used} удалена строка id={value_id}', 3)

    def clear_tabl(self):
        '''Удаления всех данных таблицы, без столбцов'''
        rowcount = self.tableWidget.row_count_tabl()
        if rowcount == 0:
            # self.logs_msg(f'Таблица: {self.table_used} пустая', 3)
            return
        while rowcount >= 0:
            self.tableWidget.removeRow(rowcount)
            self.tableWidget_dub.removeRow(rowcount)
            rowcount -= 1
        self.editSQL.clear_tabl(self.table_us)
        self.l_enter_req.clear()
        # self.logs_msg(f'Таблица: {self.table_used} полностью очищена!', 3)

    def drop_tabl(self):
        '''Удаление таблицы из базы данных'''
        self.editSQL.drop_tabl(self.table_us)

    def apply_query(self):
        """Рукописный запрос к базе SQL

        Args:
            input_query (str): текст запроса
        """
        rowcount = self.tableWidget.row_count_tabl()
        if not len(self.l_enter_req.text()):
            # self.logs_msg(f'Пустой запрос!', 2)
            print('пустой')
            return
        table_now, column, row, hat_name, value, msg = self.editSQL.apply_request_select(self.l_enter_req.text(), self.table_us)
        # self.logs_msg('default', 1, msg, True)

        self.tableWidget.table_us = table_now
        self.tableWidget_dub.table_us = table_now

        if column == 'error':
            return

        self.tableWidget.tw_clear_lines(rowcount)
        self.tableWidget_dub.tw_clear_lines(rowcount)

        self.tableWidget.blockSignals(True)
        self.tableWidget_dub.blockSignals(True)

        self.tableWidget.init_table(column, row, hat_name, value)
        self.tableWidget_dub.init_table(column, row, hat_name, value)

    def reset_query(self):
        '''Сброс запроса и возврат таблицы к состоянию до запроса'''
        rowcount = self.tableWidget.row_count_tabl()

        self.tableWidget.table_us = self.table_us
        self.tableWidget_dub.table_us = self.table_us

        self.tableWidget.tw_clear_lines(rowcount)
        self.tableWidget_dub.tw_clear_lines(rowcount)

        column, row, hat_name, value, msg = self.tableWidget.object_data_table()
        # self.logs_msg('default', 1, msg, True)
        self.tableWidget.blockSignals(True)
        self.tableWidget_dub.blockSignals(True)

        self.tableWidget.init_table(column, row, hat_name, value)
        self.tableWidget_dub.init_table(column, row, hat_name, value)
        # self.l_enter_req.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow('ai')
    myWin.show()
    sys.exit(app.exec())