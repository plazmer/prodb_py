import csv
import re
import operator as op
from collections import Counter

# 01. Вернуть список из словарей - полное имя (name) и телефон (tel) для всех 
# "Сергей" из файла 02.csv (сгенерирован при помощи Faker)
# можно использовать дополнительные библиотеки для работы с csv
# и внимание с кодировкой

def func01():
    with open('02.csv') as filec:
        reader = csv.DictReader(filec)
        serg = []
        for row in reader:
            if "Сергей" in row['name']:
                serg.append({'name': row['name'], 'tel': row['phone']}) # ключ "phone" в таблице                 
    return serg
    
# 02. Из файла 02_alice.txt загрузить все слова длиннее 3 букв, вернуть 5 tuple -  самых
# частых - слово и количество, отсортированных по частоте встречаемости от большего к меньшему. 
# При обработке удалить все знаки за исключением букв/цифр, привести всё к нижнему регистру

def func02():
    with open('02_alice.txt') as f:
        reg = re.compile('[^a-zA-Z]')
        f1 = reg.sub(' ', re.sub(r'\b\w{1,3}\b', '', f.read().lower())) #мб переборщила ┐(‘～` )┌ но вроде работает        
        return sorted( Counter(f1.split()).most_common(5), key=lambda element: (-element[1], element[0]))
      # или  
      # return Counter(f1.split()).most_common(5) 
       
# используется для проверки, 
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s got: %s \nexpected: %s\n' % (prefix, repr(got), repr(expected)))


# Запускает проверку
def main():
    print('func01')
    test(func01(), [
        {'name': 'Сергеев Сергей Харлампович', 'tel': '+7 (258) 587-21-61'},
        {'name': 'Степанов Сергей Геннадиевич', 'tel': '+7 (662) 339-87-88'}])
    print()
    print('func02')
    test(func02(), [('said', 462), ('alice', 398), ('that', 315), ('with', 180), ('they', 153)])

if __name__ == '__main__':
    main()
