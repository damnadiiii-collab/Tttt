import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8526692802:AAGj0Z8f2Rn1Q9SZqb7Hvh9Nnoi5XnmjeiU"
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Welcome! To aviator prediction bot:")
    user_data[message.chat.id] = {"step": "app"}

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    chat_id = message.chat.id
    step = user_data.get(chat_id, {}).get("step", "")

    if step == "app":
        user_data[chat_id]["app"] = message.text
        user_data[chat_id]["step"] = "gameid"
        bot.send_message(chat_id, "✅ App saved! Now enter Game ID:")

    elif step == "gameid":
        user_data[chat_id]["gameid"] = message.text
        user_data[chat_id]["step"] = "lastpoint"
        bot.send_message(chat_id, "✅ Game ID saved! Now enter Last Flew Away Point:")

    elif step == "lastpoint":
        try:
            last_point = float(message.text)
        except ValueError:
            bot.send_message(chat_id, "❌ Please enter a valid number!")
            return

        predicted = round(last_point * 0.8 + 1.0, 2)  # Example prediction logic
        user_data[chat_id]["lastpoint"] = last_point

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Next", callback_data="next"))

        bot.send_message(chat_id, f"🎯 Predicted Next Crash Point: {predicted}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "next")
def handle_next(call):
    user_data[call.message.chat.id]["step"] = "lastpoint"
    bot.send_message(call.message.chat.id, "🔄 Enter Last Flew Away Point:")

print("🤖 AviatorSignalBot is running on Render!")
bot.polling()
