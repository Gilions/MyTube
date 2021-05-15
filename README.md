# MyTube - Социальная сеть. Онлайн дневник.

Проект разрабатывался в рамках обучения языку Python, framework Django на курсах Python разработчик. Yandex практикум.

Это первый мой проект. Изучал возможности Django, написал тесты контролирующие работу сайта.

## Системные требования
_____

- Python 3
- Django 2.2.9
- NGINX - Gunicorn
- PostgreSQL

##  Установка
______

Для устновки проекта пребуется python3, venv, git

Используйте команду:

`sudo apt install python3-pip python3-venv git -y`

Клонируйте проект:

`git clone https://github.com/Gilions/MyTube.git`

Перейдите в директорию проекта. Активируйте виртуальное окружение и
установите пакеты из requirements.txt

`python3 -m venv venv`

`source venv/bin/activate`

`python -m pip install -r requirements.txt `

Для запуска Django сервера используйте команду

`python manage.py runserver`
