TAIL=100

# Переменные, которые используются в скриптах, для использование нужно указать ее при запуске
# Например make logs c=celery

# Переменная "c", для указания с каким контейнером взаимодействовать. По дефолту - django
define set-default-container
	ifndef c
	c = django
	else ifeq (${c},all)
	override c=
	endif
endef


set-container:
	$(eval $(call set-default-container))


build:
	docker compose -f docker-compose.dev.yml build
up:
	docker compose -f docker-compose.dev.yml up --remove-orphans  -d $(c)
up-default-workers:
	docker compose -f docker-compose.dev.yml up -d --scale celery-worker-default=$(NUM_WORKERS)
down:
	docker compose -f docker-compose.dev.yml down
logs: set-container
	docker compose -f docker-compose.dev.yml logs --tail=$(TAIL) -f $(c)
restart: set-container
	docker compose -f docker-compose.dev.yml restart $(c)
exec: set-container
	docker compose -f docker-compose.dev.yml exec $(c) /bin/bash
remove: set-container
	docker compose -f docker-compose.dev.yml rm -fs $(c)


migrate: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) bash -c './manage.py migrate'
migrations: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) bash -c './manage.py makemigrations'
shell: set-container
	docker compose -f docker-compose.dev.yml exec $(c) /bin/bash -c './manage.py shell'

test: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) bash -c 'pytest -x -n 4'
pre-commit: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) bash -c 'PRE_COMMIT_HOME=.precomcache pre-commit run --all-files'