import telebot

from openai import OpenAI

TELEGRAM_BOT_TOKEN = ""
OPENAI_API_KEY = ""
client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
ALLOWED_USER_IDS = []

def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="o1-preview",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return e

@bot.message_handler(commands=["start"])
def send_welcome(message):
    if message.from_user.id in ALLOWED_USER_IDS:
        bot.reply_to(message, "Все сообщения будут отправляться o1-preview")
    else:
        bot.reply_to(message, "у тебя нет доступа к боту")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id in ALLOWED_USER_IDS:
        user_input = message.text
        bot.send_chat_action(message.chat.id, "typing")
        response = ask_openai(user_input)
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "у тебя нет доступа к боту")

bot.polling()
