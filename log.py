import db


def bot(text, chat_id):
    '''Logging BOT answers'''
    db.insert_log(text, -1, int(chat_id))


def user(message):
    '''Logging USER answers'''
    db.insert_log(message.text, int(
        message.from_user.id), int(message.chat.id))
