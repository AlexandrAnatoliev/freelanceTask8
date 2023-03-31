# freelanceTask8

# N работ могут исполняться n исполнителями. Известно время исполнения каждой работы каждым исполнителем tij,ij=1..n
# Распределить работы между исполнителями так, чтобы каждая работа выполнялась одним исполнителем,
# каждый исполнитель выполнял одну работу, а суммарное время выполнения всех работ было минимальным.

# Метод решения простым перебором комбинаций

import math


class Data:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Cell:
    name = Data()
    work = Data()
    x_coord = Data()
    y_coord = Data()
    time_zero = Data()
    fl_zero = Data()

    def __init__(self, value, name, work, x, y):
        self.__value = value  # чтобы случайно не изменить значение
        self.name = name
        self.work = work
        self.x_coord = x
        self.y_coord = y
        self.time_zero = None
        self.fl_zero = True

    @property
    def value(self):
        return self.__value


class Matrix:
    def __init__(self):
        self.cells_list = []
        self.len_matrix = None

    def add_cell(self, cell):
        self.cells_list.append(cell)

    def add_len_matrix(self, len_matrix):
        self.len_matrix = len_matrix

        # редукция матрицы по строкам

    def line_reduct(self):
        """
                Работа1     Работа2     Работа3

        Имя1    время11     время12     время13
        Имя2    время21     время22     время23
        Имя3    время31     время32     время33

        :return:
        """
        for x in range(self.len_matrix):
            min_value_line = math.inf  # бесконечность
            for y in range(self.len_matrix):
                cell = self.get_cell(x, y)
                value = cell.value
                min_value_line = min(min_value_line, value)
            for y in range(self.len_matrix):
                cell = self.get_cell(x, y)
                cell.time_zero = cell.value - min_value_line

    def column_reduct(self):
        for y in range(self.len_matrix):
            min_value_column = math.inf
            for x in range(self.len_matrix):
                cell = self.get_cell(x, y)
                value = cell.time_zero
                min_value_column = min(min_value_column, value)
            for x in range(self.len_matrix):
                cell = self.get_cell(x, y)
                cell.time_zero = cell.time_zero - min_value_column

    def get_cell(self, x, y):
        cell = [cell for cell in self.cells_list if cell.x_coord == x and cell.y_coord == y]
        return cell[0]

    def is_answer(self):
        for x in range(self.len_matrix):
            if self.count_zero_x(x) != 1:
                return False
        for y in range(self.len_matrix):
            if self.count_zero_y(y) != 1:
                return False
        return True

    def get_answer(self):
        answer = [cell for cell in self.cells_list if cell.time_zero == 0]
        return answer

    def count_zero_x(self, x):
        count = 0
        for y in range(self.len_matrix):
            cell = self.get_cell(x, y)
            if cell.time_zero == 0 and cell.fl_zero is True:
                count += 1
        return count

    def count_zero_y(self, y):
        count = 0
        for x in range(self.len_matrix):
            cell = self.get_cell(x, y)
            if cell.time_zero == 0 and cell.fl_zero is True:
                count += 1
        return count

    def del_line_column(self):
        while self.check_fl_zero():
            count_zero_x = 0
            coord_z_x = None
            for x in range(self.len_matrix):
                if self.count_zero_x(x) > count_zero_x:
                    count_zero_x = self.count_zero_x(x)
                    coord_z_x = x
            count_zero_y = 0
            coord_z_y = None
            for y in range(self.len_matrix):
                if self.count_zero_y(y) > count_zero_y:
                    count_zero_y = self.count_zero_y(y)
                    coord_z_y = y
            if count_zero_x > count_zero_y and coord_z_x is not None:
                self.del_zero_line(coord_z_x)
            elif count_zero_x < count_zero_y and coord_z_y is not None:
                self.del_zero_column(coord_z_y)
            elif count_zero_x == count_zero_y and coord_z_x is not None and coord_z_y is not None:
                if self.count_false_x(coord_z_x) > self.count_false_y(coord_z_y):
                    self.del_zero_line(coord_z_x)
                else:
                    self.del_zero_column(coord_z_y)

    def count_false_x(self, x):
        count = 0
        for y in range(self.len_matrix):
            cell = self.get_cell(x, y)
            if cell.fl_zero is False:
                count += 1
        return count

    def count_false_y(self, y):
        count = 0
        for x in range(self.len_matrix):
            cell = self.get_cell(x, y)
            if cell.fl_zero is False:
                count += 1
        return count

    def del_zero_line(self, coord_z_x):
        for cell in self.cells_list:
            if cell.x_coord == coord_z_x:
                cell.fl_zero = False

    def del_zero_column(self, coord_z_y):
        for cell in self.cells_list:
            if cell.y_coord == coord_z_y:
                cell.fl_zero = False

    def check_fl_zero(self):
        for cell in self.cells_list:
            if cell.fl_zero is True and cell.time_zero == 0:
                return True
        return False

    def matrix_reduct(self):
        non_zero_list = [cell.time_zero for cell in self.cells_list if cell.fl_zero is True]
        zero_list = [cell.time_zero for cell in self.cells_list if cell.fl_zero is False]
        min_value = min(non_zero_list)
        for cell in non_zero_list:
            cell.time_zero -= min_value
        for cell in zero_list:
            cell.time_zero += min_value

    def if_too_math_zero(self):
        count = self.len_matrix
        while count != 0:
            x_fl = [True for i in range(self.len_matrix)]
            y_fl = [True for i in range(self.len_matrix)]
            answers = []
            start = self.len_matrix - count
            finish = start + 1
            for answ in (self.get_answer()[start:] + self.get_answer()[:finish]):
                if x_fl[answ.x_coord] is True and x_fl[answ.x_coord] is True:
                    answers.append(answ)
                    x_fl[answ.x_coord] = False
                    y_fl[answ.x_coord] = False
            if len(answers) == self.len_matrix:
                return answers
            else:
                count -= 1
        return answers


def check_input(nms, wrk):
    if len(nms) != len(wrk):
        print("Количество работ должно равняться количеству работников!")
        return False
    return True


def user_input_names():
    nms = list(map(str, input("Перечислите имена исполнителей в строку через пробел: ").split()))
    wrk = list(map(str, input("Перечислите названия выполняемых работ в строку через пробел: ").split()))
    return nms, wrk


def user_input_times(nms, wrks):
    m = Matrix()
    m.add_len_matrix(len(nms))
    for x, nm in enumerate(nms):
        for y, wr in enumerate(wrks):
            tm = int(input(f"Введите время за которое {nm} выполнит работу {wr}: "))
            m.add_cell(Cell(tm, nm, wr, x, y))
    return m


names, works = user_input_names()  # два списка с именами и работами
if check_input(names, works) is False:
    print("Введите данные еще раз")
    names, works = user_input_names()
    while check_input(names, works) is False:
        print("Введите данные еще раз")
        names, works = user_input_names()

cl = user_input_times(names, works)  # объект класса Matrix - список клеток
count = 2
fl = True
while count != 0 or fl is False:
    cl.line_reduct()
    cl.column_reduct()
    if cl.is_answer():
        for answer in cl.get_answer():
            print(f"{answer.name} выполнит работу {answer.work} за время {answer.value}")
        fl = False
    else:
        cl.del_line_column()
        cl.column_reduct()
        if cl.is_answer():
            for answer in cl.get_answer():
                print(f"{answer.name} выполнит работу {answer.work} за время {answer.value}")
            fl = False
    count -= 1

if cl.is_answer():
    for answer in cl.get_answer():
        print(f"{answer.name} выполнит работу {answer.work} за время {answer.value}")
else:
    for answer in cl.if_too_math_zero():
        print(f"{answer.name} выполнит работу {answer.work} за время {answer.value}")
