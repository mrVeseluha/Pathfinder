# -*- coding: utf-8 -*-
#
#  PathFinder.py
#
#  Copyright 2016 Максим <MaximVUstinov@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Программа поиска кратчайших маршрутов в лабиринте между двумя точками.

import time, random


class StopWatch():
    def __init__(self):
        self.start = time.time()

    def check(self):
        return time.time() - self.start

    def reset(self):
        self.start = time.time()


# Лабиринт задан матрицей. 0 - ячейка занята; 1 - свободна.
MAZE = [[1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # 0
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 1],  # 1
        [1, 1, 0, 0, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1],  # 3
        [1, 1, 1, 0, 1, 0, 1, 0, 0, 0],  # 4
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1],  # 5
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],  # 6
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],  # 7
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],  # 8
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1]]  # 9
# columns 0  1  2  3  4  5  6  7  8  9

MAZE1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0
         [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # 1
         [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # 2
         [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # 3
         [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # 4
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 5
         [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # 6
         [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # 7
         [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # 8
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # 9
# columns 0  1  2  3  4  5  6  7  8  9

MAZE2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0
         [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],  # 1
         [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],  # 2
         [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],  # 3
         [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],  # 4
         [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],  # 5
         [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],  # 6
         [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],  # 7
         [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],  # 8
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # 9
# columns 0  1  2  3  4  5  6  7  8  9

CLEAN_MAZE = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0 rows
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 2
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 3
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 4
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 5
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 6
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 7
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 8
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # 9
# columns      0  1  2  3  4  5  6  7  8  9

COUNTS = 0


def ShowMaze(route=[], a=None, b=None, digit=False, maze=MAZE):
    """
    Функция отображает лабиринт на экране и может вывести маршрут между двух точек
    :type route: list
    :param route: Маршрут в лабиринте. Список из элементов (кортежей) вида (ряд, колонка)
    :type a: tuple
    :param a: Координаты начальной точки маршрута
    :type b: tuple
    :param b: Конечная точка маршрута
    :type digit: bool
    :param digit: Если True, то выводит вместо точек номер шага в маршруте
    """
    # Легенда для отображения при выводе на экран. 0 - для занятой ячейки; 1 - для свободной ячейки
    legend = {0: '🌲', 1: '⬛'}
    # text = ' ' + '_' * len(MAZE[0]) * 3 + '_\n'  # Создадим верхнюю линию
    text = ''
    for row in range(0, len(maze)):  # Цикл перебора рядов
        text += str(row)  # Укажем номер ряда
        for col in range(0, len(maze[row])):  # Цикл перебора колонок
            if (row, col) == a:  # Если указана первая точка маршрута, то проверим на неё
                text += '|' + '🏃'  # если Да, то выведем "a"
            elif (row, col) == b:  # Если указана конечная точка маршрута, то проверим на неё
                text += '|' + '⛩'  # если Да, то выведем "b"
            elif (row, col) in route and digit:  # Если это точка маршрута и он задан
                text += '|' + '{:02d}'.format(route.index((row, col)))  # '.'   # выведем номер шага если digit==True
            elif (row, col) in route:  # или если digit не задан
                text += '|' + '👣'  # выведем ".."
            else:  # Во всех остальных случаях
                text += '|' + legend[maze[row][col]]  # выводим содержимое в соответствии с легендой
        text += '\n'  # Переводим на новую строку и добавляем последнюю чёрточку в ряду :-)
    # text += ' ' + '-' * len(MAZE[0]) * 3 + '-\n'  # и нижнюю линию
    text += ' |0️|1️|2️|3️|4️|5️|6️|7️|8️|9️\n'
    print(text)  # Выводим всё это на экран


def distance(a: tuple, b: tuple, cross: bool = False) -> int:
    """
    Функция возвращает расстояние между точками(ячейками) в шагах с учётом способа перехода между точками.
    :type a: tuple
    :type b: tuple
    :type cross: bool
    :param a: Точка А, кортеж вида (ряд, колонка)
    :param b: Точка В, кортеж вида (ряд, колонка)
    :param cross: Способ перемещения между точками ("крест" - на 4-е стороны или во все соседние, на 8 сторон
    :return: Возвращает количество шагов
    """
    if cross:
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
    else:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


def sort_point_list(points: list, dest: tuple, cross=False) -> list:
    """
    Сортирует список точек лабиринта по удалённости от точки dest
    :type points: list
    :param points: Список координат точек для сортировки
    :type dest: tuple
    :param dest: Точка для которой определяется расстояние для последующей сортировки
    :rtype: list
    :return: Возвращает отсортированный список точек
    """
    points_dict = {}  # Создадим словарь для сортировки {координаты точки (ряд, колонка): расстояние до точки dest}
    for point in points:  # Цикл перебора всех точек
        dist = distance(point, dest, cross)  # Считаем расстояние (в шагах) между точками,
        points_dict.setdefault(dist, [])  # в словаре создаём/проверяем запись с индексом в виде расстояния
        points_dict[dist] += [point]  # и запишем результат в словарь points_dict
    # Достаем и возвращаем все точки из полученного словаря отсортировав по удалённости
    return (lambda ll: [el for lst in ll for el in lst])([points_dict[i] for i in sorted(points_dict.keys())])


def get_possible_moves(a: tuple, cross=False, b=None, maze=MAZE):
    """
    Фунция определяет возможные дальнейшие шаги из заданой точки "а" и возвращает в виде списка.
    :type a: tuple
    :param a: Координаты точки для которой надо найти точки в которые возможно перейти. (ряд,колонка)
    :type b: tuple
    :param b: Если задана эта точка, то конечный список возможных ходов сортируется в зависимости от расстояния до неё.
    :type cross: bool
    :param cross: Если этот параметр True, то список ходов ограничивается "крестом", т.е. влево, вправо, вверх, вниз.
    :rtype: list
    :return: Возвращает список возможных шагов из точки "а".
    """
    moves = []  # Создадим будущий список точек возможных для перемещения
    if cross:  # Если активорован метод "креста"
        for shift in [-1, 1]:  # то перебирём сдвиг от шага назад, до шага вперёд
            moves.append((a[0] + shift, a[1]))  # Вычислим шаги по вертикали (в рядах)
            moves.append((a[0], a[1] + shift))  # Вычислим шаги по горизонтали (в колонках)
        # Отфильтруем результаты, что бы они не выходили за границы диапазона лабиринта
        moves = list(filter(lambda point: 0 <= point[0] < len(maze) and 0 <= point[1] < len(maze[point[0]]), moves))
        moves = list(filter(lambda point: maze[point[0]][point[1]], moves))  # Выбрасываем из результатов занятые ячейки
    else:  # А если метод передвижения не "крест" (а как ходит ферзь по доске), то
        for vshift in [-1, 0, 1]:  # то перебирём сдвиг по вертикали
            for hshift in [-1, 0, 1]:  # перебирём сдвиг по горизонтали
                # Проверим получившееся значение на корректность диапазона значений, но лишь для отрицательных величин,
                # так как Python позволяет получать значения из списка по отрицательному индексу
                if a[0] + vshift > -1 and a[1] + hshift > -1:  # Выход за границы в большую сторону проверим по другому
                    try:  # Попробуем получить значение из массива с лабиринтом
                        if maze[a[0] + vshift][a[1] + hshift]:  # Если удалось и значение допустимое (1),
                            moves.append((a[0] + vshift, a[1] + hshift))  # то записываем точку в список точек
                    except:  # Если же мы всё таки вышли за границы диапазона,
                        continue  # то переходим на следующий цикл перебора точек (или заканчиваем его :-) )
        moves.remove(a)  # Удаляем из получившегося списка точку из которой мы собираемся двигаться
    if b is not None:  # Если задана точка для сравнения (b),
        moves = sort_point_list(moves, b, cross)  # то сортируем список по удалённости от этой точки.
    return moves  # Возвращаем значение в виде списка найденных точек!


def IsNext(a: tuple, b: tuple) -> bool:
    """
    Функция проверяет являются ли две точки соседями (смежными)
    :type a: tuple
    :param a: Точка для сравнения
    :type b: tuple
    :param b: Точка для сравнения
    :return: Возвращает True/False в зависимости от результата сравнения
    """
    # Если модуль разницы координат по вертикали и горизонтали меньше либо равны 1,
    return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1


def FindRoute(a: tuple, b: tuple, route: list = [], n: int = 1, cross: bool = False, minimum_steps: int = None,
              maze=MAZE) -> list:
    """
    Самая главная функция! Осуществляет поиск маршрута между двумя точками (a и b). И возвращает список всех возможных
    самых коротких маршрутов.
    :param a: Точка начала маршрута.
    :type a: tuple
    :param b: Конечная точка маршрута.
    :type b: tuple
    :param route: Дополнительный, используется при рекурсии. Содержит список с уже пройденным маршрутом.
    :type route: list
    :param n: Дополнительный, необязательный параметр, используемый при рекурсии. Содержит количество пройденных шагов.
    :type n: int
    :param cross: Дополнительный параметр. Указывается если метод перемещения лишь на 4-е стороны, по умолчанию на 8.
    :type cross: bool
    :param minimum_steps: Дополнительный параметр для рекурсии. Показывает длинну найденного успешного маршрута.
    :type minimum_steps: int
    :return: Возвращает список кратчайших маршрутов или None если маршрут не найден.
    """
    global COUNTS
    COUNTS += 1
    # Сразу же проверим следующее условие, что если какой-то маршрут уже найден и его размер передан в
    # переменной minimum_steps и текущее количество шагов (n) + кратчайшая дистанция до финиша больше известного
    # минимума шагов,
    if minimum_steps and n - 0 + distance(a, b, cross) > minimum_steps:
        return None  # то прерываем поиск маршрута и возвращаем None. Дальше путь искать безсмысленно.
    full_path = route + [a]  # Добавим к уже пройденому пути текущую точку из которой мы ищем маршрут.
    next_steps = get_possible_moves(a, cross, b, maze=maze)  # Получим отсортированный список возможных ходов.
    if next_steps == []:  # Если полученный список пустой, значит ходов нет. Провал!
        return None  # Тогда возвращаем None и прерываем дальнейший поиск.
    try:  # Попытаемся удалить из списка возможных ходов точку откуда мы только что пришли
        next_steps.remove(route[-1])
    except:  # Если не получилось, значит мы стоим в самом начале маршрута и удалять нечего,
        pass  # тогда ничего и не делаем.
    # Проверим, если в списке возможных ходов есть уже пройденные шаги,
    if not set(route).isdisjoint(set(next_steps)):  # значит мы ходим кругами и маршрут точно не будет кратчайшим,
        return None  # бросаем его.
    # Главная проверка!
    if b in next_steps:  # and n <= minimum_steps:  # Если искомая точка маршрута находится в списке соседних
        return [full_path + [b]]  # то прекращаем поиск и возвращаем получившийся маршрут между точками. УРА!!!
    pathes = []  # Начинаем рекурсионную часть с создания будущего списка возможных маршрутов.
    for step in next_steps:  # Перебираем все дальнейшие шаги.
        # Рекурсия! Вызываем эту же функцию для поиска маршрута из соседних точек с учётом уже пройденного маршрута
        path = FindRoute(step, b, full_path, n + 1, cross, minimum_steps,
                         maze=maze)  # и минимальной длинны уже найденных путей.
        if path is not None:  # Если маршрут найден,
            pathes.extend(path)  # то добавляем его в список найденных
            if minimum_steps is not None:  # Если минимум уже был найден,
                minimum_steps = min(minimum_steps, len(path[0]))  # то корректируем минимальное расстояние до цели.
            else:  # А если минимум ещё не был найден,
                minimum_steps = len(path[0])  # то присвоим его первый раз
    if pathes != []:  # Если в итоге нам удалось собрать список маршрутов
        min_length = min([len(path) for path in pathes])  # определим минимальный размер маррута из найденных
        pathes = [path for path in pathes if len(path) == min_length]  # Чистим список от более длинных
        return pathes  # И возвращаем финальный список!!! Ура работа закончена!!!
    else:  # А если список маршрутов пуст,
        return None  # то бросаем всё и возвращаем ВЕЛИКОЕ НИЧТО!!!


class Mazze():
    def __init__(self, maze: list):
        self.maze = maze
        self.__counts__ = 0

    def get_possible_moves(self, a: tuple, cross=False, b=None) -> list:
        """
        Фунция определяет возможные дальнейшие шаги из заданой точки "а" и возвращает в виде списка.
        :type a: tuple
        :param a: Координаты точки для которой надо найти точки в которые возможно перейти. (ряд,колонка)
        :type b: tuple
        :param b: Если задана эта точка, то конечный список возможных ходов сортируется в зависимости от расстояния до неё.
        :type cross: bool
        :param cross: Если этот параметр True, то список ходов ограничивается "крестом", т.е. влево, вправо, вверх, вниз.
        :rtype: list
        :return: Возвращает список возможных шагов из точки "а".
        """
        moves = []  # Создадим будущий список точек возможных для перемещения
        if cross:  # Если активорован метод "креста"
            for shift in [-1, 1]:  # то перебирём сдвиг от шага назад, до шага вперёд
                moves.append((a[0] + shift, a[1]))  # Вычислим шаги по вертикали (в рядах)
                moves.append((a[0], a[1] + shift))  # Вычислим шаги по горизонтали (в колонках)
            # Отфильтруем результаты, что бы они не выходили за границы диапазона лабиринта
            moves = list(
                filter(lambda point: 0 <= point[0] < len(self.maze) and 0 <= point[1] < len(self.maze[point[0]]),
                       moves))
            moves = list(
                filter(lambda point: self.maze[point[0]][point[1]], moves))  # Выбрасываем из результатов занятые ячейки
        else:  # А если метод передвижения не "крест" (а как ходит ферзь по доске), то
            for vshift in [-1, 0, 1]:  # то перебирём сдвиг по вертикали
                for hshift in [-1, 0, 1]:  # перебирём сдвиг по горизонтали
                    # Проверим получившееся значение на корректность диапазона значений, но лишь для отрицательных величин,
                    # так как Python позволяет получать значения из списка по отрицательному индексу
                    if a[0] + vshift > -1 and a[
                        1] + hshift > -1:  # Выход за границы в большую сторону проверим по другому
                        try:  # Попробуем получить значение из массива с лабиринтом
                            if self.maze[a[0] + vshift][a[1] + hshift]:  # Если удалось и значение допустимое (1),
                                moves.append((a[0] + vshift, a[1] + hshift))  # то записываем точку в список точек
                        except:  # Если же мы всё таки вышли за границы диапазона,
                            continue  # то переходим на следующий цикл перебора точек (или заканчиваем его :-) )
            moves.remove(a)  # Удаляем из получившегося списка точку из которой мы собираемся двигаться
        if b is not None:  # Если задана точка для сравнения (b),
            moves = sort_point_list(moves, b, cross)  # то сортируем список по удалённости от этой точки.
        return moves  # Возвращаем значение в виде списка найденных точек!

    def FindRoute(self, a: tuple, b: tuple, route: list = [], n: int = 1, cross: bool = False, minimum_steps: int = None) -> list:
        """
        Самая главная функция! Осуществляет поиск маршрута между двумя точками (a и b). И возвращает список всех возможных
        самых коротких маршрутов.
        :param a: Точка начала маршрута.
        :type a: tuple
        :param b: Конечная точка маршрута.
        :type b: tuple
        :param route: Дополнительный, используется при рекурсии. Содержит список с уже пройденным маршрутом.
        :type route: list
        :param n: Дополнительный, необязательный параметр, используемый при рекурсии. Содержит количество пройденных шагов.
        :type n: int
        :param cross: Дополнительный параметр. Указывается если метод перемещения лишь на 4-е стороны, по умолчанию на 8.
        :type cross: bool
        :param minimum_steps: Дополнительный параметр для рекурсии. Показывает длинну найденного успешного маршрута.
        :type minimum_steps: int
        :return: Возвращает список кратчайших маршрутов или None если маршрут не найден.
        """
        self.__counts__ += 1
        # Сразу же проверим следующее условие, что если какой-то маршрут уже найден и его размер передан в
        # переменной minimum_steps и текущее количество шагов (n) + кратчайшая дистанция до финиша больше известного
        # минимума шагов,
        if minimum_steps and n - 0 + distance(a, b, cross) > minimum_steps:
            return None  # то прерываем поиск маршрута и возвращаем None. Дальше путь искать безсмысленно.
        full_path = route + [a]  # Добавим к уже пройденому пути текущую точку из которой мы ищем маршрут.
        next_steps = self.get_possible_moves(a, cross, b)  # Получим отсортированный список возможных ходов.
        if next_steps == []:  # Если полученный список пустой, значит ходов нет. Провал!
            return None  # Тогда возвращаем None и прерываем дальнейший поиск.
        try:  # Попытаемся удалить из списка возможных ходов точку откуда мы только что пришли
            next_steps.remove(route[-1])
        except:  # Если не получилось, значит мы стоим в самом начале маршрута и удалять нечего,
            pass  # тогда ничего и не делаем.
        # Проверим, если в списке возможных ходов есть уже пройденные шаги,
        if not set(route).isdisjoint(set(next_steps)):  # значит мы ходим кругами и маршрут точно не будет кратчайшим,
            return None  # бросаем его.
        # Главная проверка!
        if b in next_steps:  # and n <= minimum_steps:  # Если искомая точка маршрута находится в списке соседних
            return [full_path + [b]]  # то прекращаем поиск и возвращаем получившийся маршрут между точками. УРА!!!
        pathes = []  # Начинаем рекурсионную часть с создания будущего списка возможных маршрутов.
        for step in next_steps:  # Перебираем все дальнейшие шаги.
            # Рекурсия! Вызываем эту же функцию для поиска маршрута из соседних точек с учётом уже пройденного маршрута
            path = self.FindRoute(step, b, full_path, n + 1, cross, minimum_steps)  # и минимальной длинны уже найденных путей.
            if path is not None:  # Если маршрут найден,
                pathes = pathes + path  # то добавляем его в список найденных
                if minimum_steps is not None:  # Если минимум уже был найден,
                    minimum_steps = min(minimum_steps, len(path[0]))  # то корректируем минимальное расстояние до цели.
                else:  # А если минимум ещё не был найден,
                    minimum_steps = len(path[0])  # то присвоим его первый раз
        if pathes != []:  # Если в итоге нам удалось собрать список маршрутов
            min_length = min(map(len,pathes))  # определим минимальный размер маррута из найденных
            pathes = [path for path in pathes if len(path) == min_length]  # Чистим список от более длинных
            self.__pathes__ = pathes
            return pathes  # И возвращаем финальный список!!! Ура работа закончена!!!
        else:  # А если список маршрутов пуст,
            return None  # то бросаем всё и возвращаем ВЕЛИКОЕ НИЧТО!!!

    def ShowPath(self,a,b, cross=False):
        self.__counts__ = 0
        pathes = self.FindRoute(a,b,cross=cross)
        for path in pathes:
            print('Path № {} of {}, length {} steps'.format(pathes.index(path),len(pathes),len(path)))
            ShowMaze(path,a,b,maze=self.maze)


def EmptyMazeTest(n=10):
    """
    Тестирует алгоритм на поиск маршрута в пустом лабиринте на [2 х 2] до [n x n]
    :param n: Конечный размер лабиринта
    """
    global COUNTS
    timer = StopWatch()
    maze = [[1]]
    for i in range(n - 1):
        maze[i].append(1)
        maze.append(maze[0])
        COUNTS = 0
        timer.reset()
        roads = FindRoute((len(maze) - 1, 0), (0, len(maze) - 1), cross=False, maze=maze)
        print(f'{i + 2} X {i + 2}| {len(roads)} маршрутов найдено за {timer.check():,.6f} секунд.'
              f'Перебрано {COUNTS - 1} маршрутов со скоростью {(COUNTS - 1) / timer.check()} маршрута/сек.')
        ShowMaze(roads[0], maze=maze)


if __name__ == '__main__':

    EmptyMazeTest(11)
    '''
2      маршрутов найдено за  0.0002 секунд. Перебрано         3 маршрутов со скоростью 17,027 маршрата/сек.
6      маршрутов найдено за  0.0005 секунд. Перебрано        15 маршрутов со скоростью 30,690 маршрата/сек.
20     маршрутов найдено за  0.0024 секунд. Перебрано        95 маршрутов со скоростью 39,585 маршрата/сек.
70     маршрутов найдено за  0.0091 секунд. Перебрано       557 маршрутов со скоростью 60,981 маршрата/сек.
252    маршрутов найдено за  0.0466 секунд. Перебрано     3,041 маршрутов со скоростью 65,237 маршрата/сек.
924    маршрутов найдено за  0.2461 секунд. Перебрано    15,789 маршрутов со скоростью 64,166 маршрата/сек.
3,432  маршрутов найдено за  1.1850 секунд. Перебрано    79,593 маршрутов со скоростью 67,168 маршрата/сек.
12,870 маршрутов найдено за  5.9858 секунд. Перебрано   391,855 маршрутов со скоростью 65,464 маршрата/сек.
48,620 маршрутов найдено за 28.8065 секунд. Перебрано 1,892,287 маршрутов со скоростью 65,690 маршрата/сек.

2 X 2          2 маршрутов найдено за  0.0002 секунд. Перебрано         3 маршрутов со скоростью 14,631 маршрата/сек.
3 X 3          6 маршрутов найдено за  0.0003 секунд. Перебрано        15 маршрутов со скоростью 43,600 маршрата/сек.
4 X 4         20 маршрутов найдено за  0.0012 секунд. Перебрано        71 маршрутов со скоростью 57,082 маршрата/сек.
5 X 5         70 маршрутов найдено за  0.0078 секунд. Перебрано       299 маршрутов со скоростью 38,307 маршрата/сек.
6 X 6        252 маршрутов найдено за  0.0584 секунд. Перебрано     1,203 маршрутов со скоростью 20,585 маршрата/сек.
7 X 7        924 маршрутов найдено за  0.0895 секунд. Перебрано     4,793 маршрутов со скоростью 53,548 маршрата/сек.
8 X 8      3,432 маршрутов найдено за  0.3542 секунд. Перебрано    19,149 маршрутов со скоростью 54,069 маршрата/сек.
9 X 9     12,870 маршрутов найдено за  1.3656 секунд. Перебрано    76,949 маршрутов со скоростью 56,349 маршрата/сек.
10 X 10   48,620 маршрутов найдено за  4.8981 секунд. Перебрано   310,791 маршрутов со скоростью 63,452 маршрата/сек.
11 X 11  184,756 маршрутов найдено за 19.9216 секунд. Перебрано 1,260,909 маршрутов со скоростью 63,293 маршрата/сек.'''

    A = (-1, -1)
    B = (-1, -1)

    random.seed()
    for row in range(10):
        for col in range(10):
            rand = random.randint(0, 5)
            if rand == 3 or rand == 5:
                MAZE[row][col] = 0
            else:
                MAZE[row][col] = 1

    ShowMaze()

    A = (int(input('Введите координату точки А. Ряд? ')), int(input('Введите координату точки А. Колонка? ')))
    B = (int(input('Введите координату точки B. Ряд? ')), int(input('Введите координату точки B. Колонка? ')))
    cross = bool(int(input('Выберите способ поиска маршрутов. "Крестом" - 1, во все стороны - 0? ')))

    COUNTS = 0
    timer = StopWatch()
    route = FindRoute(A, B, cross=cross, maze=MAZE)
    chk_time = timer.check()

    if route is not None:
        for road in route:
            print('Path #', route.index(road) + 1, 'Length = ', len(road))
            ShowMaze(road, A, B, digit=False)
    else:
        print('Path not found in {:,.4f} seconds and {:,.0f} cjmbinations!'.format(chk_time, COUNTS))

    if route is not None:
        print('{:,.0f} - маршрута найдено за {:,.4f} секунд, длинна каждого маршрута - {:,.2f}'.format(len(route),
                                                                                                       chk_time,
                                                                                                       len(route[0])))
    print('Совершено {:,.0f} переборов со скоростью {:,.2f} переборов секунду'.format(COUNTS, COUNTS / chk_time))
