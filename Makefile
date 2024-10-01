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
	docker compose exec backend ruff check src

black:
	@echo "running black...."
	docker compose exec backend black .

mypy:
	@echo "running mypy...."
	docker compose exec backend mypy src/

# database
init-db: alembic-init alembic-migrate
	@echo "initializing database...."
	docker compose exec backend python3 src/db/init_db.py

# misc

hooks: check
	@echo "installing pre-commit hooks...."
	pre-commit install
