import telebot
from telegram.constants import ParseMode
from telebot import types
import math

# Токен вашего бота
TOKEN = '5916927645:AAE9Us2hug9n-qdzPQqr1JfBl06psjQfVbU'

# Создание экземпляра бо
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояний пользователей
user_states = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Рассчитать стоимость')
    btn2 = telebot.types.KeyboardButton('Акции')
    btn3 = telebot.types.KeyboardButton('Ответы на вопросы')
    markup.add(btn1, btn2, btn3)

    bot.send_photo(message.chat.id, photo=open('bot.jpg', 'rb'),
                   caption="<b>Привет! Это бот TaoPoizon Express! Я предназначен для того чтобы вы покупали из Китая выгодно! 💰\nВыберите действие:</b>", reply_markup=markup)



# Обработчик кнопки "Вернуться на главную"
@bot.message_handler(func=lambda message: message.text == 'Вернуться на главную')
def handle_back_to_main_button(message):
    user_states[message.chat.id] = 'waiting_for_action'  # Сбрасываем состояние пользователя
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Рассчитать стоимость')
    btn2 = telebot.types.KeyboardButton('Акции')
    btn3 = telebot.types.KeyboardButton('Ответы на вопросы')
    markup.add(btn1, btn2, btn3)

    bot.send_message(
        message.chat.id,
        "Что-то пошло не так? Ладно, давай выберем действие:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == 'Ответы на вопросы')
def handle_answers_button(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Как скачать POIZON?',
                                      url='https://telegra.ph/Kak-skachat-i-zaregistrirovatsya-v-POIZON-08-03')
    btn2 = types.InlineKeyboardButton(text='Как зарегистрироваться в POIZON?',
                                      url='https://telegra.ph/Kak-zaregistrirovatsya-v-POIZON-08-03')
    btn3 = types.InlineKeyboardButton(text='Как ориентироваться в POIZON',
                                      url='https://telegra.ph/CHto-oznachayut-ehti-vse-kitajskie-bukovy-08-03')
    btn4= types.InlineKeyboardButton(text='Не могу скачать/зарегистрироваться/найти нужный мне товар',
                                      url='https://t.me/EgorighX')
    btn5 = types.InlineKeyboardButton(text='У меня вопрос по Taobao, Alibaba или 1688',
                                      url='https://t.me/EgorighX')

    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    markup.row(btn4)
    markup.row(btn5)


    bot.send_message(message.chat.id, "Выберите вопрос, который вас интересует:", reply_markup=markup)


#Кнопка акции
@bot.message_handler(func=lambda message: message.text == 'Акции')
def handle_discounts_button(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn3 = telebot.types.KeyboardButton('Вернуться на главную')

    markup.add(btn3)
    bot.send_message(
        message.chat.id,
        "У нас сейчас действует специальное предложение! 🎉\n"
        "Ознакомьтесь со статьей о наших акциях:\n"
        "https://t.me/pt68china/70",
        reply_markup=markup,
        disable_web_page_preview=False
    )




# Обработчик нажатия на кнопку "Рассчитать стоимость"
@bot.message_handler(func=lambda message: message.text == 'Рассчитать стоимость')
def handle_price_button(message):
    user_states[message.chat.id] = 'waiting_for_x'
    bot.send_message(message.chat.id, "Введите стоимость в Юанях: 💴")


# Обработка введенного значения X
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_x')
def handle_x_input(message):
    try:
        x = int(message.text)
        if x <= 2000:
            total_cost = math.ceil(x * 1.18 / 0.075)

        else:
            total_cost = math.ceil(x * 1.15 / 0.075)


        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_make_order = telebot.types.KeyboardButton('Сделать заказ ✅')
        btn_calculate_again = telebot.types.KeyboardButton('Посчитать снова 🧮')
        btn_main = telebot.types.KeyboardButton ('Вернуться на главную')
        markup.add(btn_make_order, btn_calculate_again, btn_main)

        bot.send_message(
            message.chat.id,
            f"<b>Примерная стоимость заказа: {total_cost} рублей.\nЦена доставки не входит❗ \nОплата доставки после прибытия заказа в ваш город❗</b>",
            reply_markup=markup,
            parse_mode=ParseMode.HTML
        )
        user_states[message.chat.id] = 'waiting_for_action'
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод.")



# Обработчик нажатия на кнопки "Сделать заказ" или "Посчитать снова"
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_action')
def handle_action_buttons(message):
    if message.text == 'Сделать заказ ✅':
        bot.send_message(message.chat.id, "Для оплаты вашего заказа пишите только сюда❗ \n⬇️⬇️⬇️"
                                          
                                          "\n@EgorighX")
    elif message.text == 'Посчитать снова 🧮':
        user_states[message.chat.id] = 'waiting_for_x'
        bot.send_message(message.chat.id, " Введите стоимость в Юанях:")

# Запуск бота
bot.polling(none_stop=True)
