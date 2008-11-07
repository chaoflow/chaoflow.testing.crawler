paula.suite package Readme
==========================

This file serves for documentation and integration testing of all zope3
based paula packages with a PAU:
    - zope.app.authentication.authentication.PluggableAuthentication
    - paula.authentication
    - paula.authutil
    - paula.properties, not yet
    - paula.proputil, not yet
    - paula.groups, not yet
    - paula.grouputil, not yet
    - paula.examples

If you install paula.suite, by calling the apropriate functions, you will
end up with all of these (except paula.examples, which is just pulled in
for testing) in a 'paula' subfolder of a folder of your choice (see below)

Let's start out with a folder hierarchy containing two nested sites.

    >>> from zope.app.folder import Folder
    >>> from zope.app.component import site

    >>> class SubSiteFolder(Folder, site.SiteManagerContainer):
    ...     pass
    >>> subsite = SubSiteFolder()
    >>> subsm = site.LocalSiteManager(subsite)
    >>> subsite.setSiteManager(subsm)

    >>> root = getRootFolder()
    >>> root['subsite'] = subsite

Make sure that we are really dealing with two different component
registries:

    >>> getSiteManager(root) is not getSiteManager(subsite)
    True


Let's add a paula.suite, we want it to create a PAU with a kind of fake
credentials plugin, that allows the PAU to authenticate against plain
mappings.

    >>> from paula.suite import createPaulaSuite
 
# This is currently not true, but leads to a mess-up
#If we don't pass a container, createPauleSuite registers globally, which
#should be found from the root site manager

#    >>> createPaulaSuite(create_pau=True, create_credplugin=True)
    >>> createPaulaSuite(root, create_pau=True, create_credplugin=True)
    >>> createPaulaSuite(subsite, create_pau=True, create_credplugin=True)


We have now two nested sites, each with a full paula suite. If we add
content, that suffice paula's criteria, it should end up in the
corresponding suite and enable authentication.

Suitable content is for example MinimalPloneUser from paula.examples, which
we use here (@zope: sorry, no offense meant ;). user1 is added on the upper
level and should end up in root's suite, user2 to the contained level and
should end up in the subsite's suite:

    >>> from zope.component import createObject

    >>> user1 = createObject('paula.examples.MinimalPloneUser',
    ...         title='user1',
    ...         password='pass1',
    ...         email='user1@bar.com',
    ...         realname='User One',
    ...         )
    >>> user1_cred = UserDict(login='user1', password='pass1')
    >>> root['user1'] = user1


    >>> user2 = createObject('paula.examples.MinimalPloneUser',
    ...         title='user2',
    ...         password='pass2',
    ...         email='user2@bar.com',
    ...         realname='User Two',
    ...         )
    >>> user2_cred = UserDict(login='user2', password='pass2')
    >>> subsite['user2'] = user2


Let's see who is allowed to authenticate where:

    >>> from zope.app.security.interfaces import IAuthentication

    >>> root_pau = getUtility(IAuthentication, context=root)
    >>> sub_pau = getUtility(IAuthentication, context=subsite)

    >>> root_pau.authenticate(user1_cred)
    Principal('user1')
    >>> root_pau.authenticate(user2_cred) is None
    True
    >>> sub_pau.authenticate(user1_cred) is None
    True
    >>> sub_pau.authenticate(user2_cred)
    Principal('user2')


After removing the users, they are not allowed to authenticate anymore:

    >>> del subsite['user2']
    >>> sub_pau.authenticate(user2_cred) is None
    True
    >>> root_pau.authenticate(user1_cred)
    Principal('user1')
    >>> del root['user1']
    >>> root_pau.authenticate(user1_cred) is None
    True


Let's have a closer look at the principals, especially the properties

    >>> root['user1'] = user1
    >>> subsite['user2'] = user2

Authenticated principals

    >>> p1 = root_pau.authenticate(user1_cred)
    >>> p2 = sub_pau.authenticate(user2_cred)

There should be an id corresponding to the title, an email and realname, and
password and title may not have made it onto the principal.
    
    >>> p1.id
    'user1'
    >>> p1.email
    'user1@bar.com'
    >>> p1.realname
    'User One'
    >>> getattr(p1, 'password', 'foo')
    'foo'
    >>> getattr(p1, 'name', 'foo')
    'foo'

    >>> p2.id
    'user2'
    >>> p2.email
    'user2@bar.com'
    >>> p2.realname
    'User Two'
    >>> getattr(p2, 'password', 'foo')
    'foo'
    >>> getattr(p2, 'name', 'foo')
    'foo'

The same should be the case for found principals

    >>> p1 = root_pau.getPrincipal('user1')
    >>> p2 = sub_pau.getPrincipal('user2')

With a funny derivation from the .authenticate() behaviour. PAU's
.getPrincipal() hands over to next (higher level) PAU, in case it does not
find the principal. I am not quiet sure what to think of that, currently it
seems like a bug to me...

    >>> sub_pau.getPrincipal('user1') is None
    False

Further, an PrincipalLookupError is raised for principals that could not be
found...

    >>> root_pau.getPrincipal('user2')
    Traceback (most recent call last):
        foo
    PrincipalLookupError: user2

At least, the correct principals come back

    >>> p1.id
    'user1'
    >>> p1.email
    'user1@bar.com'
    >>> p1.realname
    'User One'
    >>> getattr(p1, 'password', 'foo')
    'foo'
    >>> getattr(p1, 'name', 'foo')
    'foo'

    >>> p2.id
    'user2'
    >>> p2.email
    'user2@bar.com'
    >>> p2.realname
    'User Two'
    >>> getattr(p2, 'password', 'foo')
    'foo'
    >>> getattr(p2, 'name', 'foo')
    'foo'



Let's add some groups, for simplicity's sake we currently only support one
level. I have a feeling that my understanding of multiple authentication
levels is currently not congruent with PAU's.

We only use the subsite, clean the other and ignore what is happening there

#    >>> del root['user1']
#    >>> del root['paula']
#    >>> subsite['user1'] = user1
#
#    >>> user3 = createObject('paula.examples.MinimalPloneUser',
#    ...         title='user3',
#    ...         password='pass3',
#    ...         email='user2@bar.com',
#    ...         realname='User Two',
#    ...         )
#    >>> user3_cred = UserDict(login='user3', password='pass3')
#    >>> subsite['user3'] = user3

There are now three users in the subsite folder:

#    >>> interact( locals() )
#    >>> subsite.keys()

#    >>> group1 = createObject('paula.examples.BasicGroup',
#    ...         title='group1',
#    ...         members=('groupuser11', 'groupuser12'),
#    ...         )
#    >>> group2 = createObject('paula.examples.BasicGroup',
#    ...         title='group2',
#    ...         members=('groupuser11', 'groupuser12'),
#    ...         )
#    >>> user2_cred = UserDict(login='user2', password='pass2')
#    >>> subsite['user2'] = user2



XXX: Should/Need we test whether persistency is working as expected?
