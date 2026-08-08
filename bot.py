import os
from flask import Flask
from threading import Thread
import telebot

# Bot tokeningiz
TOKEN = "8971695245:AAEKEq3VEuDiY_SHGyBijmEcSll_r-VXNxY"
bot = telebot.TeleBot(TOKEN)

# --- FLASK SERVER (Render porti uchun) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot serveri muvaffaqiyatli ishlayapti!"

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()


# --- BOT HANDLERLARI (Sizning kodingiz) ---
@bot.message_handler(commands=['start'])
def start_buyrugi(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("💅 Xizmatlar va Narxlar")
    btn2 = telebot.types.KeyboardButton("📍 Manzil va Aloqa")
    btn3 = telebot.types.KeyboardButton("📷 Bizning ishlarimiz")

    markup.add(btn1)
    markup.add(btn2, btn3)

    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "\"Dilya Ledy\" go'zallik saloni botiga xush kelibsiz.\n"
        "Xizmatlarni ko'rish uchun pastdagi tugmalardan birini bosing!",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def tugmalar_uchun(message):
    if message.text == "💅 Xizmatlar va Narxlar":
        try:
            with open("Xizmat va narxlar.jpg", "rb") as photo:
                bot.send_photo(
                    message.chat.id, 
                    photo, 
                    caption="✨ Salonimizdagi xizmatlar va narxlar ro'yxati:"
                )
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Xizmatlar va narxlar rasmi topilmadi.")

    elif message.text == "📍 Manzil va Aloqa":
        text = (
            "📍 **Bizning manzil:** Toshkent shahri...\n"
            "📞 **Aloqa uchun:** +998 90 123 45 67\n"
            "⏰ **Ish vaqti:** 09:00 - 20:00 (Hamma kunlar)"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "📷 Bizning ishlarimiz":
        # 1-Rasm
        try:
            with open("ish1.jpg", "rb") as rasm1:
                bot.send_photo(message.chat.id, rasm1, caption="✨ Soch turmaklash va bo'yash")
        except FileNotFoundError:
            pass

        # 2-Rasm
        try:
            with open("ish2.jpg", "rb") as rasm2:
                bot.send_photo(message.chat.id, rasm2, caption="✨ Makiyaj va vizaj")
        except FileNotFoundError:
            pass

        # 3-Rasm
        try:
            with open("ish3.jpg", "rb") as rasm3:
                bot.send_photo(message.chat.id, rasm3, caption="✨ Manikür xizmati")
        except FileNotFoundError:
            pass

        # 4-Rasm
        try:
            with open("ish4.jpg", "rb") as rasm4:
                bot.send_photo(message.chat.id, rasm4, caption="✨ Kiprik o'stirish")
        except FileNotFoundError:
            pass

        # 5-Rasm
        try:
            with open("ish5.jpg", "rb") as rasm5:
                bot.send_photo(
                    message.chat.id, 
                    rasm5, 
                    caption="✨ Labga rang berish (Biotexnika / Permanent makiyaj)\n\n"
                            "✨ Lablaringizga tabiiy, jozibador va yorqin rang baxsh eting!\n"
                            "💋 Mukammal kontur, xavfsiz pigmentlar va uzoq muddatli go'zallik kafolati.\n"
                            "✨ Go'zalligingiz o'z qo'lingizda!"
                )
        except FileNotFoundError:
            pass


# --- ISHGA TUSHIRISH ---
if __name__ == '__main__':
    print("Bot muvaffaqiyatli ishga tushdi...")
    # 1. Avval Flask serverini fonga tushiramiz
    keep_alive()

    # 2. Keyin botni yurgizamiz
    bot.remove_webhook()
    bot.polling(none_stop=True)
