.PHONY: install test

ROOT_PATH=$(shell pwd)

install:
	@pip install -r requirements.txt

test:
	@pytest --verbose
