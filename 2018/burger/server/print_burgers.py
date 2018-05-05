import sqlite3

conn = sqlite3.connect('server.db')
c = conn.cursor()
c.execute("SELECT layer0, layer1, layer2, layer3, layer4, layer5 FROM labels, layers WHERE labels.output = 1 AND labels.burger = layers.burger")
results = c.fetchall()
for i in range(len(results)):
    result = results[i]
    print("[%d,%d,%d,%d,%d,%d]" % result, end=',\n' if i < len(results)-1 else '\n')
