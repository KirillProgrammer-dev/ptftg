import telebot
import random
import csv
from telebot import types

token = "5591141286:AAGbqApi0iQ6f8EvplsHuMWxSwiKEOA8hMc"

bot = telebot.TeleBot(token)

def checkRefLinkInCsv(id):
    with open('info.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if id == row[0]:
                return (True, row[1])
        return (False, "")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет это система реферальных ссылок")
    if len(message.text.split()) == 2:
        id = message.text.split()[1]
        with open('user_from_to.csv', mode='a+') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([str(id), str(message.from_user.id), 0])
        #bot.send_message(message.chat.id, "Ваш id: " + str(id))  
        bot.send_message(message.chat.id, "Чтобы подарить бонусы другу подпишитесь на канал")  
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("✅ Я подписался")
        markup.add(btn1)
        bot.send_message(message.chat.id, "https://t.me/elen_house", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "Введите /ref для получения уникальной реферальной ссылки")

@bot.message_handler(commands=['ref'])
def ref_message(message):
    print(1)
    with open('info.csv', mode='a+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        res = checkRefLinkInCsv(str(message.from_user.id))
        print(res)
        if res[0]:
            bot.send_message(message.chat.id, "Вы уже получали свою реферальную ссылку" + res[1])
        else:
            ref_url = "http://t.me/ptichya_ferma_bot?start=" + str(message.from_user.id)
            bot.send_message(message.chat.id, ref_url)
            csv_writer.writerow([str(message.from_user.id), ref_url, "0"])
            
@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text == "✅ Я подписался":
        try:
            bot.get_chat_member(chat_id='-1001760319966', user_id=message.from_user.id)
            lines = []
            with open("info.csv", "r") as f:
                reader = csv.reader(f, delimiter="\t")
                for line in reader:
                    lines.append(line[0].split(","))

            with open('user_from_to.csv', 'rt') as f:
                reader = csv.reader(f, delimiter=',')
                done = False
                rows = []
                for row in reader:
                    rows.append(row)
                    if str(message.from_user.id) == row[1]:
                        for i in range(1, len(lines) + 1):
                            if lines[i][0] == row[0] and int(row[2]) == 0:
                                lines[i][2] = str(int(lines[i][2]) + 1)
                                done = True
                                row[2] = 1
                                rows[-1] = row
                                with open('user_from_to.csv', 'w') as f1:
                                    f1q = csv.writer(f1, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                    f1q.writerows(rows)
                                with open('info.csv', mode='w') as csv_file:
                                    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                    csv_writer.writerows(lines)
                                    bot.send_message(message.chat.id, "Вашему другу начислелись бонусы")
                                break
                            elif lines[i][0] == row[0] and int(row[2]) == 1:
                                bot.send_message(message.chat.id, "Вы уже воспользовались реферальной программой")
                    if done: break

        except: bot.send_message(message.chat.id, "Вы не подписаны")

bot.polling()