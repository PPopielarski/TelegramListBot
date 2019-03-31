import os


bot_token = '783375470:AAHjxORsSMQRcL3T2RIQgFkQs6ZSt9vpemI'
sqlite_db_path = os.path.abspath(os.path.join(os.getcwd(), "../") + '\\Utils\\list_bot.db')
log_path = os.path.abspath(os.path.join(os.getcwd(), "../") + '\\Utils\\log.txt')
db_backup_cron = ''
db_backup_max_count = 10
db_backups_path = os.path.abspath(os.path.join(os.getcwd(), "../") + '\\db_bck\\')
