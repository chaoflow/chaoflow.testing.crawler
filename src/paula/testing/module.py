from zope.interface import implements, Interface

class ISomeObjectUtility(Interface):
    pass

class SomeObject(object):
    """
    This is an example test, that just should be found by paula.testing

        >>> 1 + 1
        2
    """
    implements(ISomeObjectUtility)
    name = 'some object utility'
