SHELL = /bin/bash

.SILENT:

###############################################################################
# Docker
# -----------------------------------------------------------------------------
.PHONY: up
up:
	@echo "bringing up project...."
	docker compose up

.PHONY: down
down:
	@echo "bringing down project...."
	docker compose down

.PHONY: bash
bash:
	@echo "connecting to container...."
	docker compose exec backend bash


###############################################################################
# Python Requirements
# -----------------------------------------------------------------------------
.PHONY: install
install:
	cd ./backend
	poetry install
	cd ..


###############################################################################
# Code Quality
# -----------------------------------------------------------------------------
.PHONY: black
black:
	black --version
	black --target-version py39 --line-length 99 backend

.PHONY: black-check
black-check:
	black --version
	black --target-version py39 --line-length 99 --check backend

.PHONY: isort
isort:
	isort --version-number
	isort examples backend

.PHONY: isort-check
isort-check:
	isort --version-number
	isort --check-only backend

.PHONY: format
format: black isort

.PHONY: flake8
flake8:
	flake8 --version
	flake8 backend

.PHONY: mypy
mypy:
	mypy --version
	mypy backend

.PHONY: pylint
pylint:
	pylint --version
	pylint backend/src

.PHONY: lint
lint: flake8 mypy pylint

.PHONY: bandit
bandit:
	bandit --version
	bandit --recursive backend/src


.PHONY: secure
secure: bandit # pip-audit

.PHONY: format-lint-secure
format-lint-secure: format lint secure


###############################################################################
# Tests
# -----------------------------------------------------------------------------
.PHONY: test-unit tu
test-unit tu:
	coverage run --include "backend/src/*" -m pytest "backend/tests/unittests"
	coverage report -m --skip-covered

.PHONY: test
test: test-unit