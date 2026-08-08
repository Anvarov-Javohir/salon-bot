import os
from flask import Flask
from threading import Thread

# Bot tokeningiz
TOKEN = "8971695245:AAEKEq3VEuDiY_SHGyBijmEcSll_r-VXNxY"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_buyrugi(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("💅 Xizmatlar va Narxlar")
    btn2 = telebot.types.KeyboardButton("📍 Manzil va Aloqa")
    btn3 = telebot.types.KeyboardButton("📸 Bizning ishlarimiz")
    
    markup.add(btn1)
    markup.add(btn2, btn3)

    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "\"Dilya Ledy\" go'zallik saloni botiga xush kelibsiz.\n"
        "Xizmatlarni ko'rish uchun pastdagi tugmalardan birini bosing!",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def tugmalar_uchun(message):
    if message.text == "💅 Xizmatlar va Narxlar":
        xizmatlar = (
            "✨ **Bizning xizmatlar va narxlarimiz:**\n\n"
            "• Kiprik ekish — 200 000 so'm\n"
            "• Qosh va kiprik laminatsiya — 250 000 so'm\n"
            "• Qosh va lab bo'yash (biotexnika) — 250 000 so'm"
        )
        bot.send_message(message.chat.id, xizmatlar, parse_mode="Markdown")

    elif message.text == "📍 Manzil va Aloqa":
        manzil = (
            "📍 **Bizning manzil:** Toshkent shahri, Yashnobod tumani.\n"
            "📞 **Aloqa uchun telefon:** +998 (99) 493-63-54\n"
            "🕒 **Ish vaqti:** 08:00 dan 21:00 gacha (Har kuni)"
        )
        bot.send_message(message.chat.id, manzil, parse_mode="Markdown")

    elif message.text == "📸 Bizning ishlarimiz":
        bot.send_message(message.chat.id, "📸 Rasmlar yuklanmoqda, bir soniya...")
        
        # 1-Rasm: Kiprik ekish
        try:
            with open("ish1.jpg", "rb") as rasm1:
                bot.send_photo(
                    message.chat.id, 
                    rasm1, 
                    caption="""✨ Kiprik ekish

👁️ Koʻzlaringizga yanada maftunkor va chuqur qarash bagʻishlang! Yuqori sifatli va xavfsiz materiallar bilan mukammal hajm.

👑 Goʻzalligingizni professionallarga ishoning!"""
                )
        except FileNotFoundError:
            pass

        # 2-Rasm: Kiprik laminatsiyasi
        try:
            with open("ish2.jpg", "rb") as rasm2:
                bot.send_photo(
                    message.chat.id, 
                    rasm2, 
                    caption="""🌿 Kiprik laminatsiyasi (Kiprik laminatsya)

✨ Tabiiy kipriklaringizni qayirish, qoraytirish va vitaminlar bilan oziqlantirish xizmati. Tabiiylikni xush koʻruvchilar uchun eng mukammal tanlov!

💫 Kipriklaringiz har kuni xuddi tush surtilgandek jozibali turadi."""
                )
        except FileNotFoundError:
            pass

        # 3-Rasm: Qosh laminatsiyasi
        try:
            with open("ish3.jpg", "rb") as rasm3:
                bot.send_photo(
                    message.chat.id, 
                    rasm3, 
                    caption="""📐 Qosh laminatsiyasi

👁️ Qoshlarni tartibli, silliq va ideal shaklga keltirish. Qosh tolalari qalinlashadi va yuz tuzilishingizga mos mukammal koʻrinish oladi.

✨ Chiroyli qoshlar – yuz koʻrkidir!"""
                )
        except FileNotFoundError:
            pass

        # 4-Rasm: Qoshga rang berish
        try:
            with open("ish4.jpg", "rb") as rasm4:
                bot.send_photo(
                    message.chat.id, 
                    rasm4, 
                    caption="""🌟 Qoshga rang berish – (Biotexnika xizmat) 

👑 Ideal shakldagi qoshlar! Har bir mijoz uchun individual yondashuv va professional natija.

📅 Oʻzingizga qulay vaqtni band qilishga shoshiling!"""
                )
        except FileNotFoundError:
            pass

        # 5-Rasm: Labga rang berish
        try:
            with open("ish5.jpg", "rb") as rasm5:
                bot.send_photo(
                    message.chat.id, 
                    rasm5, 
                    caption="""👄 Labga rang berish (Biotexnika / Permanent makiyaj)

✨ Lablaringizga tabiiy, jozibador va yorqin rang baxsh eting! Har kuni pomada surtish tashvishidan butunlay qutuling. 

💋 Mukammal kontur, xavfsiz pigmentlar va uzoq muddatli goʻzallik kafolati. Ogʻriqsiz va professional yondashuv!

✨ Goʻzalligingiz oʻz qoʻlingizda!"""
                )
        except FileNotFoundError:
            pass

# Botni yurgizish
print("Bot muvaffaqiyatli ishga tushdi...")
bot.polling(none_stop=True)

app = Flask('')

@app.route('/')
def home():
    return "Bot serveri faol!"

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()
