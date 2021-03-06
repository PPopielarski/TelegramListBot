import sqlite3
import os.path

import time
from shutil import copyfile

# TODO implement new database schema: new constructor and new queries.


class SQLiteHandler:

    def __init__(self, db_path, log_handler=None, purge_database=False):
        self.log_handler = log_handler
        self.db_path = db_path

        try:
            if os.path.exists(self.db_path):
                self.__create_log("Database file found.")
                self.conn = sqlite3.connect(self.db_path)
                self.c = self.conn.cursor()
            else:
                self.conn = sqlite3.connect(self.db_path)
                self.__create_log("Database file created.")
                self.c = self.conn.cursor()
        except sqlite3.Error as er:
            self.__create_log("Error during creating database file:\n" + str(er))

        try:
            if purge_database:
                self.c.execute("DROP TABLE IF EXISTS chat;")
                self.c.execute("DROP TABLE IF EXISTS list;")
                self.c.execute("DROP TABLE IF EXISTS list_item;")
                self.c.execute("DROP TABLE IF EXISTS scheduled_list_item;")
                self.__create_log("Tables dropped.")

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
            self.__create_log("Tables created.")
        except sqlite3.Error as er:
            self.conn.rollback()
            self.__create_log("Error during tables creation:\n" + str(er))

    def __create_log(self, log):
        if self.log_handler is not None:
            self.log_handler.enter_log(log)

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.__create_log("Database connected.")

    def disconnect(self):
        self.conn.close()
        del self.conn
        del self.c
        self.__create_log("Database disconnected.")

    def create_backup(self, backup_folder_path):
        name = self.db_path.split('\\')[-1][:-3] + '_bck_' + time.time()
        if not os.path.exists(backup_folder_path + '\\' + name):
            try:
                copyfile(self.db_path, backup_folder_path + '\\' + name)
            except IOError as e:
                self.__create_log("Error during creating database backup:\n" + str(e))
                self.__create_log("Database backup created: " + name)
        else:
            self.__create_log("Error during creating database backup: file already exists.")

    def add_list(self, chat_id, list_name):
        try:
            self.c.execute("INSERT INTO list (chat_id, list_name) VALUES (?,?)", (chat_id, list_name))
            self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.__create_log("Error during inserting new list (chat_id = " + chat_id + ", list_name = " + list_name +
                              "):\n" + str(er))

    def delete_list_by_id(self, chat_id, list_id):
        try:
            self.c.execute("""UPDATE list SET deletion_time = (SELECT DATETIME('now')) WHERE list_id = ? 
                           AND (deletion_time >= (SELECT DATETIME('now')) OR deletion_time IS NULL)""", (list_id,))
            if self.c.execute("SELECT CHANGES()").fetchone()[0] == 0:
                return False
            self.c.execute("""UPDATE list_item SET deletion_time = (SELECT DATETIME('now')) WHERE list_id = ? AND 
            (deletion_time >= (SELECT DATETIME('now')) OR deletion_time IS NULL)""", (list_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as er:
            self.conn.rollback()
            self.__create_log("Error during inserting deletion_time for list (list_id = " + str(list_id) +
                              ", chat_id = " + chat_id + "):\n" + str(er))
            return False

    def delete_list_by_position(self, chat_id, position):
        try:
            list_id = self.c.execute("""WITH temp AS (SELECT list_id FROM list WHERE chat_id = ? AND 
            (deletion_time IS NULL OR deletion_time >= (SELECT DATETIME('now'))))
            SELECT list_id FROM
            (SELECT list_id, (select count(1) from temp b where a.list_id >= b.list_id) row_num from temp a)
            WHERE row_num = ?""", (chat_id, position)).fetchone()
            if len(list_id) == 0:
                return False
            list_id = list_id[0]
            self.c.execute("UPDATE list SET deletion_time = (SELECT DATETIME('now')) WHERE list_id = ?", list_id)
            self.c.execute("UPDATE list_item SET deletion_time = (SELECT DATETIME('now')) WHERE list_id = ?", list_id)
            self.conn.commit()
            return True
        except sqlite3.Error as er:
            self.conn.rollback()
            self.__create_log("Error during updating deletion_time to lists position (position =" + str(position) +
                              ", chat_id = " + chat_id + "):\n" + str(er))
            return False

    def delete_list_by_name(self, chat_id, name):
        try:
            list_id = self.c.execute("""SELECT list_id from list 
                                    WHERE list_name = ? and chat_id = ?""", (name, chat_id)).fetchone()
            if len(list_id) == 0:
                return False
            return self.delete_list_by_id(chat_id, list_id[0])
        except sqlite3.Error as er:
            self.__create_log("Error during inserting deletion_time for list (list_name = " + str(name) +
                              ", chat_id = " + chat_id + "):\n" + str(er))
            return False

    def get_list_id_by_name(self, chat_id, list_name):
        try:
            return self.c.execute("""SELECT list_id from list 
                                                WHERE list_name = ? and chat_id = ?""", (list_name, chat_id)).fetchall()
        except sqlite3.Error as er:
            self.__create_log("Error during selecting list_id by name (list_name = " + str(list_name) +
                              ", chat_id = " + chat_id + "):\n" + str(er))

    def get_list_of_lists(self, chat_id, deleted=False):
        if deleted:
            deleted = " deletion_time < (SELECT DATETIME('now')) AND "
        elif not deleted:
            deleted = " (deletion_time >= (SELECT DATETIME('now')) OR deletion_time IS NULL) AND "
        elif deleted is None:
            deleted = ' '
        else:
            raise Exception("Incorrect argument 'deleted'!")
        try:
            return self.c.execute("""SELECT list_id, list_name, (select count(1) from list b where a.list_id >= 
                                  b.list_id) row_num FROM list a WHERE """ + deleted
                                  + " chat_id = ? ORDER BY deletion_time, list_id", (chat_id,)).fetchall()
        except sqlite3.Error as er:
            self.__create_log("Error during selecting list of lists (chat_id = " + str(chat_id) + "):\n" + str(er))

    def get_list_items_by_list_id(self, list_id, deleted=False):
        if deleted:
            deleted = " deletion_time < (SELECT DATETIME('now')) AND"
        elif not deleted:
            deleted = " (deletion_time >= (SELECT DATETIME('now')) OR deletion_time IS NULL) AND"
        elif deleted is None:
            deleted = ' '
        else:
            raise Exception("Incorrect argument 'deleted'!")
        try:
            return self.c.execute("""SELECT ROW_NUMBER() OVER(ORDER BY item_id) row_num, item_id, item_name FROM 
                                  list_item WHERE? AND list_id = ? ORDER BY item_id""",
                                  (deleted, list_id)).fetchall()
        except sqlite3.Error as er:
            self.__create_log("Error during getting list items by list id:\n" + str(er))
