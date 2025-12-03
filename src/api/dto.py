from dataclasses import dataclass, asdict
from typing import Optional, List

# --- Що ми очікуємо від клієнта (Requests) ---
@dataclass
class CreateTodoDto:
    title: str
    priority: str = 'normal'
    due_date: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'CreateTodoDto':
        return CreateTodoDto(
            title=data.get('title'),
            priority=data.get('priority', 'normal'),
            due_date=data.get('dueDate') # camelCase з фронта -> snake_case в пайтон
        )

@dataclass
class UpdateTodoDto:
    title: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    is_completed: Optional[bool] = None

    @staticmethod
    def from_dict(data: dict) -> 'UpdateTodoDto':
        return UpdateTodoDto(
            title=data.get('title'),
            priority=data.get('priority'),
            due_date=data.get('dueDate'),
            is_completed=data.get('isCompleted')
        )

# --- Як виглядає помилка (Standard Error) ---
@dataclass
class ErrorDetail:
    field: str
    message: str

@dataclass
class ErrorResponse:
    error: str
    code: str
    details: List[ErrorDetail]

    def to_dict(self):
        return {
            "error": self.error,
            "code": self.code,
            "details": [asdict(d) for d in self.details]
        }