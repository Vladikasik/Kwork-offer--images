import telebot
import config

class Bot:

    def __init__(self):

        self.bot = telebot.Telebot(config.token)
    
    def mainloop(self):

        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            bot.reply_to(message, "Howdy, how are you doing?")  


        self.bot.mainloop()