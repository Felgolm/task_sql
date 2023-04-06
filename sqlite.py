import sqlite3
from sqlite3 import Connection
from typing import Tuple


# task_sql
# Создание и наполнение новой таблицы
QUERY_CREATE_AND_FILL_TABLE = (
    """
    CREATE TABLE Students
    (
    Student_Id INTEGER PRIMARY KEY, 
    Student_Name TEXT(20) NOT NULL, 
    School_Id INTEGER NOT NULL
    );
    """, 
    """ 
    INSERT INTO Students
    VALUES (201, 'Иван', 1), 
           (202, 'Петр', 2), 
           (203, 'Анастасия', 3), 
           (204, 'Игорь', 4)
    """)

# Отбор согласно заданию. Использовался Left Join
QUERY_GET_STUDENT = """ 
        SELECT s.Student_Id, s.Student_Name, s.School_Id, sh.School_Name
        FROM Students s
        LEFT JOIN School sh
        USING(School_Id)
        WHERE Student_Id = ?
    """


# Код скрипта
def get_connection() -> Connection:
    """ Создание соединения с БД """
    return sqlite3.connect("teachers.db")
   

def close_connection(connection: Connection):
    """ Завершение соединения с БД """
    if connection:
        connection.close() 

 
def set_query():
    """ Создание таблицы и внесение данных """
    connection = get_connection()
    cursor = connection.cursor()
    for query in QUERY_CREATE_AND_FILL_TABLE:
        cursor.execute(query)
    
    # коммит для внесения данных в базу
    connection.commit()
    close_connection(connection)


def get_student(student_id: int) -> Tuple[str | int]:
        """ Получение данных студента по ID """

        connection = get_connection()
        cursor = connection.cursor()
        query = QUERY_GET_STUDENT

        cursor.execute(query, (student_id,))
        response = cursor.fetchone()
        close_connection(connection)
        return response


def init():
    """ Инициализация скрипта"""

    # Создание таблицы в базе
    print("Создание таблицы в базе...")
    try:
        set_query()
        print("Таблица внесена в базу \n")
    except sqlite3.OperationalError:
         print("Таблица  уже есть в базе \n")

    # Запуск цикла с запросом к базе
    while True:
        student_id = input('Пожалуйста введите ID ученика или 0 для завершения работы: ')

        # Валидация введенных данных
        if student_id.isalpha() or int(student_id) < 0:
            print("Допускается только ввод положительных целых чисел \n")
            continue

        else:

            # Условие останова скрипта
            if int(student_id) == 0:
                break

            try:
                student = get_student(student_id)
                print(
                    f'ID ученика: {student[0]}\n',
                    f'Имя ученика: {student[1]}\n',
                    f'ID Школы: {student[2]}\n',
                    f'Название школы: {student[3]}\n', 
                    sep=''
            )
            except (Exception, sqlite3.Error) as e:
                    if str(e) == "'NoneType' object is not subscriptable":
                         print("По указанному ID данных не найдено", '\n')
                    else:
                        print("Ошибка при получении данных: ", e, '\n')


if __name__ == "__main__":
    init()