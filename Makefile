# Define variables
VENV_DIR := venv
REQUIREMENTS := requirements.txt

# Define the Python executable (customize this if needed)
PYTHON := python

# Target to create a virtual environment
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

# Target to install dependencies
install: $(VENV_DIR)
	$(VENV_DIR)\Scripts\pip.exe install -r $(REQUIREMENTS)

# Target to run the bot
run: $(VENV_DIR)
	$(VENV_DIR)\Scripts\python.exe bot.py

# Target to install a library and update the requirements file
install-lib:
	@echo "Installing specified library..."
	@install_lib.bat

# Target to remove a library and update the requirements file
remove-lib:
	@echo "Removing specified library..."
	@remove_lib.bat

# Combined target to create the virtual environment and install libraries
setup: install

# Phony targets
.PHONY: install setup
