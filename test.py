import sqlite3
from datetime import datetime

conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute(''' CREATE TABLE IF NOT EXISTS date (
            id INTEGER,
            time TIMESTAMP
        );''')

c.execute("INSERT INTO date('id', 'time') VALUES (?, ?)", (1, datetime.now()))

c.execute("SELECT * FROM date where id=1 ", {'user_id':2})

message = c.fetchone()

print(message)

c.close()