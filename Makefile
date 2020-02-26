.PHONY: install test run


install:
	@pip install -r requirements.txt

test:
	@pytest --verbose

run:
	@python -m cast ${ARGS}
