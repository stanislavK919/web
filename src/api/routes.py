from flask import Blueprint, request, jsonify, render_template
from src.service.todo_service import TodoService
from src.api.dto import CreateTodoDto, UpdateTodoDto, ErrorResponse, ErrorDetail

api_bp = Blueprint('api', __name__)
service = TodoService()  # Підключаємо сервіс


# Допоміжна функція для помилок
def make_error(error, code, details=None, status=400):
    if details is None: details = []
    return jsonify(ErrorResponse(error, code, details).to_dict()), status


# --- HTML (Frontend) ---
@api_bp.route('/')
def index():
    return render_template('index.html')


# --- API Endpoints ---

@api_bp.route('/health', methods=['GET'])
def health():
    return "ok", 200


@api_bp.route('/todos', methods=['GET'])
def list_todos():
    return jsonify(service.get_all()), 200


@api_bp.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json() or {}
    if not data.get('title'):
        return make_error("ValidationError", "TITLE_REQUIRED",
                          [ErrorDetail("title", "Title is required")], 400)

    dto = CreateTodoDto.from_dict(data)
    return jsonify(service.create(dto)), 201


@api_bp.route('/todos/<string:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = service.get_by_id(todo_id)
    if not todo:
        return make_error("NotFoundError", "NOT_FOUND", status=404)
    return jsonify(todo), 200


@api_bp.route('/todos/<string:todo_id>', methods=['PATCH', 'PUT'])
def update_todo(todo_id):
    data = request.get_json() or {}
    dto = UpdateTodoDto.from_dict(data)
    updated = service.update(todo_id, dto)
    if not updated:
        return make_error("NotFoundError", "NOT_FOUND", status=404)
    return jsonify(updated), 200


@api_bp.route('/todos/<string:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if service.delete(todo_id):
        return '', 204
    return make_error("NotFoundError", "NOT_FOUND", status=404)