import sqlite3
import os.path
from ListBot.Logger import Logger
import time
from shutil import copyfile


class SQLiteHandler:

    def __init__(self, db_path, purge_database=False):
        self.log = Logger(purge_database)
        self.db_path = db_path

        try:
            if os.path.exists(self.db_path):
                self.conn = sqlite3.connect(self.db_path)
                self.c = self.conn.cursor()
            else:
                self.conn = sqlite3.connect(self.db_path)
                self.log.enter_log("Database file created.")
                self.c = self.conn.cursor()
        except sqlite3.Error as er:
            self.log.enter_log("Error during creating database file:\n" + str(er))

        self.c = self.conn.cursor()

        try:
            if purge_database:
                self.c.execute("DROP TABLE IF EXISTS chat;")
                self.c.execute("DROP TABLE IF EXISTS list;")
                self.c.execute("DROP TABLE IF EXISTS list_item;")
                self.c.execute("DROP TABLE IF EXISTS scheduled_list_item;")
                self.log.enter_log("Tables dropped.")

            self.c.execute("CREATE TABLE IF NOT EXISTS chat (chat_id INTEGER PRIMARY KEY);")

            self.c.execute("""CREATE TABLE IF NOT EXISTS list (list_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            chat_id INTEGER NOT NULL, list_name TEXT NOT NULL, deletion_time DATETIME DEFAULT NULL);""")

            self.c.execute("""UPDATE sqlite_sequence SET seq = MAX(99, (COALESCE((SELECT MAX(list_id) FROM list), 99))) 
                            WHERE name = 'list';""")
            self.c.execute("""INSERT INTO sqlite_sequence (name,seq) SELECT 'list', 99 WHERE NOT EXISTS 
                            (SELECT changes() AS change FROM sqlite_sequence WHERE change <> 0);""")

            self.c.execute("""CREATE TABLE IF NOT EXISTS list_item(item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_id INTEGER NOT NULL, item_name INTEGER NOT NULL, deletion_time DATETIME DEFAULT NULL);""")

            self.c.execute("""UPDATE sqlite_sequence SET seq = 
            MAX(99, (COALESCE((SELECT MAX(item_id) FROM list_item), 99))) WHERE name = 'list_item';""")

            self.c.execute("""INSERT INTO sqlite_sequence (name, seq) SELECT 'list_item', 99 WHERE NOT EXISTS 
           (SELECT changes() AS change FROM sqlite_sequence WHERE change <> 0);""")

            self.c.execute("""CREATE TABLE IF NOT EXISTS scheduled_list_item (scheduled_item_id INTEGER PRIMARY KEY 
            AUTOINCREMENT, start_time DATETIME NOT NULL, setting_json TEXT);""")

            self.conn.commit()
            self.log.enter_log("Tables created.")
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during tables creation:\n" + str(er))

    def connect(self):
        self.log = Logger()
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.log.enter_log("Database connected.")

    def disconnect(self):
        self.conn.close()
        del self.conn
        del self.c
        self.log.enter_log("Database disconnected.")

    def create_backup(self, backup_folder_path):
        name = self.db_path.split('\\')[-1][:-3] + '_bck_' + time()
        if not os.path.exists(backup_folder_path + '\\' + name):
            try:
                copyfile(self.db_path, backup_folder_path + '\\' + name)
            except IOError as e:
                self.log.enter_log("Error during creating database backup:\n" + str(e))
            self.log.enter_log("Database backup created: " + name)
        else:
            self.log.enter_log("Error during creating database backup: file already exists.")

    def set_last_update_id(self, last_update_id):
        try:
            self.c.execute('UPDATE configuration SET value = ' + str(last_update_id) +
                           'WHERE name = "last_update_id" ').fetchone()[0]
        except sqlite3.Error as er:
            self.log.enter_log("Error during setting last update id:\n" + str(er))

    def get_list_of_lists(self, chat_id, deleted=False):
        if deleted:
            deleted = " deletion_time < (SELECT DATETIME('now'))"
        elif not deleted:
            deleted = " (deletion_time >= (SELECT DATETIME('now')) OR deletion_time IS NULL)"
        elif deleted is None:
            deleted = ' '
        else:
            raise Exception("Incorrect argument 'deleted'!")

        return self.c.execute("SELECT ROW_NUMBER() OVER(ORDER BY list_id) row_num, list_id, list_name FROM list WHERE" +
                              deleted + " AND chat_id = ? ORDER BY list_id", (chat_id,)).fetchall()

    def get_list_items_by_list_id(self, list_id, deleted=False):
        if deleted:
            deleted = " deletion_time < (SELECT DATETIME('now'))"
        elif not deleted:
            deleted = " (deletion_time >= (SELECT DATETIME('now')) OR deletion_time IS NULL)"
        elif deleted is None:
            deleted = ' '
        else:
            raise Exception("Incorrect argument 'deleted'!")
        try:
            return self.c.execute("""SELECT ROW_NUMBER() OVER(ORDER BY item_id) row_num, item_id, item_name FROM 
                                  list_item WHERE""" + deleted + """ AND list_id = ? ORDER BY item_id""",
                                  (list_id,)).fetchall()
        except sqlite3.Error as er:
            self.log.enter_log("Error during getting list items by list id:\n" + str(er))

    def get_list_items_by_position_number(self, position, ):
        pass