import sqlite3

conn = sqlite3.connect('server.db')
c = conn.cursor()
c.execute("SELECT COUNT(votes.burger) FROM votes, labels WHERE votes.burger = labels.burger AND labels.output = 1")
# c.execute("SELECT votes.burger, votes.vote, labels.output AS c FROM votes, labels WHERE votes.burger = labels.burger and votes.vote != labels.output")
print(c.fetchall())
