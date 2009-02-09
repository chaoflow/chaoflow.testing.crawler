Check that all tests are found

    >>> from paula.testing.utils import saneimport, pkgpath, recursedir
    >>> from paula.testing.utils import ispackagedir
    >>> from paula.testing.testing import scanfordoctest
    >>> pkg = saneimport('paula.testing')
    >>> path = pkgpath(pkg)
    >>> l1 = recursedir(path,cond=ispackagedir,filefilter=scanfordoctest)
    >>> interact( locals())


A sample integration test, our zcml should have been loaded

XXX: currently not

#    >>> from paula.testing.module import ISomeObjectUtility

#    >>> u = getUtility(ISomeObjectUtility)
#    >>> u.name
#    'some object utility'


Thx to jensens you can get an interactive prompt in your tests
(waiting to be packaged as an egg!)

    >>> interact( locals() )


