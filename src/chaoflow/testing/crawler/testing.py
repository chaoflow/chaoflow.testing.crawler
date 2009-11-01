# Copyright (c) 2008-2009 by Florian Friesdorf
#
# Lesser General Public License (LGPL)
#
# This file is part of chaoflow.testing.crawler.
# 
# chaoflow.testing.crawler is free software: you can redistribute it and/or
# modify it under the terms of the Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# chaoflow.testing.crawler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# chaoflow.testing.crawler.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Florian Friesdorf <flo@chaoflow.net>"
__docformat__ = "plaintext"

import os
import unittest

#from zope.component import testing

from zope.testing import doctest
from zope.testing import doctestunit

from chaoflow.testing.crawler.utils import hasdoctests
from chaoflow.testing.crawler.utils import ispkgdir
from chaoflow.testing.crawler.utils import pkgpath
from chaoflow.testing.crawler.utils import recursedir
from chaoflow.testing.crawler.utils import saneimport

from chaoflow.testing.crawler.globs import test_globs

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
    #testing.setUp(test)
    for k,v in test_globs.items():
        test.globs[k] = v
    test.globs['testinstance'] = test

    def testfile(path):
        if not path.startswith(os.sep):
            path = os.sep.join(test.filename.split(os.sep)[:-1]+ [path,])
        return file(path)
    test.globs['testfile'] = testfile

def tearDown(test):
    """
    """
    #testing.tearDown(test)

def scanfordoctest(file):
    """Decides whether a file should be scanned for doctests

    - all .py files
    - all .txt files for which a .py file exists
    """
    # XXX: not reimplemented
    #        # skip if it starts with a dot
    #        if item.startswith('.'):
    #            continue

    if file.endswith('.py'):
        return hasdoctests(file)

    if file.endswith('.txt'):
        pyfile = file.replace('.txt','.py')
        if os.path.isfile(pyfile):
            if hasdoctests(file):
                # skip txt files that contain 'DISABLE_DOCTEST'
                # this is for testing/evaluation, untested and might change
                for line in open(file):
                    if line.lstrip().startswith('DISABLE_DOCTEST'):
                        return False
                return True

    return False
    

def create_test_suite(pkgname, files=[]):
    """construct a test suite for a package
    
    test suite will contain all doctests found somewhere in the package and
    the tests passed as argument
    
    1. get root folder for package
    2. recurse and find everything that might contain a doctest
    3. create the test suite

    """

    def testsuite(doctestfile):
        if doctestfile.endswith('.txt'):
            doctest = doctestunit.DocFileSuite(doctestfile,
                    package=pkgname,
                    setUp=setUp, tearDown=tearDown,
                    optionflags=optionflags,
                    )
            return doctest

        if doctestfile.endswith('.py'):
            module = doctestfile.replace('.py','').replace(os.sep, '.')
            module = '.'.join((pkgname, module,))
            module = saneimport(module)
            doctest = doctestunit.DocTestSuite(module,
                    setUp=setUp, tearDown=tearDown,
                    optionflags=optionflags,
                    )
            return doctest

    def fulltestsuite():
        """
        """
        pkg = saneimport(pkgname)
        path = pkgpath(pkg)

        doctestfiles = recursedir(
                path,
                cond=ispkgdir,
                filefilter=scanfordoctest,
                )
        # make relative to pkg path
        doctestfiles = [x[len(path)+1:] for x in doctestfiles]
        doctests = [testsuite(x) for x in doctestfiles+files]

        test_suite = unittest.TestSuite(doctests)
        return test_suite

    return fulltestsuite
