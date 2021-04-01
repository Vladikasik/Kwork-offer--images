import telebot
import config
from telebot import types
from DatabaseConfig import Database


class Bot:

    def __init__(self):

        self.bot = telebot.TeleBot(config.token)
        self.db = Database()

    def mainloop(self):

        @self.bot.message_handler(commands=['start', 'help', 'balance', 'settings'])
        def send_welcome(message):
            if message.text == "/start":
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
                                                    "Напишите 1 если вы хотите указать предел разброса координат\n"
                                                    "Напишите 2 если вы хотите указать конкретные координаты\n\n"
                                                    "Всё что вы сейчас настроите, будет применятся ко всем "
                                                    "фотографиям, пока вы снова не поменяете настройки")
                self.db.write_settings_exact(message.from_user.id, coordinates=None)
                self.bot.register_next_step_handler(to_register)

        @self.bot.callback_query_handler(func=lambda call: True)
        def buttons(call):

            # juat because it is needed to be here idk
            def _photo_edit(message):
                # getting settings
                data = self._get_query(message.text)
                self.settings[message.from_user.id] = data
                self.bot.send_message(call.message.chat.id, "Теперь пришлите фотографию, которую вы хотите изменить")

            if call.data == 'change_photo':
                self.bot.send_message(call.message.chat.id,
                                      "Ваш баланс состовляет {} коинов. Вы можете сделать {} запросов.\n")
                self.bot.send_message(call.message.chat.id,
                                      "Следующим сообщением напиши настройки для изменения данных\n\n"
                                      "1) Время - используеться только дни часы минуты\n"
                                      "Пример - ('1 мин', '1 час 1 секунда', '23 дня 5 часов 7 секунд'\n"
                                      "в пределее указанного значения время в метаданных фотографии"
                                      "будет изменено время(+- 1 минута, +- 1 час 1 минута)\n\n"
                                      "2) Расположение - используются только метры (целое кол-во)\n"
                                      "Пример - ('1 метр', '5 метров', '23 метра')"
                                      "в пределее указанного значения время в метаданных фотографии"
                                      "будет изменены gps координаты (+- 1 метр, +- 5 метров)\n\n"
                                      )
                self.bot.send_message(call.message.chat.id,
                                      "Как может выглядеть ваш запрос")
                self.bot.send_message(call.message.chat.id,
                                      "1 дня 0 часов 3 минуты\n"
                                      "20 метров")
                a = self.bot.send_message(call.message.chat.id,
                                          "Если я не пойму я сообщу, в конце, мы всё равно сверимся, всё ли верно",
                                          reply_markup=self.back_button_keyboard
                                          )
                self.bot.register_next_step_handler(a, _photo_edit)

            elif call.data == 'back_to_main':
                self.bot.send_message(call.message.chat.id,
                                      "Управляйте бот кнопками\n"
                                      "Всё интуитивно понятно\n"
                                      "Если возникли вопросы напишите /help",
                                      reply_markup=self.main_menu_keyboard)

            elif call.data == 'balance':
                self.bot.send_message(call.message.chat.id,
                                      "оплата бла бла бла",
                                      reply_markup=self.back_button_keyboard)

        self.bot.polling()

    def _get_query(self, text):
        return {'time': 3,
                'gps': 8}


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
