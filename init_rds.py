
import os
import pymysql

db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME', 'kindergartens')

print(f"Connecting to {db_host}...")
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    autocommit=True
)

cursor = connection.cursor()

def run_sql_file(filename):
    print(f"Executing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        sql = f.read()
    statements = sql.split(';')
    for statement in statements:
        if statement.strip():
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"Error executing statement: {e}")

run_sql_file('db/01_init.sql')
run_sql_file('db/02_routines.sql')
print("Database initialized successfully!")
