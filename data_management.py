import sqlite3
import pandas as pd

file_path = 'order_history.csv'
data = pd.read_csv(file_path)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS order_history (
    odate CHAR(10),
    ouser CHAR(7),
    osymbol VARCHAR(30),
    oon VARCHAR(30),
    ostatus VARCHAR(30),
    obp FLOAT,
    oltp FLOAT,
    oquantity INT,
    ocon VARCHAR(30),
    ocostatus VARCHAR(30),
    ollstatus CHAR(3)
)
''')

data.to_sql('order_history', conn, if_exists='append', index=False)

conn.commit()
conn.close()
