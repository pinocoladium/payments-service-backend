# payments-service-backend

REST-сервис для управления заявками на выплату средств


### Запуск локально:
* Создать файл `.environment` в корне проекта (название переменных взять из `.environment.example`)
* Постороить образ `make build`, затем запустить приложение `make up`
* Накатить миграции `make migrate`
* Просмотреть логи `make logs`
* Запустить тесты `make test` (на работающем приложении)
* Запуск доп воркеров celery `make up-default-workers NUM_WORKERS={число}`

### Деплой:
* каждый сервис упаковывается в отдельный Docker-образ (Django, Redis, Celery, Celery-beat) - `docker compose -f docker-compose.prod.yml build`;
* эти образы закидывают на хост, где и запускаются - `docker compose -f docker-compose.prod.yml up -d`, также используются скрипты в `deploy.sh`, `.migration.sh`;
* Django запускается через gunicorn - `gunicorn payments_service.wsgi:application --bind 0.0.0.0:8000`;
* Воркеры селери запускаются `celery -A payments_service worker -l INFO --concurrency=2`, при необходимости можно запускать с различными очередями `-Q payments`;
* На хосте должны быть установлены `Docker` и `Docker Compose` или `Kubernetes`;
* Файл `.environment` удобно поддерживать через сервис `infiskal`;

## UserFlow:

* Получение токена для созданого пользователя `POST /api/users/token/`
![Получения токена](docs/images/users_token.png)

* Просмотр листа активных заявок `GET /api/payouts/`
![Список заявок](docs/images/applications_list.png)

* Просмотр ретрива активной заявки `GET /api/payouts/{id}/`
![Заявка](docs/images/application.png)

* Просмотр архивных заявок `GET /api/payouts/archived/` и `GET /api/payouts/archived/{id}/`
![Список архивных заявок](docs/images/archived_applications.png)

* Создание заявки `POST /api/payouts/` и валидация
![Создание заявки](docs/images/create_application.png)
![Валидация](docs/images/validation.png)

* Изменение заявки `PATCH /api/payouts/{id}/`
![Изменение заявки](docs/images/change_application.png)

* Удаление заявки `DELETE /api/payouts/{id}/`
![Удаление заявки](docs/images/delete_application.png)


* Просмотр сваггера `GET /api/docs/` и схемы `GET /api/schema/`
![Сваггер](docs/images/swagger.png)
![Схема](docs/images/schema.png)
