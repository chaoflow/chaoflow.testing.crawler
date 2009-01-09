from setuptools import setup, find_packages
import os

version = '0.81'

setup(name='paula.testing',
      version=version,
      description="Paula testing framework",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
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
          'zope.app.testing',
          'zope.component',
          'zope.testing',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
