"""
This bot will run on the hub/VPN server and can be used to send commands to the units and check their status
I would also like units to be able to send pictures, even videos to the bot.

Store authorised users in a table in the database file...
"""

import sys
sys.path.append("/home/main/Documents/File_Root/Main/Code/Projects/rnet/rnet/") # stop module import error ffs

from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, Dispatcher, ConversationHandler
import threading, time
from decouple import config

from hub_con import commands, dbcontrol
from hub_con.hub_bot.bot_menu import MenuTree



class HubBot():
    
    def __init__(self):
        self.tbot_key=config('tbot_key')

        self.updater = None
        self.dispatcher = None

        self.updater = Updater(self.tbot_key, use_context=True)

        self.dispatcher = self.updater.dispatcher

        self.command_channel = 7502
        self.file_root = "/home/main/Documents/Main/Code/Projects/rnet/rnet/"
        self.users = []
        # self.main_menu = MenuTree(self.updater, self.dispatcher, self.tbot_key)


        self.awaiting_file = False


    def start_bot(self):        
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        # self.dispatcher.add_handler(CommandHandler('menu', self.main_menu.open_menu))
        self.dispatcher.add_handler(CommandHandler('check', self.check))
        self.dispatcher.add_handler(CommandHandler('help', self.help))
        
        self.dispatcher.add_handler(CommandHandler('status', self.get_unit_status))
        self.dispatcher.add_handler(CommandHandler('address', self.get_unit_address))
        
        self.dispatcher.add_handler(CommandHandler('axis', self.move_servo))
        self.dispatcher.add_handler(CommandHandler('autorotate', self.move_servo))
        
        self.dispatcher.add_handler(CommandHandler('cpu', self.cpu_comd))
        self.dispatcher.add_handler(CommandHandler('send', self.send_comd))
        self.dispatcher.add_handler(CommandHandler('stream', self.stream_comd))
        self.dispatcher.add_handler(CommandHandler('stopstream', self.stop_stream_comd))
        self.dispatcher.add_handler(CommandHandler('detection', self.toggle_image_detection))
        
        self.dispatcher.add_handler(CommandHandler('wifi', self.wifi_comd))
        self.dispatcher.add_handler(CommandHandler('stopwscan', self.stop_wifi_scan))
        
        self.dispatcher.add_handler(CommandHandler('fc', self.fc_comd))
        
        # self.dispatcher.add_handler(CallbackQueryHandler(self.main_menu.main_menu, pattern="main"))
        
        # self.dispatcher.add_handler(CallbackQueryHandler(self.main_menu.rf_menu, pattern="rf_menu"))
        # self.dispatcher.add_handler(CallbackQueryHandler(self.main_menu.cam_menu, pattern="cam_menu"))
        # self.dispatcher.add_handler(CallbackQueryHandler(self.main_menu.fc_menu, pattern="fc_menu"))
        
        # self.dispatcher.add_handler(CallbackQueryHandler(self.main_menu.wifi_menu, pattern="wifi_menu"))
        
        # self.dispatcher.add_handler(CallbackQueryHandler(self.main_menu.unit_menu, pattern="unit_menu"))
        # self.dispatcher.add_handler(CallbackQueryHandler(self.main_menu.button))
        
        self.updater.start_polling()
        self.updater.idle()
        
        

        
        
        
        
        
        
        
        
        
    # ==========WORKER FUNCTIONS==========    
    # THIS GETS VERY BORING NOW
    # THESE ARE JUST FUNCTIONS YOU CAN CALL BY SENDING MESSAGES TO THE BOT
    # NOT SO DIFFERENT FROM A CLI
        
        
        
        
        
    def start(self,update, context):
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
        
    def help(self,update, context):
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
        
        
    def get_unit_address(self,update, context):
        """
        Get the address of a unit in order to send commands
        """
        name = context.args[0]
        update.message.reply_text(f"Checking database...")
        time.sleep(0.5)
        unit_address = dbcontrol.get_unit_address(name)
        update.message.reply_text(f"Stored address for {name.upper()}: {unit_address}")
        
    def get_unit_status(self,update, context):
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

        
        
        
    def move_servo(self,update, context):
        """
        Get the address of a unit in order to send commands
        """
        name = context.args[0]
        unit_address = dbcontrol.get_unit_address(name)
        
        if len(context.args) > 1: # if more than one argument, it is a specific move command, not autorotate
            axis = context.args[1]
            posn = context.args[2]
            
            try:
                commands.servo_move(unit_address, self.command_channel, axis, posn)
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
                commands.servo_move(unit_address, self.command_channel, axis, position)
                time.sleep(0.5)
                update.message.reply_text(f"[{axis.upper()}] servo command sent to {name}")
            except Exception as e:
                update.message.reply_text(f"Unable to send command to {name}")
                time.sleep(0.5)
                update.message.reply_text(f"{e}")
            
    # def autorotate(update, context):
    #     """Pan/scan with the camera"""
    #     name = con

    def check(self,update, context):
        chat_id = update['message']['chat']['id']
        user_status = dbcontrol.check_user(chat_id)
        if user_status == "regular":
            update.message.reply_text(f"You are authorised as a {user_status} user")
        elif user_status == None:
            update.message.reply_text(f"You are not in the database of authorised users")
        else:
            update.message.reply_text(f"Your authorisation status is: {user_status}")
            
            
    def cpu_comd(self,update, context):
        name = context.args[0]
        command = context.args[1]
        unit_address = dbcontrol.get_unit_address(name)

        try:
            commands.cpu_comd(unit_address, self.command_channel, command)
            update.message.reply_text(f"[CPU: {command.upper()}] command sent to {name}")

        except Exception as e:
            update.message.reply_text(f"{e}")
            
    def send_comd(self,update, context):
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
            commands.send_file(unit_address, self.command_channel, filetype, vid_length)
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
            
    def send_unrequested_file(self,unitname, filename, file_description):
        # since i added the user data base i need to change how  this works
        #users = dbcontrol.get_all_users()
        #print(users)
        print(f"[HUB - BOT] FILE SEND, users: {users}")
        try:
            for user in users:
                sent = False
                try:
                    self.updater.bot.sendPhoto(user, photo=open(filename, "rb"), timeout=50, caption=f"{unitname.upper()}: {file_description}")
                    print("[HUB - BOT] Sent photo")
                    sent = True
                except Exception as e:
                    print(f"[HUB - BOT] Not a photo...send as file?")
                    try:
                        if not sent:
                            self.updater.bot.sendDocument(user, document=open(filename, "rb"), timeout=50, caption=f"{unitname.upper()}: {file_description}")
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
            
    def send_message(self, message):
        for user in users:
            self.updater.bot.send_message(user, message)
    def send_private_message(self, user, message):
        self.updater.bot.send_message(user, message)
            

    def wifi_comd(self,update, context):
        name = context.args[0]
        command = context.args[1]
        if context.args[2]:
            scan_time = context.args[2]
        else:
            scan_time = "continuous"
        unit_address = dbcontrol.get_unit_address(name)
        
        try:
            commands.wifi_comd(unit_address, self.command_channel, command, scan_time)
            update.message.reply_text(f"Wifi scan command sent to {name}")
        except Exception as e:
            update.message.reply_text(f"Unable to initiate wifi scan. {e}")
            

    def fc_comd(self,update, context):
        name = context.args[0]
        command = context.args[1]
        update.message.reply_text(f"Sending launch command to {name}")
        unit_address = dbcontrol.get_unit_address(name)
        commands.fc_comd(unit_address, self.command_channel, command)
        
    def stream_comd(self,update, context):
        name = context.args[0]
        # if context.args[1]:
        #     stream_time = context.args[1]
        # else:
        stream_time = "continuous"
        unit_address = dbcontrol.get_unit_address(name)
        command="stream"
        
        try:
            commands.vid_comd(unit_address, self.command_channel, command, stream_time)
            update.message.reply_text(f"Video stream command sent to {name}")
        except Exception as e:
            update.message.reply_text(f"Unable to initiate video stream. {e}")
        
    def stop_stream_comd(self,update, context):
        name = context.args[0]
        # if context.args[1]:
        #     stream_time = context.args[1]
        # else:
        unit_address = dbcontrol.get_unit_address(name)
        command="stopstream"
        
        try:
            commands.vid_comd(unit_address, self.command_channel, command, "n/a")
            update.message.reply_text(f"Stop stream command sent to {name}")
        except Exception as e:
            update.message.reply_text(f"Unable to initiate video stream. {e}")
            
    def toggle_image_detection(self,update, context):
        name = context.args[0]
        duration = context.args[1]
        unit_address = dbcontrol.get_unit_address(name)
        
        try:
            commands.vid_comd(unit_address, self.command_channel, "image_detection", duration)
            update.message.reply_text(f"Object detection command send to {name}")
        except Exception as e:
            update.message.reply_text(f"Command error: {e}")
        
        
    def stop_wifi_scan(self,update, context):
        name = context.args[0]
        command = "STOP_SCAN"
        time = "n/a"
        unit_address = dbcontrol.get_unit_address(name)
        
        try:
            commands.wifi_comd(unit_address, self.command_channel, command, time)
            update.message.reply_text(f"Terminate wifi scan command sent to {name}")
        except Exception as e:
            update.message.reply_text(f"Unable to terminate wifi scan. {e}")
        
        
        
        



    def activate_hub_bot(self):
        global users
        users = [user[0] for user in dbcontrol.get_all_users()]
        print(f"[HUB - BOT] Authorised users by ID: {users}")
        bot_thread = threading.Thread(name='bot', target=self.start_bot)
        bot_thread.start()
        print("[HUB - BOT] Hub bot started")
        
# if __name__ == '__main__':
#     HubBot.start_bot()