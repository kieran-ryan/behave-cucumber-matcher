.PHONY: build
init:
	python -m venv venv
	. venv/bin/activate && pip install --requirement requirements-dev.txt

build:
	pip install build
	python -m build
