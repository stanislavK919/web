from flask import Blueprint, jsonify, request, g, render_template
import time
from src.api.middleware import generate_request_id, rate_limiter, idempotent, chaos_monkey, unified_error
from src.service.todo_service import TodoService
from src.api.dto import CreateTodoDto

api_bp = Blueprint('api', __name__)
service = TodoService()


@api_bp.before_request
def before_request():
    generate_request_id()


@api_bp.after_request
def after_request(response):
    response.headers['X-Request-Id'] = g.request_id
    return response


@api_bp.route('/')
def index():
    return render_template('index.html')


@api_bp.route('/health')
def health():
    delay = request.args.get('delay', type=int)
    if delay:
        time.sleep(delay)
    return jsonify({"status": "ok"})


@api_bp.route('/todos', methods=['POST'])
@rate_limiter
@chaos_monkey
@idempotent
def create_todo():
    data = request.get_json() or {}

    if not data.get('title'):
        return unified_error("validation_error", "TITLE_REQUIRED", "Title is required", 400)

    try:
        dto = CreateTodoDto.from_dict(data)
        result = service.create(dto)

        result['requestId'] = g.request_id
        return jsonify(result), 201
    except Exception as e:
        return unified_error("internal_error", "SERVER_ERROR", str(e), 500)