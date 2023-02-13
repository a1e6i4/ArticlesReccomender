import telebot
import requests
import json
import numpy as np

welcome_message = """\
    Привет! Я ищу статьи по программированию по вашему запросу. Просто напишите ключевые слова
    
    Так же по команде /recommend могу порекомендовать вам что почитать исходя из моих умных алгоритмов
"""


API_TOKEN = '6136534812:AAE8Iuxq_4NUpja-cCZ8BqGdaUoJ1KVXohU'
BACK_IP = 'http://45.130.42.85'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, )
    bot.reply_to(message, welcome_message)

    json_data = {
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'username': message.from_user.username,
        'id': message.from_user.id
    }

    requests.post(f"{BACK_IP}/api/user/sign_up/", json=json_data)


@bot.message_handler(commands=['like'])
def like(message):
    article_id = message.text.split()[1]
    result = requests.get(f"{BACK_IP}/api/article/like", params={'article': article_id}).text
    bot.reply_to(message, result)


@bot.message_handler(commands=['recomend'])
def recommend(message):
    bot.reply_to(message, """\
    Умные алгоритмы находятся в разработке
""")


@bot.message_handler(func=lambda message: True)
def search(message):
    q = message.text
    result = requests.get(f"{BACK_IP}/api/article/search", params={'q': q}).text
    bot.reply_to(message, result)
