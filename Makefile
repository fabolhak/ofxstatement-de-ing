PYTHON=.venv/bin/python

all: PYTHON

PYTHON: setup.py
	virtualenv -p python3 --no-site-packages .venv
	$(PYTHON) -m pip install pylint
	$(PYTHON) -m pip install mock
	$(PYTHON) setup.py develop
