import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
sys.path.append('../Project_Signal_Generator')
from logging_text import LogsTextEdit
from windows_base_editing import MainWindow as WinEditing
from main_base import General_functions as DopFunction
from models import connect

IMG_TABLE = 'graphic_arts/fon_table.jpg'
SIZE_WORK_BACK = (1200, 500)
SIZE_SPLIT_V = [500, 150]
SIZE_SPLIT_H = [602, 50]


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
                                padding: 3px;
                                border-radius: 4}
                                *:hover{background:#c0deb8;
                                        color:'black'}
                                *:pressed{background: '#7ce063'}""")


class Label(QLabel):
    '''Конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.setStyleSheet('''
                           background-color: #d95050;
                           border: 2px solid #C4C4C3;
                           border-radius: 4;
                           padding: 8px;
                           font:12px consolas;''')


class ElementSignature(QLabel):
    '''Конструктор класса текста.
    Подаись элемента виджета'''
    def __init__(self, *args, **kwargs):
        super(ElementSignature, self).__init__(*args, **kwargs)
        self.setStyleSheet('''
                           border-radius: 4;
                           padding: 0px;
                           font: 15px consolas;''')


class GenProject(QWidget):
    def __init__(self, parent=None):
        super(GenProject, self).__init__(parent)


class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super(ComboBox, self).__init__(*args, **kwargs)
        self.setStyleSheet('''
                           background: #f0f0f0;
                           padding: 0px;
                           font: 15px consolas;''')


class EditWindows(QWidget):
    '''Конструктор класса редактирования окна разработки.'''
    def __init__(self, logtext, parent=None):
        super(EditWindows, self).__init__(parent)

        self.logsTextEdit = logtext
        layout_v = QVBoxLayout(self)

        label_choise_tabl = ElementSignature('Выбери таблицу:')
        label_choise_tabl.setAlignment(Qt.AlignCenter)
        self.combo_choise_tabl = ComboBox()
        self.button_connect_1 = GenFormButton('Окно редактора №1')
        self.button_connect_2 = GenFormButton('Окно редактора №2')
        self.button_update = GenFormButton('Обновить список')

        self.button_update.setToolTip('Обновление списка таблиц после изменения БД')

        self.button_connect_1.clicked.connect(self.open_window1)
        self.button_connect_2.clicked.connect(self.open_window2)
        self.button_update.clicked.connect(self.update_list)

        layout_v.addWidget(label_choise_tabl)
        layout_v.addWidget(self.combo_choise_tabl)
        layout_v.addWidget(self.button_connect_1)
        layout_v.addWidget(self.button_connect_2)
        layout_v.addStretch()
        layout_v.addWidget(self.button_update)

    def open_window1(self):
        '''Выполнение по клику кнопки.
        Открытие окна редактирования БД 1.'''
        name_table = self.combo_choise_tabl.currentText()
        self.open_w1 = WinEditing(name_table)
        self.open_w1.show()
        self.logsTextEdit.logs_msg('Открыто окно для редактирования №1', 1)

    def open_window2(self):
        '''Выполнение по клику кнопки.
        Открытие окна редактирования БД 2.'''
        name_table = self.combo_choise_tabl.currentText()
        self.open_w2 = WinEditing(name_table)
        self.open_w2.show()
        self.logsTextEdit.logs_msg('Открыто окно для редактирования №2', 1)

    def update_list(self):
        '''Функция обновляет список таблиц по команде.'''
        dop_function = DopFunction()
        list_tabl = dop_function.all_tables()
        for tabl in list_tabl:
            self.combo_choise_tabl.addItem(str(tabl))
        self.logsTextEdit.logs_msg('Список таблиц обновлен', 1)


class TabConnect(QWidget):
    '''Конструктор класса. Проверка и подключение к БД.'''
    def __init__(self, logtext, parent=None):
        super(TabConnect, self).__init__(parent)

        self.logsTextEdit = logtext
        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()
        layout_h = QHBoxLayout(self)

        label_dev_sign = ElementSignature('База данных разработки\t\t')
        label_dev_database = ElementSignature(f'database:  {connect.database}')
        label_dev_user = ElementSignature(f'user:      {connect.user}')
        label_dev_pwd = ElementSignature(f'password:  {connect.password}')
        label_dev_host = ElementSignature(f'host:      {connect.host}')
        label_dev_port = ElementSignature(f'port:      {connect.port}')

        label_prj_sign = ElementSignature('База данных проекта')
        label_prj_database = ElementSignature(f'database:  {connect.database_msg}')
        label_prj_user = ElementSignature(f'user:      {connect.user_msg}')
        label_prj_pwd = ElementSignature(f'password:  {connect.password_msg}')
        label_prj_host = ElementSignature(f'host:      {connect.host_msg}')
        label_prj_port = ElementSignature(f'port:      {connect.port_msg}')

        layout_v1.addWidget(label_dev_sign)
        layout_v1.addWidget(label_dev_database)
        layout_v1.addWidget(label_dev_user)
        layout_v1.addWidget(label_dev_pwd)
        layout_v1.addWidget(label_dev_host)
        layout_v1.addWidget(label_dev_port)
        layout_v1.addStretch()

        layout_v2.addWidget(label_prj_sign)
        layout_v2.addWidget(label_prj_database)
        layout_v2.addWidget(label_prj_user)
        layout_v2.addWidget(label_prj_pwd)
        layout_v2.addWidget(label_prj_host)
        layout_v2.addWidget(label_prj_port)
        layout_v2.addStretch()

        layout_h.addLayout(layout_v1)
        layout_h.addLayout(layout_v2)
        layout_h.addStretch()


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
        splitter_h.setSizes(SIZE_SPLIT_H)

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
        tab_1 = TabConnect(self.logsTextEdit)
        tab_2 = TabConnect(self.logsTextEdit)
        tab_3 = TabConnect(self.logsTextEdit)
        tab_4 = TabConnect(self.logsTextEdit)
        tab_5 = TabConnect(self.logsTextEdit)
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
        self.connect_SQL_edit.setText('Соединение с БД разработки не установлена')
        self.connect_SQL_prj = Label()
        self.connect_SQL_prj.setText('Соединение с БД проекта не установлена')
        self.clear_log = PushButton()
        self.clear_log.setText('Очистить журнал')
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec())