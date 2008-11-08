from setuptools import setup, find_packages
import os

version = '0.60'

setup(name='paula.pau_addons',
      version=version,
      description="Paula subscriber to set PAU principal properties",
      long_description=open("README.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers = [
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      keywords='',
      author='Florian Friesdorf',
      author_email='flo@chaoflow.net',
      url='https://chaoflow.net/projects/gsoc2008/z3membrane-ldap',
      license='AGPL',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['paula'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zope.interface',
          'zope.schema',
      ],
      extras_require=dict(
          test = [
                'paula.testing>=0.59',
                ],
          ),
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
