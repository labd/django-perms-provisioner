.PHONY: install test


install:
	pip install -e .[test]

test:
	py.test

retest:
	py.test -vvv --lf

coverage:
	py.test --cov=django_perms_provisioner --cov-report=term-missing --cov-report=html

lint:
	flake8 src/
