import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")  # канал

bot = telebot.TeleBot(TOKEN)

# --- КНОПКИ ---
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("📢 Подпишись на канал")
    btn2 = KeyboardButton("📝 Разместить объявление")
    btn3 = KeyboardButton("ℹ️ Информация")
    markup.add(btn1)
    markup.add(btn2, btn3)
    return markup

# --- СТАРТ ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать!\n\n"
        "Здесь можно бесплатно разместить объявление.\n\n"
        "Выберите действие 👇",
        reply_markup=main_menu()
    )

# --- ПОДПИСКА ---
@bot.message_handler(func=lambda m: m.text == "📢 Подпишись на канал")
def subscribe(message):
    bot.send_message(
        message.chat.id,
        "👉 Подпишитесь на канал:
        \n\nhttps://t.me/tg_obyavleniya_onlane"
        )
    

# --- ИНФОРМАЦИЯ ---
@bot.message_handler(func=lambda m: m.text == "ℹ️ Информация")
def info(message):
    bot.send_message(
        message.chat.id,
        "📌 Как разместить объявление:\n\n"
        "Отправьте одним сообщением:\n"
        "— категория\n— город\n— описание\n— контакт"
    )

# --- РАЗМЕСТИТЬ ---
@bot.message_handler(func=lambda m: m.text == "📝 Разместить объявление")
def create_ad(message):
    bot.send_message(
        message.chat.id,
        "✍️ Отправьте объявление одним сообщением 👇"
    )

# --- ПРИЁМ ОБЪЯВЛЕНИЙ ---
@bot.message_handler(content_types=['text'])
def handle_message(message):
    user = message.from_user

    if message.text in [
        "📢 Подпишись на канал",
        "📝 Разместить объявление",
        "ℹ️ Информация"
    ]:
        return

    bot.send_message(message.chat.id, "✅ Объявление опубликовано!")

    post = (
        f"📢 Новое объявление\n\n"
        f"{message.text}\n\n"
        f"👤 @{user.username if user.username else 'без username'}"
    )

    # 👉 ПУБЛИКАЦИЯ В КАНАЛ
    bot.send_message(CHANNEL_ID, post)

    # 👉 ТЕБЕ (админу)
    bot.send_message(ADMIN_ID, post)

# --- ЗАПУСК ---
bot.infinity_polling()
