.PHONY: run_gradio run_api lint

run: dev

gradio:
	poetry run python app.py

server:
	poetry run uvicorn tenjin.main:app --workers 6 --host 0.0.0.0 --port 8000

dev:
	docker-compose up -d localstack 
	poetry run server

conversation:
	docker-compose up -d localstack 
	poetry run python conversation.py

lint:
	poetry run black .