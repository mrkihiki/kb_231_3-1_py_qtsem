import sqlite3
import sys
from PyQt6 import uic  # Импортируем uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from start_ui import Ui_MainWindow as MainFormUI
from Form1 import Form1


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('start_ui.py', self)  # Загружаем дизайн
        self.ui = MainFormUI()
        self.ui.setupUi(self)
        self.connection = sqlite3.connect("qtsem.db")
        self.ui.pushButton.clicked.connect(lambda: self.open_form(1))
        self.ui.pushButton_2.clicked.connect(lambda: self.open_form(2))

    def open_form(self, form_number):
        cursor = self.connection.cursor()
        login = self.ui.lineEdit.text()
        if login is None or login == "":
            self.ui.label_3.setText("Введите логин")
            return
        if form_number == 1:
            if cursor.execute("SELECT 1 FROM users WHERE login = ?", (login,)).fetchone():
                if cursor.execute("SELECT 1 FROM users WHERE login = ? and password = ?",
                                  (login, self.ui.lineEdit_2.text())).fetchone():
                    self.loggin_id = cursor.execute("SELECT id FROM users WHERE login = ? and password = ?",
                                                    (login, self.ui.lineEdit_2.text())).fetchone()[0]
                    self.form = Form1(self)
                    self.form.show()
                    self.close()
                else:
                    self.ui.label_3.setText("Неправильный пароль")
            else:
                self.ui.label_3.setText("Пользователь не найден")
        elif form_number == 2:
            if cursor.execute("SELECT 1 FROM users WHERE login = ?", (login,)).fetchone() is None:
                if self.ui.lineEdit_2.text() is (None or ""):
                    self.ui.label_3.setText("Введите пароль")
                else:
                    cursor.execute(
                        "INSERT INTO users (login, password) VALUES (?, ?)",
                        (login, self.ui.lineEdit_2.text())
                    )
                    self.connection.commit()
                    self.ui.label_3.setText("Зарегистрирован")
            else:
                self.ui.label_3.setText("Ошибка: Логин уже существует")

    def closeEvent(self, event):
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
