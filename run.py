from flask import Flask
from app.my_project.kindergarten.route.child_route import child_bp
from app.my_project.kindergarten.route.employee_route import employee_bp
from app.my_project.kindergarten.route.lab5_route import lab5_bp

app = Flask(__name__)
app.json.ensure_ascii = False

app.register_blueprint(child_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(lab5_bp, url_prefix='/api/lab5')


@app.route('/health')
def health():
    return {"status": "ok"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)