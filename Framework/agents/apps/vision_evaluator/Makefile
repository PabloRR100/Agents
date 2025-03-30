SHELL = bash -o pipefail

# Mute output from all targets by default
.SILENT:

# The root directory of the repository as an absolute path
PROJECT_ROOT_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))


VENV_DIR := $(PROJECT_ROOT_DIR)/.venv
VENV_PYTHON := $(VENV_DIR)/bin/python


run-ui:
	$(VENV_PYTHON) -m streamlit run ui.py


run-api:
	echo "Running Python ${VENV_PYTHON}"
	$(VENV_PYTHON) -m uvicorn api:app --reload


