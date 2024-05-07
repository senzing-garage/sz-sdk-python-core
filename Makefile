# Git variables

# Detect the operating system and architecture.

include makefiles/osdetect.mk

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

# "Simple expanded" variables (':=')

# PROGRAM_NAME is the name of the GIT repository.
PROGRAM_NAME := $(shell basename `git rev-parse --show-toplevel`)
MAKEFILE_PATH := $(abspath $(firstword $(MAKEFILE_LIST)))
MAKEFILE_DIRECTORY := $(shell dirname $(MAKEFILE_PATH))
TARGET_DIRECTORY := $(MAKEFILE_DIRECTORY)/target
DIST_DIRECTORY := $(MAKEFILE_DIRECTORY)/dist
BUILD_VERSION := $(shell git describe --always --tags --abbrev=0 --dirty  | sed 's/v//')
BUILD_TAG := $(shell git describe --always --tags --abbrev=0  | sed 's/v//')
BUILD_ITERATION := $(shell git log $(BUILD_TAG)..HEAD --oneline | wc -l | sed 's/^ *//')
GIT_REMOTE_URL := $(shell git config --get remote.origin.url)
GO_PACKAGE_NAME := $(shell echo $(GIT_REMOTE_URL) | sed -e 's|^git@github.com:|github.com/|' -e 's|\.git$$||' -e 's|Senzing|senzing|')
PATH := $(MAKEFILE_DIRECTORY)/bin:$(PATH)

# Conditional assignment. ('?=')
# Can be overridden with "export"
# Example: "export LD_LIBRARY_PATH=/path/to/my/senzing/g2/lib"

LD_LIBRARY_PATH ?= /opt/senzing/g2/lib
PYTHONPATH ?= $(MAKEFILE_DIRECTORY)/src

# Export environment variables.

.EXPORT_ALL_VARIABLES:

# -----------------------------------------------------------------------------
# The first "make" target runs as default.
# -----------------------------------------------------------------------------

.PHONY: default
default: help

# -----------------------------------------------------------------------------
# Operating System / Architecture targets
# -----------------------------------------------------------------------------

-include makefiles/$(OSTYPE).mk
-include makefiles/$(OSTYPE)_$(OSARCH).mk


.PHONY: hello-world
hello-world: hello-world-osarch-specific

# -----------------------------------------------------------------------------
# Dependency management
# -----------------------------------------------------------------------------

.PHONY: dependencies
dependencies: dependencies-osarch-specific

# -----------------------------------------------------------------------------
# build
# -----------------------------------------------------------------------------

.PHONY: package
package: clean
	python3 -m build

# -----------------------------------------------------------------------------
# publish
# -----------------------------------------------------------------------------

.PHONY: publish-test
publish-test: package
	python3 -m twine upload --repository testpypi dist/*

# -----------------------------------------------------------------------------
# Test
# -----------------------------------------------------------------------------

.PHONY: test
test: test-osarch-specific


.PHONY: bandit
bandit:
	@bandit $(shell git ls-files '*.py'  ':!:docs/source/*' ':!:tests/*' ':!:tools/*')


.PHONY: coverage
coverage: coverage-osarch-specific


.PHONY: black
black:
	@black $(shell git ls-files '*.py'  ':!:docs/source/*' ':!:tests/*' ':!:tools/*')


.PHONY: flake8
flake8:
	@flake8 $(shell git ls-files '*.py'  ':!:docs/source/*' ':!:tools/*')


.PHONY: isort
isort:
	@isort $(shell git ls-files '*.py'  ':!:docs/source/*' ':!:tools/*')


.PHONY: mypy
mypy:
	@mypy --strict $(shell git ls-files '*.py' ':!:docs/source/*' ':!:tools/*')


.PHONY: pylint
pylint:
	@pylint $(shell git ls-files '*.py'  ':!:docs/source/*' ':!:tools/*')


.PHONY: pytest
pytest:
	@pytest --cov=src/senzing --cov-report=xml  $(shell git ls-files '*.py'  ':!:docs/source/*' ':!:tools/*')

# -----------------------------------------------------------------------------
# Documentation
# -----------------------------------------------------------------------------

.PHONY: pydoc
pydoc:
	python3 -m pydoc


.PHONY: pydoc-web
pydoc-web:
	python3 -m pydoc -p 8885


.PHONY: sphinx
sphinx:
	@cd docs; rm -rf build; make html


.PHONY: view-sphinx
view-sphinx: view-sphinx-osarch-specific

# -----------------------------------------------------------------------------
# Utility targets
# -----------------------------------------------------------------------------

.PHONY: clean
clean: clean-osarch-specific


.PHONY: help
help:
	@echo "Build $(PROGRAM_NAME) version $(BUILD_VERSION)-$(BUILD_ITERATION)".
	@echo "Makefile targets:"
	@$(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs


.PHONY: print-make-variables
print-make-variables:
	@$(foreach V,$(sort $(.VARIABLES)), \
		$(if $(filter-out environment% default automatic, \
		$(origin $V)),$(warning $V=$($V) ($(value $V)))))


.PHONY: setup
setup: setup-osarch-specific