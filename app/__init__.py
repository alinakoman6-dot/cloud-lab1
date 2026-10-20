import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Реєстрація Blueprint-ів
    from app.my_project.kindergarten.route.child_route import child_bp
    from app.my_project.kindergarten.route.employee_route import employee_bp
    from app.my_project.kindergarten.route.lab5_route import lab5_bp

    app.register_blueprint(child_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(lab5_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
