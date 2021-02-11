#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telebot
from telebot import types

bot = telebot.TeleBot("")
owners = []
NAME = ""

@bot.message_handler(commands=['start'])
def handle_game(message):
	try:
		if message.chat.id in owners:
			bot.send_message(message.chat.id, "Hello my favorite admin ♥")
		else:
			bot.send_message(message.chat.id, "Hello, this is the manager of {}. \nWhat is your question?".format(NAME))
	except:
		pass

@bot.message_handler(func=lambda message: True, content_types=['text'])
def Main(message):
	for own in owners:
		key = types.InlineKeyboardMarkup()
		but = types.InlineKeyboardButton(text="Reply", callback_data="{}".format(message.chat.id))
		key.add(but)
		bot.send_message(own, '''<b>Received a new question:</b>\nОт: <a href='tg://user?id={}'>{}</a> (@{})\nText:\n<i>{}</i>'''.format(message.chat.id, message.chat.first_name, message.chat.username, message.text), parse_mode="html", reply_markup=key)
	bot.send_message(message.chat.id, "Message sent!")

@bot.callback_query_handler(func=lambda call: True)
def inline(call):
	global tgid
	tgid = int(call.data)
	bot.send_message(call.message.chat.id, "Enter answer:")
	bot.register_next_step_handler(call.message, reply)

def reply(message):
	global tgid
	bot.send_message(tgid, '''<b>Answer received:</b>\n{}\n<i>Faithfully yours admin of {}</i>'''.format(message.text, NAME), parse_mode="html")
	bot.send_message(message.chat.id, "Message sent!")

while True:
	try:
		bot.polling()
	except Exception as E:
		time.sleep(1)
