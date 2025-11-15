FROM python:3.13-slim

WORKDIR /app

# Копируем файлы проекта
COPY ./src/ ./src/
COPY ./pyproject.toml .

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install uv && \
    uv pip install --system -e .

CMD ["python", "-m", "src.main"]
