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
import unittest

from zope.app.testing.functional import ZCMLLayer, FunctionalDocFileSuite
from zope.component import testing

from zope.testing import doctest
from zope.testing import doctestunit

# --- stuff for globs -------------------------------------------------

from UserDict import UserDict
from UserList import UserList

from zope.component import provideAdapter, provideUtility
from zope.component import adapts
from zope.component import getUtility, queryUtility
from zope.component import getSiteManager

from zope.interface import alsoProvides, implements, providedBy
from zope.interface import Interface, Attribute

from paula.testing import interact

class Mock(object):
    """a mock object that carries desired interfaces

        >>> class IA(Interface):
        ...     pass

        >>> class IB(Interface):
        ...     pass

        >>> m = Mock( a = 1, f = lambda : 2, alsoProvides=(IA,IB))
        >>> m.a
        1
        >>> m.f()
        2
        >>> IA.providedBy(m)
        True
    """
    implements(Interface)
    def __init__(self, **kwargs):
        if kwargs.has_key('alsoProvides'):
            alsoProvides(self, *kwargs['alsoProvides'])
            del kwargs['alsoProvides']
        for k,v in kwargs.items():
            setattr(self, k, v)

test_globs = dict(
        Attribute = Attribute,
        Interface = Interface,
        Mock = Mock,
        UserDict = UserDict,
        UserList = UserList,
        adapts = adapts,
        alsoProvides = alsoProvides,
        getUtility = getUtility,
        getSiteManager = getSiteManager,
        interact = interact.interact,
        implements = implements,
        provideAdapter = provideAdapter,
        provideUtility = provideUtility,
        providedBy = providedBy,
        queryUtility = queryUtility,
        )

def setUp(test):
    """We can use this to set up anything that needs to be available for
    each test. It is run before each test, i.e. for each docstring that
    contains doctests.
    
    Look at the Python unittest and doctest module documentation to learn 
    more about how to prepare state and pass it into various tests.

        >>> m = Mock()
        >>> class IA(Interface):
        ...     pass

        >>> alsoProvides(m, IA)
        >>> providedBy(m) is not None
        True

        >>> provideUtility(m, IA)

        >>> class A(object):
        ...     adapts(Interface)
        ...     implements(IA)

        >>> provideAdapter(A)
    """
    testing.setUp(test)
    for k,v in test_globs.items():
        test.globs[k] = v


def tearDown(test):
    """
    """
    testing.tearDown(test)


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for x in components[1:]:
         mod = getattr(mod, x)
    return mod


def recurse(*args):
    """returns all modules, that contain doctests

    returns all doctests found within the modules passed in *args

    For paula.testing itself, recurse should find 8 modules containing tests:

        >>> to_test = recurse('paula.testing')
        >>> len(to_test)
        9
    """
    result = []
    for name in args:
        mod = my_import(name)
        result += [mod]
        modname = mod.__file__.replace('.pyc','').replace('.py','')
        if modname.endswith('__init__'):
            # a subpackage
            dirname = os.path.dirname(mod.__file__)
            dirlist = os.listdir(dirname)
            # iterate over content of current directory
            for x in dirlist:
                fullpath = os.path.join(dirname, x)
                # if neither directory nor .py file, skip it
                if not (os.path.isdir(fullpath) or x.endswith('.py')):
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
                if x == "tests":
                    continue

                mod_name = '%s.%s' % (name, x)
                result += recurse(mod_name)
    return result


# XXX: this could be moved inside the SuiteGenerator
def get_test_suite(pkg_name, tests=[]):
    """construct a test suite for a package
    
    recurses through a package and returns a test suite consisting of all
    doctest found + the tests passed as argument
    """
    def test_suite():
        to_test = recurse(pkg_name,)
        optionflags = \
                doctest.REPORT_ONLY_FIRST_FAILURE + \
                doctest.ELLIPSIS + \
                doctest.NORMALIZE_WHITESPACE
        unit_tests = []
        for x in to_test:
            unit_test = doctestunit.DocTestSuite(x,
                    setUp=setUp, tearDown=tearDown,
                    optionflags=optionflags
                    )
            unit_tests.append(unit_test)
        test_suite = unittest.TestSuite(unit_tests + tests)
        return test_suite

    return test_suite


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

