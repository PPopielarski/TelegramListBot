import os


bot_token = '783375470:AAHjxORsSMQRcL3T2RIQgFkQs6ZSt9vpemI'
sqlite_db_path = os.path.abspath(os.path.join(os.getcwd(), "../") + '\\Utils\\list_bot.db')
log_path = os.path.abspath(os.path.join(os.getcwd(), "../") + '\\Utils\\log.txt')
db_backup_cron = ''
db_backup_max_count = 10
db_backups_path = os.path.abspath(os.path.join(os.getcwd(), "../") + '\\db_bck\\')

def add_list(chat, args=None):
    if len(arguments) == 0:
        self.chat_dict[chat_id].respond(text='Enter new list name.', force_message=True)
        self.chat_dict[chat_id].command = '/add_list'
    else:
        self.db.add_list(chat_id=chat_id, list_name=arguments)
        self.chat_dict[chat_id].respond(text='List "' + arguments + '" has been added!')
        if self.chat_dict[chat_id].state == 0:
            self.function_dict['/show_lists'](chat_id, '')
        else:
            self.bot_api.send_chat_action(chat_id, 'typing')