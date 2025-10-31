from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QSpinBox, QWidget, \
    QVBoxLayout

from Form1_ui import Ui_MainWindow as Form1_ui
from player import VideoMessageBox
from Form1_1 import Form1_1


class Form1(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.ui = Form1_ui()
        self.ui.setupUi(self)
        self.parent = args[-1]
        self.bool = True
        self.sort_item = 0
        self.ui.pushButton.clicked.connect(lambda: self.run(1))
        self.ui.pushButton_4.clicked.connect(lambda: self.run(2))
        self.ui.pushButton_3.clicked.connect(lambda: self.run(3))
        self.ui.pushButton_2.clicked.connect(lambda: self.run(4))
        self.select_data(0)
        self.ui.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.on_right_click)

    def run(self, form_number):
        cursor = self.parent.connection.cursor()
        if form_number == 1:
            name = self.res[self.ui.spinBox.value() - 1][1]
            dish_id = cursor.execute("SELECT id FROM dishes WHERE name = ?", (name,)).fetchone()[0]

            # Создаем QMessageBox
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Выбор числа")
            msg_box.setText("Выберите число от 1 до 5:")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            # Создаем SpinBox
            spin_box = QSpinBox()
            spin_box.setRange(1, 5)
            spin_box.setValue(1)

            # Добавляем SpinBox в QMessageBox
            msg_box.layout().addWidget(spin_box)
            if cursor.execute("SELECT 1 FROM dish_ratings WHERE dish_id = ? and user_id = ?",
                              (dish_id, self.parent.loggin_id)).fetchone():
                # Показываем диалог и получаем результат
                result = msg_box.exec()
                if result == QMessageBox.StandardButton.Ok:
                    cursor.execute(
                        "UPDATE dish_ratings SET rating = ? WHERE user_id = ? AND dish_id = ?;",
                        (int(spin_box.value()), int(self.parent.loggin_id), int(dish_id))
                    )
                    self.parent.connection.commit()
                else:
                    return None
            else:
                # Показываем диалог и получаем результат
                result = msg_box.exec()
                if result == QMessageBox.StandardButton.Ok:
                    cursor.execute(
                        "INSERT INTO dish_ratings (user_id, dish_id, rating) VALUES (?, ?, ?)",
                        (int(self.parent.loggin_id), int(dish_id), int(spin_box.value()))
                    )
                    self.parent.connection.commit()
                else:
                    return None
            self.select_data(self.sort_item)

        elif form_number == 2:
            name = self.res[self.ui.spinBox.value() - 1][1]
            dish_id = cursor.execute("SELECT id FROM dishes WHERE name = ?", (name,)).fetchone()[0]
            if cursor.execute("SELECT 1 FROM favourites WHERE dishes_id = ? and user_id = ?",
                              (dish_id, self.parent.loggin_id)).fetchone():
                cursor.execute("DELETE FROM favourites WHERE user_id = ? and dishes_id = ?",
                               (int(self.parent.loggin_id), int(dish_id)))
                self.select_data(self.sort_item)
            else:
                cursor.execute(
                    "INSERT INTO favourites (user_id, dishes_id) VALUES (?, ?)",
                    (int(self.parent.loggin_id), int(dish_id))
                )
                self.parent.connection.commit()
                self.select_data(self.sort_item)

        elif form_number == 3:
            self.form1_1 = Form1_1(self)
            self.form1_1.show()
            self.bool = False
            self.close()

        elif form_number == 4:
            if self.ui.comboBox.currentText() == "":
                self.sort_item = 0
                self.select_data(self.sort_item)
            elif self.ui.comboBox.currentText() == "рейтинг":
                self.sort_item = 1
                self.select_data(self.sort_item)
            elif self.ui.comboBox.currentText() == "избранное":
                self.sort_item = 2
                self.select_data(self.sort_item)

    def select_data(self, sort_item):
        # Получим таблицу
        query = "SELECT * FROM dishes_with_ratings"
        self.res = self.parent.connection.cursor().execute(query).fetchall()
        names = [item[0] for item in
                 self.parent.connection.cursor().execute(
                     "SELECT name FROM pragma_table_info('dishes_with_ratings')").fetchall()]
        # Заполним размеры таблицы
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setHorizontalHeaderLabels(names[0:2] + names[4:6])
        favourites = [item[0] for item in self.parent.connection.cursor().execute(
            "SELECT dishes_id FROM favourites WHERE user_id = ?",
            (int(self.parent.loggin_id),)  # Запятая важна для кортежа с одним элементом
        ).fetchall()]
        if sort_item == 1:
            self.res = sorted(self.res, key=lambda x: x[4], reverse=True)
        # Заполняем таблицу элементами
        ii = -1
        if sort_item == 2:
            self.res = list(filter(lambda x: x[0] in favourites, self.res))
        for i, row in enumerate(self.res):
            ii += 1
            self.ui.tableWidget.setRowCount(
                self.ui.tableWidget.rowCount() + 1)
            jj = 0
            for j, elem in enumerate(row):
                if j in [0, 1, 4, 5]:
                    if j == 0:
                        self.ui.tableWidget.setItem(
                            ii, jj, QTableWidgetItem(str(ii + 1)))
                    else:
                        self.ui.tableWidget.setItem(ii, jj, QTableWidgetItem(str(elem)))
                    if str(row[0]) in str(favourites):
                        self.ui.tableWidget.item(ii, jj).setBackground(QColor('yellow'))
                    jj += 1
        self.ui.spinBox.setMaximum(self.ui.tableWidget.rowCount())

    def on_right_click(self, position):
        # Обработчик правого клика
        index = self.ui.tableWidget.indexAt(position)

        if index.isValid():
            row = index.row()
            column = index.column()
            self.show_popup_info(row, column)

    def show_popup_info(self, row, column):
        # Показывает всплывающее окно с информацией
        item = self.ui.tableWidget.item(row, column)
        if item:
            # Получаем данные из базы для этой строки
            dish_data = self.res[row]

            # Создаем детализированное сообщение
            title = f"Информация: {dish_data[1]}"  # Название

            message = f"""
            🍽️ Детальная информация о блюде:

            • ID: {dish_data[0]}
            • Название: {dish_data[1]}
            • примерные ингредиенты: {dish_data[2]}
            • Рейтинг: {dish_data[4]}
            """
            video_url = dish_data[3]
            dlg = VideoMessageBox(self, title, message.strip(), video_url)
            dlg.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def closeEvent(self, event):
        event.accept()  # Разрешаем закрытие
        if self.bool:
            del self.parent.loggin_id
            self.parent.show()
