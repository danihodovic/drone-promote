FROM python:3.9.1

RUN apt-get update && apt install -y locales libcurl4-openssl-dev libssl-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app/

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction #!COMMIT

ENV PYTHONUNBUFFERED 1

COPY . /app/

RUN poetry install --no-interaction

CMD ["drone-promote"]
