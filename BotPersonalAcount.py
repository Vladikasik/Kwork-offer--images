import telebot
import config

class Bot:

    def __init__(self):

        self.bot = telebot.TeleBot(config.token)
    
    def mainloop(self):

        @self.bot.message_handler(commands=['start', 'help', 'id'])
        def send_welcome(message):
            print(message)
            if message == "/start":
                self.bot.send_message(message.from_user.id, "Здравствуйте, рады привествовать вас в боте!")
            elif message == "/help":
                self.bot.send_message(message.from_user.id, "Если есть вопросы/предложения, пешите @vladislav_ain")
            elif message == '/id':
                self.bot.send_message(message.from_user.id, f"Ваш id {str(message.from_user.id)}")    


        self.bot.polling()


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()