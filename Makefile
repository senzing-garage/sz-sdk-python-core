# Makefile for Python project

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
BUILD_TAG := $(shell git describe --always --tags --abbrev=0  | sed 's/v//')
BUILD_ITERATION := $(shell git log $(BUILD_TAG)..HEAD --oneline | wc -l | sed 's/^ *//')
BUILD_VERSION := $(shell git describe --always --tags --abbrev=0 --dirty  | sed 's/v//')
GIT_REMOTE_URL := $(shell git config --get remote.origin.url)
GIT_REPOSITORY_NAME := $(shell basename `git rev-parse --show-toplevel`)
GIT_VERSION := $(shell git describe --always --tags --long --dirty | sed -e 's/\-0//' -e 's/\-g.......//')
PATH := $(MAKEFILE_DIRECTORY)/bin:$(PATH)

# Conditional assignment. ('?=')
# Can be overridden with "export"
# Example: "export LD_LIBRARY_PATH=/path/to/my/senzing/er/lib"

LD_LIBRARY_PATH ?= /opt/senzing/er/lib
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

.PHONY: venv
venv: venv-osarch-specific


.PHONY: dependencies-for-development
dependencies-for-development: venv dependencies-for-development-osarch-specific
	$(activate-venv); \
		python3 -m pip install --upgrade pip; \
		python3 -m pip install --requirement development-requirements.txt


.PHONY: dependencies
dependencies: venv
	$(activate-venv); \
		python3 -m pip install --upgrade pip; \
		python3 -m pip install --requirement requirements.txt

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

.PHONY: setup
setup: setup-osarch-specific

# -----------------------------------------------------------------------------
# Lint
# -----------------------------------------------------------------------------

.PHONY: lint
lint: pylint mypy bandit black flake8 isort

# -----------------------------------------------------------------------------
# Build
# -----------------------------------------------------------------------------

.PHONY: docker-build
docker-build: docker-build-osarch-specific

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Test
# -----------------------------------------------------------------------------

.PHONY: test
test: test-osarch-specific


.PHONY: docker-test
docker-test:
	@$(activate-venv); docker-compose -f docker-compose.test.yaml up

# -----------------------------------------------------------------------------
# Coverage
# -----------------------------------------------------------------------------

.PHONY: coverage
coverage: coverage-osarch-specific

# -----------------------------------------------------------------------------
# Documentation
# -----------------------------------------------------------------------------

.PHONY: documentation
documentation: documentation-osarch-specific

# -----------------------------------------------------------------------------
# Package
# -----------------------------------------------------------------------------

.PHONY: package
package: clean package-osarch-specific

# -----------------------------------------------------------------------------
# Publish
# -----------------------------------------------------------------------------

.PHONY: publish-test
publish-test: package
	$(activate-venv); python3 -m twine upload --repository testpypi dist/*

# -----------------------------------------------------------------------------
# Clean
# -----------------------------------------------------------------------------

.PHONY: clean
clean: clean-osarch-specific

# -----------------------------------------------------------------------------
# Utility targets
# -----------------------------------------------------------------------------

.PHONY: help
help:
	$(info Build $(PROGRAM_NAME) version $(BUILD_VERSION)-$(BUILD_ITERATION))
	$(info Makefile targets:)
	@$(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs


.PHONY: print-make-variables
print-make-variables:
	@$(foreach V,$(sort $(.VARIABLES)), \
		$(if $(filter-out environment% default automatic, \
		$(origin $V)),$(info $V=$($V) ($(value $V)))))

# -----------------------------------------------------------------------------
# Specific programs
# -----------------------------------------------------------------------------

.PHONY: bandit
bandit:
	$(info --- bandit ---------------------------------------------------------------------)
	@bandit $(shell git ls-files '*.py' ':!:tests/*' ':!:docs/source/*' ':!:tools/*')


.PHONY: black
black:
	$(info --- black ----------------------------------------------------------------------)
	@black $(shell git ls-files '*.py' ':!:tests/*' ':!:docs/source/*' ':!:tools/*')


.PHONY: flake8
flake8:
	$(info --- flake8 ---------------------------------------------------------------------)
	@flake8 $(shell git ls-files '*.py' ':!:docs/source/*' ':!:tools/*')


.PHONY: isort
isort:
	$(info --- isort ----------------------------------------------------------------------)
	@isort $(shell git ls-files '*.py' ':!:docs/source/*' ':!:tools/*')


.PHONY: mypy
mypy:
	$(info --- mypy -----------------------------------------------------------------------)
	# @mypy --strict $(shell git ls-files '*.py' ':!:docs/source/*' ':!:tools/*')
	@$(activate-venv); @mypy --strict $(shell git ls-files '*.py' ':!:docs/source/*' ':!:tools/*' ':!:examples/*')


.PHONY: pydoc
pydoc:
	$(info --- pydoc ----------------------------------------------------------------------)
	@$(activate-venv); python3 -m pydoc


.PHONY: pydoc-web
pydoc-web:
	$(info --- pydoc-web ------------------------------------------------------------------)
	@$(activate-venv); python3 -m pydoc -p 8885


.PHONY: pylint
pylint:
	$(info --- pylint ---------------------------------------------------------------------)
	@$(activate-venv); @pylint $(shell git ls-files '*.py' ':!:docs/source/*' ':!:tools/*')


.PHONY: pytest
pytest:
	$(info --- pytest ---------------------------------------------------------------------)
	@$(activate-venv); pytest $(shell git ls-files '*.py' ':!:docs/source/*')


.PHONY: sphinx
sphinx: sphinx-osarch-specific
	$(info --- sphinx ---------------------------------------------------------------------)


.PHONY: view-sphinx
view-sphinx: view-sphinx-osarch-specific
	$(info --- view-sphinx ----------------------------------------------------------------)
