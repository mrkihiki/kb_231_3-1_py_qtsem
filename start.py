import sys
from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from start_ui import Ui_MainWindow as MainFormUI
#from Form6 import Form6

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        #uic.loadUi('start_ui.py', self)  # Загружаем дизайн
        self.ui = MainFormUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.open_form(1))

    def open_form(self, form_number):
        #self.form = Form1(self)
        self.form.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())