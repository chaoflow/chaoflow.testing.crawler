"""
chaoflow.testing.crawler.tests.py

1. Copy this file to your package:
   - either as `tests.py` into the root of your package
   - or as anything you like (e.g. test_crawler.py) into a subpackage `tests` in the root of your
     package
2. list additional files
"""

import re

from chaoflow.testing.crawler import create_test_suite

# File to test, relative to the package root
# all .py files are found
# all .txt files with corresponding .py file are found
files = [
        'README.txt'
        ]

pkgname = __name__ + '.'
pkgname = pkgname[:pkgname.rindex('.tests.')]

test_suite = create_test_suite(pkgname, files)
