import telebot
from settings import TOKEN, ChatID

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start', 'начать'])
def start(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Привет! Я буду отправлять уведомления в Ваш чат, добавьте в настройках Ваш id либо id Вашего канала')


def send_to_tg(data, ind, ChatID=ChatID):
    bot.send_message(chat_id=ChatID, text='Таблица обновлена')
    if ind:
        bot.send_message(chat_id=ChatID, text='В талице есть просроченные поставки:')
        bot.send_message(chat_id=ChatID, text=data.to_string(index=False))


def send_error(data, ind, ChatID=ChatID):
    bot.send_message(chat_id=ChatID, text=data)


if __name__ == "__main__":
    bot.polling()
