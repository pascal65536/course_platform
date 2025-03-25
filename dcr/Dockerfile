# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . .

# Устанавливаем необходимые зависимости (если есть)
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Команда по умолчанию
CMD ["python", "script.py"]

