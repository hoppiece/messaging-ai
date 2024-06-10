poetry run ruff format --check --diff src
poetry run ruff check --output-format=github src
poetry run mypy src
