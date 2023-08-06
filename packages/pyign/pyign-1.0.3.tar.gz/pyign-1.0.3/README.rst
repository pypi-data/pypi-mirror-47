PyIGN, version 1.0.4 released on 2019-06-13
===========================================

|Build Status| |Coverage Status| |DOI|

About
=====

The Python Ignite (PyIGN) package tool is used to interface with a
Nation Instruments (NI) data acquisition (DAQ) console on a liquid
rocket engine (LRE) test stand. PyIGN is fed input sensor data, gathered
by the NI system, then computes and controls the LRE systems states. The
commands are output from PyIGN, back to the NI DAQ, which sets and
controls valve and ignitor states.

Example
=======

Navigate Installer folder or Example.rst

Once in pyign folder from command line:

-  python functions -s
-  python functions -g
-  python functions -t

Installation
============

The PyIGN package relies on other libraries: - numpy - argparse

Install those before installing the PyIGN package. To install the PyIGN
package:

-  pip install pyign

More information can be found at: https://github.com/devonburson/PyIGN

Changelog
=========

All notable changes to the PyIGN project will be documented in this
file.

[1.0.4] - 2019-06-13
--------------------

Changed
~~~~~~~

-  version.py
-  CHANGELOG.md
-  setup.cfg
-  README.md
-  

[Unreleased]
------------

.. _section-1:

[0.2.2] - 2019-06-11
--------------------

Added
~~~~~

-  version.py
-  CHANGELOG.md
-  setup.cfg

.. _changed-1:

Changed
~~~~~~~

-  setup.py format
-  version to a version.py file

.. |Build Status| image:: https://travis-ci.com/devonburson/PyIGN.svg?branch=master
   :target: https://travis-ci.com/devonburson/PyIGN
.. |Coverage Status| image:: https://coveralls.io/repos/github/devonburson/PyIGN/badge.svg?branch=master
   :target: https://coveralls.io/github/devonburson/PyIGN?branch=master
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3244879.svg
   :target: https://doi.org/10.5281/zenodo.3244879
