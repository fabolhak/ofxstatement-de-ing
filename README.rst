~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ING DiBa Germany plugin for ofxstatement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project provides a custom plugin for ofxstatement for ING (Germany / Deutschland). It is based
on the work done by jbbandos (https://github.com/jbbandos/ofxstatement-be-ing).

`ofxstatement`_ is a tool to convert proprietary bank statement to OFX format,
suitable for importing to GnuCash. Plugin for ofxstatement parses a
particular proprietary bank statement format and produces common data
structure, that is then formatted into an OFX file.

.. _ofxstatement: https://github.com/kedder/ofxstatement


Users of ofxstatement have developed several plugins for their banks. They are
listed on main `ofxstatement`_ site. If your bank is missing, you can develop
your own plugin.


Usage
=====
$ ofxstatement convert -t ingde input.csv output.ofx
