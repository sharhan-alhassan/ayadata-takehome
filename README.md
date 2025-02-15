## Table of Contents

- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Production Setup](#production-setup)
- [Screenshots](#screenshots-of-the-application)
- [Test Credentials](#test-credentials)
- [Challenges](#challenges-smtp)


## Project Structure
Ayadata Task Management API. It allows users to register, log in, and manage tasks assigments. The API is built with Django Rest Framework, Sqlite (&postgresql) for migrations/data storage, django-rq for background tasks, and gunicorn for production deployment. 

```sh
ayadata-takehome/
│
├── .env                        
├── docker-compose.yml          
├── Dockerfile                  
├── manage.py                   
├── requirements.txt            
├── core/
│   ├── __init__.py
│   ├── settings.py            
│   ├── urls.py               
│   ├── wsgi.py                
│   └── ...
├── db.sqlite3                 
└── tasks
├── users                  
└── templates
├── gunicorn_config.py                  
└── requirements.txt
├── static                 

```

##  Local Development Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env (Development settings)
# All required environment variables schema in conf.yaml

# Database Migrations
python manage.py makemigrations &&
python manage.py migrate

# Start server 
./manage.py runserver 
```

## Production Setup

```bash
# Push Image to Dockerhub
docker build -t ayadata-app:0.0.5 .
docker image tag ayadata-app:0.0.1 sharhanalhassan/ayadata-app:0.0.5
docker image push sharhanalhassan/ayadata-app:0.0.5

# Local Run with Docker compose
docker-compose up -d
docker-compose exec web python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
```

## Screenshots of the application
### List Applications Endpoint
![Home page](/images/home.png)

### List Tasks Endpoint
![List Tasks](/images/list_tasks.png)

### Registration Tasks Endpoint
![Registration Email](/images/register_email.png)

## Test Credentials
```sh
# User with admin privileges (Admin Dashboard Access)
email: admin@gmail.com
password: admin123

# Non Admin User
email: user1@gmail.com
password: adminadmin
```


## Challenges SMTP

- Couldn't get `celery` to accept secured connection for the redis container
- Tried another asychronous task queues such as the below
```sh
1. django-huey
2. django-q2
3. django-rq
```
- It happend it had to do with the scope of Google security guardrails for the `gmail` SMTP
- I had to use the `gmail` SMTP to send the email in a synchronous process

```