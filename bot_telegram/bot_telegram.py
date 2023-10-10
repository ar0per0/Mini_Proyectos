#### BOT TELEGRAM ####
# -pyTelegramBotAPI https://github.com/eternnoir/pyTelegramBotAPI

# iniciar automaticamente al iniciar equipo agregar comando, /etc/rc.local ---> su {usuario} -c "python ~/Mini_Proyectos/bot_telegram/bot_telegram.py &"

import telebot
from telebot import types
import os
from datetime import datetime
import secret_bot_telegram

TOKEN = secret_bot_telegram.TOKEN
USERS = secret_bot_telegram.USERS  # Comprovar id user @userinfobot
USER_ADMIN = secret_bot_telegram.USER_ADMIN
FILE_LOG = os.path.expanduser("~/Mini_Proyectos/bot_telegram/bot_telegram.log")
TOKEN_PRINTER3D = secret_bot_telegram.TOKEN_PRINTER3D

docker_lisen = False
docker_service = ""
bot = telebot.TeleBot(TOKEN)
commands_bot = { # descripcion de comandos "help"
            'fortune': 'Mensaje galleta de la suerte',
            'docker': '{servicio} Iniciar/Apagar',
            '3d' : 'Acciones impresora 3D',
            'system': 'Acciones sistema'
}

def check_user(m):
    if m.from_user.id in USERS:
        return True
    else:
        bot.send_message(USER_ADMIN, "🚨 Usuario no autorizado:🚨 \n id: " + str(m.from_user.id) + "\n usuario: " + m.from_user.username + " ---> " + m.from_user.first_name + " " + m.from_user.last_name)
        return False

def acction_sistem(chat_id, accion):
    n = os.system(accion)
    if n == 0:
        if chat_id != -1:
            bot.send_message(chat_id, "✅ Ejecutado Correctamente")
        return True
    else:
        if chat_id != -1:
            bot.send_message(chat_id, "❌ Error al ejecutar")
        return False
    

 # /start
@bot.message_handler(commands=['start'])
def command_start(m):
    if check_user(m):
        bot.send_message(m.chat.id, "Holaaa 😀")
    else:
        bot.send_message(m.chat.id, "🚨❗️⛔️ BOT PRIVADO, CUALQUIER ACCIÓN SERÁ NOTIFICADA AL ADMINISTRADOR ⛔️❗️🚨")
    
# /help
@bot.message_handler(commands=['help', 'ayuda'])
def command_help(m):
     if check_user(m):
        help_text = "Comandos disponibles: \n"
        for key in commands_bot:
            help_text += "/" + key + " - " + commands_bot[key] + "\n"
        bot.send_message(m.chat.id, help_text)

# /docker
@bot.message_handler(commands=['docker'])
def command_docker(m):
    if check_user(m):
        bot.send_message(m.chat.id, "Servicio:")
        global docker_lisen
        docker_lisen = True

#Servicio docker
@bot.message_handler(func=lambda message: docker_lisen)
def handle_docker_service(m):
    global docker_lisen, docker_service
    docker_lisen = False
    docker_service = m.text
    docker_service = docker_service.strip() #similar trim quitar espacios
    keyboard = types.InlineKeyboardMarkup()
    item_start = types.InlineKeyboardButton('Start', callback_data='docker_start')
    item_stop = types.InlineKeyboardButton('Stop', callback_data='docker_stop')
    item_cancel = types.InlineKeyboardButton('Cancelar', callback_data='cancel')
    keyboard.add(item_start, item_stop, item_cancel)
    bot.send_message(m.chat.id, "Acción ejecutar:", reply_markup=keyboard)

# /printer 3d
@bot.message_handler(commands=['3d'])
def command_printer3d(m):
    if check_user(m):
        keyboard = types.InlineKeyboardMarkup()
        item_status = types.InlineKeyboardButton('Status', callback_data='printer3d_status')
        item_pause = types.InlineKeyboardButton('Pause', callback_data='printer3d_pause')
        item_cancel = types.InlineKeyboardButton('Canclear', callback_data='cancel')
        keyboard.add(item_status, item_pause, item_cancel)
        bot.send_message(m.chat.id, "Impresora 3D Accion:", reply_markup=keyboard)

# /system
@bot.message_handler(commands=['system'])
def command_system(m):
    if check_user(m):
        keyboard = types.InlineKeyboardMarkup()
        item_reboot = types.InlineKeyboardButton('Reboot', callback_data='system_reboot')
        item_poweroff = types.InlineKeyboardButton('Poweroff', callback_data='system_poweroff')
        item_status = types.InlineKeyboardButton('Status', callback_data='system_status')
        item_cancel = types.InlineKeyboardButton('Canclear', callback_data='cancel')
        keyboard.add(item_status, item_reboot, item_poweroff, item_cancel)
        bot.send_message(m.chat.id, "Accion:", reply_markup=keyboard)

# /reboot
@bot.message_handler(commands=['reboot'])
def command_reboot(m):
    if check_user(m):
        keyboard = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton('Si', callback_data='yes_reboot')
        item_no = types.InlineKeyboardButton('No', callback_data='no')
        keyboard.add(item_yes, item_no)
        bot.send_message(m.chat.id, "Reiniciar sistema?", reply_markup=keyboard)

# /poweroff
@bot.message_handler(commands=['poweroff'])
def command_poweroff(m):
    if check_user(m):
        keyboard = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton('Si', callback_data='yes_poweroff')
        item_no = types.InlineKeyboardButton('No', callback_data='no')
        keyboard.add(item_yes, item_no)
        bot.send_message(m.chat.id, "❗️ Apagar sistema? ❗️", reply_markup=keyboard)

# /status
@bot.message_handler(commands=['status', 'info'])
def command_status(m):
    status = os.popen('neofetch --off --stdout | sed -n \'4p;8p;9p;10p;11p;12p;14p;15p\'')
    bot.send_message(m.chat.id, status.read())

# /fortune
@bot.message_handler(commands=['fortune'])
def command_fortune(m):
    fortune = os.popen('/usr/games/fortune')
    bot.send_message(m.chat.id, fortune.read())


# mensage especifico
#@bot.message_handler(func=lambda message: message.text == "Hola")
#def command_text_hi(m):
#    bot.send_message(m.chat.id, "Muy buenas")



@bot.message_handler(func=lambda message: True, content_types=["text"])
def command_default(m):
    bot.send_message(m.chat.id, "Comando no disponible")

# Respuestas botones
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_keyboard(call):
    delKeyboard = types.InlineKeyboardMarkup()
    global docker_service
    if call.data == "yes_reboot":
        bot.edit_message_text("Okey reiniciar sistema", call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
        acction_sistem(call.message.chat.id, "sudo reboot")
    elif call.data == "yes_poweroff":
        bot.edit_message_text("Okey apagar sistema", call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
        acction_sistem(call.message.chat.id, "sudo poweroff")
    elif call.data == "docker_start":
        bot.edit_message_text("Start docker " + docker_service, call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
        acction_sistem(call.message.chat.id, "docker start " + docker_service)
        if docker_service == "ubuntu":
            bot.send_message(call.message.chat.id, "https://linux.ropero.duckdns.org")
    elif call.data == "docker_stop":
        bot.edit_message_text("Stop docker " + docker_service, call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
        acction_sistem(call.message.chat.id, "docker stop " + docker_service)
    elif call.data == "system_reboot":
        bot.edit_message_text("/reboot", call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
    elif call.data == "system_poweroff":
        bot.edit_message_text("/poweroff", call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
    elif call.data == "system_status":
        bot.edit_message_text("/status", call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
    elif call.data == "printer3d_status":
        message_printer3d_status = "Status Impresora 3D \n"
        printer3d_status = os.popen("curl -s -X GET -H 'X-Api-Key: "+ TOKEN_PRINTER3D +"' -H 'Content-Type: application/json' http://localhost:4108/api/job | grep -E \"state|completion\" | tr -d ',\"' | awk -F ':' '{print $2}'")
        printer3d_status_progres = printer3d_status.readline()
        find_printer3d_status_progres = printer3d_status_progres.find(".")
        if find_printer3d_status_progres != -1:
            message_printer3d_status += "Progreso: " + printer3d_status_progres[:find_printer3d_status_progres+3] + "\n"
        message_printer3d_status += "Estado: " + printer3d_status.readline()
        bot.edit_message_text(message_printer3d_status, call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
    elif call.data == "printer3d_pause":
        bot.edit_message_text("Pausar Impresion 3D", call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
        keyboard = types.InlineKeyboardMarkup()
        item_okey = types.InlineKeyboardButton('Okey', callback_data='printer3d_pause_okey')
        item_cancel = types.InlineKeyboardButton('Cancelar', callback_data='cancel')
        keyboard.add(item_okey, item_cancel)
        bot.send_message(call.message.chat.id, "Seguro?", reply_markup=keyboard)
    elif call.data == "printer3d_pause_okey":
        bot.edit_message_text("Pausando Impresora 3D", call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)
        acction_sistem(-1, "curl -s -X POST -H 'X-Api-Key: "+ TOKEN_PRINTER3D + "' -H 'Content-Type: application/json' -d '{\"command\":\"M600\"}' http://localhost:4108/api/printer/command")
    else:
        bot.edit_message_text("Cancelado", call.message.chat.id, call.message.message_id, reply_markup=delKeyboard)


def listener(messages):
    with open(FILE_LOG, 'a') as f:
        now = datetime.now()
        for m in messages:
            text = now.strftime("%d/%m/%Y %H:%M:%S   ") + str(m.from_user.id) + " - " + m.from_user.username + " ----> " + m.text + "\n"
            f.write(text)

bot.set_update_listener(listener)
bot.infinity_polling()
