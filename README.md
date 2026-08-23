# Система сбора отчётов АЗС

Веб-приложение для ежедневного сбора данных с 8 автозаправочных станций и формирования сводного отчёта для главного бухгалтера.

## 🚀 Демо

[Скоро](https://)

---

## 📋 Возможности

- **Для бухгалтера АЗС**:
  - Ввод остатков топлива, продаж, выручки и кассы
  - Выбор даты отчёта
  - Отправка данных в общую базу

- **Для главного бухгалтера**:
  - Просмотр сводных данных по всем АЗС за выбранную дату
  - Расчёт остатка по цене стелы
  - Экспорт отчёта в DOCX

---

## 🛠️ Стек технологий

- **Backend**: Django 6.0.6, Python 3.12
- **База данных**: SQLite (локально) / PostgreSQL (в продакшене)
- **Frontend**: Django Templates, Vanilla JS, HTML, CSS
- **Документы**: клиентская генерация DOCX через `docx.js`

---

## 🧪 Запуск локально

1. Клонируй репозиторий:
```bash
git clone https://github.com/Lirake257/azs-accountant-website.git
cd название-репозитория
```
2. Создай виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Установи зависимости:
```bash
pip install -r requirements.txt
```
4. Примени миграции:
```bash
python manage.py migrate
```
5. Запусти сервер:
```bash
python manage.py runserver
```
6. Открой в браузере:
```
http://127.0.0.1:8000
```

---

## 📁 Структура проекта

```
core/           # Настройки Django
reports/        # Основное приложение
├── migrations/ # Миграции базы данных
├── templates/  # HTML-шаблоны
├── static/     # Статические файлы (CSS, JS)
├── models.py   # Модели данных
├── views.py    # Логика приложения
└── admin.py    # Админка
manage.py       # Точка входа
requirements.txt
```

---

MIT License
