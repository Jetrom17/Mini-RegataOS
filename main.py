import telebot
from telebot import types
import time

# Chave do seu bot fornecida pelo BotFather do Telegram
TOKEN = 'YOUR-TOKEN!'

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

faq = {
    "What is regatta?": "A regatta is a nautical speed race between various boats, such as sailboats, motorboats, or rowboats, covering a course set by the event's organizers.",
    "What is Regata OS?": "Regata OS is a Linux-based Operating System developed for all types of users, with a special focus on gamers and content creators. It's built on openSUSE.",
    "Is Regata OS just an easy-to-use version of openSUSE?": "No. Regata OS has a different proposal from openSUSE and other Linux distributions based on it. It features its own applications and targets Windows users.",
    "Is Regata OS open source?": "Yes, Regata OS is open source and available on GitHub under the MIT license. It's free for all users.",
    "How do I install Regata OS?": "Refer to our installation guide for Regata OS. Don't forget to back up your important files like photos, videos, and text documents.",
    "Which ISO should I download?": "Download the Regata OS ISO according to your graphics card. The version with NVIDIA driver is for NVIDIA GPUs; the other version includes the latest Intel and AMD video drivers.",
    "Do I need to create a swap partition?": "No, Regata OS handles the swap partition automatically for you.",
    "I didn't find an app in the store, what should I do?": "Use our app recommendation form. Our development team will consider your suggestions.",
    "How can I support the project?": "You can support the Regata OS project by spreading the word to friends and family who are interested in exploring an alternative to Windows. Additionally, providing feedback is a valuable contribution."
    # Add more FAQ pairs here
}

# Dictionary to store user's current state
user_state = {}

# Handle the /faq command
@bot.message_handler(commands=['faq'])
def send_faq(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key in faq.keys():
        item = types.InlineKeyboardButton(key, callback_data=key)
        markup.add(item)
    bot.send_message(message.chat.id, "Choose a question:", reply_markup=markup)

# Handle the chosen question
@bot.callback_query_handler(func=lambda call: call.data in faq)
def handle_question(call):
    question = call.data
    answer = faq.get(question)

    # Edit the message with the complete answer
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer)

    # Schedule deletion of the message after 30 seconds
    time.sleep(30)
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Start the bot
bot.polling()
