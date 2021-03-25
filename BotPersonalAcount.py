import telebot
import config
from telebot import types


class Bot:

    def __init__(self):

        self.bot = telebot.TeleBot(config.token)

        self.main_message = None

        self.main_menu_keyboard = types.InlineKeyboardMarkup

    def mainloop(self):

        @self.bot.message_handler(commands=['start', 'help', 'id'])
        def send_welcome(message):
            if message.text == "/start":
                self.bot.send_message(message.chat.id, "Здравствуйте, рады привествовать вас в боте!")
                self.main_message = self.bot.send(message.chat.id, "Управляйте бот кнопками\nВсё интуитивно понятно\nЕсли возникли вопросы напишите /help")
            elif message.text == "/help":
                self.bot.send_message(message.chat.id, "Если есть вопросы/предложения, пешите @vladislav_ain")

        @self.bot.callback_query_handler(func=lambda call: True)
        def buttons(call):


        self.bot.polling()


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
