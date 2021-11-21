"""
This bot will run on the hub/VPN server and can be used to send commands to the units and check their status
I would also like units to be able to send pictures, even videos to the bot.

Store authorised users in a table in the database file...
"""

import sys
sys.path.append("/home/main/Documents/File_Root/Main/Code/Projects/rnet/rnet/") # stop module import error ffs

from datetime import datetime
import json
import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, Dispatcher, ConversationHandler
import threading
import time
import socket

# import commands
# import dbcontrol
from hub_con import commands, dbcontrol
# from rnet.keys import keys
from decouple import config

tbot_key=config('tbot_key')

# logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG) # change to DEBUG for more info inc user id etc

# logger = logging.getLogger(__name__)

updater = None
dispatcher = None

updater = Updater(tbot_key, use_context=True)

dispatcher = updater.dispatcher

command_channel = 7502
file_root = "/home/main/Documents/Main/Code/Projects/rnet/rnet/"
users = []


awaiting_file = False


def start_bot():
    global updater
    global dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('menu', open_menu))
    dispatcher.add_handler(CommandHandler('check', check))
    dispatcher.add_handler(CommandHandler('help', help))
    
    dispatcher.add_handler(CommandHandler('status', get_unit_status))
    dispatcher.add_handler(CommandHandler('address', get_unit_address))
    
    dispatcher.add_handler(CommandHandler('axis', move_servo))
    dispatcher.add_handler(CommandHandler('autorotate', move_servo))
    
    dispatcher.add_handler(CommandHandler('cpu', cpu_comd))
    dispatcher.add_handler(CommandHandler('send', send_comd))
    dispatcher.add_handler(CommandHandler('stream', stream_comd))
    dispatcher.add_handler(CommandHandler('stopstream', stop_stream_comd))
    dispatcher.add_handler(CommandHandler('detection', toggle_image_detection))
    
    dispatcher.add_handler(CommandHandler('wifi', wifi_comd))
    dispatcher.add_handler(CommandHandler('stopwscan', stop_wifi_scan))
    
    dispatcher.add_handler(CommandHandler('fc', fc_comd))
    
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern="main"))
    
    dispatcher.add_handler(CallbackQueryHandler(rf_menu, pattern="rf_menu"))
    dispatcher.add_handler(CallbackQueryHandler(cam_menu, pattern="cam_menu"))
    dispatcher.add_handler(CallbackQueryHandler(fc_menu, pattern="fc_menu"))
    
    dispatcher.add_handler(CallbackQueryHandler(wifi_menu, pattern="wifi_menu"))
    
    dispatcher.add_handler(CallbackQueryHandler(unit_menu, pattern="unit_menu"))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()
    
    
# ==========MAIN MENUS==========
def open_menu(update, context):
    update.message.reply_text("Main Menuu", reply_markup=main_menu_keyboard())
    
    
# LEVEL 1
# -------
def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Main Menu", reply_markup=main_menu_keyboard())
    
# LEVEL 2
# -------
def rf_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="RF Menu", reply_markup=rf_menu_keyboard())
    
def cam_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Camera Menu", reply_markup=cam_menu_keyboard())
    
def fc_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Flight Control", reply_markup=fc_menu_keyboard())
    
# LEVEL 3
# -------    
def wifi_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Wifi Menu", reply_markup=wifi_menu_keyboard())
    
# LEVEL 4
# -------    
def unit_menu(update, context):
    print("unit menu")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Select Unit", reply_markup=unit_menu_keyboard())
    
def button(update, context):
    query = update.callback_query
    query.answer()
    choice = query.data
    if choice == "wifi_menu":
        send_message("yaaa")
    else:
        print(choice)
        
def choose_unit(update, context, command):
    print("nahhh")
    query = update.callback_query
    query.answer()
    choice = query.data
    
    
    
    
# ==========KEYBOARDS==========

# ==========LEVEL 1 (MAIN)==========
def main_menu_keyboard():
    keyboard = [
    [
        InlineKeyboardButton("RF Commands", callback_data='rf_menu'),
        InlineKeyboardButton("Camera Commands", callback_data='cam_menu'),
    ],
    [InlineKeyboardButton("Flight Control", callback_data='fc_menu')],
]
    return InlineKeyboardMarkup(keyboard)

# ==========LEVEL 2==========
    
def rf_menu_keyboard():
    print("++++++++++++++++++++++++++++++++")
    keyboard = [
    [
        InlineKeyboardButton("Wifi Scan", callback_data='wifi_menu'),
        InlineKeyboardButton("RF Emission", callback_data='rf_emit_menu'),
        InlineKeyboardButton("RF Silent Mode", callback_data='rf_silent'),
    ],
    [InlineKeyboardButton("Back", callback_data='main_menu')],
]
    return InlineKeyboardMarkup(keyboard)
        
def cam_menu_keyboard():
    print("++++++++++++++++++++++++++++++++")
    keyboard = [
    [
        InlineKeyboardButton("Send Picture", callback_data='unit_menu'),
        InlineKeyboardButton("Object Detection", callback_data='object_detection'),
        InlineKeyboardButton("Stream Video", callback_data='stream_video'),
    ],
    [InlineKeyboardButton("Back", callback_data='main_menu')],
]
    return InlineKeyboardMarkup(keyboard)
            
            
def fc_menu_keyboard():
    print("++++++++++++++++++++++++++++++++")
    keyboard = [
    [
        InlineKeyboardButton("Takeoff", callback_data='fc_takeoff'),
        InlineKeyboardButton("RTH", callback_data='fc_rth'),
        InlineKeyboardButton("Payload Release", callback_data='fc_payload_release'),
    ],
    [InlineKeyboardButton("Back", callback_data='main_menu')],
]
    return InlineKeyboardMarkup(keyboard)    

# ==========LEVEL 3========== 
def wifi_menu_keyboard():
    print("++++++++++++++++++++++++++++++++")
    keyboard = [
    [
        InlineKeyboardButton("Short Scan (5s)", callback_data='short_scan'),
        InlineKeyboardButton("Med Scan (60s)", callback_data='med_scan'),
        InlineKeyboardButton("Long Scan (5 mins)", callback_data='long_scan'),
    ],
    [InlineKeyboardButton("Back", callback_data='rf_menu')],
]
    return InlineKeyboardMarkup(keyboard)
# ==========LEVEL 4==========
       
def unit_menu_keyboard():
    print("++++++++++++++++++++++++++++++++")
    # keyboard = [InlineKeyboardButton(f"{unit}", callback_data='try') for unit in dbcontrol.get_all_units()]
    units = dbcontrol.get_all_units()
    print("====")
    print(units)
    print("===")
    buttons = []
    for unit in units:
        print(unit[1])
        buttons.append(InlineKeyboardButton(unit[1], callback_data="none"))
    print(buttons)
    
    print("right...")
    return InlineKeyboardMarkup(buttons)
    
    
    
    
    
    
    
    
    
    
    
    
    
# ==========WORKER FUNCTIONS==========    
# THIS GETS VERY BORING NOW
# THESE ARE JUST FUNCTIONS YOU CAN CALL BY SENDING MESSAGES TO THE BOT
# NOT SO DIFFERENT FROM A CLI
    
    
    
    
    
def start(update, context):
    global users
    users_name=update['message']['chat']['first_name']
    reply = "Hi " + users_name + ". I am RNet Bot. I will help you control RNet when the system and myself are up and running."
    chat_id = update['message']['chat']['id']
    users.append(chat_id)
    try:
        dbcontrol.add_authorised_user(int(chat_id), users_name, "regular")
        users = [user[0] for user in dbcontrol.get_all_users()]
        print(f"[HUB - BOT] User added to authorised users: {str(chat_id)}")
        update.message.reply_text(reply)
        time.sleep(0.5)
        update.message.reply_text(f"I have added you to the authorised users database, {users_name}")
        print(f"[HUB - BOT] Added user {users_name}, ID: {chat_id} to authorised users database")
    except Exception as e:
        update.message.reply_text(f"You're already on the authorised users list, {users_name}, or for some reason I can't add you")
        print(f"[HUB - BOT] Add authorised user error: {e}")
    
def help(update, context):
    reply = "work in progress"
    reply = """
    COMMANDS:\n
/address [unit name]: Gets the IP address of the specified unit\n
/status [unit name]: Gets the status of the specificed unit\n
/axis [unit name] [axis] [position (2.6-12.6/centre]: rotates the X or Y axis to the specified position, or centres one or both. If centering both, send "/axis [unitname] centre both"\n
/cpu [unit name] [command]: Orders the onboard computer of the specified unit to carry out the directed command (ie reboot, shutdown)\n
/send [unit name] [file type]: Orders the specified unit to send a file (if a media file is requested, the on board camera actives to capture the requested content)\n
/wifi [unit name] [command] [time (optional)]: Perform a wifi based action, i.e. "/wifi [unit name] scan" does a continuous wifi scan. Adding a number specifies in seconds how long to scan for.\n
/check Check if you are an authorised user\n
    """
    
    update.message.reply_text(reply)
    
    
def get_unit_address(update, context):
    """
    Get the address of a unit in order to send commands
    """
    name = context.args[0]
    update.message.reply_text(f"Checking database...")
    time.sleep(0.5)
    unit_address = dbcontrol.get_unit_address(name)
    update.message.reply_text(f"Stored address for {name.upper()}: {unit_address}")
    
def get_unit_status(update, context):
    name = context.args[0]
    unit_address = dbcontrol.get_unit_address(name)
    update.message.reply_text(f"Checking...")
    time.sleep(0.5)
    unit_status = commands.get_unit_status(name, unit_address)
    
    if unit_status == "no_connection":
        update.message.reply_text(f"Cannot connect to {name}")
    else:
        update.message.reply_text(f"{name.upper()} status: {unit_status[0]}")
        update.message.reply_text(f"Latest STATREP: {unit_status[1]}")

    
    
    
def move_servo(update, context):
    """
    Get the address of a unit in order to send commands
    """
    name = context.args[0]
    unit_address = dbcontrol.get_unit_address(name)
    
    if len(context.args) > 1: # if more than one argument, it is a specific move command, not autorotate
        axis = context.args[1]
        posn = context.args[2]
        
        try:
            commands.servo_move(unit_address, command_channel, axis, posn)
            time.sleep(0.5)
            update.message.reply_text(f"[{axis.upper()}: {posn}] servo command sent to {name}")
        except Exception as e:
            update.message.reply_text(f"Unable to send command to {name}")
            time.sleep(0.5)
            update.message.reply_text(f"{e}")
            
    else: # if just one argument - which is the name of the unit - it is an autorotate command
        print("[HUB - BOT] Move servo function; autorotate command")
        axis = "<AUTOROTATE>"
        position = "n/a"

        try:
            commands.servo_move(unit_address, command_channel, axis, position)
            time.sleep(0.5)
            update.message.reply_text(f"[{axis.upper()}] servo command sent to {name}")
        except Exception as e:
            update.message.reply_text(f"Unable to send command to {name}")
            time.sleep(0.5)
            update.message.reply_text(f"{e}")
        
# def autorotate(update, context):
#     """Pan/scan with the camera"""
#     name = con

def check(update, context):
    chat_id = update['message']['chat']['id']
    user_status = dbcontrol.check_user(chat_id)
    if user_status == "regular":
        update.message.reply_text(f"You are authorised as a {user_status} user")
    elif user_status == None:
        update.message.reply_text(f"You are not in the database of authorised users")
    else:
        update.message.reply_text(f"Your authorisation status is: {user_status}")
        
        
def cpu_comd(update, context):
    name = context.args[0]
    command = context.args[1]
    unit_address = dbcontrol.get_unit_address(name)

    try:
        commands.cpu_comd(unit_address, command_channel, command)
        update.message.reply_text(f"[CPU: {command.upper()}] command sent to {name}")

    except Exception as e:
        update.message.reply_text(f"{e}")
        
def send_comd(update, context):
    pic_comd = ['pic','picture','img','image','photo','photograph']
    # print(update)
    chat_id = update['message']['chat']['id']
    
    file_sent = False
    
    name = context.args[0]
    unit_address = dbcontrol.get_unit_address(name)#maybe add an if unit address is None "unit not found"
    filetype = context.args[1]
    
    if filetype in pic_comd:
        filetype = "image"
        vid_length = "n/a"
        update.message.reply_text(f"Requesting camera shot from {name}...")
    else:
        print("error not ready yet, will send image for now")
        filetype = "image"
        vid_length = "n/a"
        
    # requested_filename = file_root + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + name + ".jpg"
    # print(f"Searching for {requested_filename}")
    try:
        commands.send_file(unit_address, command_channel, filetype, vid_length)
        # for attempt in range(1,12):
        #     try:
        #         updater.bot.sendPhoto(chat_id, photo=open(requested_filename, "rb"), timeout=50, caption=f"Image from {name}")
        #         file_sent = True
        #         break
        #     except:
        #         time.sleep(attempt)
                
        # if not file_sent:
        #     update.message.reply_text(f"Nothing received from {name}")
            
    except Exception as e:
        update.message.reply_text(f"Unable to complete: {e}")
        
def send_unrequested_file(unitname, filename, file_description):
    # since i added the user data base i need to change how  this works
    #users = dbcontrol.get_all_users()
    #print(users)
    print(f"[HUB - BOT] FILE SEND, users: {users}")
    try:
        for user in users:
            sent = False
            try:
                updater.bot.sendPhoto(user, photo=open(filename, "rb"), timeout=50, caption=f"{unitname.upper()}: {file_description}")
                print("[HUB - BOT] Sent photo")
                sent = True
            except Exception as e:
                print(f"[HUB - BOT] Not a photo...send as file?")
                try:
                    if not sent:
                        updater.bot.sendDocument(user, document=open(filename, "rb"), timeout=50, caption=f"{unitname.upper()}: {file_description}")
                        print("[HUB - BOT] Sent as document")
                    sent = True
                except Exception as e:
                    print(f"[HUB - BOT] Unable to send file (neither a photo or a document recognised) {filename} - {e}")
            if sent == True:
                print(f"[HUB - BOT] File sent: {filename} to {user}")
            else:
                print(f"[HUB - BOT] Unable to send {filename} to user: {user}")
                
    except Exception as e:
        print(f"[HUB - BOT] Unable to send file {filename} - {e}")
        
def send_message(message):
    for user in users:
        updater.bot.send_message(user, message)
def send_private_message(user, message):
    updater.bot.send_message(user, message)
        

def wifi_comd(update, context):
    name = context.args[0]
    command = context.args[1]
    if context.args[2]:
        scan_time = context.args[2]
    else:
        scan_time = "continuous"
    unit_address = dbcontrol.get_unit_address(name)
    
    try:
        commands.wifi_comd(unit_address, command_channel, command, scan_time)
        update.message.reply_text(f"Wifi scan command sent to {name}")
    except Exception as e:
        update.message.reply_text(f"Unable to initiate wifi scan. {e}")
        

def fc_comd(update, context):
    name = context.args[0]
    command = context.args[1]
    update.message.reply_text(f"Sending launch command to {name}")
    unit_address = dbcontrol.get_unit_address(name)
    commands.fc_comd(unit_address, command_channel, command)
    
def stream_comd(update, context):
    name = context.args[0]
    # if context.args[1]:
    #     stream_time = context.args[1]
    # else:
    stream_time = "continuous"
    unit_address = dbcontrol.get_unit_address(name)
    command="stream"
    
    try:
        commands.vid_comd(unit_address, command_channel, command, stream_time)
        update.message.reply_text(f"Video stream command sent to {name}")
    except Exception as e:
        update.message.reply_text(f"Unable to initiate video stream. {e}")
    
def stop_stream_comd(update, context):
    name = context.args[0]
    # if context.args[1]:
    #     stream_time = context.args[1]
    # else:
    unit_address = dbcontrol.get_unit_address(name)
    command="stopstream"
    
    try:
        commands.vid_comd(unit_address, command_channel, command, "n/a")
        update.message.reply_text(f"Stop stream command sent to {name}")
    except Exception as e:
        update.message.reply_text(f"Unable to initiate video stream. {e}")
        
def toggle_image_detection(update, context):
    name = context.args[0]
    duration = context.args[1]
    unit_address = dbcontrol.get_unit_address(name)
    
    try:
        commands.vid_comd(unit_address, command_channel, "image_detection", duration)
        update.message.reply_text(f"Object detection command send to {name}")
    except Exception as e:
        update.message.reply_text(f"Command error: {e}")
    
    
def stop_wifi_scan(update, context):
    name = context.args[0]
    command = "STOP_SCAN"
    time = "n/a"
    unit_address = dbcontrol.get_unit_address(name)
    
    try:
        commands.wifi_comd(unit_address, command_channel, command, time)
        update.message.reply_text(f"Terminate wifi scan command sent to {name}")
    except Exception as e:
        update.message.reply_text(f"Unable to terminate wifi scan. {e}")
    
    
    
    



def activate_hub_bot():
    global users
    users = [user[0] for user in dbcontrol.get_all_users()]
    print(f"[HUB - BOT] Authorised users by ID: {users}")
    bot_thread = threading.Thread(name='bot', target=start_bot)
    bot_thread.start()
    print("[HUB - BOT] Hub bot started")
    
# if __name__ == '__main__':
#     start_bot()