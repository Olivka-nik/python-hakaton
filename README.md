# lab11 — Task Tracker (Django)

Веб-приложение для управления задачами (TODO / Task Tracker) с регистрацией и авторизацией пользователей.

## Демонстрация работы сайта
https://github.com/user-attachments/assets/a9ed31af-5117-4a3f-84d3-8443ecc72285



## Цель проекта
- Реализовать CRUD для сущностей `User` и `Task`.
- Организовать архитектуру MVC (Django MTV).
- Использовать SQLite и Django ORM.
- Применить миграции.
- Поддержать роль суперпользователя (админа), который может выполнять CRUD для всех сущностей.

## Стек
- Python 3.13+
- Django
- SQLite
- Django Templates + Bootstrap 5

## Функциональность
- Регистрация и авторизация пользователей.
- Создание, просмотр, редактирование, удаление задач.
- Отметка задачи как выполненной.
- Просмотр пользователей и их задач.
- Главная страница с зарегистрированными пользователями и их задачами.
- Админка Django для суперпользователя.

## Модели
### Task
- `owner` — владелец задачи (FK на `User`)
- `title` — название
- `description` — описание
- `priority` — приоритет: `low`, `medium`, `high`
- `due_date` — дата выполнения
- `status` — статус: `open`, `in_progress`, `done`
- `created_at`, `updated_at` — служебные поля

### User
Используется стандартная модель `django.contrib.auth.models.User`:
- `username`
- `email`
- `password` (хеш)

## Архитектура (MVC / MTV)
- **Model**: `tracker/models.py`
- **View (Controller logic)**: `tracker/views.py`
- **Template (Frontend)**: `templates/...`
- **Routes**: `tracker/urls.py`, `lab11/urls.py`

## Структура проекта
```text
lab11/
├── manage.py
├── db.sqlite3
├── lab11/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── tracker/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│       └── 0001_initial.py
└── templates/
    ├── base.html
    ├── home.html
    ├── registration/
    │   ├── login.html
    │   └── signup.html
    └── tracker/
        ├── task_list.html
        ├── task_form.html
        ├── task_confirm_delete.html
        ├── user_list.html
        ├── user_detail.html
        ├── user_form.html
        └── user_confirm_delete.html
```

## Маршруты
### Основные
- `/` — главная страница (пользователи и задачи)
- `/signup/` — регистрация
- `/accounts/login/` — вход
- `/accounts/logout/` — выход

### Задачи
- `/tasks/` — список задач
- `/tasks/create/` — создание задачи
- `/tasks/<id>/edit/` — редактирование
- `/tasks/<id>/delete/` — удаление
- `/tasks/<id>/complete/` — отметить выполненной

### Пользователи
- `/users/` — список пользователей
- `/users/<id>/` — профиль пользователя
- `/users/<id>/edit/` — редактирование профиля
- `/users/<id>/delete/` — удаление пользователя

### Админка
- `/admin/`

## Установка и запуск
```bash
cd /Users/mac/PycharmProjects/python-hakaton
python3 -m pip install django
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

Открыть в браузере:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

## Миграции
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Права доступа
- Обычный пользователь:
  - работает со своими задачами и своим профилем.
- Суперпользователь:
  - видит и редактирует все задачи и профили,
  - имеет полный CRUD в `/admin/`.

## Git Flow (простой вариант)
```bash
git checkout -b develop
git checkout -b feature/lab11-task-tracker
# ... коммиты ...
git checkout develop
git merge feature/lab11-task-tracker
git checkout -b release/v1.0.0
# ... финальные правки ...
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "release 1.0.0"
```
