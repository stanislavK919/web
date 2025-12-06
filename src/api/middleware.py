import time
import uuid
import random
from flask import request, g, jsonify, make_response
from functools import wraps

IDEMPOTENCY_STORE = {}
RATE_LIMIT_STORE = {}

# Налаштування
WINDOW_SEC = 10
MAX_REQ = 5
RETRY_AFTER = 5


def generate_request_id():
    rid = request.headers.get('X-Request-Id') or str(uuid.uuid4())
    g.request_id = rid
    return rid


def unified_error(error_type, code, details=None, status=400):
    return jsonify({
        "error": error_type,
        "code": code,
        "details": details,
        "requestId": getattr(g, 'request_id', 'unknown')
    }), status



def rate_limiter(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.remote_addr
        now = time.time()

        record = RATE_LIMIT_STORE.get(ip, {'count': 0, 'start_time': now})

        if now - record['start_time'] > WINDOW_SEC:
            record = {'count': 1, 'start_time': now}
        else:
            record['count'] += 1

        RATE_LIMIT_STORE[ip] = record

        if record['count'] > MAX_REQ:
            response = unified_error("too_many_requests", "RATE_LIMIT_EXCEEDED", "Try again later", 429)[0]
            response.headers['Retry-After'] = RETRY_AFTER
            return response, 429

        return f(*args, **kwargs)

    return decorated_function


def idempotent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('Idempotency-Key')
        if not key:
            return unified_error("validation_error", "IDEMPOTENCY_KEY_MISSING", "Header Idempotency-Key is required",
                                 400)

        if key in IDEMPOTENCY_STORE:
            cached = IDEMPOTENCY_STORE[key]
            print(f"[{g.request_id}] Returning cached response for key {key}")
            response = make_response(jsonify({**cached['body'], "cached": True}), cached['status'])
            return response

        response_tuple = f(*args, **kwargs)

        data, status = response_tuple

        if 200 <= status < 300:
            IDEMPOTENCY_STORE[key] = {
                'body': data.json if hasattr(data, 'json') else data,
                'status': status
            }

        return response_tuple

    return decorated_function


def chaos_monkey(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = random.random()

        if r < 0.15:
            delay = 1.5 + random.random()
            print(f"[{g.request_id}] 🐢 Chaos: Simulating delay {delay:.2f}s")
            time.sleep(delay)

        if r > 0.90:
            print(f"[{g.request_id}] 💥 Chaos: Simulating 503 error")
            return unified_error("service_unavailable", "CHAOS_ERROR", "Simulated failure", 503)

        return f(*args, **kwargs)

    return decorated_function