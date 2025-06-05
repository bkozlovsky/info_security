# info_security
## Інструкції з запуску проекту

### Передумови
Переконайтеся, що на вашому комп'ютері встановлено:
- Python 3.13
- pip (менеджер пакетів Python)

### Крок 1: Клонування репозиторію
```bash
git clone <URL_репозиторію>
cd info_security
```

### Крок 2: Створення віртуального середовища
```bash
python -m venv venv
```

### Крок 3: Активація віртуального середовища

**На Windows:**
```bash
venv\Scripts\activate
```

**На macOS/Linux:**
```bash
source venv/bin/activate
```

### Крок 4: Встановлення залежностей
```bash
pip install -r requirements.txt
```

### Крок 5: Налаштування бази даних (якщо потрібно)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Крок 6: Запуск сервера розробки
```bash
python manage.py runserver
```

Після успішного запуску, проект буде доступний за адресою: `http://127.0.0.1:8000/`

### Деактивація віртуального середовища
Коли закінчите роботу з проектом, деактивуйте віртуальне середовище:
```bash
deactivate
```
