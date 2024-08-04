FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR pylastfm/
COPY . .

RUN pip install poetry

RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
