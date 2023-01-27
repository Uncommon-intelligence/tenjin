.PHONY: run lint

run:
	poetry run python app.py

lint:
	poetry run black .