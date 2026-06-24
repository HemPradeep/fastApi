.PHONY: test

run:
	uvicorn main:app --reload
test:
	python -m pytest
format:
	black .
	isort .
lint:
	ruff check .
fix:
	ruff check . --fix
typecheck:
	mypy .