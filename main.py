import telebot
from telebot import types

# Chave do seu bot fornecida pelo BotFather do Telegram
TOKEN = 'SEU_TOKEN'

# Inicialização do bot
bot = telebot.TeleBot(TOKEN)

# Dicionários para armazenar todas as perguntas e respostas em português e inglês
faq_pt = {
    "O que é regata?": "Uma regata é uma prova náutica de velocidade entre diversas embarcações à vela, a motor ou a remo, realizando um percurso marcado por bóias que são posicionadas no mar pela organização do evento.",
    "O que é o Regata OS?": "O Regata OS é um Sistema Operacional baseado em Linux (mais precisamente em openSUSE) desenvolvido para todos os tipos de usuários, porém, com foco especial em gamers e criadores de conteúdo.",
    "O Regata OS é apenas uma versão fácil de usar do openSUSE?": "Não. O Regata OS tem uma proposta diferente do openSUSE e de outras distribuições Linux baseadas no openSUSE. Embora existam inúmeras diferenças sutis entre o Regata OS e o openSUSE, os exemplos mais óbvios incluem nossos próprios aplicativos, além, é claro, do público-alvo – usuários do Windows.",
    "O Regata OS é de código aberto?": "O Regata OS é de código aberto, disponível no GitHub sob a licença do MIT, além de ser gratuito. Acreditamos que tudo é possível com tecnologia gratuita e de código aberto.",
    "Como faço para instalar o Regata OS?": "Confira nosso guia de instalação do Regata OS. Só não se esqueça de fazer backup de fotos, vídeos, arquivos de texto, o que você achar importante, e levar o conteúdo para um disco rígido externo, pendrive ou serviço de armazenamento em nuvem (como Google Drive).",
    "Qual ISO devo baixar?": "Se você possui uma placa de vídeo NVIDIA em seu desktop ou laptop, baixe o Regata OS ISO que já vem com o driver NVIDIA por padrão, caso contrário, baixe o ISO sem o driver NVIDIA. O Regata OS já possui a versão mais recente do driver de vídeo para GPUs Intel e AMD.",
    "Preciso criar uma partição swap?": "Não. O Regata OS cria e gerencia a partição swap automaticamente para você.",
    "Não encontrei um aplicativo na loja, e agora?": "Use este formulário para recomendar novos aplicativos. Sua implementação será estudada pela equipe de desenvolvedores.",
    "Como posso apoiar o projeto?": "Você pode ajudar o projeto Regata OS promovendo nosso sistema operacional para seus amigos e familiares que desejam experimentar um mundo muito além do Windows. Além disso, também é possível ajudar com feedback."
}

faq_en = {
    "What is regatta?": "A regatta is a nautical speed race between various boats, such as sailboats, motorboats, or rowboats, following a course marked by buoys placed in the sea by the event's organization.",
    "What is Regata OS?": "Regata OS is a Linux-based Operating System (more precisely, on openSUSE) developed for all types of users, but with a special focus on gamers and content creators.",
    "Is Regata OS just an easy-to-use version of openSUSE?": "No. Regata OS has a different proposal from openSUSE and other Linux distributions based on openSUSE. Although there are numerous subtle differences between Regata OS and openSUSE, the most obvious examples include our own applications, as well as the target audience – Windows users.",
    "Is Regata OS open source?": "Regata OS is open source, available on GitHub under the MIT license, and it's free. We believe everything is possible with free and open-source technology.",
    "How do I install Regata OS?": "Check out our Regata OS installation guide. Just don't forget to back up photos, videos, text files, or anything else you find important and transfer the content to an external hard drive, USB flash drive, or cloud storage service (such as Google Drive).",
    "Which ISO should I download?": "If you have an NVIDIA graphics card in your desktop or laptop, download the Regata OS ISO that already comes with the NVIDIA driver by default; otherwise, download the ISO without the NVIDIA driver. Regata OS already has the latest version of the video driver for Intel and AMD GPUs.",
    "Do I need to create a swap partition?": "No. Regata OS creates and manages the swap partition automatically for you.",
    "I didn't find an app in the store, what should I do?": "Use this form to recommend new apps. Your implementation will be studied by the development team.",
    "How can I support the project?": "You can help the Regata OS project by promoting our operating system to friends and family who want to experience a world beyond Windows. Additionally, you can also help by providing feedback."
}

# Dicionário para armazenar o estado atual de cada usuário
user_state = {}

# Lidar com o comando /faq
@bot.message_handler(commands=['faq'])
def send_faq(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_pt = types.InlineKeyboardButton('Português', callback_data='pt')
    item_en = types.InlineKeyboardButton('English', callback_data='en')
    markup.add(item_pt, item_en)

    bot.send_message(message.chat.id, "Escolha o idioma / Choose the language:", reply_markup=markup)

# Lidar com as respostas do idioma
@bot.callback_query_handler(func=lambda call: call.data in ['pt', 'en'])
def handle_language(call):
    language = call.data

    if language == 'pt':
        send_questions(call.message, faq_pt)
    elif language == 'en':
        send_questions(call.message, faq_en)

# Função para enviar as perguntas
def send_questions(message, faq):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key in faq.keys():
        item = types.InlineKeyboardButton(key, callback_data=key)
        markup.add(item)
    bot.send_message(message.chat.id, "Escolha uma pergunta / Choose a question:", reply_markup=markup)
    user_state[message.chat.id] = faq

# Lidar com as perguntas escolhidas
@bot.callback_query_handler(func=lambda call: call.data in faq_pt or call.data in faq_en)
def handle_question(call):
    question = call.data
    faq = user_state.get(call.message.chat.id)
    if faq and question in faq:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=faq[question])
        send_back_button(call.message)

# Enviar botão "Voltar"
def send_back_button(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton('Voltar / Back', callback_data='back')
    markup.add(back_button)
    bot.send_message(message.chat.id, "Pressione 'Voltar' para retornar às perguntas / Press 'Back' to return to the questions:", reply_markup=markup)

# Lidar com o botão "Voltar"
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def handle_back(call):
    faq = user_state.get(call.message.chat.id)
    if faq:
        send_questions(call.message, faq)

# Iniciar o bot
bot.polling()
