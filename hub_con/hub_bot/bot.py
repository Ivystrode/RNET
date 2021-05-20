"""
This bot will run on the hub/VPN server and can be used to send commands to the units and check their status
I would also like units to be able to send pictures, even videos to the bot.
"""

import sys
sys.path.append("/home/main/Documents/File_Root/Main/Code/Projects/rnet/") # stop module import error ffs

import json
import logging
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


    

def start_bot():
    global updater
    global dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('name', get_unit_name))
    dispatcher.add_handler(CommandHandler('status', get_unit_status))
    dispatcher.add_handler(CommandHandler('axis', move_servo))
    
    updater.start_polling()
    updater.idle()
    
def start(update, context):
    users_name=update['message']['chat']['first_name']
    reply = "Hi " + users_name + ". I am RNet Bot. I will help you control RNet when the system and myself are up and running."
    update.message.reply_text(reply)
    active.test()
    
def test():
    print("bot import test")
    
def get_unit_address(update, context):
    """
    Get the address of a unit in order to send commands
    """
    name = context.args[0]
    unit_address = dbcontrol.get_unit_address(name)
    update.message.reply_text(f"{name} address: {unit_address}")
    commands.servo_test(unit_address, 7502, 12)
    
def move_servo(update, context):
    """
    Get the address of a unit in order to send commands
    """
    name = context.args[0]
    axis = context.args[1]
    posn = context.args[2]
    unit_address = dbcontrol.get_unit_address(name)
    update.message.reply_text(f"{name} address: {unit_address}")
    
    try:
        commands.servo_test(unit_address, 7502, axis, posn)
        time.sleep(0.5)
        update.message.reply_text(f"[{axis.upper()}: {posn}] servo command sent to {name}")
    except Exception as e:
        update.message.reply_text(f"Unable to send command to {name}")
        time.sleep(0.5)
        update.message.reply_text(f"{e}")
        
    
def get_unit_name(update, context):
    """
    Eventually want to replace this with a direct communication to the hostname/IP of the unit
    Not a CC1 asking this particular unit to respond/comply... 
    """
    print(context.args)
    # update.message.reply_text(unit_main.unit.get_name(context.args[0]))
    
def get_unit_status(update, context):
    """
    Get status of a unit
    """
    print(context.args)
    # update.message.reply_text(unit_main.unit.get_name(context.args[0]))


    

bot_thread = threading.Thread(name='bot', target=start_bot)

bot_thread.start()