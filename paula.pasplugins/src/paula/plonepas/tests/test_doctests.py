# paula.testing.test_doctests.py
#
# Just put a copy of this in your tests subpackage and all your modules'
# doctests will be found recursively.
#
# There are several globs available, have a look at paula.testing.testing.py
"""
"""

import unittest
import doctest

from Testing import ZopeTestCase as ztc

from paula.testing import get_test_suite, test_globs

from paula.plonepas.tests import plone_base as base

# XXX: this could be derived from __name__, but then it would not work,
# if being called as __main__ (see bottom) - is that needed?
# eventually we could then derive it from path?!
from config import PACKAGE_NAME

tests = [
        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'README.txt', package='paula.plonepas',
            test_class=base.PaulaFunctionalTestCase,
            globs=test_globs,
            optionflags= \
                    doctest.NORMALIZE_WHITESPACE | \
                    doctest.ELLIPSIS),
    ]


test_suite = get_test_suite(PACKAGE_NAME, tests)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
