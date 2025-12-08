FROM python:3.14-slim
ENV PYTHONUNBUFFERED 1
ENV LANG ru_RU.UTF-8

RUN apt-get update &&  \
    apt-get install --no-install-recommends -y \
    git \
    libpq-dev `# build psycopg2` \
    gcc `# install psycopg2 & pre-commit` && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY ./requirements.txt .
RUN pip install uv && uv pip install --system --no-cache-dir --no-deps -r requirements.txt

WORKDIR /code
COPY . /code

EXPOSE 8000
