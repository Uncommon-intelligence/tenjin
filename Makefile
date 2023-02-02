.PHONY: run_gradio run_api lint

run-gradio:
	poetry run python app.py

run-api:
	poetry run uvicorn api:app --reload

lint:
	poetry run black .