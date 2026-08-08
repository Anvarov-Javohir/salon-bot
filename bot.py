import os
import time
from flask import Flask
from threading import Thread
import telebot

TOKEN = "8971695245:AAEKEq3VEuDiY_SHGyBijmEcSll_r-VXNxY"
ADMIN_ID = 8187441767  # Admin ID-si

bot = telebot.TeleBot(TOKEN)

# --- Render 24/7 ishlashi uchun Flask Server ---
app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!", 200

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()


# --- LUG'ATLAR (Foydalanuvchi holatlarini saqlash uchun) ---
user_steps = {}
user_data = {}


# 1. ASOSIY MENYU TUGMALARI
def asosiy_menyu_yuborish(chat_id, matn):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("🚀 Xizmatlar va Narxlar")
    btn2 = telebot.types.KeyboardButton("📍 Manzil va Aloqa")
    btn3 = telebot.types.KeyboardButton("📷 Bizning ishlarimiz")
    btn4 = telebot.types.KeyboardButton("📅 Qabulga yozilish")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    bot.send_message(chat_id, matn, reply_markup=markup)


# 2. START BUYRUG'I
@bot.message_handler(commands=['start'])
def start_message(message):
    user_steps[message.chat.id] = None
    user_data[message.chat.id] = {}
    asosiy_menyu_yuborish(
        message.chat.id, 
        f"Assalomu alaykum, {message.from_user.first_name}! Salon botimizga xush kelibsiz!"
    )


# 3. KONTAKT (TELEFON RAQAM) QABUL QILISH BOSQICHI
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    chat_id = message.chat.id
    if user_steps.get(chat_id) == "WAITING_PHONE":
        phone_number = message.contact.phone_number
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
            
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        user_data[chat_id]['phone'] = phone_number
        user_data[chat_id]['first_name'] = message.from_user.first_name
        user_data[chat_id]['username'] = message.from_user.username

        user_steps[chat_id] = "WAITING_TIME"
        remove_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            chat_id, 
            "Qachon kelmoqchisiz? O'zingizga qulay vaqtni yozing\n\n*(Namuna: ertaga soat 12:00 da)*", 
            parse_mode="Markdown",
            reply_markup=remove_markup
        )


# 4. MATNLI XABARLARNI TUTISH
@bot.message_handler(func=lambda message: True)
def text_handler(message):
    chat_id = message.chat.id
    text = message.text

    # --- QABULGA YOZILISH: VAQTNI QABUL QILISH ---
    if user_steps.get(chat_id) == "WAITING_TIME":
        user_steps[chat_id] = None
        user_time = text
        
        phone = user_data.get(chat_id, {}).get('phone', "Kiritilmadi")
        first_name = user_data.get(chat_id, {}).get('first_name', "Mijoz")
        username = user_data.get(chat_id, {}).get('username', None)
        user_link = f"@{username}" if username else "Mavjud emas"

        asosiy_menyu_yuborish(
            chat_id, 
            "Muvaffaqiyatli o'tdingiz! Tez orada operatorimiz bog'lanadi."
        )

        # Adminga (Oyijoningizga) xabar yuborish
        admin_msg = (
            f"🔔 **Yangi qabulga yozilish!**\n\n"
            f"👤 **Mijoz:** {first_name}\n"
            f"📞 **Tel:** {phone}\n"
            f"💬 **Telegram:** {user_link}\n"
            f"⏰ **Kelish vaqti:** {user_time}"
        )
        try:
            bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
        except Exception as e:
            print("Adminga xabar yuborishda xatolik:", e)
        return

    # --- BIZNING ISHLARIMIZ ---
    if "Bizning ishlarimiz" in text:
        user_steps[chat_id] = None
        
        temp_msg = bot.send_message(chat_id, "⏳ Rasmlar yuklanmoqda.....")
        time.sleep(2)
        try:
            bot.delete_message(chat_id, temp_msg.message_id)
        except Exception as e:
            print("Xabarni o'chirishda xato:", e)
        
        ishlar = [
            ("ish1.jpg", "👑 Nigohingizga o'zgacha joziba va hajm beruvchi kiprik ulash."),
            ("ish2.jpg", "✨ Tabiiy kipriklaringizni qayirish va oziqlantirish."),
            ("ish3.jpg", "👁 Qoshlarni tartibli va ideal shaklga keltirish."),
            ("ish4.jpg", "🌟 Qosh shaklini tahrirlash va rang berish (Biotexnika)."),
            ("ish5.jpg", "👄 Lablarga tabiiy va jozibali rang berish (Permanent makiyaj).")
        ]
        
        for photo_name, caption in ishlar:
            try:
                with open(photo_name, "rb") as photo:
                    bot.send_photo(chat_id, photo, caption=caption)
            except Exception as e:
                print(f"{photo_name} yuklanishida xato:", e)

    # --- XIZMATLAR VA NARXLAR ---
    elif "Xizmatlar va Narxlar" in text:
        user_steps[chat_id] = None
        
        temp_msg = bot.send_message(chat_id, "⏳ Rasmlar yuklanmoqda.....")
        time.sleep(2)
        try:
            bot.delete_message(chat_id, temp_msg.message_id)
        except Exception as e:
            print("Xabarni o'chirishda xato:", e)
        
        xizmat_rasmlari = [
            "photo_2026-06-26_19-46-49.jpg",
            "Xizmat va narxlar.jpg"
        ]
        
        for xizmat_photo in xizmat_rasmlari:
            try:
                with open(xizmat_photo, "rb") as photo:
                    bot.send_photo(chat_id, photo)
            except Exception as e:
                print(f"{xizmat_photo} yuklanishida xato:", e)

    # --- MANZIL VA ALOQA ---
    elif "Manzil va Aloqa" in text:
        user_steps[chat_id] = None
        manzil_matn = (
            "📍 **Manzilimiz:** Toshkent sh., Yashnobod tumani, Do'stlik metro yonidagi yangi domlar\n\n"
            "📞 **Telefon:** +998 99 493 63 54\n"
            "📞 **Qo'shimcha tel:** +998 97 738 63 54"
        )
        bot.send_message(chat_id, manzil_matn, parse_mode="Markdown")

    # --- QABULGA YOZILISH ---
    elif "Qabulga yozilish" in text:
        user_steps[chat_id] = "WAITING_PHONE"
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_phone = telebot.types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
        markup.add(btn_phone)
        bot.send_message(
            chat_id, 
            "Qabulga yozilish uchun pastdagi tugmani bosib telefon raqamingizni qoldiring 👇", 
            reply_markup=markup
        )

    else:
        user_steps[chat_id] = None
        asosiy_menyu_yuborish(chat_id, "Iltimos, pastdagi bo'limlardan birini tanlang 👇")


# --- ISHGA TUSHIRISH ---
if __name__ == '__main__':
    print("Bot Render serverida muvaffaqiyatli ishga tushdi...")
    
    # Eski webhooklarni to'liq o'chirish
    try:
        bot.remove_webhook(drop_pending_updates=True)
    except Exception as e:
        print("Webhook o'chirishda xato:", e)

    # Server va botni yurgizish
    keep_alive()
    bot.polling(none_stop=True, interval=0)
