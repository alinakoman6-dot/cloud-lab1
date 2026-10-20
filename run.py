import os
from flask import Flask, jsonify, request
from flasgger import Swagger
import pymysql

app = Flask(__name__)

# Ініціалізація Swagger UI
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
        "description": "API для управління дитячими садками, вихованцями та працівниками",
        "version": "1.0.0"
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

@app.route('/health', methods=['GET'])
def health():
    """
    Health check ендпоінт
    ---
    responses:
      200:
        description: Повертає статус OK для ALB health check
    """
    return jsonify({"status": "ok"}), 200

@app.route('/children', methods=['GET'])
def get_children():
    """
    Отримання списку всіх вихованців
    ---
    responses:
      200:
        description: Список вихованців із бази даних
      500:
        description: Помилка з'єднання з базой даних
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
def get_employees():
    """
    Отримання списку всіх працівників
    ---
    responses:
      200:
        description: Список працівників із бази даних
      500:
        description: Помилка з'єднання з базой даних
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
