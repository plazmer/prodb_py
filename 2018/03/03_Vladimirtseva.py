import csv
import sqlite3

DATABASE_NAME = '../queries.db'


# Работа с реляционной БД SQLITE и файлами
# Написать код для функций ниже
# Проверка производится в функции main()

# 00. Создать таблицу для хранения данных в формате ключ-значение, заполнить, вернуть результат
def func00(connection): 
    c = connection.cursor()
    c.execute('DROP TABLE IF EXISTS func00')
    c.execute('''CREATE TABLE IF NOT EXISTS func00 (
                      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                      key TEXT NOT NULL, 
                      value TEXT NOT NULL)''')
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS func00_key ON func00(key)''')
    connection.commit()
    
    c.execute('INSERT INTO func00 (key,value) VALUES(:name,:value)',{'name':2,'value':'test2'})
    c.execute('INSERT INTO func00 (key,value) VALUES(?,?)',('33','test3'))
    connection.commit()
    
    c.execute('SELECT value FROM func00 WHERE key=?',('33',))
    row = dict(c.fetchone())
    return row['value']

# 01. Загрузить в таблицу func01 содержимое файла 02.csv, названия полей те же.
# при повторном запуске скрипт должен давать такой же результат. 

def func01(connection):
    with open ('02.csv') as data:
        rows = csv.reader(data)

        c = connection.cursor()
        c.execute('DROP TABLE IF EXISTS func01')
        c.execute('''CREATE TABLE IF NOT EXISTS func01 (
                          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                          address TEXT NOT NULL, 
                          birthdate TEXT NOT NULL,
                          blood_group TEXT NOT NULL,
                          company TEXT NOT NULL,
                          job TEXT NOT NULL,
                          mail TEXT NOT NULL, 
                          name TEXT NOT NULL,
                          phone TEXT NOT NULL,
                          residence TEXT NOT NULL,
                          sex TEXT NOT NULL,
                          ssn TEXT NOT NULL,
                          username TEXT NOT NULL,
                          website TEXT NOT NULL)''')
        connection.commit()

        next(rows)
        for row in rows:
           c.execute('''INSERT INTO func01
                        (address,birthdate,blood_group,company,job,mail,name,phone,residence,sex,ssn,username,website)     
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', (row)[1:])
        connection.commit()
    
        c.execute('SELECT COUNT(*) as cnt FROM func01')
        row = dict(c.fetchone())
        return row['cnt']

# 02. Из заполненной базы данных (func01) вернуть имя человека по номеру телефона

def func02(phone,connection):
    c = connection.cursor()
    c.execute('SELECT name FROM func01 WHERE phone=?', (phone,))
    result = c.fetchone()
    return result ['name'] if result is not None else None
    
   
# используется для проверки, 
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print('%s got: %s \nexpected: %s\n' % (prefix, repr(got), repr(expected)))


# Запускает проверку
def main():
    conn=sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row    
    print('func00')
    test(func00(conn), 'test3')
    conn.close()

    conn=sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row    
    print('func01')
    test(func01(conn),999)
    test(func01(conn),999)
    conn.close()

    conn=sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row       
    print('func02')
    test(func02('+7 (964) 974-92-82',conn),'Гурьев Лазарь Герасимович')
    test(func02('123',conn),None)
    conn.close()

if __name__ == '__main__':
  main()
