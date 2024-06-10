poetry run coverage run --source=src -m pytest -vv --doctest-modules src
poetry run coverage report --show-missing
