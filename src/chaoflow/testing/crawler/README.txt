Check that all tests are found

    >>> from chaoflow.testing.crawler.testing import scanfordoctest
    >>> pkg = saneimport('chaoflow.testing.crawler')
    >>> path = pkgpath(pkg)
    >>> l1 = recursedir(path,cond=ispkgdir,filefilter=scanfordoctest)
    >>> interact( locals())


Thx to jensens you can get an interactive prompt in your tests:

    >>> interact( locals() )


