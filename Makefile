echo:
	@echo $(PYTHONPATH)

.PHONY: run_gradio run_api lint

run: dev


server:
	poetry run uvicorn tenjin.main:app --workers 6 --host 0.0.0.0 --port 8000

dev:
	docker-compose up -d localstack 
	poetry run server

lint:
	poetry run black .

test:
	poetry run pytest tests/unit_tests

test_watch:
	poetry run pytest tests/unit_tests

help:
	@echo '----'
	@echo 'dev                 - Run app in dev mode'
	@echo 'server              - Run app in server mode'
	@echo 'lint                - run linters'
	@echo 'test                - run unit tests'
	@echo 'test_watch          - run unit tests in watch mode'
	@echo 'integration_tests   - run integration tests'