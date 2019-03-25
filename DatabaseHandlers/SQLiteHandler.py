import sqlite3
import os.path
from DatabaseHandlers.DBLogger import Logger


class SQLiteHandler:

    conn = None
    c = None
    log = None

    def __init__(self, purge_database=False):
        """Provides functions to create SQLite database, create tables, insert, update and select data."""
        self.log = Logger(purge_database)
        self.__create_database()
        self.c = self.conn.cursor()
        self.__create_tables(purge_database)

    def __create_tables(self, drop_if_exists=False):
        """Creates tables, if they already exist it drops them before."""
        try:
            if drop_if_exists:
                self.c.execute("""  DROP TABLE IF EXISTS chat;
                                    DROP TABLE IF EXISTS list;
                                    DROP TABLE IF EXISTS list_item;
                                    DROP TABLE IF EXISTS scheduled_list_item;
                                    DROP TABLE IF EXISTS configuration;""")

            self.c.execute("""
            CREATE TABLE IF NOT EXISTS chat (chat_id INTEGER PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS list (list_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            chat_id INTEGER NOT NULL, list_name TEXT NOT NULL, deletion_time DATETIME DEFAULT NULL);
            CREATE TABLE IF NOT EXISTS list_item(item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            list_id INTEGER NOT NULL, item_name INTEGER NOT NULL, 
                            deletion_time DATETIME DEFAULT NULL);
            CREATE TABLE IF NOT EXISTS scheduled_list_item (scheduled_item_id INTEGER PRIMARY KEY 
            AUTOINCREMENT, list_id INTEGER NOT NULL, start_time DATETIME NOT NULL, setting_json TEXT);
            CREATE TABLE IF NOT EXISTS configuration (name TEXT NOT NULL, value TEXT);
            INSERT INTO configuration (name, value) VALUES ('GetUpdate_offset', Null);
            CREATE VIEW IF NOT EXISTS numbered_item_list AS select 
            item_id, list_id, item_name, deletion_time, ROW_NUMBER() OVER(ORDER BY item_id) row_num from list_item;
            CREATE VIEW IF NOT EXISTS numbered_list AS select 
            list_id, chat_id, list_name, deletion_time, ROW_NUMBER() OVER(ORDER BY list_id) row_num from list;
            """)
            self.conn.commit()
            self.log.enter_log("Tables created.")
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during tables creation:\n" + str(er))

    def __create_database(self):
        """Connects to database. If necessary it creates it before."""
        try:
            if os.path.exists('list_bot_db.db'):
                self.conn = sqlite3.connect('list_bot_db.db')
                self.c = self.conn.cursor()
            else:
                self.conn = sqlite3.connect('list_bot_db.db')
                self.log.enter_log("Database file created.")
                self.c = self.conn.cursor()
        except sqlite3.Error as er:
            self.log.enter_log("Error during connecting to database:\n" + str(er))

    def add_list(self, chat_id, list_name, deletion_time=None):
        self.c.execute('''INSERT INTO list (chat_id, list_num, list_name) values (?, (SELECT MAX(list_num) + 1 FROM list 
                        WHERE list.chat_id = ''' + str(chat_id) + ') ,?)', (chat_id, list_name))
        try:
            if int(self.c.execute("SELECT EXISTS (SELECT COUNT(1) FROM list WHERE chat_id = ? LIMIT 1)",
                                  (chat_id,)).fetchone()[0]) > 0:
                return False
            self.c.execute("insert into list (chat_id, list_name) values(?, ?)", (chat_id, list_name))
            self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during adding new list (chat_id = "+str(chat_id)+", list_name ="+list_name+"):\n"
                               + str(er))
