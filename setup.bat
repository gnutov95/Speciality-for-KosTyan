@echo off
echo ==========================================
echo Установка проекта Speciality-for-KosTyan
echo ==========================================
echo.

echo [1/5] Создание виртуального окружения...
python -m venv .venv

echo [2/5] Активация виртуального окружения...
call .venv\Scripts\activate

echo [3/5] Установка зависимостей...
pip install -r requirements.txt

echo [4/5] Применение миграций базы данных...
python manage.py migrate

echo [5/5] Создание суперпользователя (опционально)...
echo Если хотите создать админа - введите данные, иначе просто нажмите Ctrl+C
python manage.py createsuperuser

echo.
echo ==========================================
echo Установка завершена!
echo Для запуска проекта выполните:
echo .venv\Scripts\activate
echo python manage.py runserver
echo ==========================================
pause