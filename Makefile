PYTHON=.venv/bin/python

all: PYTHON

test: PYTHON
	virtualenv -p python3 .venv
	$(PYTHON) test/test_ingde.py

PYTHON: setup.py
	virtualenv -p python3 .venv
	$(PYTHON) -m pip install pylint
	$(PYTHON) -m pip install mock
	$(PYTHON) -m pip install ofxstatement
	$(PYTHON) setup.py build --verbose
	$(PYTHON) -m pip install -e .
