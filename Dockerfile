FROM python:3.13-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only=main

# Копирование исходного кода
COPY . .

CMD ["python", "main.py"]