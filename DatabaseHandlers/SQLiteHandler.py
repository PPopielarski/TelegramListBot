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
                                    DROP TABLE IF EXISTS configuration;
                                    """)

            self.c.execute("""
            CREATE TABLE IF NOT EXISTS chat (chat_id INTEGER PRIMARY KEY);
            
            CREATE TABLE IF NOT EXISTS list (list_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            chat_id INTEGER NOT NULL, list_name TEXT NOT NULL, deletion_time DATETIME DEFAULT NULL);
                            
            UPDATE sqlite_sequence SET seq = MAX(99, (COALESCE((SELECT MAX(list_id) FROM list), 99))) 
            WHERE name = 'list';
            INSERT INTO sqlite_sequence (name,seq) SELECT 'list', 99 WHERE NOT EXISTS 
           (SELECT changes() AS change FROM sqlite_sequence WHERE change <> 0);
           
            CREATE TABLE IF NOT EXISTS list_item(item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_id INTEGER NOT NULL, item_name INTEGER NOT NULL, deletion_time DATETIME DEFAULT NULL,
            completion_time DATETIME DEFAULT NULL);
                            
            UPDATE sqlite_sequence SET seq = MAX(99, (COALESCE((SELECT MAX(item_id) FROM list_item), 99))) 
            WHERE name = 'list_item';
            INSERT INTO sqlite_sequence (name, seq) SELECT 'list_item', 99 WHERE NOT EXISTS 
           (SELECT changes() AS change FROM sqlite_sequence WHERE change <> 0);
           
            CREATE TABLE IF NOT EXISTS scheduled_list_item (scheduled_item_id INTEGER PRIMARY KEY 
            AUTOINCREMENT, list_id INTEGER NOT NULL, start_time DATETIME NOT NULL, setting_json TEXT);
            
            CREATE TABLE IF NOT EXISTS configuration (name TEXT NOT NULL, value TEXT);
            
            INSERT INTO configuration (name, value) VALUES ('GetUpdate_offset', Null);
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

    def get_list_of_lists(self, chat_id, deleted=False):
        if deleted:
            deleted = " deletion_time < (SELECT DATETIME('now'))"
        elif not deleted:
            deleted = " (deletion_time >= (SELECT DATETIME('now')) OR deletion_time IS NULL)"
        elif deleted is None:
            deleted = ' '
        else:
            raise Exception("Incorrect argument 'deleted'!")

        self.c.execute("SELECT ROW_NUMBER() OVER(ORDER BY list_id) row_num, list_id, list_name FROM list WHERE"
                       + deleted + " AND chat_id = ? ORDER BY list_id", (chat_id,)).fetchall()


