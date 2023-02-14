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
    article_doi = message.text.split()[1]
    result = requests.get(f"{BACK_IP}/api/article/like", params={'doi': article_doi})

    if result.status_code == 200:
        bot.reply_to(message, 'Ok!')
    else:
        bot.reply_to(message, 'smth went wrong')


@bot.message_handler(commands=['recomend'])
def recommend(message):
    result = json.loads(requests.get(f"{BACK_IP}/api/article/recommend").text)
    msg = "\n\n".join([f"{r['title']}\n{r['doi']}\n{r['url']}" for r in result])

    bot.reply_to(message, msg)


@bot.message_handler(func=lambda message: True)
def search(message):
    q = message.text
    result = json.loads(requests.get(f"{BACK_IP}/api/article/search", params={'q': q}).text)[0:10]

    msg = "\n\n".join([f"{r['prism:title']}\n{r['prism:doi']}\n{r['prism:url']}" for r in result])
    bot.reply_to(message, msg)
