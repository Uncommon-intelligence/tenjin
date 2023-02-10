.PHONY: run_gradio run_api lint

run: dev


server:
	poetry run uvicorn tenjin.main:app --workers 6 --host 0.0.0.0 --port 8000

dev:
	docker-compose up -d localstack 
	poetry run server

gradio:
	poetry run python app.py

conversation:
	docker-compose up -d localstack 
	poetry run python conversation.py

build:
	docker-compose build --no-cache server

lint:
	poetry run black .