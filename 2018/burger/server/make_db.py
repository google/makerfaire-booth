import sqlite3
import pandas

conn = sqlite3.connect('server.db')
cursor = conn.cursor()

try:
    cursor.execute('''CREATE TABLE votes (burger CHARACTER(6), vote BOOLEAN)''')
except sqlite3.OperationalError as e:
    print("failed to create table", e)
    pass
