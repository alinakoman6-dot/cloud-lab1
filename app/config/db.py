import os
import mysql.connector
from mysql.connector import Error


def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", "3306")),
            database=os.environ.get("DB_NAME", "kindergartens"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ["DB_PASSWORD"],  # без значення за замовчуванням: пароль лише ззовні
            autocommit=True,
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None