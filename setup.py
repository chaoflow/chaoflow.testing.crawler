from setuptools import setup, find_packages
import os

version = '0.3'

setup(name='chaoflow.testing.crawler',
      version=version,
      description="Recursively finds tests in your package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          ],
      keywords='',
      author='Florian Friesdorf',
      author_email='flo@chaoflow.net',
      url='http://github.com/chaoflow/chaoflow.testing.crawler',
      license='LGPL',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['chaoflow','chaoflow.testing'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'interlude',
      ],
      extras_require={
          'test': [
              'interlude',
              'chaoflow.testing.crawler',
              ],
          },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
