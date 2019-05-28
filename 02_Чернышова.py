# Формат сдачи работы
# Создаём ветку Фамилия_02
# Pull Request файла 02_Фамилия.py в ветку Фамилия_02
# Фамилия на русском
# Добиваемся, чтобы все тесты проходили успешно, потом отсылаем результат


# Заменить в переданной строке символ на указанной позиции на переданную строку
def func_str_01(original_str, replace_str, position):
    return original_str[:position] + replace_str + original_str[position + 1:]


# Возвращает элемент из середины списка если число элементов нечетное, если число элементов четное - возвращает второй из двух посередине (правеее середины)
def func_list_01(arr):
    m = len(arr)
    if m % 2 == 1:
        return (m // 2) + 1
    else:
        return (m // 2) + 1


# Возвращает отсортированный список
def func_list_021(arr):
    return sorted(arr)


# Возвращает отсортированный список в обратную сторону
def func_list_022(arr):
    return sorted(arr, reverse=True)


# Возвращает самый большой элемент
def func_list_03(arr):
    return max(arr)


# Возвращает элемент, ближайший к среднему значению элементов списка
def func_list_04(arr):
    f = sum(arr) / len(arr)
    k = min(arr, key=lambda x: abs(x - f))
    return k


# Возвращает сумму числовых элементов массива или тех, которые можно свести к числу
def func_list_05(arr):
    x = 0
    for y in arr:
        try:
            x += float(y)
        except:
            pass
    return x


# Принимает два списка, возвращает отсортированный список с уникальными элементами, которые есть в обоих списках
def func_list_06(arr1, arr2):
    i = arr1 + list(set(arr2) - set(arr1))
    i.sort()
    return i


# Принимает список, возвращает tuple(кортеж) только из отсортированных чисел
def func_tuple_01(arr):
    i = []
    for x in arr:
        if type(x) == int:
            i.append(x)
        else:
            continue
    i.sort()
    return tuple(i)


# Для списков имен и оценок вернуть список из кортежей (имя, значение)
def func_tuple_02(names, values):
    return list(zip(names, values))


# Для кортежа из двух элементов поменять местами первый и последний элементы
def func_tuple_03(tupl):
    return tupl[-1], tupl[0]


# Для словаря вернуть список ключей
def func_dict_01(arr):
    arr1 = list()
    for i in arr.keys():
        arr1.append(i)
    return arr1


# Для словаря вернуть список значений
def func_dict_02(arr):
    arr1 = list()
    for i in arr.values():
        arr1.append(i)
    return arr1


# Вернуть словарь, в котором числовые значения возведены в квадрат, не числовые значения не трогать
def func_dict_03(arr):
    for key in arr.keys():
        try:
            arr[key] = arr.get(key) ** 2
        except:
            pass
    return arr


# Если название ключа содержит Show, вернуть значение, иначе вернуть ""
def func_dict_04(arr):
    for x in arr.keys():
        if 'Show' in x != -1:
            return arr.get(x)
        else:
            return ''


# используется для проверки, 
def test(msg, got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s\t%s\tПолучено: %s \tОжидалось: %s' % (msg, prefix, repr(got), repr(expected)))


def main():
    test('func_str_01', func_str_01('This a test', 'is a', 5), 'This is a test')
    test('func_list_01', func_list_01([1, 2, 3, 4, 5]), 3)
    test('func_list_01', func_list_01([1, 2, 3, 4, 5, 6]), 4)
    test('func_list_021', func_list_021([1, 3, 6, 2, 9]), [1, 2, 3, 6, 9])
    test('func_list_022', func_list_022([1, 3, 6, 2, 9]), [9, 6, 3, 2, 1])
    test('func_list_03', func_list_03([1, 3, 6, 2, 9]), 9)
    test('func_list_04', func_list_04([1, 3, 6, 2, 9]), 3)
    test('func_list_04', func_list_04([-1, -2, -6, -20, -9]), -9)
    test('func_list_05', func_list_05([1, 2, 3.3, 'a', '2.2']), 8.5)
    test('func_list_06', func_list_06([1, 2], [2, 3]), [1, 2, 3])
    test('func_list_06', func_list_06(['b', 'a'], ['c', 'a', 'd']), ['a', 'b', 'c', 'd'])

    test('func_tuple_01', func_tuple_01([9, 'a', 1, 4]), (1, 4, 9))
    test('func_tuple_02', func_tuple_02(['a', 'b'], [1, 2]), [('a', 1), ('b', 2)])
    test('func_tuple_03', func_tuple_03((9, 99)), (99, 9))

    test('func_dict_01', func_dict_01({'a': 1, 2: 'b', 'c': [1, 2]}), ['a', 2, 'c'])
    test('func_dict_02', func_dict_02({'a': 1, 2: 'b', 'c': [1, 2]}), [1, 'b', [1, 2]])
    test('func_dict_03', func_dict_03({'a': 2, 'b': 'a', 'c': 3}), {'a': 4, 'b': 'a', 'c': 9})
    test('func_dict_04', func_dict_04({'if you Show me': 1, 'b': 'a'}), 1)
    test('func_dict_04', func_dict_04({'a': 2, 'b': 'a', 'c': 3}), '')


if __name__ == '__main__':
    main()
