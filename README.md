# Skystore

Учебный проект **Skystore** — маркетплейс плагинов и примеров кода на Django.
Включает каталог продуктов и блог с полным CRUD.

## Описание

Проект представляет собой веб-приложение на Django:

- **Каталог** — продукты с категориями, изображениями, ценой. Создание, редактирование, удаление, детальная страница. Пагинация.
- **Блог** — статьи с превью, признаком публикации и счётчиком просмотров. Полный CRUD на CBV. Email-уведомление при 100 просмотрах.
- **Контакты** — форма обратной связи и контактные данные из БД.
- **Валидация форм** — запрещённые слова (в названии и описании), отрицательная цена, формат и размер изображения.
- **Админка** — управление всеми моделями.
- **CI** — GitHub Actions с PostgreSQL-сервисом.

## Технологии

- Python 3.10+
- Django 6.1
- PostgreSQL
- Bootstrap 5
- Pillow (для ImageField)
- python-dotenv (для `.env`)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/DenWhite77/Skystore.git
cd Skystore
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux / macOS:
```bash
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка окружения (`.env`)

Скопируйте шаблон `.env.example` в `.env` и заполните значения:

```bash
copy .env.example .env      # Windows
cp .env.example .env         # Linux / macOS
```

Пример содержимого `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=skystore
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 5. Создание базы данных PostgreSQL

В `psql` или pgAdmin создайте базу:

```sql
CREATE DATABASE skystore;
```

### 6. Миграции и запуск

```bash
python manage.py migrate
python manage.py createsuperuser   # по желанию — для доступа в админку
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## Структура проекта

```
Skystore/
├── blog/               — приложение блога
├── catalog/            — приложение каталога
├── config/             — настройки Django-проекта
├── templates/          — HTML-шаблоны
│   ├── base.html       — базовый шаблон
│   ├── includes/       — подшаблоны (меню)
│   ├── blog/           — шаблоны блога
│   └── catalog/        — шаблоны каталога
├── static/             — статические файлы (Bootstrap)
├── screenshots/        — скриншоты для домашек
├── .env.example        — шаблон переменных окружения
├── requirements.txt    — зависимости проекта
└── manage.py
```

Автор
DenWhite77
