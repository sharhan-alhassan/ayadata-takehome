
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

# apt install python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libharfbuzz-subset0 libffi-dev libjpeg-dev libopenjp2-7-dev

COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

############################

# ARG REDIS_HOST
# ARG REDIS_PORT
# ARG REDIS_USERNAME
# ARG REDIS_PASSWORD
# ARG DBNAME
# ARG DBUSER
# ARG DBHOST
# ARG DBPASSWORD
# ARG DBPORT
# ARG EMAIL_HOST_USER
# ARG EMAIL_HOST_PASSWORD
# ARG DEFAULT_FROM_EMAIL
# ARG SERVER_EMAIL
# ARG EMAIL_PORT



# ENV DBNAME=$DBNAME
# ENV DBUSER=$DBUSER
# ENV DBHOST=$DBHOST
# ENV DBPASSWORD=$DBPASSWORD
# ENV DBPORT=$DBPORT
# ENV REDIS_HOST=$REDIS_HOST
# ENV REDIS_PORT=$REDIS_PORT
# ENV REDIS_USERNAME=$REDIS_USERNAME
# ENV REDIS_PASSWORD=$REDIS_PASSWORD
# ENV EMAIL_HOST_USER=$EMAIL_HOST_USER
# ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
# ENV DEFAULT_FROM_EMAIL=$DEFAULT_FROM_EMAIL
# ENV SERVER_EMAIL=$SERVER_EMAIL
# ENV EMAIL_PORT=$EMAIL_PORT

ENV ENV=production
ENV DJANGO_SETTINGS_MODULE=core.settings


# RUN python manage.py collectstatic --noinput
# RUN python manage.py makemigrations
# RUN python manage.py migrate


# ENV DJANGO_SUPERUSER_PASSWORD=admin
# ENV DJANGO_SUPERUSER_EMAIL=admin@gmail.com


EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "setup.wsgi:application"]
CMD ["gunicorn", "--config", "gunicorn_config.py", "core.wsgi:application"]
# CMD ["sh", "-c", "pip install gunicorn && gunicorn --config gunicorn_config.py"]
