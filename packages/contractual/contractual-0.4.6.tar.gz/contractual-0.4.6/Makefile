RELEASE_TYPE ?= patch

format:
	black .

lint:
	black --check .

test: lint
	pytest --cov=contractual tests

publish:
	python setup.py sdist bdist_wheel
	twine upload -u ${PYPI_USER} -p ${PYPI_PASS} dist/*
