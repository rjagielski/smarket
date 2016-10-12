help:
	@echo "    init"
	@echo "        install dependencies with pip"
	@echo "    freeze"
	@echo "        pip freeze and save, keep requirements order"
	@echo "    test"
	@echo "        Run pytest"

init:
	pip install --upgrade pip
	pip install -r requirements.txt

freeze:
	pip freeze -r requirements.txt > requirements.txt

run:
	python run.py

test:
	pytest
