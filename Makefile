.PHONY: run_gradio run_api lint

run: api

gradio:
	poetry run python app.py

api:
	docker-compose up -d localstack 
	poetry run uvicorn api:app --reload

conversation:
	docker-compose up -d localstack 
	poetry run python conversation.py

lint:
	poetry run black .