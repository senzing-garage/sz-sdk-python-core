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
	@pytest --cov=src --cov-report=xml $(shell git ls-files '*.py')
	@coverage html
	@xdg-open $(MAKEFILE_DIRECTORY)/htmlcov/index.html


.PHONY: documentation-osarch-specific
documentation-osarch-specific:
	@cd docs; rm -rf build; make html
	@xdg-open file://$(MAKEFILE_DIRECTORY)/docs/build/html/index.html


.PHONY: hello-world-osarch-specific
hello-world-osarch-specific:
	$(info Hello World, from linux.)


.PHONY: package-osarch-specific
package-osarch-specific:
	@python3 -m build


.PHONY: setup-osarch-specific
setup-osarch-specific:
	@mkdir  /tmp/sqlite
	@cp testdata/sqlite/G2C.db /tmp/sqlite/G2C.db


.PHONY: test-osarch-specific
test-osarch-specific:
	@echo "--- Unit tests -------------------------------------------------------"
	@pytest tests/ --verbose --capture=no --cov=src/senzing --cov-report xml:coverage.xml
	# @echo "--- Test examples ----------------------------------------------------"
	# @pytest examples/ --verbose --capture=no
	@echo "--- Test examples using unittest -------------------------------------"
	@python3 -m unittest \
		examples/szconfig/*.py \
		examples/szconfigmanager/*.py \
		examples/szdiagnostic/*.py \
		examples/szengine/*.py \
		examples/szproduct/*.py


.PHONY: test-examples
test-examples:
	@echo "--- Test examples using unittest -------------------------------------"
	@python3 -m unittest \
		examples/misc/add_truthset_datasources.py \
		examples/misc/add_truthset_data.py

# -----------------------------------------------------------------------------
# Makefile targets supported only by this platform.
# -----------------------------------------------------------------------------

.PHONY: only-linux
only-linux:
	$(info Only linux has this Makefile target.)
