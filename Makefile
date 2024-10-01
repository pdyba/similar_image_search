# docker
up:
	@echo "bringing up project...."
	docker compose up

down:
	@echo "bringing down project...."
	docker compose down

bash:
	@echo "connecting to container...."
	docker compose exec backend bash

# test
test:
	@echo "running pytest...."
	docker compose exec backend pytest --cov-report xml --cov=src tests/

# lint
lint:
	@echo "running ruff...."
	docker compose exec backend ruff check /code/src

black:
	@echo "running black...."
	docker compose exec backend black /code/src

mypy:
	@echo "running mypy...."
	docker compose exec backend mypy /code/src


# misc
hooks: check
	@echo "installing pre-commit hooks...."
	pre-commit install
