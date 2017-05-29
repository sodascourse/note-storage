default: sync-deps


# Dependency Management

sync-deps: compile-deps
	pip-sync requirements/dev.txt

sync-prod-deps: compile-deps
	pip-sync requirements/project.txt

compile-deps:
	pip-compile requirements/project.in
	pip-compile requirements/dev.in

clean:
	find . -name "*.pyc" -o -name __pycache__ | xargs rm -rf

test: clean
	pytest
