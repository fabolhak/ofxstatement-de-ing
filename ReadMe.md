# ING DiBa Germany plugin for ofxstatement

This project provides a custom plugin for ofxstatement for ING (Germany / Deutschland).
It is based on the work done by [jbbandos](https://github.com/jbbandos/ofxstatement-be-ing).

[ofxstatement](https://github.com/kedder/ofxstatement) is a tool to convert proprietary bank statement to OFX format,
suitable for importing to GnuCash. Plugin for ofxstatement parses a particular proprietary bank statement format and
produces common data structure, that is then formatted into an OFX file. Users of ofxstatement have developed several
plugins for their banks. They are listed on the main `ofxstatement` site. If your bank is missing, you can develop your
own plugin.

This plugin supports *.csv exports from ING DiBa (Germany).

**Important**: Exported csv files must include Saldo!

## Install

Clone:

```bash
git clone https://github.com/fabolhak/ofxstatement-de-ing
cd ofxstatement-de-ing
```

Method 1: Install in Python [virtual environment](https://docs.python.org/3/tutorial/venv.html):

```bash
make
```

Method 2: Install system-wide via [pip](https://packaging.python.org/guides/tool-recommendations/):

```bash
sudo pip install -e .
```

## Usage

Method 1: Run in virtual environment:

```bash
source .venv/bin/activate
ofxstatement convert -t ingde input.csv output.ofx
```

Method 2: Run system-wide:

```bash
ofxstatement convert -t ingde input.csv output.ofx
```
