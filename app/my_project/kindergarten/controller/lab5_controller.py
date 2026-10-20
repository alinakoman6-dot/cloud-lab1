from app.my_project.kindergarten.service.lab5_service import Lab5Service

class Lab5Controller:
    def __init__(self):
        self.service = Lab5Service()

    def insert_child(self, data):
        success = self.service.add_child(data)
        if success:
            # ТУТ БУВ АНГЛІЙСЬКИЙ ТЕКСТ, ТЕПЕР УКРАЇНСЬКИЙ
            return {"message": "Дитину успішно додано через збережену процедуру"}, 201
        return {"message": "Не вдалося додати дитину (перевірте дані)"}, 400

    def assign_position(self, data):
        msg = self.service.assign_position(data)
        return {"db_result": msg}, 200

    def generate_dummy(self):
        success = self.service.generate_dummy()
        if success:
            return {"message": "10 тестових записів успішно додано"}, 201
        return {"message": "Не вдалося згенерувати дані"}, 500

    def get_salary_stats(self):
        avg = self.service.get_stats()
        if avg is not None:
            return {"average_salary": avg}, 200
        return {"message": "Помилка розрахунку"}, 500

    def run_cursor(self):
        msg = self.service.run_cursor()
        return {"cursor_result": msg}, 200
    
    def add_attendance(self, data):
        success, message = self.service.add_attendance(data)
        if success:
            return {"message": message}, 201
        # Якщо помилка (спрацював тригер), повертаємо її текст
        return {"error": message}, 400
    
    def create_parent(self, data):
        success, message = self.service.add_parent(data)
        if success:
            return {"message": message}, 201
        return {"error": message}, 400

    def delete_kindergarten(self, k_id):
        success, message = self.service.delete_kindergarten(k_id)
        if success:
            return {"message": message}, 200
        return {"error": message}, 400

    def delete_employee(self, emp_id):
        success, message = self.service.delete_employee(emp_id)
        if success:
            return {"message": message}, 200
        return {"error": message}, 400
        
    def get_audit_logs(self):
        logs = self.service.get_logs()
        return logs, 200