LINT_TARGET := . *.py


format-black:
	black ${LINT_TARGET}

format-isort:
	isort ${LINT_TARGET}

lint: lint-isort lint-black lint-flake8

lint-black:
	black --check --diff ${LINT_TARGET}

lint-flake8:
	flake8 --statistics ${LINT_TARGET}

lint-isort:
	isort --df -c ${LINT_TARGET} --skip
