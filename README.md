# 📝 PasteBin Clone — Учебный проект на Flask

Учебный проект, разработанный в рамках курса **Learn Python** . Представляет собой аналог PasteBin: сервис для размещения текстовых фрагментов (snippets) с возможностью делиться ими по ссылке, ограничивать доступ по паролю и времени жизни, а также оценивать (лайкать) тексты.

## 🚀 Возможности

- Создание, редактирование, удаление текстов
- Парольная защита и ограничение времени жизни для каждого текста
- Отправка ссылки на текст другим пользователям
- Оценка (лайки) текстов
- Личный кабинет пользователя с просмотром всех своих текстов
- Аутентификация и авторизация
- Простой адаптивный интерфейс на базе Jinja2 + Bootstrap

---

## 🧰 Технологии

- 🐍 Python 3.10+
- 🔥 Flask
- 🗃 PostgreSQL
- 🧪 SQLAlchemy + Alembic (перенос с Flask-Migrate)
- 🧪 Jinja2 + Bootstrap 5
- ⚙️ dotenv для конфигурации
- 🐳 Docker Compose для запуска БД

## 👥 Формат работы над проектом

Проект выполнялся **в команде**. Основная цель — не только углублённое изучение Flask и смежных технологий, но и получение **опыта командной разработки**:

- Работа с git в команде (feature-ветки, pull requests)
- Разрешение merge-конфликтов
- Code review
- Согласование архитектурных решений

---
## ⚙️ Запуск приложения
1. Клонируйте репозиторий
```
git clone https://github.com/AlexeyPetrochenko/PasteBin-LearnPython
cd PasteBin-LearnPython
```
2. Создайте файл `.env` в корне проекта на основе файла `.env-example`.

3. Установка зависимостей

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Запуск базы данных через Docker Compose 
- Убедитесь, что установлен Docker и Docker Compose.
```
docker compose up -d
```
5.  Накатить миграции
```
alembic upgrade head
```
6. Запуск проекта
```
export FLASK_APP=app_paste_bin.app
export FLASK_ENV=development
flask run
```

## 📌 Автор
Алексей Петроченко
* Контакты: [GitHub](https://github.com/AlexeyPetrochenko) | [Telegram](https://t.me/AlekseyPetrochenko) | [alexeypetrochenko1@gmail.com](mailto:alexeypetrochenko1@gmail.com)