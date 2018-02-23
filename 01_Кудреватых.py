
# Работа со списками
# Написать код для функций ниже
# Проверка производится в функции main()

# 00. Пример. Дан список (list) строк. Вернуть число - количество строк, у которых
# 1. длина строки 2 и больше
# 2. первый и последний символ одинаковые

def func00(words):
    count = 0
    for w in words:
        if len(w)>=2 and w[0]==w[-1]:
            count += 1
    return count


# 01. Из списка строк вернуть список в отсортированном по алфавиту порядке, но строки 
# начинающиеся с числа (0-9) должны идти после строк, начинающихся с букв
# Подсказка: можно создать два списка, отсортировать их по отдельности перед объединением

def func01(words):
    numb=[]
    word=[]
    for w in words:
        if w[0].isdigit() is False:
           word.append(w)
        else:
           numb.append(w)
word.sort()
numb.sort()
return word + numb
  
    
# 02. Отсортировать по последнему
# Дан список не пустых tuples, вернуть список, отсортированный по возрастанию
# последнего элемента tuple
def func02(tuples):
    s=sorted(tuples, reverse = True)
    return s
    
#Или

def func02(tuples):
    tuples.sort(key=op.itemgetter(-1))
    return tuples

# используется для проверки, 
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# Запускает проверку
def main():
    print('func00')
    test(func00(['abba', 'xyz01', 'nn', 'y', '444']), 3)
    test(func00(['', 'a', 'ab', 'cvc', 'jj']), 2)
    test(func00(['rrr', 'db', 'pro', 'hello']), 1)

    print('func01')
    test(func01(['1aa', '2bb', 'axx', 'xzz', 'xaa']),
                ['axx', 'xaa', 'xzz', '1aa', '2bb'])
    test(func01(['ccc', 'bbb', '9aa', 'xcc', 'xaa']),
                ['bbb', 'ccc', 'xaa', 'xcc', '9aa'])
    test(func01(['mix', 'xyz', '6apple', 'xanadu', 'aardvark']),
                ['aardvark', 'mix', 'xanadu', 'xyz', '6apple'])

    print('func02')
    test(func02([(1, 3), (3, 2), (2, 1)]),
                [(2, 1), (3, 2), (1, 3)])
    test(func02([(2, 3), (1, 2), (3, 1)]),
                [(3, 1), (1, 2), (2, 3)])
    test(func02([(1, 7), (1, 3), (3, 4, 5), (2, 2)]),
                [(2, 2), (1, 3), (3, 4, 5), (1, 7)])

if __name__ == '__main__':
    main()
