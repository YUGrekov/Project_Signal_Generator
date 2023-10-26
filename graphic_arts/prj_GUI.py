import sys
import traceback
from psycopg2 import Error
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QCheckBox
sys.path.append('../Project_Signal_Generator')
from logging_text import LogsTextEdit
from window_editing import MainWindow as WinEditing
from general_functions import General_functions as DopFunction
from graphic_arts.new_db_station import NewDB
from model_new import connect
from model_new import db
from model_new import db_prj
from model_new import Signals
from backend_importKD import Import_in_SQL
from request_sql import RequestSQL
from hmi_defence import DefenceMap
from hmi_uso import DaignoPicture


SIZE_WORK_BACK = (1200, 500)
SIZE_SPLIT_V = [500, 150]
SIZE_SPLIT_H = [602, 40]


class EditTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(EditTabWidget, self).__init__(*args, **kwargs)
        self.setStyleSheet("""QTabWidget::pane {
                           border: 2px solid #C4C4C3;
                           border-bottom-left-radius: 5;
                           border-bottom-right-radius: 5;
                           padding: 10px;}
                           QTabBar::tab{
                           border: 2px solid #C4C4C3;
                           min-width: 255px;
                           min-height: 30;
                           font: 15px consolas;}
                           QTabBar::tab:selected{
                           color: rgb(0, 0, 0);
                           background: #51c4a9}
                           """)


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(QTabWidget, self).__init__(*args, **kwargs)
        self.setStyleSheet("""QTabWidget::pane {
                           border: 2px solid #C4C4C3;
                           border-bottom-left-radius: 5;
                           border-bottom-right-radius: 5;
                           padding: 10px;
                           margin-top: 1px;}
                           QTabBar::tab{
                           min-width:153px;
                           min-height:30;
                           font:15px consolas;}
                           QTabBar::tab:selected{
                           color:rgb(0, 0, 0);
                           background: #51c4a9}
                           """)


class CheckBox(QCheckBox):
    '''Конструктор класса чекбокса.'''
    def __init__(self, *args, **kwargs):
        super(CheckBox, self).__init__(*args, **kwargs)
        self.setStyleSheet("""*{
                           font:15px consolas;
                           padding: 3px;
                           border-radius: 4
                           }""")


class PushButton(QPushButton):
    '''Конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(PushButton, self).__init__(*args, **kwargs)


class GenFormButton(QPushButton):
    '''Общий конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(GenFormButton, self).__init__(*args, **kwargs)
        self.setStyleSheet("""*{font:15px consolas;
                                border: 2px solid #C4C4C3;
                                border-bottom-color: #C2C7CB;
                                padding: 4px;
                                border-radius: 4}
                                *:hover{background:#c0deb8;
                                        color:'black'}
                                *:pressed{background: '#7ce063'}""")


class LineEdit(QLineEdit):
    '''Общий конструктор строки заполнения.'''
    def __init__(self, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)
        self.setStyleSheet("""*{
                                background-color: #f0f0f0;
                                font:15px consolas;
                                border: 2px solid #C4C4C3;
                                border-bottom-color: #C2C7CB;
                                padding: 3px;
                                border-radius: 4}""")


class Label(QLabel):
    '''Конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.setStyleSheet('''
                           background-color: #d95050;
                           border: 2px solid #C4C4C3;
                           border-radius: 4;
                           padding: 4px;
                           font:12px consolas;''')

    def connect_true(self):
        self.setStyleSheet('''
                           background-color: #7ce063;
                           border: 2px solid #C4C4C3;
                           border-radius: 4;
                           padding: 8px;
                           font:12px consolas;''')

    def connect_false(self):
        self.setStyleSheet('''
                           background-color: #d95050;
                           border: 2px solid #C4C4C3;
                           border-radius: 4;
                           padding: 8px;
                           font:12px consolas;''')


class LabelSimple(QLabel):
    '''Конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(LabelSimple, self).__init__(*args, **kwargs)
        self.setStyleSheet('''font:12px consolas;''')
        self.setAlignment(Qt.AlignCenter)


class ElementSignature(QLabel):
    '''Конструктор класса текста.
    Подаись элемента виджета'''
    def __init__(self, *args, **kwargs):
        super(ElementSignature, self).__init__(*args, **kwargs)
        self.setStyleSheet('''
                           border-radius: 4;
                           padding: 0px;
                           font: 15px consolas;''')


class LabelHMI(QLabel):
    '''Конструктор класса текста.
    Подпись элемента виджета'''
    def __init__(self, *args, **kwargs):
        super(LabelHMI, self).__init__(*args, **kwargs)
        self.setStyleSheet('''border-radius: 4;
                              padding: 0px;
                              font: 18px consolas;''')
        self.setAlignment(Qt.AlignCenter)


class GenProject(QWidget):
    def __init__(self, parent=None):
        super(GenProject, self).__init__(parent)


class ComboBox(QComboBox):
    def __init__(self, text):
        super(ComboBox, self).__init__()
        self.setEditable(True)
        self.setCurrentIndex(-1)
        self.setCurrentText(text)
        self.setMinimumContentsLength(22)
        self.setStyleSheet('''
                           padding: 4px;
                           font: 15px consolas;''')


class EditWindows(QWidget):
    '''Конструктор класса редактирования окна разработки.'''
    def __init__(self, logtext, parent=None):
        super(EditWindows, self).__init__(parent)

        self.logsTextEdit = logtext
        layout_v = QVBoxLayout(self)

        self.combo_choise_tabl = ComboBox('Выбери таблицу')
        self.button_connect_1 = GenFormButton('Окно редактора №1')
        self.button_connect_2 = GenFormButton('Окно редактора №2')
        self.button_update = GenFormButton('Обновить список')

        self.button_update.setToolTip('Обновление списка таблиц после изменения БД')

        self.button_connect_1.clicked.connect(self.open_window1)
        self.button_connect_2.clicked.connect(self.open_window2)
        self.button_update.clicked.connect(self.update_list)

        layout_v.addWidget(self.combo_choise_tabl)
        layout_v.addWidget(self.button_connect_1)
        layout_v.addWidget(self.button_connect_2)
        layout_v.addStretch()
        layout_v.addWidget(self.button_update)

    def open_window1(self):
        '''Выполнение по клику кнопки.
        Открытие окна редактирования БД 1.'''
        name_table = self.combo_choise_tabl.currentText()

        if name_table == 'Выбери таблицу':
            self.logsTextEdit.logs_msg('Не выбрана таблица для открытия окна для редактирования!', 2)
            return
        try:
            self.open_w1 = WinEditing(name_table)
            self.open_w1.show()
            self.logsTextEdit.logs_msg(f'''Открыто окно для редактирования №1.\n
                                        Таблица: {name_table}''', 1)
        except Exception:
            self.logsTextEdit.logs_msg('''Невозможно подключиться к таблице.
                                       Нет подключения к БД разработки''', 2)

    def open_window2(self):
        '''Выполнение по клику кнопки.
        Открытие окна редактирования БД 2.'''
        name_table = self.combo_choise_tabl.currentText()

        if name_table == 'Выбери таблицу':
            self.logsTextEdit.logs_msg('Не выбрана таблица для открытия окна для редактирования!', 2)
            return
        try:
            self.open_w2 = WinEditing(name_table)
            self.open_w2.show()
            self.logsTextEdit.logs_msg(f'''Открыто окно для редактирования №2.\n
                                        Таблица: {name_table}''', 1)
        except Exception:
            self.logsTextEdit.logs_msg('''Невозможно подключиться к таблице.
                                       Нет подключения к БД разработки''', 2)

    def update_list(self):
        '''Функция обновляет список таблиц по команде.'''
        try:
            reqsql = RequestSQL()
        except Exception:
            self.logsTextEdit.logs_msg('''Невозможно обновить список.
                                       Нет подключения к БД разработки''', 2)
            self.combo_choise_tabl.clear()
            self.combo_choise_tabl.addItem('Выбери таблицу')
            return

        list_table = reqsql.get_tabl()
        self.combo_choise_tabl.clear()
        for table in list_table:
            self.combo_choise_tabl.addItem(str(table))
        self.logsTextEdit.logs_msg('Список таблиц обновлен', 1)


class TabConnect(QWidget):
    '''Конструктор класса. Проверка и подключение к БД.'''
    def __init__(self, logtext, parent=None):
        super(TabConnect, self).__init__(parent)

        self.logsTextEdit = logtext
        self.parent = parent
        self.dop_function = DopFunction()

        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()
        layout_v3 = QVBoxLayout()
        layout_h1 = QHBoxLayout()
        layout_h2 = QHBoxLayout(self)
        # Подписи
        label_dev_sign = ElementSignature('База данных разработки\t')
        label_dev_database = ElementSignature(f'database:  {connect.database}')
        label_dev_user = ElementSignature(f'user:      {connect.user}')
        label_dev_pwd = ElementSignature(f'password:  {connect.password}')
        label_dev_host = ElementSignature(f'host:      {connect.host}')
        label_dev_port = ElementSignature(f'port:      {connect.port}')

        label_prj_sign = ElementSignature('База данных проекта\t')
        label_prj_database = ElementSignature(f'database:  {connect.database_msg}')
        label_prj_user = ElementSignature(f'user:      {connect.user_msg}')
        label_prj_pwd = ElementSignature(f'password:  {connect.password_msg}')
        label_prj_host = ElementSignature(f'host:      {connect.host_msg}')
        label_prj_port = ElementSignature(f'port:      {connect.port_msg}')
        # Кнопки
        self.button_connect_devSQL = GenFormButton('Подключиться к БД')
        self.button_connect_devSQL.setToolTip('Подключение к БД разработки')
        self.button_connect_prjSQL = GenFormButton('Подключиться к БД')
        self.button_connect_prjSQL.setToolTip('Подключение к БД проекта')
        self.button_disconnect_devSQL = GenFormButton('Отключиться от БД')
        self.button_disconnect_prjSQL = GenFormButton('Отключиться от БД')
        self.button_connect_devSQL.clicked.connect(self.connect_devSQL)
        self.button_connect_prjSQL.clicked.connect(self.connect_prjSQL)
        self.button_disconnect_devSQL.clicked.connect(self.disconnect_devSQL)
        self.button_disconnect_prjSQL.clicked.connect(self.disconnect_prjSQL)
        # Новая БД
        label_newBD_1 = ElementSignature('\tСоздание новой SQL БД разработки\t')
        label_newBD_2 = ElementSignature('Название: init_conf.cfg: [SQL] -> database: NEW_NAME')
        self.button_newDB = GenFormButton('Создать SQL БД разработки')
        self.button_newDB.setToolTip('''Создается новая БД вместе с пустыми таблицами под определенную систему(МНС, ПТ и тд.).\nНазвание БД берется из файла init_conf.cfg в разделе [SQL] - database''')
        self.button_newDB.clicked.connect(self.clicked_newDB)
        self.checkbox_sys_mns = CheckBox('МНС')
        self.checkbox_sys_pt = CheckBox('ПТ')

        layout_v1.addWidget(label_dev_sign)
        layout_v1.addWidget(label_dev_database)
        layout_v1.addWidget(label_dev_user)
        layout_v1.addWidget(label_dev_pwd)
        layout_v1.addWidget(label_dev_host)
        layout_v1.addWidget(label_dev_port)
        layout_v1.addWidget(self.button_connect_devSQL)
        layout_v1.addWidget(self.button_disconnect_devSQL)
        layout_v1.addStretch()

        layout_v2.addWidget(label_prj_sign)
        layout_v2.addWidget(label_prj_database)
        layout_v2.addWidget(label_prj_user)
        layout_v2.addWidget(label_prj_pwd)
        layout_v2.addWidget(label_prj_host)
        layout_v2.addWidget(label_prj_port)
        layout_v2.addWidget(self.button_connect_prjSQL)
        layout_v2.addWidget(self.button_disconnect_prjSQL)
        layout_v2.addStretch()

        layout_h1.addStretch()
        layout_h1.addWidget(self.checkbox_sys_mns)
        layout_h1.addWidget(self.checkbox_sys_pt)
        layout_h1.addStretch()

        layout_v3.addWidget(label_newBD_1)
        layout_v3.addWidget(label_newBD_2)
        layout_v3.addLayout(layout_h1)
        layout_v3.addWidget(self.button_newDB)
        layout_v3.addStretch()

        layout_h2.addLayout(layout_v1)
        layout_h2.addLayout(layout_v2)
        layout_h2.addLayout(layout_v3)
        layout_h2.addStretch()

    def connect_devSQL(self):
        '''Обработка клика по подключению к БД разработки.'''
        try:
            db.init(connect.database,
                    user=connect.user,
                    password=connect.password,
                    host=connect.host,
                    port=connect.port)

            if not self.dop_function.exist_check_db(connect.database,
                                                    connect.user,
                                                    connect.password,
                                                    connect.host,
                                                    connect.port):
                raise Exception('Проверь даннные для подключения к БД')

            self.logsTextEdit.logs_msg('БД разработки: подключение установлено', 0)
            self.parent.connect_SQL_edit.setText('Соединение с БД разработки установлено')
            self.parent.connect_SQL_edit.connect_true()
        except (Exception, Error) as error:
            self.logsTextEdit.logs_msg(f'Ошибка поключения к БД разработки: {error}', 2)

    def disconnect_devSQL(self):
        '''Обработка клика по отключению БД разработки.'''
        try:
            db.init(None)
            self.logsTextEdit.logs_msg('БД разработки: подключение разорвано', 2)
            self.parent.connect_SQL_edit.setText('Соединение с БД разработки разорвано')
            self.parent.connect_SQL_edit.connect_false()
        except (Exception, Error) as error:
            self.logsTextEdit.logs_msg(f'Ошибка: {error}', 2)

    def connect_prjSQL(self):
        '''Обработка клика по подключению к БД проекта.'''
        try:
            db_prj.init(connect.database_msg,
                        user=connect.user_msg,
                        password=connect.password_msg,
                        host=connect.host_msg,
                        port=connect.port_msg)

            if not self.dop_function.exist_check_db(connect.database_msg,
                                                    connect.user_msg,
                                                    connect.password_msg,
                                                    connect.host_msg,
                                                    connect.port_msg):
                raise Exception('Проверь даннные для подключения к БД')

            self.logsTextEdit.logs_msg('БД проекта: подключение установлено', 0)
            self.parent.connect_SQL_prj.setText('Соединение с БД проекта установлено')
            self.parent.connect_SQL_prj.connect_true()
        except (Exception, Error) as error:
            self.logsTextEdit.logs_msg(f'Ошибка поключения к БД проекта: {error}', 2)

    def disconnect_prjSQL(self):
        '''Обработка клика по отключению БД проекта.'''
        try:
            db_prj.init(None)
            self.logsTextEdit.logs_msg('БД проекта: подключение разорвано', 2)
            self.parent.connect_SQL_prj.setText('Соединение с БД проекта разорвано')
            self.parent.connect_SQL_prj.connect_false()
        except (Exception, Error) as error:
            self.logsTextEdit.logs_msg(f'Ошибка: {error}', 2)

    def clicked_newDB(self):
        '''Выбор системы и создание БД.'''
        obj_new_db = NewDB()
        if not self.checkbox_sys_mns.isChecked() and not self.checkbox_sys_pt.isChecked():
            self.logsTextEdit.logs_msg('Выбери систему для новой БД!', 3)
        if self.checkbox_sys_mns.isChecked():
            obj_new_db.create_new_base('MNS', self.logsTextEdit)
        if self.checkbox_sys_pt.isChecked():
            obj_new_db.create_new_base('PT', self.logsTextEdit)


class ImportKD(QWidget):
    '''Проверка и подключение к БД.'''
    def __init__(self, logtext, parent=None):
        super(ImportKD, self).__init__(parent)

        self.logsTextEdit = logtext
        self.parent = parent
        self.dop_function = DopFunction()
        self.fl_connect = False
        self.fl_load_hat = False

        button_connectKD = GenFormButton('Подключиться к КД')
        button_disconnectKD = GenFormButton('Отключиться от КД')
        button_read_table = GenFormButton('Подключиться к таблице')
        button_clear_table = GenFormButton('Очистить таблицу')
        button_add_signals = GenFormButton('Добавить сигналы нового УСО')
        button_update_signals = GenFormButton('Обновить сигналы УСО')
        # Events buttons
        button_connectKD.clicked.connect(self.connectKD)
        button_disconnectKD.clicked.connect(self.disconnectKD)
        button_read_table.clicked.connect(self.read_table)
        button_clear_table.clicked.connect(self.clear_table)
        button_add_signals.clicked.connect(self.add_new_signals)
        button_update_signals.clicked.connect(self.update_signals)

        self.combo_choise_tabl = ComboBox('Шкаф')
        self.combo_type = ComboBox('Тип')
        self.combo_shema = ComboBox('Схема')
        self.combo_basket = ComboBox('Корзина')

        self.select_row = LineEdit(placeholderText='Номер строки заголовка',
                                   clearButtonEnabled=True)

        self.combo_tag = ComboBox('Тэг')
        self.combo_klk = ComboBox('Клеммник')
        self.combo_module = ComboBox('Модуль')

        self.combo_name = ComboBox('Наименование')
        self.combo_kont = ComboBox('Контакт')
        self.combo_channel = ComboBox('Канал')

        label_type = LabelSimple('Тип')
        label_schema = LabelSimple('Схема')
        label_basket = LabelSimple('Корзина')
        label_tag = LabelSimple('Тэг')
        label_klk = LabelSimple('Клеммник')
        label_modul = LabelSimple('Модуль')
        label_name = LabelSimple('Наименование')
        label_kont = LabelSimple('Контакт')
        label_channel = LabelSimple('Канал')

        layout_v0 = QVBoxLayout()
        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()
        layout_v3 = QVBoxLayout()
        layout_v4 = QVBoxLayout(self)
        layout_h1 = QHBoxLayout()
        layout_h2 = QHBoxLayout()

        layout_v0.addWidget(button_connectKD)
        layout_v0.addWidget(button_disconnectKD)
        layout_v0.addSpacing(97)
        layout_v0.addWidget(button_clear_table)
        layout_v0.addStretch()

        layout_v1.addWidget(self.combo_choise_tabl)
        layout_v1.addWidget(label_type)
        layout_v1.addWidget(self.combo_type)
        layout_v1.addWidget(label_schema)
        layout_v1.addWidget(self.combo_shema)
        layout_v1.addWidget(label_basket)
        layout_v1.addWidget(self.combo_basket)
        layout_v1.addStretch()

        layout_v2.addWidget(self.select_row)
        layout_v2.addWidget(label_tag)
        layout_v2.addWidget(self.combo_tag)
        layout_v2.addWidget(label_klk)
        layout_v2.addWidget(self.combo_klk)
        layout_v2.addWidget(label_modul)
        layout_v2.addWidget(self.combo_module)
        layout_v2.addStretch()

        layout_v3.addWidget(button_read_table)
        layout_v3.addWidget(label_name)
        layout_v3.addWidget(self.combo_name)
        layout_v3.addWidget(label_kont)
        layout_v3.addWidget(self.combo_kont)
        layout_v3.addWidget(label_channel)
        layout_v3.addWidget(self.combo_channel)
        layout_v3.addStretch()
        layout_v3.addSpacing(10)

        layout_h1.addLayout(layout_v0)
        layout_h1.addSpacing(15)
        layout_h1.addLayout(layout_v1)
        layout_h1.addLayout(layout_v2)
        layout_h1.addLayout(layout_v3)
        layout_h1.addStretch()

        layout_h2.addSpacing(347)
        layout_h2.addWidget(button_update_signals)
        layout_h2.addSpacing(40)
        layout_h2.addWidget(button_add_signals)
        layout_h2.addStretch()

        layout_v4.addLayout(layout_h1)
        layout_v4.addLayout(layout_h2)
        layout_v4.addStretch()

    def disconnectKD(self):
        try:
            if not self.fl_connect:
                raise
            self.connectKD.disconnect_exel()
        except Exception:
            self.logsTextEdit.logs_msg('''Импорт КД: нечего разрывать!
                                       Соединение не было установлено''', 3)
            return

        self.fl_connect = False
        self.parent.connect_exel.connect_false()
        self.logsTextEdit.logs_msg('Импорт КД: соединение c Exel разорвано', 0)

    def connectKD(self):
        '''Подключение к файлу КД(КЗФКП) формата Exel.'''
        try:
            self.connectKD = Import_in_SQL(connect.path_to_exel,
                                           self.logsTextEdit)
            hat_table = self.connectKD.read_table()
            self.combo_choise_tabl.clear()
            self.combo_choise_tabl.addItems(hat_table)
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       соединение c Exel установлено''', 0)
            self.logsTextEdit.logs_msg('Импорт КД: названия шкафов обновлены', 0)
            self.parent.connect_exel.connect_true()
            self.parent.connect_exel.setText('''Импорт КД: соединение с Exel установлено''')
            self.fl_connect = True
        except Exception:
            self.logsTextEdit.logs_msg(f'''Импорт КД:
                                       ошибка поключения к файлу КД
                                       {traceback.format_exc()}''', 2)

    def read_table(self):
        '''Чтение шапки таблицы для определения позиции столбцов.'''
        name_uso = self.combo_choise_tabl.currentText()
        if not self.fl_connect:
            self.logsTextEdit.logs_msg('''Импорт КД: нет
                                       подключения к файлу Exel''', 2)
            return
        try:
            row = "".join(self.select_row.text().split())
            self.logsTextEdit.logs_msg(f'''Импорт КД: выбрано УСО: {name_uso},
                                       ряд таблицы: {int(row)}''', 1)
            self.fl_load_hat = True
        except Exception:
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       некорректный номер строки''', 2)
            return

        self.fill_combobox(self.connectKD.read_hat_table(name_uso, row, False))

    def fill_combobox(self, hat_table: dict):
        '''Заполняем названиями столбцы для верного импорта сигналов.'''
        self.combo_type.addItems(hat_table)
        self.combo_shema.addItems(hat_table)
        self.combo_basket.addItems(hat_table)
        self.combo_tag.addItems(hat_table)
        self.combo_klk.addItems(hat_table)
        self.combo_kont.addItems(hat_table)
        self.combo_module.addItems(hat_table)
        self.combo_name.addItems(hat_table)
        self.combo_channel.addItems(hat_table)

    def clear_table(self):
        '''Полная очистка(не удаление) таблицы Signals.'''
        try:
            reqsql = RequestSQL()
        except Exception:
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       невозможно обновить список.
                                       Нет подключения к БД разработки''', 2)
            return

        list_tabl = reqsql.get_tabl()
        check_table = self.dop_function.check_in_table('signals', list_tabl)
        if check_table:
            reqsql.clear_table('signals')
            self.logsTextEdit.logs_msg('Импорт КД: таблица signals очищена', 1)
        else:
            reqsql.new_table(Signals)
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       таблица signals создана в БД,
                                       т.к. её существовало''', 1)

    def hat_list(self):
        dict_column = {'type_signal': self.combo_type.currentText(),
                       'uso': '',
                       'tag': self.combo_tag.currentText(),
                       'description': self.combo_name.currentText(),
                       'schema': self.combo_shema.currentText(),
                       'klk': self.combo_klk.currentText(),
                       'contact': self.combo_kont.currentText(),
                       'basket': self.combo_basket.currentText(),
                       'module': self.combo_module.currentText(),
                       'channel': self.combo_channel.currentText()}
        return dict_column

    def add_new_signals(self):
        '''Добавление нового шкафа с сигналами.'''
        if not self.fl_load_hat:
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       необходимо подключиться к таблице''', 2)
            return
        name_uso = self.combo_choise_tabl.currentText()
        try:
            data_uso = self.connectKD.preparation_import(name_uso,
                                                         self.select_row.text(),
                                                         self.hat_list())
            self.connectKD.database_entry_SQL(data_uso, name_uso)

        except Exception:
            self.logsTextEdit.logs_msg(f'''Импорт КД:
                                       ошибка {traceback.format_exc()}''', 2)
            return

    def update_signals(self):
        '''Обновление сигналов у выбранного шкафа.'''
        if not self.fl_load_hat:
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       необходимо подключиться к таблице''', 2)
            return
        name_uso = self.combo_choise_tabl.currentText()
        try:
            data_uso = self.connectKD.preparation_import(name_uso,
                                                         self.select_row.text(),
                                                         self.hat_list())
            self.connectKD.row_update_SQL(data_uso, name_uso)

        except Exception:
            self.logsTextEdit.logs_msg(f'''Импорт КД:
                                       ошибка {traceback.format_exc()}''', 2)
            return


class GenHMIandDev(QWidget):
    '''Генерация ВУ HMI и DevStudio.'''
    def __init__(self, logtext, parent=None):
        super(GenHMIandDev, self).__init__(parent)
        self.logsTextEdit = logtext
        self.parent = parent
        self.dop_function = DopFunction()

        layout_h1 = QHBoxLayout()
        layout_v1 = QVBoxLayout(self)

        label_hmi_sign = LabelHMI('HMI')
        label_devstudio_sign = LabelHMI('DevStudio')
        self.select_row = LineEdit(placeholderText='Номер МА',
                                   clearButtonEnabled=True)
        self.select_row.setMaximumSize(135, 100)
        self.select_row.setValidator(QIntValidator())
        self.select_row.setToolTip('''Если необходимо собрать\nзашиты или готовности по конкретному МА,\nто укажи номер''')

        self.checkbox_hmi_ktpr = CheckBox('KTPR')
        self.checkbox_hmi_ktpra = CheckBox('KTPRA')
        self.checkbox_hmi_gmpna = CheckBox('GMPNA')
        self.checkbox_hmi_ktprp = CheckBox('KTPRP')
        self.checkbox_hmi_uso = CheckBox('USO')
        self.checkbox_hmi_uts = CheckBox('UTS')
        self.checkbox_hmi_upts = CheckBox('UPTS')

        self.button_gen_hmi = GenFormButton('\t\t\t\tСобрать Pictures\t\t\t\t')
        self.button_gen_hmi.clicked.connect(self.gen_hmi)

        layout_h1.addWidget(self.select_row)
        layout_h1.addWidget(self.checkbox_hmi_ktpra)
        layout_h1.addWidget(self.checkbox_hmi_gmpna)
        layout_h1.addWidget(self.checkbox_hmi_ktpr)
        layout_h1.addWidget(self.checkbox_hmi_ktprp)
        layout_h1.addWidget(self.checkbox_hmi_uso)
        layout_h1.addWidget(self.checkbox_hmi_uts)
        layout_h1.addWidget(self.checkbox_hmi_upts)
        layout_h1.addWidget(self.button_gen_hmi)

        layout_v1.addWidget(label_hmi_sign)
        layout_v1.addLayout(layout_h1)
        layout_v1.addWidget(label_devstudio_sign)
        layout_v1.addStretch()

    def object_uso(self):
        self.defence = DefenceMap(self.logsTextEdit)
        self.defence.fill_pic_new()

    def object_defence(self, table: dict, number_pump: int = None):
        '''Объект класса генерация защит.'''
        self.defence = DefenceMap(self.logsTextEdit)
        self.defence.fill_pic_new(table, number_pump)

    def object_siren(self):
        pass

    def gen_hmi(self):
        '''Клик по кнопке собрать Pictures.'''
        if self.checkbox_hmi_ktpr.isChecked():
            self.object_defence('KTPR')
        if self.checkbox_hmi_ktpra.isChecked():
            num_pump = self.select_row.text()
            if num_pump == '':
                num_pump = None
            self.object_defence('KTPRA', int(num_pump))
        if self.checkbox_hmi_gmpna.isChecked():
            num_pump = self.select_row.text()
            if num_pump == '':
                num_pump = None
            self.object_defence('GMPNA', int(num_pump))
        if self.checkbox_hmi_ktprp.isChecked():
            self.object_defence('KTPRP')

        # if self.checkbox_hmi_uso.isChecked():
        #     self.object_uso()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Генератор проекта')
        self.setFixedSize(SIZE_WORK_BACK[0], SIZE_WORK_BACK[1])
        # Журнал сообщений
        self.logsTextEdit = LogsTextEdit(self)
        self.logsTextEdit.setStyleSheet('''
                                        font:12px consolas;
                                        background-color: #f0f0f0;
                                        border-top-left-radius: 5;
                                        border-top-right-radius: 5;
                                        border-bottom-left-radius: 5;
                                        border-bottom-right-radius: 5;
                                        border: 2px solid #C4C4C3;''')
        # Основное окно с вкладками
        self.tabwidget = TabWidget()
        self.set_tabs()
        # Окно редактирования
        self.edit_window = EditTabWidget()
        self.edit_tab()
        # Нижние ряд с индикаций
        self.bottom_row()
        # Макет
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        splitter_h = QSplitter(Qt.Horizontal)
        splitter_h.addWidget(self.tabwidget)
        splitter_h.addWidget(self.edit_window)
        splitter_h.setSizes([100, 236])

        splitter_v = QSplitter(Qt.Vertical)
        splitter_v.addWidget(splitter_h)
        splitter_v.addWidget(self.logsTextEdit)
        splitter_v.setSizes(SIZE_SPLIT_V)

        layout_h = QHBoxLayout()
        layout_h.addWidget(self.clear_log)
        layout_h.addWidget(self.connect_exel)
        layout_h.addWidget(self.connect_SQL_edit)
        layout_h.addWidget(self.connect_SQL_prj)

        layout_v = QVBoxLayout(self.centralwidget)
        layout_v.addWidget(splitter_v)
        layout_v.addLayout(layout_h)

        self.logsTextEdit.logs_msg('Генератор разработки проекта запущен', 1)

    def edit_tab(self):
        '''Добавление на экран виджетов для запуска окна редактирования.'''
        tab_1 = EditWindows(self.logsTextEdit)
        self.edit_window.addTab(tab_1, 'Окно редактирования БД SQL')

    def set_tabs(self):
        tab_1 = TabConnect(self.logsTextEdit, self)
        tab_2 = ImportKD(self.logsTextEdit, self)
        tab_3 = TabConnect(self.logsTextEdit)
        tab_4 = TabConnect(self.logsTextEdit)
        tab_5 = GenHMIandDev(self.logsTextEdit)
        tab_6 = TabConnect(self.logsTextEdit)

        self.tabwidget.addTab(tab_1, 'Соединение')
        self.tabwidget.addTab(tab_2, 'Импорт КЗФКП')
        self.tabwidget.addTab(tab_3, 'SQL разработки')
        self.tabwidget.addTab(tab_4, 'SQL проекта')
        self.tabwidget.addTab(tab_5, 'ВУ')
        self.tabwidget.addTab(tab_6, 'СУ')

    def bottom_row(self):
        '''Нижний ряд с кнопкой и ииндикацией.'''
        self.connect_exel = Label()
        self.connect_exel.setText('Соединение с Exel не установлено')
        self.connect_SQL_edit = Label()
        self.connect_SQL_edit.setText('Соединение с БД разработки не установлено')
        self.connect_SQL_prj = Label()
        self.connect_SQL_prj.setText('Соединение с БД проекта не установлено')
        self.clear_log = PushButton('Очистить журнал')
        self.clear_log.clicked.connect(self.clear_jornal)
        self.clear_log.setStyleSheet("""*{
                                     font:15px consolas;
                                     background-color: #d5d90b;
                                     border: 2px solid #C4C4C3;
                                     border-bottom-color: #C2C7CB;
                                     padding: 5px;
                                     border-radius: 4}
                                     *:hover{background:#f1f520;
                                             color:'black'}
                                     *:pressed{background: '#d5d90b'}""")

    def clear_jornal(self):
        '''Чистка журнала при нажатии кнопки.'''
        self.logsTextEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec())