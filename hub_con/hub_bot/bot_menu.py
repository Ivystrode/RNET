from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, Dispatcher, ConversationHandler

from hub_con import dbcontrol


# ==========MENU TREE==========
class MenuTree():
    
    def __init__(self, update, context, botkey):
        self.update = update
        self.context = context
        self.botkey = botkey
        
        self.updater = Updater(self.botkey, use_context=True)

        self.dispatcher = self.updater.dispatcher
        
        self.COMMAND, self.UNIT, self.COMMAND_DETAIL = range(3)
        self.command = ''
        self.unit = ''
        self.command_detail = ''
        
        self.menu_handler = ConversationHandler(
            entry_points=[self.main_menu(update, context)],
            states= {
                self.COMMAND: [MessageHandler(Filters.text, self.command)],
                self.UNIT: [MessageHandler(Filters.text, self.unit)],
                self.COMMAND_DETAIL: [MessageHandler(Filters.text, self.command_detail)],
            },
            fallbacks=[CommandHandler('cancel',self.cancel)]
        )
        
    def cancel(self, update, context):
        print("[HUB - BOT] Cancelled command")
        return ConversationHandler.END
    
    def open_menu(self, update, context):
        update.message.reply_text("Main Menuu", reply_markup=MenuTree.main_menu_keyboard())
        
        
    # LEVEL 1
    # -------
    def main_menu(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Main Menu", reply_markup=MenuTree.main_menu_keyboard())
        
    # LEVEL 2
    # -------
    def rf_menu(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="RF Menu", reply_markup=MenuTree.rf_menu_keyboard())
        
    def cam_menu(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Camera Menu", reply_markup=MenuTree.cam_menu_keyboard())
        
    def fc_menu(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Flight Control", reply_markup=MenuTree.fc_menu_keyboard())
        
    # LEVEL 3
    # -------    
    def wifi_menu(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Wifi Menu", reply_markup=MenuTree.wifi_menu_keyboard())
        
    # LEVEL 4
    # -------    
    def unit_menu(self, update, context):
        print("unit menu")
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Select Unit", reply_markup=MenuTree.unit_menu_keyboard())
        
    def button(self, update, context):
        query = update.callback_query
        query.answer()
        choice = query.data
        if choice == "wifi_menu":
            print("aaa")
        else:
            print(choice)
            
    def choose_unit(self, update, context, command):
        print("nahhh")
        query = update.callback_query
        query.answer()
        choice = query.data
        
        
        
        
    # ==========KEYBOARDS==========

        
    # LEVEL 1
    # -------  
    def main_menu_keyboard(self):
        keyboard = [
        [
            InlineKeyboardButton("RF Commands", callback_data='rf_menu'),
            InlineKeyboardButton("Camera Commands", callback_data='cam_menu'),
        ],
        [InlineKeyboardButton("Flight Control", callback_data='fc_menu')],
    ]
        return InlineKeyboardMarkup(keyboard)

        
    # LEVEL 2
    # -------  
    def rf_menu_keyboard(self):
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
            
    def cam_menu_keyboard(self):
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
                
                
    def fc_menu_keyboard(self):
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

        
    # LEVEL 3
    # -------  
    def wifi_menu_keyboard(self):
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
        
    # LEVEL 4
    # -------  
    def unit_menu_keyboard(self):
        print("++++++++++++++++++++++++++++++++")
        # keyboard = [InlineKeyboardButton(f"{unit}", callback_data='try') for unit in dbcontrol.get_all_units()]
        units = dbcontrol.get_all_units()
        print("====")
        print(units)
        print("===")
        buttons = []
        for unit in units:
            print(unit[1])
            buttons.append(InlineKeyboardButton(unit[1], callback_data=unit[1]))
        print(buttons)
        
        print("right...")
        return InlineKeyboardMarkup(buttons)
    
    


    