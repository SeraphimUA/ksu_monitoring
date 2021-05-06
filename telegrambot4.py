import json
from os import path
import telebot
from monitoring.check_utils import check_domain

bot = telebot.TeleBot('TOKEN_ID')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello, I got /start')

@bot.message_handler(commands=['greeting'])
def send_greeting(message):
    bot.send_message(message.chat.id, 'Hello, how are you?')

@bot.message_handler(commands=['check'])
def check(message):
    check_answer = message.text.lower().split()[1]
    if check_domain(check_answer):
        domain_file = f'results/{check_answer}.json'
        if path.exists(domain_file):
            with open(domain_file, 'r') as f:
                domain_info = json.load(f)
                domain_name = domain_info['domain']
                domain_time = domain_info['timestamp']
                domain_ping = domain_info['results']['ping']['status']
                domain_http = domain_info['results']['http']['status']
                bot.send_message(message.chat.id, f'Domain: {domain_name}\n' + f'Last check time: {domain_time}\n' + f'Ping: {domain_ping}\n' + f'HTTP: {domain_http}')
        else:
            bot.send_message(message.chat.id, f'Failed to find information about the domain {check_answer}')
    else:
        bot.send_message(message.chat.id, f'Incorrect message sent')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, 'Hello, Creator')
    elif message.text.lower() == 'bye':
        bot.send_message(message.chat.id, 'Goodbye, Creator')
    else:
        bot.reply_to(message, message.text)

bot.polling()
