ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

db:
	docker-compose up -d

open_db:
	docker exec -it $(DB_CONTAINER_NAME) psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

lint:
	pylint shortener test

test:
	poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG

run:
	uvicorn shortener.__main__:app --reload --port=8080
