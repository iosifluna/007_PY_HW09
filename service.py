# TODO переделать всё в методы из общей каши, научить бота спрашивать если неправильно ответил и что отвечать правильно



# TODO status, undefined
# def answer_bot(text):
#     # 0 - not in BD, 1 - undefined, 2 - approved
#     #status = 2

#     # Get data from confirmed answers 
#     answer_approved = db.select_data("answer", "approved", "question", text)

#     if answer_approved != None:
#         #return (answer_approved, status);
#         return (answer_approved);
    
#     else:
#         return None;


    # else:
    #     # Get data from non confirmed answers   
    #     answer_undefined = db.select_data("answer", "undefined", "question", text)

    #     if answer_undefined != None:
    #         status = 1
    #         return (answer_undefined, status);

    #     else:
    #         status = 0
    #         return ("Я такого не знаю", status);



# def learning(wrong, right):
# 	a = f"{question}\{message.text.lower()} \n"
# 	with open('dialogues.txt', "a", encoding='utf-8') as f:
# 		f.write(a)
# 	bot.send_message(message.from_user.id, "Готово")
# 	update()
