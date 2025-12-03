import sqlite3


conn = sqlite3.connect('../todo.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT)')

cursor.execute("INSERT INTO items (name) VALUES ('Купити хліб')")
cursor.execute("INSERT INTO items (name) VALUES ('Зробити домашнє')")
cursor.execute("INSERT INTO items (name) VALUES ('Прибрати кімнату')")

conn.commit()
conn.close()

print("База даних створена")