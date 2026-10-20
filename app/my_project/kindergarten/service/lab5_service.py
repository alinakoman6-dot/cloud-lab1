from app.my_project.kindergarten.dao.lab5_dao import Lab5DAO

class Lab5Service:
    def __init__(self):
        self.dao = Lab5DAO()

    def add_child(self, data):
        if not data.get('first_name') or not data.get('last_name'):
            return False
        return self.dao.call_insert_child(data['first_name'], data['last_name'], data['birth_date'])

    def assign_position(self, data):
        return self.dao.call_assign_position(data['first_name'], data['last_name'], data['position_title'])

    def generate_dummy(self):
        return self.dao.call_insert_dummy()

    def get_stats(self):
        return self.dao.call_salary_stats()

    def run_cursor(self):
        return self.dao.call_dynamic_cursor()
    
    def add_attendance(self, data):
        return self.dao.insert_attendance_log(data['child_id'], data['visit_date'], data['status'])
    
    # ВИПРАВЛЕНИЙ МЕТОД (без адреси)
    def add_parent(self, data):
        # Передаємо тільки 3 параметри
        return self.dao.insert_parent(data['first_name'], data['last_name'], data['phone'])

    def delete_kindergarten(self, k_id):
        return self.dao.delete_kindergarten(k_id)

    def delete_employee(self, emp_id):
        return self.dao.delete_employee(emp_id)

    def get_logs(self):
        return self.dao.get_audit_log()