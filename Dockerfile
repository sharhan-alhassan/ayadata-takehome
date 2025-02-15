
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get dist-upgrade -y && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    weasyprint && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV ENV=production
ENV DJANGO_SETTINGS_MODULE=core.settings


EXPOSE 8000
CMD ["gunicorn", "--config", "gunicorn_config.py", "core.wsgi:application"]
