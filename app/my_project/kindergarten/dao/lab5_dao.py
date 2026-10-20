import mysql.connector
from app.config.db import get_db_connection

class Lab5DAO:
    def __init__(self):
        pass

    def get_connection(self):
        return get_db_connection()

    def call_insert_child(self, first_name, last_name, birth_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('insert_new_child', [first_name, last_name, birth_date])
            conn.commit()
            return True
        except Exception as e:
            print(f"Помилка DAO (вставка дитини): {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def call_assign_position(self, first_name, last_name, position_title):
        conn = self.get_connection()
        cursor = conn.cursor()
        msg = "Помилка виконання"
        try:
            cursor.callproc('assign_position_to_employee', [first_name, last_name, position_title])
            conn.commit()
            for res in cursor.stored_results():
                row = res.fetchone()
                if row:
                    msg = row[0]
            return msg
        except Exception as e:
            print(f"Помилка DAO (призначення посади): {e}")
            return str(e) # Повертаємо текст помилки SQL українською
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def call_insert_dummy(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('insert_dummy_children')
            conn.commit()
            return True
        except Exception as e:
            print(f"Помилка DAO (генерація даних): {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def call_salary_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        avg = 0.0
        try:
            cursor.callproc('show_salary_stats')
            for res in cursor.stored_results():
                row = res.fetchone()
                if row:
                    avg = row[0]
            return float(avg)
        except Exception as e:
            print(f"Помилка DAO (статистика): {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def call_dynamic_cursor(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        msg = ""
        try:
            cursor.callproc('dynamic_table_cursor')
            conn.commit()
            for res in cursor.stored_results():
                row = res.fetchone()
                if row:
                    msg = row[0]
            return msg
        except Exception as e:
            print(f"Помилка DAO (курсор): {e}")
            return str(e)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

            # Новий метод: Додавання запису в журнал відвідування
    def insert_attendance_log(self, child_id, visit_date, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Звичайний SQL INSERT
            query = "INSERT INTO attendance_log (child_id, visit_date, status) VALUES (%s, %s, %s)"
            cursor.execute(query, (child_id, visit_date, status))
            conn.commit()
            return True, "Запис успішно додано!"
        except Exception as e:
            # Тут ми ловимо помилку від ТРИГЕРА
            print(f"Помилка тригера: {e}")
            # Повертаємо текст помилки, щоб побачити його в Postman
            return False, str(e) 
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

            # 1. Для тесту телефону батьків
    # ВИПРАВЛЕНИЙ МЕТОД (без адреси)
    def insert_parent(self, first_name, last_name, phone):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Прибрали address із запиту
            query = "INSERT INTO parents (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
            cursor.execute(query, (first_name, last_name, phone))
            conn.commit()
            return True, "Батька успішно додано!"
        except Exception as e:
            return False, str(e)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    # 2. Для тесту видалення садочка
    def delete_kindergarten(self, kindergarten_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "DELETE FROM kindergartens WHERE kindergarten_id = %s"
            cursor.execute(query, (kindergarten_id,))
            conn.commit()
            return True, "Садочок видалено (цього не має статися)"
        except Exception as e:
            return False, str(e) # Повертаємо помилку тригера
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    # 3. Для тесту видалення співробітника
    def delete_employee(self, employee_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "DELETE FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            conn.commit()
            return True, f"Співробітника ID {employee_id} видалено. Перевірте таблицю логів!"
        except Exception as e:
            return False, str(e)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    # 4. Щоб побачити лог аудиту в Postman
    def get_audit_log(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM employee_audit_log ORDER BY log_time DESC LIMIT 5")
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()