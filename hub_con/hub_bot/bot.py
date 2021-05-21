"""
This bot will run on the hub/VPN server and can be used to send commands to the units and check their status
I would also like units to be able to send pictures, even videos to the bot.
"""

import sys
sys.path.append("/home/main/Documents/File_Root/Main/Code/Projects/rnet/") # stop module import error ffs

from datetime import datetime
import json
import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, ConversationHandler
import threading
import time
import socket

import commands
import dbcontrol
from rnet.keys import keys
# from unit import unit_main
from rnet.unit_con.sdr import active

# logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG) # change to DEBUG for more info inc user id etc

# logger = logging.getLogger(__name__)

updater = None
dispatcher = None

updater = Updater(keys.tbot_key, use_context=True)

dispatcher = updater.dispatcher

command_channel = 7502


def start_bot():
    global updater
    global dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    
    dispatcher.add_handler(CommandHandler('status', get_unit_status))
    dispatcher.add_handler(CommandHandler('address', get_unit_address))
    
    dispatcher.add_handler(CommandHandler('axis', move_servo))
    dispatcher.add_handler(CommandHandler('cpu', cpu_comd))
    
    dispatcher.add_handler(CommandHandler('send', send_comd))
    
    updater.start_polling()
    updater.idle()
    
def start(update, context):
    users_name=update['message']['chat']['first_name']
    reply = "Hi " + users_name + ". I am RNet Bot. I will help you control RNet when the system and myself are up and running."
    update.message.reply_text(reply)
    
def help(update, context):
    reply = "work in progress"
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
    axis = context.args[1]
    posn = context.args[2]
    unit_address = dbcontrol.get_unit_address(name)
    
    try:
        commands.servo_move(unit_address, command_channel, axis, posn)
        time.sleep(0.5)
        update.message.reply_text(f"[{axis.upper()}: {posn}] servo command sent to {name}")
    except Exception as e:
        update.message.reply_text(f"Unable to send command to {name}")
        time.sleep(0.5)
        update.message.reply_text(f"{e}")
        
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
    unit_address = dbcontrol.get_unit_address(name)
    filetype = context.args[1]
    
    if filetype in pic_comd:
        filetype = "image"
        vid_length = "n/a"
        update.message.reply_text(f"Requesting camera shot from {name}...")
    else:
        print("error not ready yet, will send image for now")
        filetype = "image"
        vid_length = "n/a"
        
    requested_filename = "/home/main/Documents/File_Root/Main/Code/Projects/rnet/rnet/" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + name + ".jpg"
    print(f"Searching for {requested_filename}")
    try:
        commands.send_file(unit_address, command_channel, filetype, vid_length)
        for attempt in range(1,6):
            try:
                updater.bot.sendPhoto(chat_id, photo=open(requested_filename, "rb"), timeout=20, caption=f"Image from {name}")
                file_sent = True
                break
            except:
                time.sleep(attempt)
                
        if not file_sent:
            update.message.reply_text(f"Nothing received from {name}")
            
    except Exception as e:
        update.message.reply_text(f"Unable to complete: {e}")
        
    



    

bot_thread = threading.Thread(name='bot', target=start_bot)

bot_thread.start()