import sqlite3
import os.path
from ListBot.Logger import Logger
from ListBot import Config


class SQLiteHandler:

    def __init__(self, purge_database=False):
        self.log = Logger(purge_database)

        try:
            if os.path.exists(Config.sqlite_db_path):
                self.conn = sqlite3.connect(Config.sqlite_db_path)
                self.c = self.conn.cursor()
            else:
                self.conn = sqlite3.connect(Config.sqlite_db_path)
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
                self.c.execute("DROP TABLE IF EXISTS configuration;")
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

            self.c.execute("CREATE TABLE IF NOT EXISTS configuration (name TEXT NOT NULL, value TEXT);")

            self.c.execute("INSERT INTO configuration (name, value) VALUES ('last_update_id', Null);")

            self.conn.commit()
            self.log.enter_log("Tables created.")
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during tables creation:\n" + str(er))

    def connect(self):
        self.log = Logger()
        self.conn = sqlite3.connect(Config.sqlite_db_path)
        self.c = self.conn.cursor()
        self.log.enter_log("Database connected.")

    def disconnect(self):
        del self.c
        self.conn.close()
        del self.conn
        self.log.enter_log("Database disconnected.")

    def get_last_update_id(self):
        try:
            res = self.c.execute('SELECT value FROM configuration WHERE name = "last_update_id" ').fetchone()
            if len(res) == 1:
                return int(res)
            else:
                return None
        except sqlite3.Error as er:
            self.log.enter_log("Error during reading last update id:\n" + str(er))
            return None

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