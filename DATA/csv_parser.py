import csv
import pymysql
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_SCHEMA

# файл для парсинга, этот с диалогами из фильмов от яндекса
file = "C:\\GitHub\\geekbrains\\007_python\\007_PY_HW09\\DATA\\good.csv"

CONN = pymysql.connect(host = DB_HOST, port = DB_PORT, user = DB_USER, password = DB_PASS, db = DB_SCHEMA, charset='utf8')

323232
with open(file, mode="r", encoding="utf-8") as r_file:
    reader = csv.reader(r_file, delimiter = "\t", lineterminator="\r")
    for i, line in enumerate(reader):
        # Берем 2 (вопрос от пользователя) и 3 (ответ от бота)
        # print(line[0] + "|" + line[1] + "|" +  line[2] + "|" +  line[3] + "|" + line[4])
        with CONN.cursor() as c: 
            c.execute('SELECT id, answer FROM answers WHERE answer = %s;', line[0])
            CONN.commit()

            result = c.fetchone()
            print(result)

            if result == None:
                with CONN.cursor() as c:      
                    c.execute("INSERT INTO answers (answer) VALUES (%s);", (line[0]))
                    CONN.commit()

                    c.execute("INSERT INTO questions (question, answer_id) VALUES (%s, %s);", (line[1], c.lastrowid))
                    CONN.commit()
          
            else:
                c.execute("INSERT INTO questions (question, answer_id) VALUES (%s, %s);", (line[1], result[0]))
                CONN.commit()

