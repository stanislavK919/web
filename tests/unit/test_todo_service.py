import unittest
from src.service.todo_service import TodoService
from src.api.dto import CreateTodoDto, UpdateTodoDto


class TestTodoService(unittest.TestCase):

    def setUp(self):
        self.service = TodoService()
        self.service.db_name = ':memory:'
        self.service._init_db()

    def test_create_todo_success(self):
        dto = CreateTodoDto(title="Test Unit", priority="high")
        result = self.service.create(dto)

        self.assertIsNotNone(result)
        self.assertEqual(result['title'], "Test Unit")
        self.assertIn('id', result)

    def test_get_non_existent_todo(self):
        result = self.service.get_by_id("fake-id-999")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()