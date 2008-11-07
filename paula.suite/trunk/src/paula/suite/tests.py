# paula.testing.tests.py
#
# You can simply copy this file to your package and adjust it to your needs
#
# pt.FunctionalDocFileSuite will load your package's ftesting.zcml and
# otherwise setup the same globs as pt.setUp - have a look at __init__.py
"""
"""

import unittest
#from zope.testing import doctestunit
#from zope.component.testing import setUp

from paula.testing import get_test_suite, SuiteGenerator

# XXX: this could be derived from __name__, but then it would not work,
# if being called as __main__ (see bottom) - is that needed?
# eventually we could then derive it from path?!
from config import PACKAGE_NAME

sg = SuiteGenerator(PACKAGE_NAME)

tests = [
    # doctests in all submodules of the package are found by paula.testing

    # doctests in files need to be declared
    #doctestunit.DocFileSuite( 'README.txt',
    #       package=PACKAGE_NAME, setUp=pt.setUp, tearDown=pt.tearDown
    #       ),

    # functional doctests in files, don't pass setUp/tearDown, except if you
    # really know what you are doing...
    sg.FunctionalDocFileSuite('README.txt')

    ]

test_suite = get_test_suite(PACKAGE_NAME, tests)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
