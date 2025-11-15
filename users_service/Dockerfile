FROM python:3.13-slim

WORKDIR /app

COPY ./src/ ./src/
COPY ./pyproject.toml .

RUN pip install --upgrade pip && \
    pip install uv && \
    uv pip install --system -e .

CMD ["python", "-m", "src.main"]

