# Skystore

Учебный проект **Skystore** — маркетплейс плагинов и примеров кода на Django.

## Описание

Проект представляет собой веб-приложение на Django, реализующее платформу
для хранения и продажи плагинов и примеров кода. На текущем этапе реализованы
главная страница (каталог) и страница контактов с формой обратной связи.

## Технологии

- Python 3.10+
- Django 5.x
- Bootstrap 5
- SQLite

## Установка и запуск

### 1. Клонирование репозитория

git clone https://github.com/DenWhite77/Skystore.git
cd Skystore

### 2. Создание и активация виртуального окружения

python -m venv venv

Windows:
venv\Scripts\activate

Linux / macOS:
source venv/bin/activate

### 3. Установка зависимостей

pip install -r requirements.txt

### 4. Применение миграций и запуск сервера

python manage.py migrate
python manage.py runserver

Приложение будет доступно по адресу: http://127.0.0.1:8000/

### 5. Структура проекта

config/ — настройки Django-проекта
catalog/ — приложение каталога
templates/ — HTML-шаблоны
static/ — статические файлы (CSS, JS, изображения)

Автор
DenWhite77