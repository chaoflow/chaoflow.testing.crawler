Introduction
============

paula.authentication provides a PAU (zope.app.authentication) authenticator
plugin and a PAU credentials plugin.

Authenticator Plugin
--------------------

The authenticator plugin retrieves an authentication provider from a list of
providers and uses that for authentication. The list is registered as a
utility.

Credentials Plugin
------------------

The credentials plugin accepts a simple mapping, makes sure that it claims to
provide IRequest and returns it. (Needed by internals of PAU.)
