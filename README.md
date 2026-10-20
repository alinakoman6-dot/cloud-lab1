# Лабораторна робота №1: Розгортання контейнеризованого Flask API в AWS ECS Fargate

**Студентка:** Аліна  
**Курс:** 3 курс, Бази даних і знань / Хмарні технології  
**Репозиторій:** [alinakoman6-dot/cloud-lab1](https://github.com/alinakoman6-dot/cloud-lab1)  
**Публічна адреса (ALB):** `http://lab1-alb-1481910119.eu-central-1.elb.amazonaws.com`

---

## 🚀 Опис проєкту

Даний проєкт являє собою REST API на Flask для управління дитячими садками, вихованцями та співробітниками. Застосунок запакований у Docker-контейнер, розгорнутий у бессерверному середовищі **AWS ECS Fargate** за **Application Load Balancer (ALB)** та підключений до приватного екземпляра **AWS RDS MySQL 8.0**.

---

## 🏛️ Архітектура інфраструктури (AWS)

Уся інфраструктура описана як код (**IaC**) за допомогою **Terraform**:

- **VPC & Security:** Публічні та приватні підмережі в двох зонах доступності (`eu-central-1a`, `eu-central-1b`).
- **Database (RDS MySQL 8.0):** Розміщена у приватній підмережі (`publicly_accessible = false`). Безпека забезпечується Security Group, яка дозволяє з'єднання за портом 3306 **виключно** від Security Group контейнера (`app_sg`).
- **Compute (ECS Fargate):** Контейнеризована Flask-програма запускається від непривілейованого користувача (`appuser`) у Fargate.
- **Load Balancer (ALB):** Єдина публічна точка входу з підключеним Health Check за адресою `/health`.
- **CI/CD:** GitHub Actions workflow з автентифікацією через **OIDC** та IAM Role (без збереження довговічних ключів доступу).
- **Monitoring:** Логи додатків та ініціалізації БД збираються в **AWS CloudWatch** (`/ecs/lab1-app`).

---

## 📡 Основні REST API Endpoints

| Метод | Маршрут | Опис |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check для ALB та моніторингу (повертає `200 OK`) |
| `GET` | `/children` | Отримання списку дітей з RDS БД |
| `GET` | `/employees` | Отримання списку співробітників з RDS БД |
| `POST`| `/insert-child` | Виклик збереженої процедури додавання вихованця |

---

## 🛠️ Локальний запуск (Docker Compose)

Для локального розгортання додатка разом із локальною MySQL виконайте:

```bash
docker compose up --build -d
