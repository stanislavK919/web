# src/app.py
from flask import Flask
from flask_cors import CORS
from src.api.routes import api_bp  # <-- Імпортуємо наш Blueprint (де живуть нові роути)


def create_app():
    # template_folder='../templates' вказує Flask шукати HTML у папці templates/,
    # яка знаходиться поруч із папкою src/, а не всередині неї.
    app = Flask(__name__, template_folder='../templates')

    # Дозволяємо запити з інших доменів (як було у вас раніше)
    CORS(app)

    # Реєструємо Blueprint. Це підключає всі маршрути (/todos, /health) до додатка.
    app.register_blueprint(api_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    # Запускаємо сервер на порту 8080 (або 5000 за замовчуванням)
    app.run(debug=True, port=8080)