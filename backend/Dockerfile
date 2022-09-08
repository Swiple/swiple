FROM python:3.9

WORKDIR /code

COPY poetry.lock pyproject.toml  /code/

RUN pip install --no-cache-dir --upgrade pip poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Add Connectors
RUN poetry install \
    -E postgres    \
    -E redshift    \
    -E mysql       \
    -E trino       \
    -E athena      \
    -E snowflake

COPY app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]