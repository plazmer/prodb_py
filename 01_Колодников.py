# Формат сдачи работы: Pull Request файла 01_Фамилия.py
# Фамилия на русском
# Добиваемся, чтобы все тесты проходили успешно, потом отсылаем результат

## INT / FLOAT

# Пример:
# Возвести переданное число в квадрат и вернуть
def func_num_01( number ):
    return number * number


# Передано значение температуры в градусах Цельсия, вернуть в Кельвинах
def func_num_02( number ):
    return number + 273.15


# Если переданное число больше 2.5, вернуть 1, если меньше 2.5 вернуть 0
def func_num_03( number ):
    return 1 if number > 2.5 else 0


# Передана строка, содержащая целое число. Вернуть число, умноженное на 5
def func_num_04( string ):
    return int(string) * 5


# Передано дробное число, вернуть целую часть
def func_num_05( float_number ):
    return int(float_number)


# Передано дробное число, вернуть округленную до 2 знаков часть после запятой
def func_num_06( float_number ):
    return round(float_number%1,2)


## STR
# Вернуть текст "func01"
def func_str_01():
    return "func01"


# Вернуть переданный текст, дописав к нему " finished"
def func_str_02( msg ):
    return msg + " finished"


# Вернуть переданный текст, заменив все буквы на заглавные
def func_str_03( msg ):
    return msg.upper()


# Вернуть длину переданной строки
def func_str_04( msg ):
    return len(msg)


# Если длина текста больше 5 символов, вернуть с 3 по 5 символы, иначе вернуть пустую строку
def func_str_05( msg ):
    return msg[3:5] if len(msg) >= 5 else ""


# Передан шаблон и число, подставить внутрь шаблона число, вернуть результат
def func_str_06( msg, number ):
    # Верно или я не понял, что от меня хотят??
    return msg.replace("%s", str(number))


# используется для проверки,
def test(msg, got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print('%s\t%s\tПолучено: %s \tОжидалось: %s' % (msg, prefix, repr(got), repr(expected)))


def main():
    test('func_int_01', func_num_01(7), 49)
    test('func_int_02', func_num_02(0), 273.15)
    test('func_int_03', func_num_03(0), 0)
    test('func_int_03', func_num_03(3), 1)
    test('func_int_04', func_num_04(" 297 "), 297*5)
    test('func_int_05', func_num_05(9.9), 9)
    test('func_int_06', func_num_06(9.99), 0.99)

    test('func_str_01', func_str_01(), 'func01')
    test('func_str_02', func_str_02('test'), 'test finished')
    test('func_str_03', func_str_03('tEsT по-РуссКи'), 'TEST ПО-РУССКИ')
    test('func_str_05', func_str_04('123'), 3)
    test('func_str_05', func_str_05('123'), '')
    test('func_str_05', func_str_05('12345'), '45')
    test('func_str_05', func_str_06('Вы дали число ** %s **', 42), 'Вы дали число ** 42 **')



if __name__ == '__main__':
    main()
