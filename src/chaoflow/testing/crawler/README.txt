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

The output is not suitable to be used as a doctest. However, you can also run
it in a mode suitable for doctest generation:

    >>> ipshell( locals(), doctest=True)

or shorter:

    >>> dtipshell( locals())
