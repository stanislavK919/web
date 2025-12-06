import sqlite3
import uuid
from src.api.dto import CreateTodoDto, UpdateTodoDto

class TodoService:
    def __init__(self):
        self.db_name = 'todo.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                priority TEXT,
                is_completed BOOLEAN,
                due_date TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_all(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_by_id(self, todo_id: str):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def create(self, dto: CreateTodoDto):
        new_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (id, title, priority, is_completed, due_date) VALUES (?, ?, ?, ?, ?)",
            (new_id, dto.title, dto.priority, False, dto.due_date)
        )
        conn.commit()
        conn.close()
        return self.get_by_id(new_id)

    def update(self, todo_id: str, dto: UpdateTodoDto):
        current = self.get_by_id(todo_id)
        if not current:
            return None

        fields = []
        values = []
        if dto.title is not None:
            fields.append("title = ?")
            values.append(dto.title)
        if dto.priority is not None:
            fields.append("priority = ?")
            values.append(dto.priority)
        if dto.is_completed is not None:
            fields.append("is_completed = ?")
            values.append(dto.is_completed)
        if dto.due_date is not None:
            fields.append("due_date = ?")
            values.append(dto.due_date)

        if not fields:
            return current

        values.append(todo_id)
        query = f"UPDATE todos SET {', '.join(fields)} WHERE id = ?"

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return self.get_by_id(todo_id)

    def delete(self, todo_id: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted_count > 0