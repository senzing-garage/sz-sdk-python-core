# Makefile extensions for linux.

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

SENZING_TOOLS_DATABASE_URL ?= sqlite3://na:na@/tmp/sqlite/G2C.db

# -----------------------------------------------------------------------------
# OS specific targets
# -----------------------------------------------------------------------------

.PHONY: clean-osarch-specific
clean-osarch-specific:
	@rm -rf /tmp/sqlite
	@rm -rf $(TARGET_DIRECTORY) || true
	@rm -f $(GOPATH)/bin/$(PROGRAM_NAME) || true


.PHONY: dependencies-osarch-specific
dependencies-osarch-specific:
	python3 -m pip install --upgrade pip
	pip install build psutil pytest pytest-cov pytest-schema virtualenv


.PHONY: hello-world-osarch-specific
hello-world-osarch-specific:
	@echo "Hello World, from linux."


.PHONY: setup-osarch-specific
setup-osarch-specific:
	@mkdir  /tmp/sqlite
	@cp testdata/sqlite/G2C.db /tmp/sqlite/G2C.db


.PHONY: test-osarch-specific
test-osarch-specific:
	@echo "--- Unit tests -------------------------------------------------------"
	@pytest tests/szconfigmanager_test.py --verbose --capture=no --cov=src/senzing --cov-report xml:coverage.xml
#	@echo "--- Test examples ----------------------------------------------------"
#	@pytest examples/ --verbose --capture=no --cov=src/senzing
	@echo "--- Test examples using unittest -------------------------------------"
	# @python3 -m unittest \
	# 	examples/szconfig/*.py \
	# 	examples/szconfigmanager/*.py \
	# 	examples/szdiagnostic/*.py \
	# 	examples/szengine/*.py \
	# 	examples/szproduct/*.py

.PHONY: test-examples
test-examples:
	@echo "--- Test examples using unittest -------------------------------------"
	@python3 -m unittest \
		examples/misc/add_truthset_datasources.py \
		examples/misc/add_truthset_data.py


.PHONY: view-sphinx-osarch-specific
view-sphinx-osarch-specific:
	@xdg-open file://$(MAKEFILE_DIRECTORY)/docs/build/html/index.html

# -----------------------------------------------------------------------------
# Makefile targets supported only by this platform.
# -----------------------------------------------------------------------------

.PHONY: only-linux
only-linux:
	@echo "Only linux has this Makefile target."
