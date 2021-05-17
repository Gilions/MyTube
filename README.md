<p align="center">
    <img src="https://user-images.githubusercontent.com/68146917/118444573-f8a90000-b6f5-11eb-9244-43ac420b6e74.jpg">
</p>


# MyTube - Социальная сеть. Онлайн дневник.

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)




Первый мой проект. Это не большая социальная сеть, где пользователи могут вести свой онлайн дневник.

**На сайте реализована возможность регистрации**

Обязательные поля для пользователя:
+ Логин
+ Пароль
+ Email


**Уровни доступа пользователей:**

+ Гость (неавторизованный пользователь)
+ Авторизованный пользователь
+ Администратор

**Что могут делать неавторизованные пользователи**
+ Создать аккаунт.
+ Просматривать посты на главной странице.
+ Просматривать отдельные страницы постов.
+ Просматривать страницы пользователей.

**Что могут делать авторизованные пользователи**
+ Входить в систему под своим логином и паролем.
+ Выходить из системы (разлогиниваться).
+ Восстанавливать свой пароль.
+ Менять свой пароль.
+ Создавать/редактировать/удалять собственные посты
+ Создавать/редактировать/удалять посты в группах
+ Просматривать посты опубликованных в группах.
+ Просматривать посты на главной.
+ Просматривать страницы пользователей.
+ Просматривать отдельные страницы постов.
+ Подписываться на публикации авторов и отменять подписку, просматривать свою страницу подписок.

**Что может делать администратор**

 Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
+ изменять пароль любого пользователя,
+ создавать/блокировать/удалять аккаунты пользователей,
+ редактировать/удалять любые посты,
+ добавлять/удалять/редактировать группы.

**Инфраструктура**

Проект использует базу данных [PostgrSQL](https://www.postgresql.org/).

В корневой папке расположен файл requirements.txt со всеми зависимостями.

## Системные требования
_____

- [Python 3](https://www.python.org/)
- [Django 2.2.9](https://www.djangoproject.com/)
- [NGINX](https://www.nginx.com/)
- [Gunicorn](https://gunicorn.org/)
- [PostgrSQL](https://www.postgresql.org/)

##  Установка
______

Для устновки проекта пребуется:
- [Python 3](https://www.python.org/)
- [PostgrSQL](https://www.postgresql.org/)
- [venv](https://docs.python.org/3/library/venv.html)
- [GitHub](https://github.com/git-guides/install-git)

Используйте команду:

`sudo apt install python3-pip python3-venv git -y`

Клонируйте проект:

`git clone https://github.com/Gilions/MyTube.git`

Перейдите в директорию проекта. Активируйте виртуальное окружение и
установите пакеты из requirements.txt
```
python3 -m venv venv

source venv/bin/activate

python -m pip install -r requirements.txt
```

В корневом каталоге созайде файл .env со следующем содержанием

```
SECRET_KEY='6m+%9$h)m7_s_m^=$q-1v@pbf25i4d1uonrzq=4rvhov%t%ozl1'

#Postgres setting
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<Yours password>
DB_HOST=localhost
DB_PORT=5432
```
становите базу данных PostgreSQL

[Download PostgreSQL](https://www.postgresql.org/download/)

Запустите базу данных, убедитесь в том, что локальный сервер запущен.
Это можно понять в приложении [pgAdmin4](https://www.pgadmin.org/download/)

![](https://user-images.githubusercontent.com/68146917/118441461-e6c55e00-b6f1-11eb-992e-60c48be9dc85.png)

Перед запуском проекта, необходимо выполнить миграции. В терминале из коневого каталога выполните:

`python3 manage.py migrate`

Для запуска Django сервера используйте команду

`python manage.py runserver`
