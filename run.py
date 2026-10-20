import os
import datetime
from functools import wraps
from flask import Flask, jsonify, request
from flasgger import Swagger
import pymysql
import jwt

app = Flask(__name__)

# Секретний ключ для підпису JWT
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-key-123')
app.config['SECRET_KEY'] = SECRET_KEY

# Конфігурація Swagger з підтримкою Bearer Token
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda model: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "specs_route": "/apidocs/"
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "Kindergartens REST API",
        "description": "API з JWT-автентифікацією для управління дитячими садками",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Введіть токен у форматі: Bearer <ваш_JWT_токен>"
        }
    }
}

swagger = Swagger(app, config=swagger_config, template=template)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME', 'kindergartens'),
        cursorclass=pymysql.cursors.DictCursor
    )

# Декоратор для перевірки JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Токен відсутній!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Термін дії токена закінчився!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Недійсний токен!'}), 401

        return f(*args, **kwargs)
    return decorated

@app.route('/health', methods=['GET'])
def health():
    """
    Health check ендпоінт (Відкритий)
    ---
    responses:
      200:
        description: Повертає статус OK
    """
    return jsonify({"status": "ok"}), 200

@app.route('/login', methods=['POST'])
def login():
    """
    Авторизація та отримання JWT токена
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: admin123
    responses:
      200:
        description: Повертає згенерований JWT токен
      401:
        description: Невірні облікові дані
    """
    auth = request.get_json() or {}
    username = auth.get('username')
    password = auth.get('password')

    # Тестові облікові дані (admin / admin123)
    if username == 'admin' and password == 'admin123':
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token}), 200

    return jsonify({'message': 'Невірний логін або пароль!'}), 401

@app.route('/children', methods=['GET'])
@token_required
def get_children():
    """
    Отримання списку вихованців (Захищено JWT)
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Список вихованців
      401:
        description: Токен відсутній або недійсний
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM children;")
            result = cursor.fetchall()
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/employees', methods=['GET'])
@token_required
def get_employees():
    """
    Отримання списку працівників (Захищено JWT)
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Список працівників
      401:
        description: Токен відсутній або недійсний
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM employees;")
            result = cursor.fetchall()
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
