# Формат сдачи работы: Pull Request файла 01_Фамилия.py 
# Фамилия на русском

## INT / FLOAT

# Пример:
# Возвести переданное число в квадрат и вернуть
def func_num_01( number ):
    return number * number
    

# Передано значение температуры в градусах Цельсия, вернуть в Кельвинах
def func_num_02( number ):
    return 


# Если переданное число больше 2.5, вернуть 1, если меньше 2.5 вернуть 0
def func_num_03( number ):
    return 


# Передана строка, содержащая целое число. Вернуть число, умноженное на 5
def func_num_04( string ):
    return 


# Передано дробное число, вернуть целую часть
def func_num_05( float_number ):
    return 


# Передано дробное число, вернуть округленную до 2 знаков часть после запятой
def func_num_06( float_number ):
    return 


# Задача 1
# Вернуть текст "func01"
def func01():
    return 

# Задача 2
# Вернуть переданный текст, дописав к нему " finished"
def func02( msg ):
    return

# Задача 3
# 


# используется для проверки, 
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print('%s \n Получено: %s \nОжидалось: %s\n' % (prefix, repr(got), repr(expected)))


def main():
    print('func_int_01')
    test(func_num_01(7), 49)

    print('func_int_02')
    test(func_num_02(0), 273.15)

    print('func_int_03')
    test(func_num_03(0), 0)
    test(func_num_03(3), 1)

    print('func_int_04')
    test(func_num_04(" 297 "), 297*5)

    print('func_int_05')
    test(func_num_05(9.9), 9)

    print('func_int_06')
    test(func_num_06(9.99), 0.99)
    
    print('func01')
    test(func01(), 'func01')
    
    print('func02')
    test(func02('test'), 'test finished')


if __name__ == '__main__':
    main()
