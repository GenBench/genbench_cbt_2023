.PHONY: quality style

# Check that source code meets quality standards
# Adapted from https://github.com/huggingface/evaluate/blob/main/Makefile

quality:
	black --check --line-length 119 --target-version py36 tests src metrics comparisons measurements
	isort --check-only tests src metrics measurements
	flake8 tests src metrics

# Format source code automatically

style:
	black --line-length 119 --target-version py38 tests src
	#isort tests src