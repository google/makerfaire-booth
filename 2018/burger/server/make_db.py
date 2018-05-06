import sqlite3
import pandas

conn = sqlite3.connect('server.db')
cursor = conn.cursor()

df = pandas.read_hdf('../machine/data.h5', 'df')

layers = df[['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']]
layers.to_sql('layers', conn, index_label='burger', if_exists='replace')

labels = df['output']
labels.to_sql('labels', conn, index_label='burger', if_exists='replace')


try:
    cursor.execute('''CREATE TABLE votes (burger CHARACTER(6), vote BOOLEAN)''')
except sqlite3.OperationalError as e:
    print("failed to create table", e)
    pass
