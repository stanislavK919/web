from flask import Flask, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_items():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1]} for row in rows]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def items():
    return jsonify(get_items())

if __name__ == '__main__':
    app.run(debug=True)