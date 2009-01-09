# paula.testing.tests.py
#
# You can simply copy this file to your package and adjust it to your needs
#
# pt.FunctionalDocFileSuite will load your package's ftesting.zcml and
# otherwise setup the same globs as pt.setUp - have a look at __init__.py
"""
"""

import unittest
from zope.testing import doctestunit
#from zope.component.testing import setUp

from paula.testing import get_test_suite
from paula.testing import setUp, tearDown

# XXX: this could be derived from __name__, but then it would not work,
# if being called as __main__ (see bottom) - is that needed?
# eventually we could then derive it from path?!
from config import PACKAGE_NAME

# File to test, relative to the package root
# all .py files are found
# all .txt files with corresponding .py file are found
files = [
        'README.txt'
        ]

test_suite = get_test_suite(PACKAGE_NAME, files)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
