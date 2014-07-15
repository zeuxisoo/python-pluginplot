.PHONY: install test clean clean-pyc

all:
	@echo "make install"
	@echo "make test"

install:
	virtualenv-2.7 --no-site-package venv
	source venv/bin/activate && pip install -r requirements.txt

test:
	py.test tests

clean: clean-build clean-pyc

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

create-dist: clean
	@python setup.py sdist

setup-develop:
	python setup.py develop

upload-dist:
	@python setup.py sdist upload

register-dist:
	@python setup.py register
