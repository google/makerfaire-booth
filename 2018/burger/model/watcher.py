import time
import datetime
import sqlite3

conn = sqlite3.connect('../data/server.db')
cursor = conn.cursor()

cursor.execute('''SELECT * FROM votes ORDER BY timestamp''')
results = cursor.fetchall()
print(results)
last = datetime.datetime.utcnow()
while True:
    s = '''SELECT datetime(timestamp), burger, vote FROM votes WHERE datetime(timestamp) > datetime(?) ORDER BY timestamp'''
    cursor.execute(s, [last.isoformat()])
    results = cursor.fetchall()
    print(results)
    last = datetime.datetime.utcnow()
    time.sleep(1)
