import db


# Logging BOT answers
def bot(text, chat_id):
    db.insert_log(text, -1, int(chat_id))


# Logging USER answers
def user(message):
    db.insert_log(message.text, int(message.from_user.id), int(message.chat.id))