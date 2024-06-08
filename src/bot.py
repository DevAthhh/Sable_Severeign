import telebot

from config import TOKEN

bot = telebot.TeleBot(TOKEN)

def send_message(msg):
    bot.send_message(-4217228648, msg)