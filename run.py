import os
import re
import pymysql
from app import create_app

app = create_app()

def execute_sql_file(cursor, filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Спеціальна обробка для файлів із DELIMITER (процедури, тригери)
    if 'DELIMITER' in content:
        # Видаляємо всі оголошення DELIMITER
        content_clean = re.sub(r'DELIMITER\s+\$\$', '', content, flags=re.IGNORECASE)
        content_clean = re.sub(r'DELIMITER\s+;', '', content_clean, flags=re.IGNORECASE)
        statements = content_clean.split('$$')
    else:
        statements = content.split(';')

    for stmt in statements:
        stmt_stripped = stmt.strip()
        if stmt_stripped:
            try:
                cursor.execute(stmt_stripped)
            except Exception as e:
                print(f"SQL statement notice: {e}")

def init_db():
    db_host = os.environ.get('DB_HOST')
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME', 'kindergartens')

    if not db_host or not db_password:
        print("DB configuration missing, skipping init")
        return

    print(f"Connecting to RDS at {db_host}...")
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        autocommit=True
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
    cursor.execute(f"USE `{db_name}`;")

    print("Applying db/01_init.sql...")
    execute_sql_file(cursor, 'db/01_init.sql')

    print("Applying db/02_routines.sql...")
    execute_sql_file(cursor, 'db/02_routines.sql')

    cursor.close()
    conn.close()
    print("Database migration completed successfully!")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
