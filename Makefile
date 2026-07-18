.PHONY: test compile example check

compile:
	python -m compileall -q src tests examples

test:
	python -m unittest discover -s tests -v

example:
	python examples/union_closed_bootstrap.py

check: compile test example
