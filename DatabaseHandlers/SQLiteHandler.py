import sqlite3
import os.path
from DatabaseHandlers.DBLogger import Logger
import re


class SQLiteHandler:

    conn = None
    c = None
    log = None

    def __init__(self, purge_database=False):
        """Provides functions to create SQLite database, create tables, insert, update and select data."""
        self.log = Logger(purge_database)
        self.start()
        self.c = self.conn.cursor()
        self.__create_tables(purge_database)
        self.c.close()

    def __create_tables(self, drop_if_exists=False):
        """Creates tables, if they already exist it drops them before."""
        try:
            existing_tables = self.c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

            if drop_if_exists:
                self.c.execute('''drop table if exists chat''')
                self.c.execute('''drop table if exists list''')
                self.c.execute('''drop table if exists task''')
                self.c.execute('''drop table if exists scheduled_task''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS chat(chat_id INTEGER PRIMARY KEY, 
                              message_id integer not null)''')
            self.c.execute('''CREATE TABLE IF NOT EXISTS list(list_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         chat_id integer not null, list_name text not null)''')
            self.c.execute('''CREATE TABLE IF NOT EXISTS task(task_id INTEGER PRIMARY KEY AUTOINCREMENT, list_id integer 
                                not null, task_name text not null, deletion_time DATETIME DEFAULT NULL)''')
            self.c.execute('''CREATE TABLE IF NOT EXISTS scheduled_task(scheduled_task_id INTEGER PRIMARY KEY 
                            AUTOINCREMENT, list_id integer, start_time DATETIME, setting_json text)''')
            self.c.execute('''CREATE TABLE IF NOT EXISTS configuration(name text not null, value text''')
            self.c.execute("insert into configuration (name, value) values(?, ?)", ('GetUpdate_offset', None))

            if len(existing_tables) > 0:
                self.log.enter_log("Tables creation.\nTables existing before operation (" + re.sub('[' +
                                   re.escape('[](),') + ']', '', str(existing_tables)).replace("' ", "', ") +
                                   (") were dropped." if drop_if_exists else ") were not dropped.") +
                                   "\nExisting tables now: " + re.sub('[' + re.escape('[](),') + ']', '', str(
                                    self.c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())))
            else:
                self.log.enter_log("Tables created: " + re.sub('[' + re.escape('[](),') + ']', '',
                                   str(self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
                                   .fetchall())).replace("' ", "', "))
            self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during tables creation:\n" + str(er))

    def start(self):
        """Connects to database. If necessary it creates it before."""
        try:
            if os.path.exists('smarttodo.db'):
                self.conn = sqlite3.connect('smarttodo.db')
                self.c = self.conn.cursor()
            else:
                self.conn = sqlite3.connect('smarttodo.db')
                self.log.enter_log("database created")
                self.c = self.conn.cursor()
            return True
        except sqlite3.Error as er:
            self.log.enter_log("Error during connecting to database:\n" + str(er))
            return False

    def add_chat(self, chat_id, message_id, commit=False):
        try:
            self.c.execute("insert into chat (chat_id, message_id) values(?, ?)", (chat_id, message_id))
            if commit is True:
                self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during adding new chat (chat_id = "+str(chat_id)+", message_id = "+str(message_id)
                               + "):\n" + str(er))

    def delete_chat(self, chat_id, commit=False):
        try:
            self.c.execute("DELETE FROM task WHERE list_id IN (SELECT list_id FROM list WHERE chat_id = ?)", (chat_id,))
            self.c.execute("DELETE FROM list WHERE chat_id = ?", (chat_id,))
            self.c.execute("DELETE FROM chat WHERE chat_id = ?", (chat_id,))
            if commit is True:
                self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during deleting chat (chat_id = " + str(chat_id) + "):\n" + str(er))

    def check_chat_existence(self, chat_id):
        return True if self.c.execute("SELECT EXISTS (SELECT 1 FROM chat WHERE chat_id = ? LIMIT 1)", chat_id) \
                                      .fetchone()[0] > 0 else False

    def add_list(self, chat_id, list_name, commit=False):
        """Adds task list for specified chat.
        If there already are list with this name the function returns False and adds no list."""
        try:
            if int(self.c.execute("SELECT EXISTS (SELECT COUNT(1) FROM list WHERE chat_id = ? LIMIT 1)",
                                  (chat_id,)).fetchone()[0]) > 0:
                return False
            self.c.execute("insert into list (chat_id, list_name) values(?, ?)", (chat_id, list_name))
            if commit is True:
                self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during adding new list (chat_id = "+str(chat_id)+", list_name ="+list_name+"):\n"
                               + str(er))

    def select_from_list_tab(self, select_list_id=False, select_chat_id=False, select_list_name=False,
                             where_list_id=None, where_chat_id=None, where_list_name=None):
        """Performs select clause on list table. Selected data is specified by parameters."""
        select = []
        if select_list_id:
            select.append('list.list_id')
        if select_chat_id:
            select.append('list.chat_id')
        if select_list_name:
            select.append('list.list_name')
        if len(select) == 0:
            raise Exception('No values in SELECT list.')
        select = ', '.join(select)
        where = []
        if where_list_id:
            where.append('list.list_id = ' + str(where_list_id))
        if where_chat_id:
            where.append('list.chat_id = ' + str(where_chat_id))
        if where_list_name:
            where.append('list.list_name = ' + str(where_list_name))
        where = 'AND '.join(where)
        try:
            return self.c.execute("SELECT " + select + " FROM list WHERE " + where).fetchall()
        except sqlite3.Error as er:
            self.log.enter_log("Error during selecting lists ( " + str(select) + ") where (" + where + "):\n" + str(er))
            return None

    def add_item_by_list_id(self, task_name, list_id, deletion_time=None, commit=False):
        try:
            self.c.execute("insert into task (list_id, task_name, deletion_time) values(?,?,?)",
                           (list_id, task_name, deletion_time))
            if commit is True:
                self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during adding new task (list_id = " + str(list_id) + ", task_name = " + task_name
                               + ", deletion_time = "+str(deletion_time) + "):\n" + str(er))

    def add_item_by_chat_id_and_list_name(self, task_name, chat_id, list_name, deletion_time=None, commit=False):
        try:
            self.add_item_by_list_id(task_name, self.c.execute('''SELECT list.list_id FROM list WHERE list.chat_id 
                                     = ? AND list.list_name = ? LIMIT 1''', (chat_id, list_name)).fetchone()[0],
                                     deletion_time, commit)
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during adding new task (chat_id = " + str(chat_id) + ", task_name = " + task_name
                               + ", list_name = " + list_name + ", deletion_time = " + str(deletion_time) + "):\n"
                               + str(er))

    def update_chat_message_id(self, chat_id, new_message_id, commit=False):
        try:
            self.c.execute("UPDATE chat SET message_id = ? WHERE chat_id = ?", (new_message_id, chat_id))
            if commit is True:
                self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during updating message_id in chat tab (chat_id = " + str(chat_id) +
                               ", new_message_id =" + str(new_message_id) + "):\n" + str(er))

    def update_list_name(self, list_id, new_name, commit=False):
        """Update tasks name and returns True if the operation was successful.
        Name of the list must be unique for one chat."""
        try:
            if self.c.execute("""SELECT EXISTS (SELECT COUNT(1) FROM list WHERE list_name = ? and chat_id = 
            (SELECT chat_id FROM list WHERE list_id = ? LIMIT 1))""", (new_name, list_id)).fetchone()[0] > 0:
                return False
            self.c.execute("UPDATE list SET list_name = ? WHERE list_id = ?", (new_name, list_id))
            if commit is True:
                self.conn.commit()
            return True
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during updating list_name in list tab (list_id = " + str(list_id) +
                               ", new_name =" + new_name + "):\n" + str(er))
            return False

    def update_item_name(self, task_id, new_name, commit=False):
        """Update tasks name and returns True if the operation was successful."""
        try:
            self.c.execute("UPDATE list_item SET list_item_name = ? WHERE list_id = ?", (new_name, task_id))
            if commit is True:
                self.conn.commit()
            return True
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during updating task_name in TASK tab (list_id = " + str(task_id) +
                               ", new_name =" + new_name + "):\n" + str(er))
            return False

    def delete_task(self, task_id, commit=False):
        try:
            self.c.execute("DELETE FROM TASK WHERE task_id = ?", (task_id,))
            if commit is True:
                self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during deleting task (task_id = " + str(task_id) + "):\n" + str(er))

    def delete_list(self, list_id=None, list_name=None, chat_id=None, commit=False):
        try:
            if list_name is not None and chat_id is not None and list_id is None:
                list_id = "(SELECT list.list_id FROM list WHERE list.chat_id = " + str(chat_id) + " AND list.name = '" \
                          + list_name + "')"
            elif not (list_id is not None and list_name is None and chat_id is None):
                raise Exception("Incorrect input:" + (' list_id set' if list_id is not None else '') +
                                (' list_name set' if list_name is not None else '') +
                                (' chat_id set' if chat_id is not None else ''))
            self.c.execute("delete from task where list_id = ?", (list_id,))
            self.c.execute("delete from list where list_id = ?", (list_id,))
            self.c.execute("delete from scheduled_task where list_id = ?", (list_id,))
            if commit is True:
                self.conn.commit()
        except sqlite3.Error as er:
            self.conn.rollback()
            self.log.enter_log("Error during deleting list (list_id = " + str(list_id) + "):\n" + str(er))

    def select_task_names(self, chat_id=None, list_id=None, task_id=None, is_deleted=None):
        """Selects tasks specified by chet_id, list_id, task_id and conditions is_scheduled and has_cron_string"""
        try:
            where = ""
            if chat_id is not None:
                where += " AND list.chat_id =" + str(chat_id)
            if list_id is not None:
                where += " AND task.list_id =" + str(list_id)
            if task_id is not None:
                where += " AND task.task_id =" + str(task_id)
            if is_deleted is True:
                where += " AND task.deletion_time <= date('now')"
            elif is_deleted is False:
                where += " AND (task.deletion_time IS NULL OR task.deletion_time > date('now'))"
            sel = self.c.execute("""SELECT task.task_name FROM list, task 
                                 WHERE list.list_id = task.list_id"""+where).fetchall()
        except sqlite3.Error as er:
            lo = ""
            if chat_id is not None:
                lo += "chat_id = " + str(chat_id)
            if list_id is not None:
                lo += " list_id = " + str(list_id)
            if task_id is not None:
                lo += " task_id = " + str(task_id)
            if list_id is not None:
                lo += " is_deleted = " + str(is_deleted)
            if lo == "":
                lo = "empty where"
            self.log.enter_log("Error during selecting tasks (" + str(lo.strip) + "):\n" + str(er))
            return False
        return sel

    def set_get_update_offset_value(self, value):
        try:
            self.c.execute("UPDATE configuration SET value = ? WHERE name = 'GetUpdate_offset'", value)
        except sqlite3.Error as er:
            self.log.enter_log("Error during updating GetUpdate_offset:\n" + str(er))
            return False

    def get_get_update_offset_value(self):
        try:
            return self.c.execute("Select value FROM configuration WHERE name = 'GetUpdate_offset'").fetchall()[0]
        except sqlite3.Error as er:
            self.log.enter_log("Error during selecting GetUpdate_offset:\n" + str(er))
            return None
