# Хмарні технології: Лабораторні роботи №1 та №2 (AWS ECS Fargate, Autoscaling, CloudWatch & k6)

**Студентка:** Аліна  
**Курс:** 3 курс, Хмарні технології  
**Репозиторій:** [alinakoman6-dot/cloud-lab1](https://github.com/alinakoman6-dot/cloud-lab1)  
**Публічна адреса (ALB):** `http://lab1-alb-1765514118.eu-central-1.elb.amazonaws.com`

---

## 🚀 Опис проєкту

Проєкт охоплює розгортання REST API на Flask у **AWS ECS Fargate** за **Application Load Balancer (ALB)** з підключенням до **AWS RDS MySQL 8.0** (Лабораторна робота №1), а також налаштування навантажувального тестування **k6**, автоматичного масштабування сервісу та сповіщень **CloudWatch + SNS** (Лабораторна робота №2)[cite: 6, 7, 8].

---

## 🏛️ Архітектура інфраструктури (AWS)

Уся інфраструктура описана як код (**IaC**) за допомогою **Terraform**:

- **VPC & Security:** Публічні та приватні підмережі у двох зонах доступності (`eu-central-1a`, `eu-central-1b`), Security Groups для ALB, ECS-контейнерів та БД.
- **Database (RDS MySQL 8.0):** Приватна база даних у прихованій підмережі з доступом лише за портом 3306 із Security Group контейнера (`app_sg`).
- **Compute & Autoscaling (ECS Fargate):** Сервіс `lab1-app-service` у кластері `lab1-ecs-cluster` з **Target Tracking** політикою (`lab2-cpu-target-tracking`, ціль **60% CPU**, `min_capacity = 1`, `max_capacity = 3`, `ScaleOutCooldown = 60 с`, `ScaleInCooldown = 300 с`)[cite: 7].
- **Load Balancer (ALB):** Публічна точка входу з Health Check за `/health` та розподілом навантаження між активними копіями сервісу[cite: 7].
- **Monitoring & Alerts (CloudWatch & SNS):** Дашборд `lab2-dashboard`, метрики CPU/запитів/латентності/5xx та тривога `lab2-cpu-high` (**> 70% CPU** протягом **2 хвилин**, топік `lab2-alerts` з email-підпискою на стани `ALARM` та `OK`)[cite: 6, 7].
- **CI/CD:** GitHub Actions workflow (`.github/workflows/deploy.yml`) для збірки Docker-образу, пушу в ECR та оновлення сервісу ECS.

---

## 📂 Документація лабораторних робіт

- [LOADTEST.md](LOADTEST.md) — сценарій k6, профілі навантаження (`3 + 5 + 2 хв`), вибір `N` та результати тестування (`loadtest/summary.json`)[cite: 8].
- [AUTOSCALING.md](AUTOSCALING.md) — конфігурація Target Tracking, cooldown-паузи, таймлайн масштабування та панель CloudWatch[cite: 7].
- [ALERTS.md](ALERTS.md) — умови спрацювання `lab2-cpu-high`, логіка затримок та сповіщення `ALARM` / `OK`[cite: 6].

---

## 📡 Основні REST API Endpoints

| Метод | Маршрут | Опис |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check для ALB та моніторингу (`200 OK`) |
| `GET` | `/children` | Отримання списку вихованців з RDS БД |
| `GET` | `/employees` | Отримання списку співробітників з RDS БД |
| `POST` | `/children` | Створення запису вихованця (використовується у навантажувальному тесті)[cite: 8] |
