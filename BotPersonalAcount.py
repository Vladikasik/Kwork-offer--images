import telebot
import config
from telebot import types
from DatabaseConfig import Database


class Bot:

    def __init__(self):

        self.bot = telebot.TeleBot(config.token)
        self.db = Database()

    def mainloop(self):

        # function need to be declareted Before you use it in next_step_handler
        def make_settings(message):
            params = message.text.split('_')

            # trying to check all the requirements for params
            if len(params) == 3:
                if params[0].startswith('(') and params[0].endswith(')') and params[1].startswith('(') and params[1].endswith(')'):
                    if params[2].isdigit():
                        coordinates = params[0] + ' ' + params[1]
                        self.db.write_settings_exact(message.from_user.id, coordinates,
                                                     params[3])  # params[3] is metres
                    else:
                        msg = self.bot.send_message(message.chat.id, "Мне кажется вы ввели что-то неправильно\n"
                                                                     "Кажется разброс в метрах вы указали не как число\n"
                                                                     "Попробуйте ещё раз")
                        self.bot.register_next_step_handler(msg, make_settings)  # recursion
                else:
                    msg = self.bot.send_message(message.chat.id, "Мне кажется вы ввели что-то неправильно\n"
                                                                 "Проверьте в каком формате вы ввели координаты\n"
                                                                 "Попробуйте ещё раз")
                    self.bot.register_next_step_handler(msg, make_settings)  # recursion
            else:
                msg = self.bot.send_message(message.chat.id, "Мне кажется вы ввели что-то неправильно\n"
                                                             "Проверьте что вы разделили все 3 параметра "
                                                             "нижним подчеркиванием '_'\n"
                                                             "Попробуйте ещё раз")
                self.bot.register_next_step_handler(msg, make_settings)  # recursion

        @self.bot.message_handler(commands=['start', 'help', 'balance', 'settings'])
        def send_welcome(message):
            if message.text == "/start":

                # create user in db if it is first launch
                if message.from_user.id not in self.db.get_all_ids():
                    name = message.from_user.first_name + ' ' + message.from_user.last_name
                    self.db.create_user(message.from_user.id, name, 1)

                self.bot.send_message(message.chat.id, "Здравствуйте, рады привествовать вас в боте!")
                self.bot.send_message(message.chat.id,
                                      "/photo - для изменения данных о фотографии\n"
                                      "/balance - баланс и пополнение\n"
                                      "/settings - изменение настроек по умолчанию")

            elif message.text == "/help":
                self.bot.send_message(message.chat.id, "Если есть вопросы/предложения, пешите @vladislav_ain")

            elif message.text == '/balance':
                self.bot.send_message(message.chat.id, "Информация о балансе\n"
                                                       f"На вашем счету {self.db.get_balance(message.from_user.id)} токенов\n"
                                                       "И тут какая-то муть с пополнением")
            elif message.text == '/settings':
                to_register = self.bot.send_message(message.chat.id,
                                                    "Вы зашли в меню настройки изменения координат в метаданных\n"
                                                    "Напишите /start чтобы выйти в главное меню\n\n"
                                                    "Напишите сначала исходные координаты потом разброс\n\n"
                                                    "Пример:\n"
                                                    "(55.0, 40.0, 51.64)_(37.0, 8.0, 15.02)_25\n"
                                                    "где (55.0, 40.0, 51.64) широта\n"
                                                    "где (37.0, 8.0, 15.02) долгота\n"
                                                    "где 25 это разброс в метрах\n\n"
                                                    "Пожалуйста, проверьте ещё раз ваше сообщение перед отправлением, "
                                                    "если вы что-либо заполнили неправильно, при отправке фотографии, "
                                                    "вам напишут что у вас ошибка в введеных данных\n"
                                                    "В таком случае, перейдите обратно в настройки и попробуйте ещё раз\n"
                                                    "Всё что вы сейчас настроите, будет применятся ко всем "
                                                    "фотографиям, пока вы снова не поменяете настройки\n"
                                                    "Извините за неудобства в найтроке. В ближайшее время мы сделаем"
                                                    "процесс настройке гараздо легче.")
                self.bot.register_next_step_handler(to_register,
                                                    make_settings)  # waiting for next message with settings
                                                                    # messsage with setting is processed in make_settings()


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
