#!/usr/bin/python

import csv
from pathlib import Path
import sqlite3
import sys
from config import DB_SCHEMA

# база вопросов и ответов
database = Path(__file__).parent / 'DATA' / DB_SCHEMA

# файл для парсинга, этот с диалогами из фильмов от яндекса
file = Path(__file__).parent / 'DATA' / 'good.csv'


def create_database():
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS answers')
        cur.execute('DROP TABLE IF EXISTS questions')
        cur.execute('DROP TABLE IF EXISTS logs')

        con.commit()

        cur.execute('''CREATE TABLE IF NOT EXISTS 'answers' (
                        'id' INTEGER NOT NULL UNIQUE,
                        'answer' TEXT NOT NULL,
                        PRIMARY KEY('id' AUTOINCREMENT)
                        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS 'questions' (
                        'id' INTEGER NOT NULL UNIQUE,
                        'answer_id' INTEGER NOT NULL,
                        'question' TEXT NOT NULL,
                        PRIMARY KEY('id' AUTOINCREMENT),
                        FOREIGN KEY('answer_id') REFERENCES 'answers' ('id')
                        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS 'logs' (
                        'id' INTEGER NOT NULL UNIQUE,
                        'user_id' INTEGER NOT NULL,
                        'chat_id' INTEGER NOT NULL,
                        'created_at' TEXT NOT NULL,
                        'event' TEXT NOT NULL,
                        PRIMARY KEY('id' AUTOINCREMENT)
                        )''')

        con.commit()
        cur.close()

    except sqlite3.Error as error:
        print(f'Ошибка при создании базы данных: {error}')
        return False

    finally:
        if con:
            con.close()

    return True


if not create_database():
    sys.exit(1)

try:
    con = sqlite3.connect(database)
    cur = con.cursor()

    with open(file, mode='r', encoding='utf-8') as r_file:
        reader = csv.reader(r_file, delimiter='\t', lineterminator='\r')

        # для скорости тут только транзакции без коммита
        for i, line in enumerate(reader):
            if i % 10 == 0:
                print(f'{i} records handled...\r', end='')

            cur.execute(
                "SELECT id, answer FROM answers WHERE answer = ?", (line[0],))

            result = cur.fetchone()

            if result == None:
                cur.execute(
                    "INSERT INTO answers (answer) VALUES (?)", (line[0],))
                cur.execute(
                    "INSERT INTO questions (question, answer_id) VALUES (?, ?)", (line[1], cur.lastrowid))
            else:
                cur.execute(
                    "INSERT INTO questions (question, answer_id) VALUES (?, ?)", (line[1], result[0]))

    # а тут уже коммиттим все оставшиеся транзакции
    con.commit()
    cur.close()

    print(f'Total {i} records handled, done!')

except sqlite3.Error as error:
    print(f'\nОшибка при работе с базой данных: {error}')
    sys.exit(1)

finally:
    if con:
        con.close()

sys.exit(0)
