.PHONY: install lint clean

# Installation section
install:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt

# Linting section
lint:
	pylint **/*.py
	black --check .
	flake8 .
