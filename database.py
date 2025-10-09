import sqlite3

# Підключення до бази
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Створення таблиці items
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
''')

# Додавання тестових записів
cursor.execute("INSERT INTO items (name) VALUES ('Купити хліб')")
cursor.execute("INSERT INTO items (name) VALUES ('Зробити домашнє')")
cursor.execute("INSERT INTO items (name) VALUES ('Прибрати кімнату')")

conn.commit()
conn.close()

print("✅ База даних створена і заповнена!")