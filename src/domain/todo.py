from dataclasses import dataclass
from typing import Optional

@dataclass
class Todo:
    id: str
    title: str
    priority: str = "normal"
    is_completed: bool = False
    due_date: Optional[str] = None