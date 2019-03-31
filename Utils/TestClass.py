from DatabaseHandlers import SQLiteHandler
from ListBot import Chat, Config, CommandHandler
import sqlite3

db = SQLiteHandler.SQLiteHandler(Config.sqlite_db_path)
db.conn.set_trace_callback(print)

deleted = " (deletion_time >= (SELECT DATETIME('now')) OR deletion_time IS NULL) AND "
chat_id = 139257826
db.c.execute("UPDATE list SET deletion_time = NULL WHERE chat_id = ?", (1,)).fetchall()
x = db.c.execute("SELECT CHANGES()").fetchall()

for i in x:
    print(str(i))
