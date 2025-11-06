.PHONY: install lint clean format test all

all: install lint test

# Installation section
install:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt

# Linting section
lint:
	pylint --disable=C0114,C0115,C0116 **/*.py 
	black --check .
	flake8 .

# Testing section
test:
	@echo "→ Running tests with pytest"
	pytest -q --disable-warnings --maxfail=1

# Cleaning section
clean:
	@echo "→ Cleaning temporary files"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov dist build *.egg-info || true
	@echo "✓ Clean complete"

# Code formatting section
format:
	@echo "→ Formatting code with Black"
	black app
