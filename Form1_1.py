import sqlite3
from datetime import date

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox

from Form1_1_ui import Ui_MainWindow as Form1_1_ui


class Form1_1(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.ui = Form1_1_ui()
        self.ui.setupUi(self)
        self.parent = args[-1]
        self.id = int(self.parent.ui.spinBox.text())
        self.ui.pushButton.clicked.connect(self.run)
        self.ui.pushButton_2.clicked.connect(self.close)

    @staticmethod
    def is_youtube_link(url):
        return "youtube.com" in url or "youtu.be" in url

    def run(self):
        params = [
            self.ui.lineEdit.text(),
            str(self.ui.textEdit.toPlainText()),
            self.ui.lineEdit_2.text(),
        ]
        params[0] = " ".join(params[0].split())
        if "" in [" ".join(self.ui.lineEdit.text().split()), " ".join(str(self.ui.textEdit.toPlainText()).split())]:
            QMessageBox.warning(
                self, '', "Заполните все столбцы",
                QMessageBox.StandardButton.Ok)
            return
        if not self.is_youtube_link(self.ui.lineEdit_2.text()) and not "" == self.ui.lineEdit_2.text():
            QMessageBox.warning(
                self, '', "Неверная ссылка",
                QMessageBox.StandardButton.Ok)
            return
        cur = self.parent.parent.connection.cursor()
        # if self.parent.bool_new:
        if "" == self.ui.lineEdit_2.text():
            que = "INSERT INTO dishes (name, ingredients) VALUES(?, ?)"
            params = [
                self.ui.lineEdit.text(),
                str(self.ui.textEdit.toPlainText()),
            ]
            params[0] = " ".join(params[0].split())
        else:
            que = "INSERT INTO dishes (name, ingredients, url) VALUES(?, ?, ?)"
        cur.execute(que, params)
        self.parent.parent.connection.commit()
        self.parent.select_data(0)
        self.close()
        # else:
        #     que = "UPDATE films SET\n"
        #     que += ", ".join([f"{col} = ?" for col in self.parent.names[1:]])
        #     que += " WHERE id = ?"
        #     print(que)
        #     cur.execute(que, (params + [int(self.id)]))
        #     self.parent.connection.commit()
        #     self.parent.select_data()
        #     self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def closeEvent(self, event):
        # self.connection.close()
        event.accept()  # Разрешаем закрытие
        self.parent.bool = True
        self.parent.show()
