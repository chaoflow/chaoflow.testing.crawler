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

def hasdoctests(file):
    """Check whether a file has doctests
    """
    for line in open(file):
        if line.lstrip().startswith('>>>'):
            return True


def ispkgdir(path):
    initfile = os.path.join(path, '__init__.py')
    result = os.path.isfile(initfile)
    return result


def pkgpath(pkg):
    """Returns the path to a imported package

        >>> pkg = saneimport('chaoflow.testing.crawler')
        >>> pkgpath(pkg).split(os.sep)[-3:]
        ['chaoflow', 'testing', 'crawler']
    """
    path = pkg.__file__.replace('.pyc','').replace('.py','')
    if not path.endswith('__init__'):
        raise ValueError
    path = path.replace(os.sep+'__init__', '')
    if path.endswith(os.sep):
        raise ValueError
    return path


def recursedir(path, cond=lambda x: True, filefilter=lambda x: True):
    """Recurses a directory structure and returns all contained files

    Optionally a condition can be given that must be met in order to recurse
    into a directory. The condition is a function that takes the directory as
    argument and returns either True or False.

        >>> from chaoflow.testing.crawler.utils import recursedir
        >>> pkg = saneimport('chaoflow.testing.crawler')
        >>> l1 = recursedir(pkgpath(pkg))
        >>> l1 = filter(lambda x: not x.endswith('.swp'), l1)
        >>> len(l1)
        30

        >>> l2 = recursedir(pkgpath(pkg), cond=ispkgdir)
        >>> l2 = filter(lambda x: not x.endswith('.swp'), l2)
        >>> len(l2)
        26
    """
    files=[]
    ls = os.listdir(path)
    for item in ls:
        fullpath = os.path.join(path, item)
        if os.path.isdir(fullpath):
            if cond(fullpath):
                files += recursedir(fullpath,cond,filefilter)
            continue
        if filefilter(fullpath):
            files.append(fullpath)
    return files


def saneimport(name):
    try:
        mod = __import__(name, globals())
    except Exception, e:
        # Somehow the traceback of ImportErrors gets screwed
        # quickfix, we just print it here
        import traceback
        traceback.print_exc()
        raise e
    components = name.split('.')
    for x in components[1:]:
         mod = getattr(mod, x)
    return mod
