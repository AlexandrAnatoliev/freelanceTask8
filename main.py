# freelanceTask8

# N работ могут исполняться n исполнителями. Известно время исполнения каждой работы каждым исполнителем tij,ij=1..n
# Распределить работы между исполнителями так, чтобы каждая работа выполнялась одним исполнителем,
# каждый исполнитель выполнял одну работу, а суммарное время выполнения всех работ было минимальным.

# Метод решения простым перебором комбинаций

import math


class Data:
    """
    Дескриптор данных
    """

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        """
        Позволяет возвращать данные
        """
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        """
        Позволяет изменять значение данных
        """
        setattr(instance, self.name, value)


class Cell:
    """
    Класс, содержащий данные конкретной ячейки таблицы
                Работа1     Работа2     Работа3

        Имя1    время11     время12     время13
        Имя2    время21     время22     время23
        Имя3    время31     время32     время33
    """
    name = Data()  # объекты-свойства для считывания и изменения данных
    work = Data()
    x_coord = Data()
    y_coord = Data()
    time_zero = Data()
    fl_zero = Data()

    def __init__(self, value, name, work, x, y):
        """
        Данные ячейки при инициализации
        :param value: время выполнения работы (конкретным работником конкретной работы)
        :param name: имя исполнителя
        :param work: наименование работы
        :param x: координаты ячейки в матрице
        :param y: координаты ячейки в матрице
        """
        self.__value = value  # __чтобы случайно не изменить значение
        self.name = name
        self.work = work
        self.x_coord = x
        self.y_coord = y
        self.time_zero = None  # переменная для расчетов - изменяется в процессе расчета
        self.fl_zero = True  # можно ли вычеркнуть ноль, True - можно, False - ноль уже вычеркнут

    @property
    def value(self):
        """
        :return: возвращает время выполнения работы (только возвращает - не изменяет)
        """
        return self.__value


class Matrix:
    """
        Класс, описывающий взаимодействие ячеек таблицы в процессе расчета
                    Работа1     Работа2     Работа3

            Имя1    время11     время12     время13
            Имя2    время21     время22     время23
            Имя3    время31     время32     время33
        """

    def __init__(self):
        self.cells_list = []  # список объектов-ячеек
        self.len_matrix = None  # длина квадратной матрицы

    def add_cell(self, cell):
        """Добавляем новую ячейку"""
        self.cells_list.append(cell)

    def add_len_matrix(self, len_matrix):
        """Вычисляем длину квадратной матрицы"""
        self.len_matrix = len_matrix

    def line_reduct(self):
        """
        Редукция матрицы по строкам
        [1, 2, 3] -> min_value_line == 1 -> [1 - 1, 2 - 1, 3 - 1] -> [0, 1, 2]

                [1,  2,  3]
                 4   5   6
                 7   8   9

        """
        for x in range(self.len_matrix):
            min_value_line = math.inf  # бесконечность
            for y in range(self.len_matrix):
                cell = self.get_cell(x, y)
                value = cell.value
                min_value_line = min(min_value_line, value)  # вычисляем минимальный элемент строки
            for y in range(self.len_matrix):
                cell = self.get_cell(x, y)
                # из каждого элемента строки вычитаем минимальный элемент
                cell.time_zero = cell.value - min_value_line

    def column_reduct(self):
        """
        Редукция матрицы по столбцам
        [1, 4, 7] -> min_value_line == 1 -> [1 - 1, 4 - 1, 7 - 1] -> [0, 3, 6]

                [1,  2   3
                 4,  5   6
                 7]  8   9

        """
        for y in range(self.len_matrix):
            min_value_column = math.inf  # бесконечность
            for x in range(self.len_matrix):
                cell = self.get_cell(x, y)
                value = cell.time_zero
                min_value_column = min(min_value_column, value)  # вычисляем минимальный элемент столбца
            for x in range(self.len_matrix):
                cell = self.get_cell(x, y)
                # из каждого элемента столбца вычитаем минимальный элемент
                cell.time_zero = cell.time_zero - min_value_column

    def get_cell(self, x, y):
        """
        Возвращает ссылку на ячейку по ее координатам в матрице
        :param x: координата x
        :param y: координата y
        :return: ссылка на объект класса Cell
        """
        cell = [cell for cell in self.cells_list if cell.x_coord == x and cell.y_coord == y]
        return cell[0]

    def is_answer(self):
        """
        Возвращает True, если в каждой строке и каждом столбце только один ноль - т.е есть ответ
        :return: True/False
        """
        for x in range(self.len_matrix):
            if self.count_zero_x(x) != 1:
                return False
        for y in range(self.len_matrix):
            if self.count_zero_y(y) != 1:
                return False
        return True

    def get_answer(self):
        """
        Возвращет список возможных ответов - клеток с нулями
        :return: список со ссылками на объекты класса Cell
        """
        answer = [cell for cell in self.cells_list if cell.time_zero == 0]
        return answer

    def count_zero_x(self, x):
        """
        Подсчитывает количество нулей в строке
        :param x: с координатой x
        :return: количество нулей
        """
        count = 0
        for y in range(self.len_matrix):
            cell = self.get_cell(x, y)
            if cell.time_zero == 0 and cell.fl_zero is True:
                count += 1
        return count

    def count_zero_y(self, y):
        """
        Подсчитывает количество нулей в столбце
        :param y: с координатой y
        :return: количество нулей
        """
        count = 0
        for x in range(self.len_matrix):
            cell = self.get_cell(x, y)
            if cell.time_zero == 0 and cell.fl_zero is True:
                count += 1
        return count

    def del_line_column(self):
        """

        :return:
        """
        while self.check_fl_zero():  # пока есть невычеркнутые нули
            max_cnt_z_x = 0
            coord_z_x = None
            for x in range(self.len_matrix):
                if self.count_zero_x(x) > max_cnt_z_x:  # если в строке x число нулей максимально
                    max_cnt_z_x = self.count_zero_x(x)  # сохраняем количество нулей
                    coord_z_x = x  # сохраняем координату строки
            max_cnt_z_y = 0
            coord_z_y = None
            for y in range(self.len_matrix):
                if self.count_zero_y(y) > max_cnt_z_y:  # если в столбце y число нулей максимально
                    max_cnt_z_y = self.count_zero_y(y)  # сохраняем количество нулей
                    coord_z_y = y  # сохраняем координату столбца
            if max_cnt_z_x > max_cnt_z_y and coord_z_x is not None:
                # удаляем строку или столбец с максимальным количеством нулей
                self.del_zero_line(coord_z_x)
            elif max_cnt_z_x < max_cnt_z_y and coord_z_y is not None:
                self.del_zero_column(coord_z_y)
            elif max_cnt_z_x == max_cnt_z_y and coord_z_x is not None and coord_z_y is not None:
                # если количество невычеркнутых нулей в столбцах и ячейках равно
                if self.count_false_x(coord_z_x) > self.count_false_y(coord_z_y):
                    # вычеркиваем строку или столбец с большим количеством уже вычеркнутых нулей
                    self.del_zero_line(coord_z_x)
                else:
                    self.del_zero_column(coord_z_y)

    def check_fl_zero(self):
        """
        Проверяет, есть ли клетки с нулями, которые еще можно вычеркнуть
        :return: True/False
        """
        for cell in self.cells_list:
            if cell.fl_zero is True and cell.time_zero == 0:
                return True
        return False

    def count_false_x(self, x):
        """
        Возвращает количество вычеркнутых ячеек
        :param x: в строке x
        :return: количество вычеркнутых ячеек
        """
        count = 0
        for y in range(self.len_matrix):
            cell = self.get_cell(x, y)
            if cell.fl_zero is False:
                count += 1
        return count

    def count_false_y(self, y):
        """
        Возвращает количество вычеркнутых ячеек
        :param y: в столбце y
        :return: количество вычеркнутых ячеек
        """
        count = 0
        for x in range(self.len_matrix):
            cell = self.get_cell(x, y)
            if cell.fl_zero is False:
                count += 1
        return count

    def del_zero_line(self, coord_z_x):
        """
        Вычеркиваем строку - присваиваем параметру fl_zero ячеек значение False
        :param coord_z_x: координата x строки
        """
        for cell in self.cells_list:
            if cell.x_coord == coord_z_x:
                cell.fl_zero = False

    def del_zero_column(self, coord_z_y):
        """
        Вычеркиваем столбец - присваиваем параметру fl_zero ячеек значение False
        :param coord_z_y: координата y столбца
        """
        for cell in self.cells_list:
            if cell.y_coord == coord_z_y:
                cell.fl_zero = False

    def matrix_reduct(self):
        """
        Вычисляется min_value - минимальное значение time_zero у невычеркнутых ячеек.
        Из значения time_zero невычеркнутых ячеек вычитается min_value
        К значению time_zero вычеркнутых ячеек прибавляется min_value
        """
        non_del_list = [cell.time_zero for cell in self.cells_list if cell.fl_zero is True]
        del_list = [cell.time_zero for cell in self.cells_list if cell.fl_zero is False]
        min_value = min(non_del_list)
        for cell in non_del_list:
            cell.time_zero -= min_value
        for cell in del_list:
            cell.time_zero += min_value

    def if_too_math_zero(self):
        """
        В случае, если в каждой строке и столбце есть хотя бы один ноль, но их количество больше одного,
        осуществляется поиск варианта при котором будет лишь один ноль в каждой строке и столбце
        :return: список ответов
        """
        count = self.len_matrix
        while count != 0:
            x_fl = [True for i in range(self.len_matrix)]
            y_fl = [True for i in range(self.len_matrix)]
            answers = []
            start = self.len_matrix - count
            finish = start
            answer_list = self.get_answer()[start:] + self.get_answer()[:finish]
            for answ in answer_list:
                if x_fl[answ.x_coord] is True and y_fl[answ.y_coord] is True:
                    answers.append(answ)
                    x_fl[answ.x_coord] = False
                    y_fl[answ.y_coord] = False
                if len(answers) == self.len_matrix:
                    return answers
            else:
                count -= 1
        return answers


def check_input(nms, wrk):
    """
    Проверка квадратности таблицы
    :param nms: список имен
    :param wrk: список работ
    :return: True/False
    """
    if len(nms) != len(wrk):
        print("Количество работ должно равняться количеству работников!")
        return False
    return True


def user_input_names():
    """
    Формирование двух списков
    :return: список имен, список работ
    """
    nms = list(map(str, input("Перечислите имена исполнителей в строку через пробел: ").split()))
    wrk = list(map(str, input("Перечислите названия выполняемых работ в строку через пробел: ").split()))
    return nms, wrk


def user_input_times(nms, wrks):
    """
    Формирует список клеток - объектов класса Cell
    :param nms: список имен
    :param wrks: список работ
    :return: список клеток
    """
    m = Matrix()
    m.add_len_matrix(len(nms))
    for x, nm in enumerate(nms):
        for y, wr in enumerate(wrks):
            tm = int(input(f"Введите время за которое {nm} выполнит работу {wr}: "))
            m.add_cell(Cell(tm, nm, wr, x, y))
    return m


names, works = user_input_names()  # два списка с именами и работами

while check_input(names, works) is False:
    print("Введите данные еще раз")
    names, works = user_input_names()

cl = user_input_times(names, works)  # объект класса Matrix - список клеток
count = 2  # две попытки вычислить ответ через редукцию
fl = True
while count != 0 or fl is False:
    cl.line_reduct()  # редукция по строкам -> [1, 2, 3] -> min = 1 -> [1 - 1, 2 - 1, 3 - 1] -> [0, 1, 2]
    cl.column_reduct()  # редукция по столбцам
    if cl.is_answer():  # если в каждой строчке и столбце только один ноль
        # for answer in cl.get_answer():
        #     print(f"{answer.name} выполнит работу {answer.work} за время {answer.value}")
        fl = False
    else:
        cl.del_line_column()  # вычеркиваем строки и столбцы с нулями
        cl.column_reduct()
        if cl.is_answer():
            # for answer in cl.get_answer():
            #     print(f"{answer.name} выполнит работу {answer.work} за время {answer.value}")
            fl = False
    count -= 1

if cl.is_answer():
    for answer in cl.get_answer():
        print(f"{answer.name} выполнит работу {answer.work} за время {answer.value}")
else:  # если нулей слишком много - подбираем ответ
    for answer in cl.if_too_math_zero():
        print(f"{answer.name} выполнит работу {answer.work} за время {answer.value}")
