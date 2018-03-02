import csv
import re
import operator as op
from collections import Counter

#два полезных намёка

# Работа со словарями и файлами
# Написать код для функций ниже
# Проверка производится в функции main()

# 00. Из списка слов вернуть список tuples в формате слово - количество, 
# отсортированные по частоте, потом по алфавиту от меньшего к большему

def func00(words):
    return sorted(Counter(words).items(), key=lambda element: (-element[1], element[0]))
    


# 01. Вернуть список из словарей - полное имя (name) и телефон (tel) для всех 
# "Сергей" из файла 02.csv (сгенерирован при помощи Faker)
# можно использовать дополнительные библиотеки для работы с csv
# и внимание с кодировкой


def func01():
    with open("02.csv") as v:
        reader = csv.reader(v)
        serg = list()
        for row in reader:
            if re.findall("Сергей", row[7]):
                serg.append({'name': row[7], 'tel': row[8]})
    return serg

# 02. Из файла 02_alice.txt загрузить все слова длиннее 3 букв, вернуть 5 tuple -  самых 
# частых - слово и количество, отсортированных по частоте встречаемости от большего к меньшему. 
# При обработке удалить все знаки за исключением букв/цифр, привести всё к нижнему регистру
def func02():
    with open('02_alice.txt') as v:
        counter = {}
        for line in v:
            line = re.sub(r'[^a-zA-Z]', ' ', line).strip().lower().split()
            for subline in line:
                if len(subline) > 3:
                    if counter.get(subline):
                        counter[subline] += 1
                    else:
                        counter[subline] = 1
    return sorted(counter.items(), key=op.itemgetter(1), reverse=True)[:5]

# используется для проверки, 
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s got: %s \nexpected: %s\n' % (prefix, repr(got), repr(expected)))

# Запускает проверку
def main():
    print('func00')
    test(func00(['z', 'a', 'b', 'a', 'x']), [('a', 2), ('b', 1), ('x', 1), ('z', 1)])
    test(func00(['', 'a', 'ab', 'cvc', 'ab']), [('ab', 2), ('', 1), ('a', 1), ('cvc', 1)])
    test(func00(['rrr', 'db', 'pro', 'hello']),  [('db', 1), ('hello', 1), ('pro', 1), ('rrr', 1)])
    
    print()
    
    print('func01')
    test(func01(),[
            {'name': 'Сергеев Сергей Харлампович', 'tel': '+7 (258) 587-21-61'}, 
            {'name': 'Степанов Сергей Геннадиевич', 'tel': '+7 (662) 339-87-88'}])

    print()
    
    print('func02')
    test(func02(),[('said', 462), ('alice', 398), ('that', 315), ('with', 180), ('they', 153)])

if __name__ == '__main__':
    main()

