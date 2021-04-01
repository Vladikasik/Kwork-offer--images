import telebot
import config
from telebot import types
from DatabaseConfig import Database
from GpsEditor import GPS


class Bot:

    def __init__(self):

        self.bot = telebot.TeleBot(config.token)
        self.db = Database()

    def mainloop(self):

        # function need to be declareted Before you use it in next_step_handler
        def make_settings(message):
            params = message.text.split('_')

            if message.text != '/start':  # to let people exit from settings
                # trying to check all the requirements for params
                if len(params) == 3:
                    if params[0].startswith('(') and params[0].endswith(')') \
                            and params[1].startswith('(') and params[1].endswith(')'):
                        if params[2].isdigit():
                            coordinates = params[0] + '_' + params[1]
                            self.db.write_settings_exact(message.from_user.id, coordinates,
                                                         params[2])  # params[2] is metres
                            self.bot.send_message(message.chat.id, "Мы записали ваши настройки\n"
                                                                   "Нажмите или напишите /start чтобы перейти в главное меню")
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

        @self.bot.message_handler(commands=['start', 'help', 'balance', 'photo', 'latlon', 'zip'])
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
                                      "/latlon - изменение настроек gps по умолчанию\n"
                                      "/zip - изменение настроек сжатия по умолчанию")

            elif message.text == "/help":
                self.bot.send_message(message.chat.id, "Если есть вопросы/предложения, пешите @vladislav_ain")

            elif message.text == '/balance':
                self.bot.send_message(message.chat.id, "Информация о балансе\n"
                                                       f"На вашем счету {self.db.get_balance(message.from_user.id)} токенов\n"
                                                       "И тут какая-то муть с пополнением\n\n"
                                                       "Напишите /start чтобы вернуться в меню")
            elif message.text == '/latlon':
                self.bot.send_message(message.chat.id, "Вы зашли в меню настройки изменения координат в метаданных\n"
                                                       "Напишите /start чтобы выйти в главное меню\n\n")
                settings_info = self.db.get_user_settings(message.from_user.id)
                if settings_info:
                    self.bot.send_message(message.chat.id, f"Ваши настройки сечас\n"
                                                           f"Координаты - {settings_info['coordinates']}\n"
                                                           f"Разброс в метрах - {settings_info['raszbros']}")
                to_register = self.bot.send_message(message.chat.id,
                                                    "Если вы хотите изменить/задать настройки\n\n"
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
            elif message.text == '/photo':
                settings_info = self.db.get_user_settings(message.from_user.id)
                if self.db.get_balance() > 0:
                    if settings_info:
                        data = self.db.get_user_settings(message.from_user.id)
                        pre_coordinates = data['coordinates']
                        metres = data['raszbros']
                        coordinates = [tuple([float(i) for i in i.replace('(', '').replace(')', '').split(', ')]) for i in pre_coordinates.split('_')]
                        gps = GPS(coordinates, metres)
                        self.bot.send_message(message.chat.id, "")
                    else:
                        self.bot.send_message(message.chat.id,
                                              "Извините, но для отправки фото вам сначала нужно заполнить "
                                              "настройки gps по умолчанию.\n"
                                              "Сделать это можно написав команду /latlon")
                else:
                    self.bot.send_message(message.chat.id, "Извините, у вас недостаточно токенов на балансе.\n"
                                                           "Напишите /balance для пополнения")
            else:
                self.bot.send_message(message.chat.id, "Извините, я вас не понимаю\n"
                                                       "Напишите /start для навигации по боту")

        self.bot.polling()


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
