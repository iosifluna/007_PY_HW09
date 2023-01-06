from pathlib import Path
import sqlite3
from config import DB_SCHEMA

''' INSERT '''


def insert_log(event, user_id, chat_id):
    '''Logging chat'''

    con = sqlite3.connect(Path(__file__).parent / 'DATA' / DB_SCHEMA)
    cur = con.cursor()
    cur.execute('''INSERT INTO logs (event, user_id, chat_id, created_at) \
                VALUES (?, ?, ?, DATETIME('NOW'))''', (event, user_id, chat_id))
    cur.close()
    con.commit()
    con.close()


''' SELECT'''


def get_answers():
    '''Answers data'''

    con = sqlite3.connect(Path(__file__).parent / 'DATA' / DB_SCHEMA)
    cur = con.cursor()
    cur.execute('SELECT id, answer FROM answers')

    retval = cur.fetchall()

    cur.close()
    con.commit()
    con.close()

    return retval


def get_questions():
    '''Questions data'''

    con = sqlite3.connect(Path(__file__).parent / 'DATA' / DB_SCHEMA)
    cur = con.cursor()
    cur.execute('SELECT question, answer_id FROM questions')

    retval = cur.fetchall()

    cur.close()
    con.commit()
    con.close()

    return retval
