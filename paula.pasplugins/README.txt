SOON TO BE VALID:

paula.pasplugins provides plugins to use a Pluggable Authentication Utility
(PAU, from zope.app.authentication) for authentication within a Pluggable Auth
Service (PAU, as used for example by Plone 3.x). A PAU is created as local
utility through GenericSetup, if you do not use GenericSetup, you need to
provide one yourself.

The following are provided:

- *PAU CredentialsFromMappingPlugin* accepts credentials to be passed in a
  simple mapping and just returns the very same.  Further, it ensures, that
  the mapping provides IRequest, as PAU needs that to find its factories by
  multi-adapter-lookup.  Note: We are not using PAU to handle the request, but
  only to authenticate the user and to return a user object.

- *PAS AuthenticationPlugin* accepts credentials for authentication, transfers
  them into a UserDict, provides IRequest on it, and hands it over to PAU for
  authentication. In case of successful authentication, it returns a tuple
  containing containing the user id twice, i.e. it does not know about a
  difference between login and user id, yet.

- *PAS GroupsPlugin* tries to retrieve a principal from PAU and returns a
  tuple containing the principal's groups attribute. If anything goes wrong,
  an empty tuple is returned.

- *PAS PropertiesPlugin* tries to retrieve a principal from PAU and returns
  its properties as a MutablePropertySheet (from Products.PlonePAS.sheet,
  ATTENTION: Plone specific behaviour). The properties are expected to be
  normal attributes of the PAU principal and need to be part of a specially
  marked schema (ATTENTION: A normal PAU is not doing this). Please, look at
  the code (src/paula/pasplugins/plugins/properties.py) for details. I
  currently like the concept of properties being normal specially marked
  attributes - however, this might change. Feedback highly appreciated.
