FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# спочатку залежності: цей шар кешується, поки requirements.txt не змінився
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# потім код: змінюється часто, тому йде після залежностей
COPY app ./app
COPY run.py .
COPY db ./db

# процес не від root
RUN useradd --create-home --uid 1000 appuser
USER appuser

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--preload", "run:app"]