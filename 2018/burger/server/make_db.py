import sqlite3

conn = sqlite3.connect('../data/server.db')
cursor = conn.cursor()

try:
    s = '''CREATE TABLE votes (timestamp DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), burger CHARACTER(6), vote BOOLEAN)'''
    print(s)
    cursor.execute(s)
except sqlite3.OperationalError as e:
    print("failed to create table", e)
    pass
