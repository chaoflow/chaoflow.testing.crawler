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

from paula.testing.testing import get_test_suite
from paula.testing.testing import test_globs
from paula.testing.testing import SuiteGenerator
from paula.testing.testing import setUp, tearDown
from paula.testing.testing import my_import
try:
    from paula.testing.plonetesting import setup_package
    from paula.testing.plonetesting import setupPloneSite
    from paula.testing.plonetesting import PloneTestCase
    from paula.testing.plonetesting import FunctionalTestCase
    from paula.testing.plonetesting import PanelTestCase
    from paula.testing.plonetesting import KSSTestCase
except ImportError:
    # no plone testing possible
    pass
