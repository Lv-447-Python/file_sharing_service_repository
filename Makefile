.PHONY: help setup

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python3

.DEFAULT: help
all: setup test run

help:
	@echo "make setup"
	@echo "       full "
	@echo "make run"
	@echo "       run project"
	@echo "make lint"
	@echo "       run pylint and mypy"
	@echo "make test"
	@echo "       run tests"


setup: $(VENV_NAME)/bin/activate
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate
ifeq ($(wildcard /migrations/.*),)
	@echo "Found ~/migrations/."
	${PYTHON} manage.py db upgrade
	${PYTHON} manage.py db migrate
else
	make db_migrate
endif


db_migrate: $(VENV_NAME)/bin/activate
	${PYTHON} manage.py db init
	${PYTHON} manage.py db upgrade
	${PYTHON} manage.py db migrate

run: $(VENV_NAME)/bin/activate
	${PYTHON} app.py

test:
	@echo "Will be soon..."

lint: $(VENV_NAME)/bin/activate
	$(PYTHON) -m pylint file_sharing_service
