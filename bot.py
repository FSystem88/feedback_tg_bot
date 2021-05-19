#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Dev: FSystem88

import telebot, requests as r, time, threading
from telebot import types
from threading import Thread
bot = telebot.TeleBot("")

NAME = " ИМЯ ВАШЕГО МАГАЗИНА/БРЭНДА/КАНАЛА "
url = "https://example.com/feedback_tg_bot/php/"
# ВМЕСТО example.com НА ПИШИТЕ ВАШ САЙТ ГДЕ ВЫ РАЗМЕСТИЛИ API (папку php из этого репозитория)
# либо просто напишите мне @FSystem88_bot и я за скромную плату смогу разместить API и БД у себя на web сервере 

######################################################### / C O M M A N D S ##############################################################


@bot.message_handler(commands=['start'])
def start(message):
	try:
		res = r.post(url+"adm.php", data={"data":"find","tgid": message.chat.id}).json()
		if res == []:
			r.post(url+"adm.php", data={
				"data":"adduser",
				"tgid": message.chat.id,
				"name": message.chat.first_name,
				"username": message.chat.username
			} )
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
		res = r.post(url+"adm.php", data={"data":"god"}).json()
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
	res = r.post(url+"adm.php", data={"data":"admins"}).json()
	for i in res:
		owns.append(i['tgid'])
	return owns


def Home(message):
	res = r.post(url+"adm.php", data={"data":"god"}).json()
	idgod = res[0]['tgid']
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	if str(message.chat.id) == idgod:
		keyboard.row('Cообщения','Админы')	
	else:
		keyboard.row('Cообщения')	
	bot.send_message(message.chat.id, "<b>Привет мой любимый админ ♥</b>", reply_markup=keyboard, parse_mode="html")


def admins(message):
	res = r.post(url+"adm.php", data={"data":"god"}).json()
	idgod = res[0]['tgid']
	if str(message.chat.id) == idgod:
		keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.row('Добавить админа')
		keyboard.row('Черный список','Добавить в ЧС')
		keyboard.row('Отправить всем сообщение')
		keyboard.row('Домой')
		bot.send_message(message.chat.id, "Все админы:", reply_markup=keyboard)
		res = r.post(url+"adm.php", data={"data":"admins"}).json()
		for own in res:
			if own['status'] == "god":
				bot.send_message(message.chat.id, "<b>БОГ</b>\nИмя: <a href='tg://user?id={}'>{}</a>\n@{}".format(own['tgid'], own['name'], own['username']), parse_mode="html")
			elif own['status'] == "admin":
				key = types.InlineKeyboardMarkup()
				but1 = types.InlineKeyboardButton(text="Удалить админа", callback_data="deladmin{}".format(own['tgid']))
				key.add(but1)
				bot.send_message(message.chat.id, "Имя: <a href='tg://user?id={}'>{}</a>\n@{}".format(own['tgid'], own['name'], own['username']), parse_mode="html", reply_markup=key)
		bot.register_next_step_handler(message, admins1)
	else:
		bot.send_message(message.chat.id, "Эта функция доступна только главному администратору!")


def admins1(message):
	if message.text == "Добавить админа":
		bot.send_message(message.chat.id, "Чтобы добавить нового администратора надо чтобы кандидат отправил боту команду:\n\n/getadmin\n\nПринять заявку может только самый главный админ.")
		bot.register_next_step_handler(message, admins1)
	elif message.text == "Черный список":
		res = r.post(url+"adm.php", data={"data":"allblock"}).json()
		if res == []:
			bot.send_message(message.chat.id, "Черный список пуст!")
		else:
			for user in res:
				key = types.InlineKeyboardMarkup()
				but = types.InlineKeyboardButton(text="Разблокировать", callback_data="delban{}".format(user['tgid']))
				key.add(but)
				bot.send_message(message.chat.id, "Имя: <a href='tg://user?id={}'>{}</a> (@{})\nID: <code>{}</code>".format(user['tgid'], user['name'], user['username'], user['tgid']), parse_mode="html", reply_markup=key)
		bot.register_next_step_handler(message, admins1)
	elif message.text == "Добавить в ЧС":
		keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.row('Отмена')
		bot.send_message(message.chat.id, "Введите id пользователя", reply_markup=keyboard)
		bot.register_next_step_handler(message, block)
	elif message.text == "Отправить всем сообщение":
		keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.row('Отмена')
		bot.send_message(message.chat.id, "Введите сообщение:", reply_markup=keyboard)
		bot.register_next_step_handler(message, sends)
	elif message.text == "Домой":
		Home(message)


def sends(message):
	if message.text == "Отмена":
		admins(message)
	else:
		res = r.post(url+"adm.php", data={"data":"user"}).json()
		for user in res:
			thread_list = []
			t = threading.Thread (target=sends1, args=(message, user['tgid'], message.text))
			thread_list.append(t)
			t.start()
		bot.send_message(message.chat.id, "Отправлено!")
		Home(message)


def sends1(message, tgid, text):
	try:
		bot.send_message(tgid, text)
	except:
		pass


def block(message):
	if message.text == "Отмена":
		admins(message)
	else:
		res = r.post(url+"adm.php", data={"data":"find","tgid":message.text}).json()
		if res == []:
			bot.send_message(message.chat.id, "Пользователь не найден")
			bot.register_next_step_handler(message, block)
		else:
			bot.send_message(message.chat.id, "‼️ ЗАБЛОКИРОВАН ‼️\n<a href='tg://user?id={}'>{}</a> (@{})\nID: <code>{}</code>".format(res[0]['tgid'], res[0]['name'], res[0]['username'], res[0]['tgid']), parse_mode="html")
			r.post(url+"adm.php", data={"data":"block", "tgid":res[0]['tgid']})
			admins(message)


def reply(message):
	global tgid
	global text
	if message.text == "Отмена":
		bot.send_message(message.chat.id, "<i>Отменено</i>", parse_mode="html")
		Home(message)
	else:
		bot.send_message(tgid, '''<b>Ответ получен:</b>\n\n{}\n\n<i>С уважением админ {}</i>'''.format(message.text, NAME), parse_mode="html")
		bot.send_message(message.chat.id, "Сообщение отправлено!")
		r.post(url+"mess.php", data={
			"data" : "reply",
			"answer" : message.text,
			"adminID" : message.chat.id,
			"adminName" : message.chat.first_name,
			"text" : text,
			"tgid" : tgid
		})
		Home(message)


def Messages(message):
	if str(message.chat.id) in owners():
		res = r.post(url+"mess.php", data={"data":"count"})
		cnt = res.text
		keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.row('Непрочитанные','Старые')
		keyboard.row('Домой')
		bot.send_message(message.chat.id, "<b>Количество непрочитанных сообщений: {}</b>".format(cnt), reply_markup=keyboard, parse_mode="html")
		bot.register_next_step_handler(message, Messages1)


def Messages1(message):
	if message.text == "Домой":
		Home(message)
	elif message.text == "Непрочитанные":
		res = r.post(url+"mess.php", data={"data":"unread"}).json()
		if res == []:
			bot.send_message(message.chat.id, "Пусто")
		else:
			for ask in res:
				key = types.InlineKeyboardMarkup()
				but1 = types.InlineKeyboardButton(text="Ответить", callback_data="reply{}".format(ask['tgid']))
				but2 = types.InlineKeyboardButton(text="Удалить", callback_data="delete{}".format(ask['tgid']))
				key.add(but1, but2)
				bot.send_message(message.chat.id, '''<b>От:</b> <a href='tg://user?id={}'>{}</a> (@{})\n<b>Текст:</b>\n<i>{}</i>'''.format(ask['tgid'], ask['name'], ask['username'], ask['text']), parse_mode="html", reply_markup=key)
		bot.register_next_step_handler(message, Messages1)
	elif message.text == "Старые":
		res = r.post(url+"mess.php", data={"data":"old"}).json()
		if res == []:
			bot.send_message(message.chat.id, "Пусто")
		else:
			for ask in res:
				key = types.InlineKeyboardMarkup()
				but1 = types.InlineKeyboardButton(text="Изменить ответ", callback_data="rreply{}".format(ask['tgid']))
				but2 = types.InlineKeyboardButton(text="Удалить", callback_data="ddelete{}".format(ask['tgid']))
				key.add(but1, but2)
				bot.send_message(message.chat.id, '''<b>От:</b> <a href='tg://user?id={}'>{}</a> (@{})\n<b>Текст:</b>\n<i>{}</i>\n<b>Админ:</b>  <a href='tg://user?id={}'>{}</a>\n<b>Ответ:</b>\n<i>{}</i>'''.format(ask['tgid'], ask['name'], ask['username'], ask['text'], ask['adminID'], ask['adminName'], ask['answer'] ), parse_mode="html", reply_markup=key)
		bot.register_next_step_handler(message, Messages1)
	

################################################################ T E X T #################################################################


@bot.message_handler(func=lambda message: True, content_types=['text'])
def Main(message):
	res = r.post(url+"adm.php", data={"data":"checkblock", "tgid":message.chat.id}).json()
	if res == []:
		TEXT = message.text
		if TEXT == "Домой":
			Home(message)
		elif TEXT == "Админы":
			admins(message)
		elif TEXT == "Cообщения":
			Messages(message)
		else:
			if str(message.chat.id) not in owners():
				r.post(url+"mess.php", data={"data":"new","tgid":message.chat.id,"name":message.chat.first_name,"username":message.chat.username,"text":message.text})
				for own in owners():
					key = types.InlineKeyboardMarkup()
					but1 = types.InlineKeyboardButton(text="Ответить", callback_data="reply{}".format(message.chat.id))
					but2 = types.InlineKeyboardButton(text="Удалить", callback_data="delete{}".format(message.chat.id))
					key.add(but1, but2)
					bot.send_message(own, '''<b>Получен новый вопрос!</b>\n<b>От:</b> <a href='tg://user?id={}'>{}</a> (@{})\n<b>Текст:</b>\n<i>{}</i>'''.format(message.chat.id, message.chat.first_name, message.chat.username, message.text), parse_mode="html", reply_markup=key)
				bot.send_message(message.chat.id, "Сообщение отправлено!")
	else:
		bot.send_message(message.chat.id, "Вы заблокированы ‼️")

###################################################### C A L L B A C K ###################################################################


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
	if call.data[:6] == "delete":
		_tgid = call.data[6:]
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<i>Удалено</i>", parse_mode="html")
		arr = call.message.text.split("\nТекст:\n", 1)[1]
		r.post(url+"mess.php", data={"data":"delete", "text":arr, 'tgid':_tgid})
	
	elif call.data[:7] == "ddelete":
		_tgid = call.data[7:]
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<i>Удалено</i>", parse_mode="html")
		arr = call.message.text.split("\nТекст:\n", 1)[1].split("\nАдмин:")[0]
		r.post(url+"mess.php", data={"data":"delete", "text":arr, 'tgid':_tgid})
		
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
	
	elif call.data[:5] == "reply":
		global tgid
		global text
		tgid = int(call.data[5:])
		text = call.message.text.split("\nТекст:\n", 1)[1]
		keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.row('Отмена')
		bot.send_message(call.message.chat.id, "Введите ответ:", reply_markup=keyboard)
		bot.register_next_step_handler(call.message, reply)

	elif call.data[:6] == "rreply":
		tgid = int(call.data[6:])
		text = call.message.text.split("\nТекст:\n", 1)[1].split("\nАдмин:")[0]
		keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.row('Отмена')
		bot.send_message(call.message.chat.id, "Введите ответ:", reply_markup=keyboard)
		bot.register_next_step_handler(call.message, reply)

	elif call.data[:6] == "delban":
		_tgid = call.data[6:]
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<i>Пользователь разблокирован</i>", parse_mode="html")
		r.post(url+"adm.php", data={"data":"delblock", "tgid":_tgid})


######################################################## L A U N C H #####################################################################

while True:
	try:
		bot.polling()
	except Exception as E:
		time.sleep(1)
