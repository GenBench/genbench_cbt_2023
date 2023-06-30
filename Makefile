.PHONY: quality style

# Check that source code meets quality standards
# Adapted from https://github.com/huggingface/evaluate/blob/main/Makefile

check-quality:
	black --check --line-length 119 --target-version py38 tests src
	isort --check-only tests src
	flake8 tests src

# Format source code automatically

style:
	black --line-length 119 --target-version py38 tests src
	isort tests src