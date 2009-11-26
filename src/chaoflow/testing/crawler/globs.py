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

from UserDict import UserDict
from UserList import UserList

from chaoflow.testing.crawler import utils

test_globs = dict(
        UserDict = UserDict,
        UserList = UserList,
        ispkgdir = utils.ispkgdir,
        pkgpath = utils.pkgpath,
        recursedir = utils.recursedir,
        saneimport = utils.saneimport,
        )
try:
    import interlude
except ImportError:
    pass
else:
    test_globs['interact'] = interlude.interact

try:
    import chaoflow.testing.ipython
except ImportError:
    pass
else:
    from chaoflow.testing.ipython import ipshell, dtipshell
    test_globs['ipshell'] = ipshell
    test_globs['dtipshell'] = dtipshell
