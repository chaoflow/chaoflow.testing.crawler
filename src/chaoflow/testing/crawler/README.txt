Check that all tests are found

    >>> from chaoflow.testing.crawler.testing import scanfordoctest
    >>> pkg = saneimport('chaoflow.testing.crawler')
    >>> path = pkgpath(pkg)
    >>> l1 = recursedir(path,cond=ispkgdir,filefilter=scanfordoctest)


Thx to jensens you can get an interactive prompt in your tests, iff interlude
is available:

    >>> interact( locals() )

The output is suitable to be used as a doctest.


Further, there is a fancier ipython based shell, iff chaoflow.testing.ipython
is avavailable:

    >>> ipshell( locals())

The output is suitable to be used as a doctest.


You can also run it with the real ipython prompt, where output is fancier but
cannot be used as a doctest:

    >>> ipshell( locals(), doctest=False)
