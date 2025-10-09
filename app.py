from flask import Flask, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # дозволяє JS звертатись до API

# Функція для отримання всіх записів із бази
def get_items():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1]} for row in rows]

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint для отримання списку
@app.route('/items', methods=['GET'])
def items():
    return jsonify(get_items())

if __name__ == '__main__':
    app.run(debug=True)