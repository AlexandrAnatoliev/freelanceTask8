# freelanceTask8

[Ru] Задание со фриланс-биржи

## Описание:

#### N работ могут исполняться n исполнителями. Известно время исполнения каждой работы каждым исполнителем tij,ij=1..n. Распределить работы между исполнителями так, чтобы каждая работа выполнялась одним исполнителем, каждый исполнитель выполнял одну работу, а суммарное время выполнения всех работ было минимальным.

## Примеры использования

#### Вводим данные: имена работников, название работ, время выполнения конкретным исполнителем конкретной работы

```python
names, works = user_input_names()  # два списка с именами и работами

while check_input(names, works) is False:
    print("Введите данные еще раз")
    names, works = user_input_names()

cl = user_input_times(names, works)  # объект класса Matrix - список клеток
```

#### Ввод имен и работ

```python
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
```

#### Ввод времени выполнения работ, формирование матрицы

```python
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
```

#### Решается задача через редукцию по строкам и столбцам. Если не найден ответ - подбором комбиации ответов из найденных

```python
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
```
