import telebot
import config
from telebot import types
from DatabaseConfig import Database
from GpsEditor import GPS
from PhotoDataChanger import ImageEditor


class Bot:

    def __init__(self):

        self.bot = telebot.TeleBot(config.token)
        self.db = Database()

        self.query = {}

    def mainloop(self):

        # function need to be declareted Before you use it in next_step_handler
        def make_gps(message):
            params = message.text.split('_')

            if message.text != '/start':  # to let people exit from settings
                # trying to check all the requirements for params
                if len(params) == 3:
                    try:
                        are_degrees = float(params[0]) and float(params[1])
                    except:
                        are_degrees = False
                    if are_degrees and params[2].isdigit():
                        coordinates = params[0] + '_' + params[1]
                        self.db.write_settings_exact(message.from_user.id, coordinates,
                                                     params[2])  # params[2] is metres
                        self.bot.send_message(message.chat.id, "Мы записали ваши настройки\n"
                                                               "Нажмите или напишите /start чтобы перейти в главное меню")
                    else:
                        msg = self.bot.send_message(message.chat.id, "Мне кажется вы ввели что-то неправильно\n"
                                                                     "Попробуйте ещё раз")
                        self.bot.register_next_step_handler(msg, make_gps)
                else:
                    msg = self.bot.send_message(message.chat.id, "Мне кажется вы ввели что-то неправильно\n"
                                                                 "Проверьте что вы разделили все 3 параметра "
                                                                 "нижним подчеркиванием '_'\n"
                                                                 "Попробуйте ещё раз")
                    self.bot.register_next_step_handler(msg, make_gps)  # recursion
            else:
                send_welcome(message)

        def edit_and_send_photo(message):
            print(self.query[message.from_user.id])
            print(message.document)
            file_id_info = self.bot.get_file(message.document.file_id)
            downloaded_file = self.bot.download_file(file_id_info.file_path)
            with open(str(message.document.file_name), 'wb') as file:
                file.write(downloaded_file)
            editor = ImageEditor(str(message.document.file_name), self.query[message.from_user.id])
            answer = editor.edit_image()
            if answer is not False:
                self.bot.send_document(message.chat.id, open(answer, 'rb'))

        def make_photo(message):
            if message.text.startswith('+') or message.text.startswith('-'):
                splited = message.text.split(' ')
                if len(splited) == 3:
                    edit_to = int(splited[0][1:]) * 1440 + int(splited[1]) * 60 + int(splited[2])
                    is_plus = splited[0][:1] == '+'
                    self.query[message.from_user.id]["time"] = [edit_to, is_plus]
                    photo_wait = self.bot.send_message(message.chat.id, "Все настройки заполнены!\n"
                                                                        "Теперь пришлите фото которое вы хотите изменить")
                    self.bot.register_next_step_handler(photo_wait, edit_and_send_photo)
                else:
                    msg = self.bot.send_message(message.chat.id, "Вы неправильно ввели изменение времени\n"
                                                                 "Данный параметр разделен на 3 пункта ПРОБЕЛАМИ\n"
                                                                 "Первый пункт +5 или -5 часов\n"
                                                                 "Второй пункт через пробел - кол-во минут\n"
                                                                 "Третий пункт через пробел - кол-во секунд\n"
                                                                 "Попробуйте ещё раз")
                    self.bot.register_next_step_handler(msg, make_photo)  # recursion
            else:
                msg = self.bot.send_message(message.chat.id, "Вы неправильно ввели изменение времени\n"
                                                             "Данный параметр должен начинаться\n"
                                                             "Либо с минуса -\n"
                                                             "Либо с плюса +\n"
                                                             "В зависимости от того, прибавляете вы или "
                                                             "отнимаете время от оригинала\n"
                                                             "Попробуйте ещё раз")
                self.bot.register_next_step_handler(msg, make_photo)  # recursion

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
                                                    "55.7522200_37.6155600_25\n"
                                                    "где 55.7522200 широта\n"
                                                    "где 37.6155600 долгота\n"
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
                                                    make_gps)  # waiting for next message with settings
                # messsage with setting is processed in make_settings()
            elif message.text == '/photo':

                settings_info = self.db.get_user_settings(message.from_user.id)

                # to say fuck off if something wrong
                if self.db.get_balance(message.from_user.id) > 0:
                    if settings_info:
                        data = self.db.get_user_settings(message.from_user.id)
                        coordinates = data['coordinates']
                        metres = data['raszbros']
                        try:
                            gps = GPS(coordinates, metres)
                            new_one = gps._edit()
                            self.query[message.from_user.id] = {"gps": new_one}
                            self.bot.send_message(message.chat.id, f"Ваши сгенерированные координаты:\n"
                                                                   f"{new_one[0]}\n"
                                                                   f"{new_one[1]}")
                            msg = self.bot.send_message(message.chat.id, "Осталось совсем чуть-чуть\n"
                                                                         "Просто введите как вы хотите изменить время\n\n"
                                                                         "Пример\n"
                                                                         "-1 0 3\n"
                                                                         "что означает изменить время на\n"
                                                                         "оригинальное минус 1 сутки 0 часов 3 минуты\n\n"
                                                                         "+0 2 5\n"
                                                                         "что означает изменить время на\n"
                                                                         "оригинальное плюс 0 суток 2 часа 5 минут\n\n"
                                                                         "Пожалуйста учтите что писать нули нужно ОБЯЗАТЕЛЬНО "
                                                                         "для корректной работы программы")
                            self.bot.register_next_step_handler(msg, make_photo)
                        except Exception as ex:
                            print(ex)
                            self.bot.send_message(message.chat.id, "Проболема в считывании координат, "
                                                                   "скорее всего вы где-то ошиблись.\n"
                                                                   "Попробуйте заново настроить gps\n"
                                                                   "Просто напишите /latlon для настройки gps")

                    else:
                        self.bot.send_message(message.chat.id,
                                              "Для отправки фото вам сначала нужно заполнить "
                                              "настройки gps по умолчанию.\n"
                                              "Сделать это можно написав команду /latlon")
                else:
                    self.bot.send_message(message.chat.id, "У вас недостаточно токенов на балансе.\n"
                                                           "Напишите /balance для пополнения")
            else:
                self.bot.send_message(message.chat.id, "Извините, я вас не понимаю\n"
                                                       "Напишите /start для навигации по боту")

        self.bot.polling()


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
