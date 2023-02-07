.PHONY: run_gradio run_api lint

run: api

gradio:
	poetry run python app.py

api:
	poetry run uvicorn api:app --reload

conversation:
	poetry run python conversation.py

lint:
	poetry run black .