import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = "8110384134:AAGr1g6NoU39ZXCrmnFk0l6K4_x-cEWDbxM"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط تيك توك وسأقوم بتحميله لك 📥")

@bot.message_handler(func=lambda message: True)
def download_tiktok_video(message):
    url = message.text.strip()
    if "tiktok.com" not in url:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط تيك توك صحيح!")
        return

    msg = bot.reply_to(message, "⏳ جاري تحميل الفيديو...")
    out_filename = f"video_{message.chat.id}.mp4"
    ydl_opts = {'format': 'b/best', 'outtmpl': out_filename, 'quiet': True}

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(out_filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption="✅ تم التحميل بنجاح!")

        bot.delete_message(message.chat.id, msg.message_id)
        if os.path.exists(out_filename):
            os.remove(out_filename)
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: {str(e)}", message.chat.id, msg.message_id)
        if os.path.exists(out_filename):
            os.remove(out_filename)

bot.infinity_polling()