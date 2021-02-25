#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Dev: FSystem88

import telebot, requests as r, time
from telebot import types

bot = telebot.TeleBot("")

NAME = "ИМЯ МАГАЗИНА"
url = "https://example.com/feedback_tg_bot/php/"

######################################################### / C O M M A N D S ##############################################################


@bot.message_handler(commands=['start'])
def start(message):
	try:
		if str(message.chat.id) in owners():
			Home(message)
		else:
			for own in owners():
				bot.send_message(own, "<b>New user:</b> <a href='tg://user?id={}'>{}</a>\n<b>Username:</b> @{}\n<b>iD:</b> <code>{}</code>\n".format(message.chat.id, message.chat.first_name, message.chat.username, message.chat.id), parse_mode="HTML")
			bot.send_message(message.chat.id, "Привет! Это бот-помощник {}. \nВ чем твой вопрос?".format(NAME))
	except:
		pass


@bot.message_handler(commands=['getadmin'])
def getadmin(message):
	if str(message.chat.id) in owners():
		bot.send_message(message.chat.id, "<b>Вы уже администратор!</b>", parse_mode="html")
	else:
		res = r.post(url+"all.php", data={"status":"god"}).json()
		idgod = res[0]['tgid']
		key = types.InlineKeyboardMarkup()
		but1 = types.InlineKeyboardButton(text="Принять", callback_data="addadmin{}".format(message.chat.id))
		but2 = types.InlineKeyboardButton(text="Отклонить", callback_data="failadmin{}".format(message.chat.id))
		key.add(but1, but2)
		bot.send_message(idgod, "<a href='tg://user?id={}'>{}</a> (@{}) хочет быть админом!".format(message.chat.id, message.chat.first_name, message.chat.username), parse_mode="html", reply_markup=key)
		bot.send_message(message.chat.id, "Заявка отправлена, одижайте решение главного администратора.")


@bot.message_handler(commands=['restart'])
def restart(message):
	if str(message.chat.id) in owners():
		r.post(url+"adm.php", data={"data":"update", "tgid":message.chat.id, "name":message.chat.first_name, "username":message.chat.username})
		bot.send_message(message.chat.id, "<b>Поздравляю, Вы администратор {}!</b>".format(NAME), parse_mode="html")
		Home(message)


######################################################### D E F ' S ######################################################################


def owners():
	owns = []
	res = r.get(url+"all.php").json()
	for i in res:
		owns.append(i['tgid'])
	return owns


def Home(message):
	res = r.post(url+"all.php", data={"status":"god"}).json()
	idgod = res[0]['tgid']
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	if str(message.chat.id) == idgod:
		keyboard.row('Админы')	
	bot.send_message(message.chat.id, "<b>Привет мой любимый админ ♥</b>", reply_markup=keyboard, parse_mode="html")


def admins(message):
	res = r.post(url+"all.php", data={"status":"god"}).json()
	idgod = res[0]['tgid']
	if str(message.chat.id) == idgod:
		keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.row('Добавить')
		keyboard.row('Домой')
		bot.send_message(message.chat.id, "Все админы:", reply_markup=keyboard)
		bot.register_next_step_handler(message, admins1)		
		res = r.get(url+"all.php").json()
		for own in res:
			key = types.InlineKeyboardMarkup()
			but1 = types.InlineKeyboardButton(text="Удалить админа", callback_data="deladmin{}".format(own['tgid']))
			key.add(but1)
			bot.send_message(message.chat.id, "Имя: <a href='tg://user?id={}'>{}</a>\n@{}".format(own['tgid'], own['name'], own['username']), parse_mode="html", reply_markup=key)

	else:
		bot.send_message(message.chat.id, "Эта функция доступна тольк главному администратору")


def admins1(message):
	if message.text == "Добавить":
		bot.send_message(message.chat.id, "Чтобы добавить нового администратора надо чтобы кандидат отправил боту команду:\n\n/getadmin\n\nПринять заявку может только самый главный админ.")
	elif message.text == "Домой":
		Home(message)


def reply(message):
	global tgid
	bot.send_message(tgid, '''<b>Ответ получен:</b>\n\n{}\n\n<i>С уважением админ {}</i>'''.format(
		message.text, NAME), parse_mode="html")
	bot.send_message(message.chat.id, "Сообщение отправлено!")


################################################################ T E X T #################################################################


@bot.message_handler(func=lambda message: True, content_types=['text'])
def Main(message):
	TEXT = message.text
	if TEXT == "Домой":
		Home(message)
	elif TEXT == "Админы":
		admins(message)
	else:
		for own in owners():
			key = types.InlineKeyboardMarkup()
			but1 = types.InlineKeyboardButton(text="Ответить", callback_data="{}".format(message.chat.id))
			but2 = types.InlineKeyboardButton(text="Удалить", callback_data="delete")
			key.add(but1, but2)
			bot.send_message(own, '''<b>Получен новый вопрос!</b>\n<b>От:</b> <a href='tg://user?id={}'>{}</a> (@{})\n<b>Текст:</b>\n<i>{}</i>'''.format(message.chat.id, message.chat.first_name, message.chat.username, message.text), parse_mode="html", reply_markup=key)
		bot.send_message(message.chat.id, "Сообщение отправлено!")


###################################################### C A L L B A C K ###################################################################


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
	if call.data == "delete":
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<i>Удалено</i>", parse_mode="html")
	elif call.data[:8] == "deladmin":
		key = types.InlineKeyboardMarkup()
		but1 = types.InlineKeyboardButton(text="Да", callback_data="deldeladm{}".format(call.data[8:]))
		but2 = types.InlineKeyboardButton(text="Нет", callback_data="nodeladm")
		key.add(but1, but2)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы уверены, что хотите удалить данного администратора?", parse_mode="html", reply_markup=key)
	elif call.data[:8] == "nodeladm":
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<i>Удаление отменено</i>", parse_mode="html")
	elif call.data[:9] == "deldeladm":
		_tgid = call.data[9:]
		r.post(url+"adm.php", data={"data":"delete", "tgid":_tgid})
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Администратор удалён</b>", parse_mode="html")
		


	elif call.data[:8] == "addadmin":
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<i>Заявка принята</i>", parse_mode="html")
		_tgid = call.data[8:]
		r.post(url+"adm.php", data={"data":"addadmin", "tgid":_tgid})
		bot.send_message(_tgid, "<b>Ваша заявка на администрирование принята!\n\nАктивируйте администрирование:</b>\n/restart", parse_mode="html")
	elif call.data[:9] == "failadmin":
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<i>Заявка отклонена</i>", parse_mode="html")
		_tgid = call.data[9:]
		bot.send_message(_tgid, "<b>Ваша заявка на администрирование отклонена!</b>", parse_mode="html")
	else:
		global tgid
		tgid = int(call.data)
		bot.send_message(call.message.chat.id, "Введите ответ:")
		bot.register_next_step_handler(call.message, reply)


######################################################## L A U N C H #####################################################################

while True:
	try:
		bot.polling()
	except Exception as E:
		time.sleep(1)
