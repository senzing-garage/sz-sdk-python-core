# Makefile extensions for windows.

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

SENZING_TOOLS_DATABASE_URL ?= sqlite3://na:na@nowhere/C:\Temp\sqlite\G2C.db

# -----------------------------------------------------------------------------
# OS specific targets
# -----------------------------------------------------------------------------

.PHONY: clean-osarch-specific
clean-osarch-specific:
	del /F /S /Q $(DIST_DIRECTORY)
	del /F /S /Q $(MAKEFILE_DIRECTORY)/.coverage
	del /F /S /Q $(MAKEFILE_DIRECTORY)/.mypy_cache
	del /F /S /Q $(MAKEFILE_DIRECTORY)/.pytest_cache
	del /F /S /Q $(MAKEFILE_DIRECTORY)/__pycache__
	del /F /S /Q $(MAKEFILE_DIRECTORY)/coverage.xml
	del /F /S /Q $(MAKEFILE_DIRECTORY)/dist
	del /F /S /Q $(MAKEFILE_DIRECTORY)/docs/build
	del /F /S /Q $(MAKEFILE_DIRECTORY)/htmlcov
	del /F /S /Q $(TARGET_DIRECTORY)


.PHONY: coverage-osarch-specific
coverage-osarch-specific: export SENZING_LOG_LEVEL=TRACE
coverage-osarch-specific:
	@pytest --cov=src --cov-report=xml  $(shell git ls-files '*.py')
	@coverage html
	@explorer $(MAKEFILE_DIRECTORY)/htmlcov/index.html


.PHONY: documentation-osarch-specific
documentation-osarch-specific:
	# @cd docs; rm -rf build; make html
	@explorer file://$(MAKEFILE_DIRECTORY)/docs/build/html/index.html


.PHONY: dependencies-osarch-specific
dependencies-osarch-specific:
	python3 -m pip install --upgrade pip
	pip install psutil pytest pytest-cov pytest-schema


.PHONY: hello-world-osarch-specific
hello-world-osarch-specific:
	$(info Hello World, from windows.)


.PHONY: package-osarch-specific
package-osarch-specific:
	@python3 -m build


.PHONY: setup-osarch-specific
setup-osarch-specific:
	@mkdir C:\Temp\sqlite
	@type nul > C:\Temp\sqlite\G2C.db


.PHONY: test-osarch-specific
test-osarch-specific:
	@echo "--- Unit tests -------------------------------------------------------"
	@pytest tests/ --verbose --capture=no --cov=src/senzing
	@echo "--- Test examples ----------------------------------------------------"
	@pytest examples/ --verbose --capture=no --cov=src/senzing


.PHONY: venv-osarch-specific
venv-osarch-specific:
	@python -m venv .venv

# -----------------------------------------------------------------------------
# Makefile targets supported only by this platform.
# -----------------------------------------------------------------------------

.PHONY: only-windows
only-windows:
	$(info Only windows has this Makefile target.)
