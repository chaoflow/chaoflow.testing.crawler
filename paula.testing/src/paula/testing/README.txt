A sample integration test, our zcml should have been loaded

    >>> from paula.testing.module import ISomeObjectUtility

    >>> u = getUtility(ISomeObjectUtility)
    >>> u.name
    'some object utility'


Thx to jensens you can get an interactive prompt in your tests
(waiting to be packaged as an egg!)

    >>> interact( locals() )
