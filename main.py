import telebot
import os

from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# 🔥 Username канала
CHANNEL_USERNAME = "@obyavleniy_online"

# 🔥 ID канала
# пример: -1001234567890
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = telebot.TeleBot(TOKEN)

# =========================
# КНОПКИ
# =========================

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton("📢 Подпишись на канал")
    btn2 = KeyboardButton("📝 Разместить объявление")
    btn3 = KeyboardButton("ℹ️ Информация")

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    return markup


# =========================
# ПРОВЕРКА ПОДПИСКИ
# =========================

def check_subscription(user_id):

    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status in ["member", "administrator", "creator"]:
            return True

    except Exception as e:
        print(e)

    return False


# =========================
# START
# =========================

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать!\n\n"
        "Здесь можно бесплатно разместить объявление.\n\n"
        "Выберите действие 👇",
        reply_markup=main_menu()
    )


# =========================
# КНОПКА КАНАЛА
# =========================

@bot.message_handler(func=lambda m: m.text == "📢 Подпишись на канал")
def open_channel(message):

    bot.send_message(
        message.chat.id,
        f"📢 Наш канал:\nhttps://t.me/obyavleniy_online"
    )


# =========================
# ИНФОРМАЦИЯ
# =========================

@bot.message_handler(func=lambda m: m.text == "ℹ️ Информация")
def info(message):

    bot.send_message(
        message.chat.id,
        "📌 Как разместить объявление:\n\n"
        "Отправьте одним сообщением:\n"
        "— категория\n"
        "— город\n"
        "— описание\n"
        "— контакт\n\n"
        "Пример:\n"
        "Работа\nМосква\nКурьер 3000₽\n@username"
    )


# =========================
# РАЗМЕСТИТЬ ОБЪЯВЛЕНИЕ
# =========================

@bot.message_handler(func=lambda m: m.text == "📝 Разместить объявление")
def create_ad(message):

    user_id = message.from_user.id

    # ✅ проверка подписки
    if check_subscription(user_id):

        bot.send_message(
            message.chat.id,
            "✍️ Отправьте ваше объявление одним сообщением 👇"
        )

    else:

        markup = InlineKeyboardMarkup()

        btn1 = InlineKeyboardButton(
            "📢 Подписаться",
            url="https://t.me/obyavleniy_online"
        )

        btn2 = InlineKeyboardButton(
            "✅ Я подписался",
            callback_data="check_sub"
        )

        markup.add(btn1)
        markup.add(btn2)

        bot.send_message(
            message.chat.id,
            "❌ Чтобы разместить объявление,\n"
            "пожалуйста подпишитесь на наш канал 👇",
            reply_markup=markup
        )


# =========================
# ПРОВЕРКА ПОСЛЕ ПОДПИСКИ
# =========================

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):

    user_id = call.from_user.id

    if check_subscription(user_id):

        bot.answer_callback_query(
            call.id,
            "✅ Подписка подтверждена!"
        )

        bot.send_message(
            call.message.chat.id,
            "✍️ Теперь отправьте ваше объявление одним сообщением 👇"
        )

    else:

        bot.answer_callback_query(
            call.id,
            "❌ Вы ещё не подписались"
        )


# =========================
# ПРИЁМ ОБЪЯВЛЕНИЙ
# =========================

@bot.message_handler(content_types=['text'])
def handle_message(message):

    user = message.from_user

    # игнор кнопок
    if message.text in [
        "📢 Подпишись на канал",
        "📝 Разместить объявление",
        "ℹ️ Информация"
    ]:
        return

    # повторная проверка подписки
    if not check_subscription(user.id):

        bot.send_message(
            message.chat.id,
            "❌ Сначала подпишитесь на канал."
        )

        return

    # сообщение пользователю
    bot.send_message(
        message.chat.id,
        "✅ Объявление принято!\n\n"
        "Мы опубликуем его в ближайшее время."
    )

    # пост в канал
    post = (
        f"📢 Новое объявление\n\n"
        f"{message.text}\n\n"
        f"👤 @{user.username if user.username else 'без username'}"
    )

    bot.send_message(
        CHANNEL_ID,
        post
    )

    # отправка админу
    bot.send_message(
        ADMIN_ID,
        post
    )


# =========================
# ЗАПУСК
# =========================

print("Бот запущен...")

bot.infinity_polling()
