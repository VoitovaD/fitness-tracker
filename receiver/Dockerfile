FROM python:3.11.11-slim

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-root

COPY src/ .

CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000"]