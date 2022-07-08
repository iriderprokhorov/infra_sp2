# Проект YaMDb упакованный в докер


Сам проект YaMDb расположен тут https://github.com/iriderprokhorov/api_yamdb

## Шаблон для заполнения env-файла

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=имя базы данных
POSTGRES_USER=логин для подключения к базе данных
POSTGRES_PASSWORD=пароль для подключения к БД
DB_HOST= название сервиса (контейнера)
DB_PORT=порт для подключения к БД


## Системные требования
 Python3 
 
## Как запустить проект:

Клонировать образ из Dockerhub:

```
docker pull iriderpro/api_yamdb:latest
```
Запустите контейнеры


## Выполните миграции, создайте суперпользователя, собирите статику


```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```


## Заполните данные через api по инструкции расположенно по адресу http://localhost/redoc


### Авторы 
Петр, Илья, Николай
