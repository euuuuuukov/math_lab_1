from PyQt6.QtWidgets import QMainWindow, QLineEdit, QGroupBox, QVBoxLayout, QRadioButton, QPushButton, QLabel,\
    QPlainTextEdit, QApplication
from PyQt6.QtGui import QPixmap, QResizeEvent

from math import *

from random import uniform

from matplotlib import pyplot

from PIL.Image import open

from os.path import exists
from os import remove

from sys import argv


class IntegralBuilder(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Построение интегральных сумм')
        self.setMinimumSize(700, 500)

        self.function, self.start_interval, self.end_interval, self.n, self.equipment = '', 0, 0, 0, 0
        self.plot = QPixmap()

        self.input_function = QLineEdit('', self)
        self.input_function.setPlaceholderText('Функция')

        self.input_start_interval = QLineEdit('', self)
        self.input_start_interval.setPlaceholderText('Начало промежутка')

        self.input_end_interval = QLineEdit('', self)
        self.input_end_interval.setPlaceholderText('Конец промежутка')

        self.input_n = QLineEdit('', self)
        self.input_n.setPlaceholderText('Число точек разбиения')

        self.layout_equipment = QGroupBox('Оснащение:', self)
        self.choose_equipment_buttons = QVBoxLayout(self)
        self.equipments = [QRadioButton(equipment, self)
                           for equipment in ['левое', 'правое', 'среднее', 'случайная точка']]
        for i in range(1, 4):
            self.equipments[i].setChecked(False)
        self.equipments[0].setChecked(True)
        for equipment in self.equipments:
            self.choose_equipment_buttons.addWidget(equipment)
        self.layout_equipment.setLayout(self.choose_equipment_buttons)

        self.btn = QPushButton('Построить', self)
        self.btn.clicked.connect(self.get_sum)

        self.picture_ans = QLabel(self)

        self.sum_ans = QPlainTextEdit('Здесь будет значение интегральной суммы...', self)
        self.sum_ans.setReadOnly(True)

    def get_sum(self) -> None:
        try:
            self.function = self.input_function.text().replace('^', '**')
            self.start_interval = float(eval(self.input_start_interval.text()))
            self.end_interval = float(eval(self.input_end_interval.text()))
            self.n = int(self.input_n.text())
            for equipment_number in range(4):
                if self.equipments[equipment_number].isChecked():
                    self.equipment = equipment_number

            x_plot, y_plot, x_sum, y_sum = [], [], [], []
            delta = (self.end_interval - self.start_interval) / self.n
            mas = [self.start_interval + j * delta for j in range(self.n + 1)]
            for i in range(self.n):
                if self.equipment == 0:
                    current_x = mas[i]
                elif self.equipment == 1:
                    current_x = mas[i + 1]
                elif self.equipment == 2:
                    current_x = (mas[i] + mas[i + 1]) / 2
                else:
                    current_x = uniform(mas[i], mas[i + 1])
                f_res = self.f(current_x)
                x_plot.append(current_x)
                y_plot.append(f_res)
                x_sum.extend([mas[i], mas[i + 1]])
                y_sum.extend([f_res, f_res])

            pyplot.clf()
            pyplot.axis((self.start_interval, self.end_interval, min(y_plot), max(y_plot)))
            pyplot.bar(mas, [0 for _ in range(self.n + 1)], color='cyan', label='Интегральная сумма', width=0)
            pyplot.plot(x_plot, y_plot, color='green', label='График функции')
            pyplot.fill_between(x_sum, y_sum, color='cyan')
            pyplot.xlabel('x')
            pyplot.ylabel('y')
            pyplot.title('Расчет интегральной суммы')
            pyplot.legend()

            pyplot.savefig('image.png')
            open('image.png').resize((self.picture_ans.width(), self.picture_ans.height())).save('image2.png')

            self.plot = QPixmap('image2.png')
            self.picture_ans.setPixmap(self.plot)

            remove('image2.png')

            self.sum_ans.setPlainText(f'Значение интегральной суммы:\n{sum(y_plot) * delta}')

        except Exception as exc:
            self.sum_ans.setPlainText(f'Не все поля заполнены корректно!\n{exc}\n{type(exc)}')
            self.picture_ans.setPixmap(QPixmap())

    def f(self, x):
        return float(eval(self.function.replace('x', str(x))))

    def resizeEvent(self, event: QResizeEvent) -> None:
        width, height = self.width(), self.height()
        widget_width, widget_height = (width - width // 20 * 3) // 2, (height - height // 20 * 6) // 9
        space_width, space_height = width // 20, height // 20
        left_interval_height = (widget_width - space_width) // 2

        self.input_function.resize(widget_width, widget_height)
        self.input_function.move(space_width, space_height)

        self.input_start_interval.resize((widget_width - space_width) // 2, widget_height)
        self.input_start_interval.move(space_width, space_height * 2 + widget_height)

        self.input_end_interval.resize(left_interval_height, widget_height)
        self.input_end_interval.move(space_width * 2 + left_interval_height, space_height * 2 + widget_height)

        self.input_n.resize(widget_width, widget_height)
        self.input_n.move(space_width, space_height * 3 + widget_height * 2)

        self.layout_equipment.resize(widget_width, widget_height * 5)
        self.layout_equipment.move(space_width, space_height * 4 + widget_height * 3)

        self.btn.resize(widget_width, widget_height)
        self.btn.move(space_width, space_height * 5 + widget_height * 8)

        self.picture_ans.resize(widget_width, height - space_height * 3 - widget_height * 2)
        self.picture_ans.move(width - space_width - widget_width, space_height)

        if exists('image.png'):
            open('image.png').resize((widget_width, height - space_height * 3 - widget_height * 2)).save('image2.png')
            self.plot = QPixmap('image2.png')
            self.picture_ans.setPixmap(self.plot)
            remove('image2.png')

        self.sum_ans.resize(widget_width, widget_height * 2)
        self.sum_ans.move(width - space_width - widget_width, height - widget_height * 2 - space_height)


app = QApplication(argv)
integral_builder = IntegralBuilder()
integral_builder.show()
app.exec()
if exists('image.png'):
    remove('image.png')
