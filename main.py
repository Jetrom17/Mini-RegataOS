import telebot
from telebot import types

# Token do seu bot fornecido pelo BotFather
TOKEN = 'SEU_TOKEN'

bot = telebot.TeleBot(TOKEN)

support_ids = [123, 321, 000]  # Lista de IDs dos suportes.
tickets = {}

def generate_support_markup(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Eu assumo este caso", callback_data=f"assume_{chat_id}")) # Botão que aparece para todos os suportes.
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Olá! Para abrir um ticket, use /ticket") # Para o cliente

# Função do Ticket.
@bot.message_handler(commands=['ticket'])
def new_ticket(message):
    chat_id = message.chat.id
    if chat_id not in tickets:
        tickets[chat_id] = {'client_id': message.from_user.id, 'support': None, 'messages': []}
        for support_id in support_ids:
            bot.send_message(support_id, f"Novo ticket de {message.from_user.username}:\n{message.text}",
                             reply_markup=generate_support_markup(chat_id))
        bot.reply_to(message, "Ticket criado! Aguarde um atendente responder o seu caso em privado.")
    else:
        bot.reply_to(message, "Você já tem um ticket aberto. Aguarde uma resposta em privado.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('assume'))
def handle_assume_case(call):
    chat_id = int(call.data.split('_')[1])
    support_id = call.from_user.id
    support_username = call.from_user.username  # Obtém o nome de usuário do suporte que clicou no botão "Eu assumo este caso".

    if chat_id in tickets and tickets[chat_id]['support'] is None:
        tickets[chat_id]['support'] = support_id

        for id in support_ids:
            if id != support_id:
                bot.send_message(id, f"Suporte @{support_username} assumiu o caso!")

        bot.send_message(chat_id, "Um suporte assumiu o seu caso!")
        bot.answer_callback_query(call.id, "Você assumiu este caso.")
    else:
        if tickets[chat_id]['support'] is not None:
            support_name = f"@{support_username}"  # Usa o nome de usuário como nome.
            bot.answer_callback_query(call.id, f"Este caso já foi assumido por {support_name}.")
        else:
            bot.answer_callback_query(call.id, "Este caso já foi assumido ou não está mais disponível.")

# Chat privado, entre o "client and support".
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id in tickets and user_id == tickets[chat_id]['client_id']:
        if 'support' in tickets[chat_id] and tickets[chat_id]['support'] is not None:
            support = tickets[chat_id]['support']
            bot.send_message(support, f"Cliente: {message.text}", reply_markup=generate_close_markup(chat_id))
            tickets[chat_id]['messages'].append((message.text, user_id))
            bot.send_message(chat_id, "Mensagem enviada para o suporte!")
        else:
            bot.send_message(chat_id, "Aguarde um suporte assumir o seu caso.")
    elif 'support' in tickets.get(chat_id, {}) and tickets[chat_id]['support'] is not None and chat_id in tickets and user_id == tickets[chat_id]['support']:
        client_id = tickets[chat_id]['client_id']
        bot.send_message(client_id, f"Suporte: {message.text}", reply_markup=generate_close_markup(chat_id))
        tickets[chat_id]['messages'].append((message.text, user_id))
        bot.send_message(client_id, "Mensagem enviada para o cliente!")
    else:
        bot.send_message(chat_id, "Por favor, use um comando válido ou aguarde por uma interação do suporte.")

# Encerra o caso.
def generate_close_markup(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Encerrar caso", callback_data=f"close_{chat_id}"))
    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('close'))
def handle_close_case(call):
    chat_id = int(call.data.split('_')[1])
    support_id = call.from_user.id
    if chat_id in tickets and tickets[chat_id]['support'] == support_id:
        del tickets[chat_id]
        bot.send_message(support_id, "O caso foi encerrado.")
        bot.answer_callback_query(call.id, "Caso encerrado.")
    else:
        bot.answer_callback_query(call.id, "Você não tem permissão para encerrar este caso.")

# Bot em loop.
bot.polling()
