.. image:: https://travis-ci.org/mozilla-releng/signtool.svg?branch=master
    :target: https://travis-ci.org/mozilla-releng/signtool

.. image:: https://coveralls.io/repos/github/mozilla-releng/signtool/badge.svg?branch=master
    :target: https://coveralls.io/github/mozilla-releng/signtool?branch=master

This repository contains the tool ``signtool`` used by Mozilla Release Engineering, but forked to support python 3 with requests.

The original copy of signtool is `here`_

.. _here: https://github.com/mozilla/build-tools/blob/master/release/signing/signtool.py

To run tests::

    pip install tox
    tox
