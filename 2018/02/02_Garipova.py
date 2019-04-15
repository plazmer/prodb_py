import csv
import re
from collections import Counter
#два полезных намёка

# Работа со словарями и файлами
# Написать код для функций ниже
# Проверка производится в функции main()

# 00. Из списка слов вернуть список tuples в формате слово - количество, 
# отсортированные по частоте, потом по алфавиту от меньшего к большему

def func00(words): #TODO сделать оптимально
    return sorted(Counter(words).items(), key=lambda element: (-element[1], element[0]))


# 01. Вернуть список из словарей - полное имя (name) и телефон (tel) для всех 
# "Сергей" из файла 02.csv (сгенерирован при помощи Faker)
# можно использовать дополнительные библиотеки для работы с csv
# и внимание с кодировкой
    
def func01():
    with open ("02.csv", "r") as file:
        allrow = csv.DictReader(file)
        sergey = []
        for row in allrow:
            if "Сергей" in row ["name"]:
                sergey.append({"name": row["name"],"tel": row["phone"]})
    return sergey

# 02. Из файла 02_alice.txt загрузить все слова длиннее 3 букв, вернуть 5 tuple -  самых 
# частых - слово и количество, отсортированных по частоте встречаемости от большего к меньшему. 
# При обработке удалить все знаки за исключением букв/цифр, привести всё к нижнему регистру
def func02():
    with open ("02_alice.txt", "r") as text:
        tmp={}
        for string in text:
            words = re.sub(r'[^a-zA-Z]', ' ', string).lower().split()
            long_words = list(filter(lambda x : len(x)>3,  words))
            for word in long_words:
                if tmp.get(word):
                    tmp[word] += 1
                else:
                    tmp[word] = 1              
    tuples = sorted(tmp.items(), reverse=False, key=lambda element: (-element[1], element[0]))[:5]
    return tuples


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
