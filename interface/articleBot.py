import telebot
import requests
import json
from settings import *
from telebot.types import BotCommand
from telebot import custom_filters
from telebot.storage import StateMemoryStorage


bot = telebot.TeleBot(API_TOKEN, state_storage=StateMemoryStorage())

bot.set_my_commands([
    BotCommand('start', 'Нажмите чтобы начать'),
    BotCommand('recommend', 'Порекомендовать статьи'),
    BotCommand('search', 'Поиск статей'),
])


@bot.message_handler(commands=['help', 'start', 'recommend', 'search'])
def handle_commands(message):
    if message.text in ['/help', '/start']:
        bot.reply_to(message, welcome_message)

        json_data = {
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'username': message.from_user.username,
            'id': message.from_user.id
        }

        requests.post(f"{BACK_IP}/api/user/sign_up/", json=json_data)
    elif message.text == '/recommend':
        result = requests.get(f"{BACK_IP}/api/article/recommend", params={
            'user_id': message.from_user.id
        }).json()
        for r in result:
            bot.send_message(message.chat.id, f"{r['title']}\n-----------------\n{r['url']}",
                             reply_markup=rating_markup(r['doi']))
    elif message.text == '/search':
        bot.set_state(message.from_user.id, BotStates.search, message.chat.id)
        bot.reply_to(message, "Введите ключевые слова")


@bot.message_handler(func=lambda message: True, state=BotStates.search)
def search_command(message):
    q = message.text
    result = json.loads(requests.get(f"{BACK_IP}/api/article/search", params={'q': q}).text)[0:10]

    if len(result) == 1 and 'error' in result[0]:
        bot.reply_to(message, 'По вашему запросу ничего не найдено')
        return
    for r in result:
        bot.send_message(message.chat.id, f"{r['dc:title']}\n-----------------\n{r['prism:url']}",
                         reply_markup=rating_markup(r['prism:doi']))


@bot.callback_query_handler(func=lambda call: True)
def handle_rating(call):
    if call.data.startswith('like'):
        doi = call.data.split()[1]
        rating = int(call.data.split()[2])
        requests.get(f"{BACK_IP}/api/article/like", params={'doi': doi,
                                                            'user_id': call.from_user.id,
                                                            'rating': rating})
        bot.answer_callback_query(call.id, text=f"Вы поставили рейтинг {rating} статье {doi}")


bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling()
