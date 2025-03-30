SHELL = bash -o pipefail

# Mute output from all targets by default
.SILENT:

# The root directory of the repository as an absolute path
PROJECT_ROOT_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

VENV_DIR := $(PROJECT_ROOT_DIR)/.venv
VENV_PIP := $(VENV_DIR)/bin/pip
VENV_PYTHON := $(VENV_DIR)/bin/python

.PHONY: log
log:
	echo "PROJECT_ROOT_DIR: ${PROJECT_ROOT_DIR}"


.PHONY: lock
lock: log
	uv pip compile pyproject.toml --all-extras --generate-hashes > uv.lock


.PHONY: release
release:
	uv ...


.PHONY: run-ui
run-ui:
	$(VENV_PYTHON) -m streamlit run ui.py


.PHONY: run-api
run-api:
	echo "Running Python ${VENV_PYTHON}"
	$(VENV_PYTHON) -m uvicorn api:app --reload


.PHONY: build-api-image
build-api-image:
	docker build -t vision-evaluator:latest .
