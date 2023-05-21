from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.handler_backends import State, StatesGroup
import os

API_TOKEN = os.getenv('API_TOKEN')
BACK_IP = os.getenv('BACK_IP')


class BotStates(StatesGroup):
    intro = State()
    search = State()


def rating_markup(doi):
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    markup.add(InlineKeyboardButton("😡", callback_data=f"like {doi} 1"),
               InlineKeyboardButton("😟", callback_data=f"like {doi} 2"),
               InlineKeyboardButton("😐", callback_data=f"like {doi} 3"),
               InlineKeyboardButton("😊", callback_data=f"like {doi} 4"),
               InlineKeyboardButton("😍", callback_data=f"like {doi} 5"))
    return markup


welcome_message = """\
    Привет! Я бот, который поможет тебе найти интересные статьи по твоей теме. Особенно хорошо\
    я работаю с темами по программированию. 
    
    У меня есть несколько команд:
    /start - начать работу со мной
    /recommend - порекомендовать статьи
    /search - поиск статей
    
    Ты можешь оценивать результаты поиска и рекомендаций, чтобы я мог лучше подбирать статьи под твои интересы.
    
    Приятного пользования!
"""
