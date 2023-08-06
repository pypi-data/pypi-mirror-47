PyIGN, version 0.2.1 released on 2019-06-12
===========================================

|Build Status|

About
=====

The Python Ignite (PyIGN) package tool is used to interface with a
Nation Instruments (NI) data acquisition (DAQ) console on a liquid
rocket engine (LRE) test stand. PyIGN is fed input sensor data, gathered
by the NI DAQ, then computes and controls the LRE systems states. The
commands are output from PyIGN, back to the NI DAQ, which sets and
controls valve and ignitor states.

Installation
============

The PyIGN package relies on other libraries:

-  numpy
-  argparse

Install those before installing the PyIGN package. To install the PyIGN
package:

-  pip install pyign

More information can be found at:
https://devonburson.github.io/pyign/html/

Changelog
=========

All notable changes to the PyIGN project will be documented in this
file.

[Unreleased]
------------

[0.2.2] - 2019-06-11
--------------------

Added
~~~~~

-  version.py
-  CHANGELOG.md
-  setup.cfg

Changed
~~~~~~~

-  setup.py format
-  version to a version.py file

.. |Build Status| image:: https://travis-ci.org/SoftwareDevEngResearch/PyIGN.svg?branch=master
   :target: https://travis-ci.org/SoftwareDevEngResearch/PyIGN
