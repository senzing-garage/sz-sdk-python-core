# Makefile extensions for linux.

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

PATH := $(MAKEFILE_DIRECTORY)/bin:$(PATH)
SENZING_TOOLS_DATABASE_URL ?= sqlite3://na:na@/tmp/sqlite/G2C.db

# -----------------------------------------------------------------------------
# OS specific targets
# -----------------------------------------------------------------------------

.PHONY: clean-osarch-specific
clean-osarch-specific:
	@rm -fr /tmp/sqlite || true
	@rm -f  $(MAKEFILE_DIRECTORY)/.coverage || true
	@rm -f  $(MAKEFILE_DIRECTORY)/coverage.xml || true
	@rm -fr $(DIST_DIRECTORY) || true
	@rm -fr $(MAKEFILE_DIRECTORY)/.mypy_cache || true
	@rm -fr $(MAKEFILE_DIRECTORY)/.pytest_cache || true
	@rm -fr $(MAKEFILE_DIRECTORY)/dist || true
	@rm -fr $(MAKEFILE_DIRECTORY)/docs/build || true
	@rm -fr $(MAKEFILE_DIRECTORY)/htmlcov || true
	@rm -fr $(TARGET_DIRECTORY) || true
	@find . | grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | xargs rm -rf


.PHONY: coverage-osarch-specific
coverage-osarch-specific: export SENZING_LOG_LEVEL=TRACE
coverage-osarch-specific:
	@$(activate-venv); pytest --cov=src --cov-report=xml  $(shell git ls-files '*.py')
	@$(activate-venv); coverage html
	@xdg-open $(MAKEFILE_DIRECTORY)/htmlcov/index.html 1>/dev/null 2>&1


.PHONY: dependencies-for-development-osarch-specific
dependencies-for-development-osarch-specific:

.PHONY: dependencies-for-documentation-osarch-specific
dependencies-for-documentation-osarch-specific:


.PHONY: documentation-osarch-specific
documentation-osarch-specific:
	@$(activate-venv); cd docs; rm -rf build; make html
	@xdg-open file://$(MAKEFILE_DIRECTORY)/docs/build/html/index.html  1>/dev/null 2>&1


.PHONY: hello-world-osarch-specific
hello-world-osarch-specific:
	$(info Hello World, from linux.)


.PHONY: package-osarch-specific
package-osarch-specific:
	@$(activate-venv); python3 -m build


.PHONY: setup-osarch-specific
setup-osarch-specific:
	@mkdir /tmp/sqlite
	@cp testdata/sqlite/G2C.db /tmp/sqlite/G2C.db


.PHONY: test-osarch-specific
test-osarch-specific:
	$(info --- Unit tests -------------------------------------------------------)
	@$(activate-venv); pytest tests/ --verbose --capture=no --cov=src --cov-report xml:coverage.xml
	$(info --- Test examples using pytest -------------------------------------)
	@$(activate-venv); pytest examples/szconfig/ \
		examples/szconfigmanager/ \
		examples/szdiagnostic/ \
		examples/szengine/ \
		examples/szproduct/ \
		examples/extras/ \
		examples/misc/ \
		--capture=no \
		-o python_files=*.py \
		--verbose; \
		pytest_exit_code="$$?"; \
		if [ "$$pytest_exit_code" -eq 5 ]; then \
			printf '\nExit code from pytest was %s, this is expected testing the examples if there were no Python errors\n' "$$pytest_exit_code"; \
			exit 0; \
		else \
			exit "$$pytest_exit_code"; \
		fi


.PHONY: venv-osarch-specific
venv-osarch-specific:
	@python3 -m venv .venv

# -----------------------------------------------------------------------------
# Makefile targets supported only by this platform.
# -----------------------------------------------------------------------------

.PHONY: only-linux
only-linux:
	$(info Only linux has this Makefile target.)
