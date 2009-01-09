# Copyright (c) 2008 by Florian Friesdorf
#
# GNU Affero General Public License (AGPL)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
"""
"""
__author__ = "Florian Friesdorf <flo@chaoflow.net>"
__docformat__ = "plaintext"

import os
import os.path
import types
import unittest

from zope.app.testing.functional import ZCMLLayer, FunctionalDocFileSuite
from zope.component import testing

from zope.testing import doctest
from zope.testing import doctestunit

from paula.testing.utils import saneimport, hasdoctests
from paula.testing.globs import test_globs

optionflags = \
        doctest.REPORT_ONLY_FIRST_FAILURE + \
        doctest.ELLIPSIS + \
        doctest.NORMALIZE_WHITESPACE


def setUp(test):
    """We can use this to set up anything that needs to be available for
    each test. It is run before each test, i.e. for each docstring that
    contains doctests.
    
    Look at the Python unittest and doctest module documentation to learn 
    more about how to prepare state and pass it into various tests.
    """
    testing.setUp(test)


def tearDown(test):
    """
    """
    testing.tearDown(test)

# ------------------------------------------------------------------------

def recurse(*args):
    """
    returns all doctests found within the modules passed in *args

    That is:
        - modules containing doctests
        - text files named after modules, containing doctests

    For paula.testing itself, recurse should find 9 modules containing tests:

        >>> to_test = recurse('paula.testing')
        >>> len(to_test)
        9
    """
    result = []
    for modname in args:
        # import module and append to result, iff it contains doctests
        mod = saneimport(modname)
        if hasdoctests(mod):
            result.append(mod)

        # Check module vs package
        realmodname = mod.__file__.replace('.pyc','').replace('.py','')
        if not realmodname.endswith('__init__'):
            # a module, not a package, we can stop recursing here
            continue

        # list package contents and evtl. recurse further
        dirname = os.path.dirname(mod.__file__)
        dirlist = os.listdir(dirname)
        for item in dirlist:
            fullpath = os.path.join(dirname, item)
            # skip, if neither directory nor .py file nor txt file
            if not os.path.isdir(fullpath):
                if not item.endswith('.py')):
                continue

            # skip directories, that are not packages
            if os.path.isdir(fullpath) and not \
               os.path.isfile(os.path.join(fullpath, '__init__.py')): 
                continue
        
            # get rid of .py ending
            x = x.replace('.py','')

            # skip if it starts with a dot
            if x.startswith('.'):
                continue

            # skip __init__.py, it _is_ the current package, which was
            # added above: result += [mod]
            if x == "__init__":
                continue

            # don't test tests/ and tests.py, XXX: why not?
            #if x == "tests":
            #    continue

            mod_name = '%s.%s' % (name, x)
            result += recurse(mod_name)
    return result


def doctestsuite(mod):
    return doctestunit.DocTestSuite(mod,
            setUp=setUp, tearDown=tearDown,
            optionflags=optionflags
            )

def testsuite(*args):
    """
    """
    testsuites = []
    for pkgname in args:
        mod = saneimport(pkgname)
        if hasdoctests(mod):
            testsuites.append(doctestsuite(mod))

        # Only recurse for packages, for modules continue with next loop
        if not '__init__' in mod.__file__:
            continue


    XXX

        if txtfile:
            if not hasdoctests(txtfile):
                return []

            testsuite = doctestunit.DocFileSuite( txtfile
                    package=pkgname,
                    setUp=setUp, tearDown=tearDown,
                    optionflags=optionflags
                    )
            return testsuite



# XXX: this could be moved inside the SuiteGenerator
def get_test_suite(pkg_name, tests=[]):
    """construct a test suite for a package
    
    recurses through a package and returns a test suite consisting of all
    doctest found + the tests passed as argument
    """
    def testsuite(x):
        if type(x) == types.ModuleType:
            return doctestunit.DocTestSuite(x,
                    setUp=setUp, tearDown=tearDown,
                    optionflags=optionflags
                    )

        if type(x) == types.StringTypes:
            return doctestunit.DocFileSuite( XXX
                    package=XXX,
                    setUp=setUp, tearDown=tearDown,
                    optionflags=optionflags
                    )
    def fulltestsuite():
        to_test = recurse(pkg_name,)
        testsuites = [testsuite(x) for x in to_test]
        for x in to_test:
            test = doctestunit.DocFileSuite( XXX
                    package=XXX,
                    setUp=setUp, tearDown=tearDown,
                    optionflags=optionflags
                    )
            unit_tests.append(test)

        test_suite = unittest.TestSuite(unit_tests + tests)
        return test_suite

    return fulltestsuite


# TestSuite/Cases loading ftesting.zcml
# taken from a zopeproject generated testing.py - thank you

#ftesting_zcml = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
#FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer')

class SuiteGenerator(object):
    """
    """
    def __init__(self, package_name):
        self.package_name = package_name
        self.package = my_import(package_name)
        self.package_dir = os.path.dirname(self.package.__file__)
        self.ftesting_zcml = os.path.join(self.package_dir, 'ftesting.zcml')
        try:
            self.FunctionalLayer = ZCMLLayer(
                    self.ftesting_zcml,
                    package_name, 
                    'FunctionalLayer',
                    allow_teardown=True,
                    )
        except TypeError:
            self.FunctionalLayer = ZCMLLayer(
                    self.ftesting_zcml,
                    package_name, 
                    'FunctionalLayer',
                    )

    @property
    def FunctionalDocFileSuite(self):

        def myFunctionalDocFileSuite(path, **kw):
            if not 'package' in kw:
                kw['package'] = self.package_name
            suite = FunctionalDocFileSuite(path, globs=test_globs, **kw)
            suite.layer = self.FunctionalLayer
            return suite

        return myFunctionalDocFileSuite



# we currently don't care about these

#class FunctionalTestCase(FunctionalTestCase):
#    layer = FunctionalLayer


#def FunctionalDocTestSuite(module=None, **kw):
#    module = doctest._normalize_module(module)
#    suite = FunctionalDocTestSuite(module, globs=test_globs, **kw)
#    suite.layer = FunctionalLayer
#    return suite

