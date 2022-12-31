import pymysql

from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_SCHEMA


CONN = pymysql.connect(host = DB_HOST, port = DB_PORT, user = DB_USER, password = DB_PASS, db = DB_SCHEMA, charset='utf8')

''' INSERT '''

# Logging chat
def insert_log(event, user_id, chat_id):

    with CONN.cursor() as c:      
        c.execute("INSERT INTO logs (event, user_id, chat_id, created_at) \
                            VALUES (%s, %s, %s, CURRENT_TIMESTAMP());", (event, user_id, chat_id))
        CONN.commit()


''' SELECT'''

# Answers data
def get_answers():
    with CONN.cursor() as c: 
        c.execute('SELECT id, answer FROM answers;')
        CONN.commit()

        return c.fetchall()


# Questions data
def get_questions():
    with CONN.cursor() as c: 
        c.execute('SELECT question, answer_id FROM questions;')
        CONN.commit()

        return c.fetchall()

