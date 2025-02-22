PYTHON = python3
PIP = pip3

.PHONY: init
init:
	virtualenv venv
	$(PIP) install -r requirements.txt

.PHONY: clean
clean:
	rmdir /s /q venv

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  init       - Install dependencies from requirements.txt"
	@echo "  clean      - Clean up Python cache files"
	@echo "  help       - Show this help message"