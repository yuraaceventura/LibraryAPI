FROM python:3.13-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only=main --no-root

# Копирование исходного кода
COPY . .

CMD alembic upgrade head && python main.py