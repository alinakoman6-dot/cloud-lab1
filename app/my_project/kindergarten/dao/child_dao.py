# app/my_project/kindergarten/dao/child_dao.py
from app.config.db import get_db_connection

class ChildDAO:
    # --- Хелпер для команд, що змінюють дані (ГАРАНТУЄ COMMIT) ---
    def _execute_write_command(self, sql, val=None):
        conn = get_db_connection()
        if conn is None: return None
        cursor = conn.cursor()
        
        try:
            # КРИТИЧНО ВАЖЛИВІ КОМАНДИ: Вимкнення блокування та примусовий автокомміт
            cursor.execute("SET SQL_SAFE_UPDATES = 0")
            cursor.execute("SET AUTOCOMMIT = 1") 
            
            cursor.execute(sql, val)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            # Це виведе помилку в консоль, якщо MySQL не може виконати команду
            print(f"DAO WRITE ERROR: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    # --- CRUD: Read (GET) ---
    def get_all(self):
        conn = get_db_connection()
        if conn is None: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM children")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def get_by_id(self, child_id):
        conn = get_db_connection()
        if conn is None: return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM children WHERE child_id = %s", (child_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    # --- CRUD: Create (POST) ---
    def create(self, data):
        sql = "INSERT INTO children (first_name, last_name, birth_date) VALUES (%s, %s, %s)"
        val = (data['first_name'], data['last_name'], data['birth_date'])
        new_id = self._execute_write_command(sql, val)
        return new_id

    # --- CRUD: Update (PUT - повне оновлення) ---
    def update(self, child_id, data):
        sql = "UPDATE children SET first_name = %s, last_name = %s, birth_date = %s WHERE child_id = %s"
        val = (data['first_name'], data['last_name'], data['birth_date'], child_id)
        self._execute_write_command(sql, val)

    # --- CRUD: Delete (DELETE) ---
    def delete(self, child_id):
        sql = "DELETE FROM children WHERE child_id = %s"
        val = (child_id,)
        self._execute_write_command(sql, val)
    
    # --- CRUD: Patch (PATCH - часткове оновлення) ---
    def patch(self, child_id, data):
        fields = []
        values = []
        if 'first_name' in data:
            fields.append("first_name = %s")
            values.append(data['first_name'])
        if 'last_name' in data:
            fields.append("last_name = %s")
            values.append(data['last_name'])
        if 'birth_date' in data:
            fields.append("birth_date = %s")
            values.append(data['birth_date'])
            
        if not fields:
            return 
            
        sql = f"UPDATE children SET {', '.join(fields)} WHERE child_id = %s"
        values.append(child_id)
        
        self._execute_write_command(sql, tuple(values))

    # --- Складні запити (M:M та M:1) ---
    def get_parents_by_child(self, child_id):
        conn = get_db_connection()
        if conn is None: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.parent_id, p.first_name, p.last_name, p.phone_number, cp.relation_type
            FROM parents p
            JOIN child_parents cp ON p.parent_id = cp.parent_id
            WHERE cp.child_id = %s
        """, (child_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def get_children_in_kindergarten(self, kindergarten_name):
        conn = get_db_connection()
        if conn is None: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.first_name, c.last_name, g.name as group_name, k.name as kindergarten_name
            FROM children c
            JOIN child_enrollment ce ON c.child_id = ce.child_id
            JOIN child_groups g ON ce.group_id = g.group_id
            JOIN kindergartens k ON g.kindergarten_id = k.kindergarten_id
            WHERE k.name LIKE %s
        """, (f"%{kindergarten_name}%",))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    
    