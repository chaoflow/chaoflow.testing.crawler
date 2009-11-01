from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='chaoflow.testing.crawler',
      version=version,
      description="Recursively finds tests in your package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers = [
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          ],
      keywords='',
      author='Florian Friesdorf',
      author_email='flo@chaoflow.net',
      url='http://github.com/chaoflow/chaoflow.testing.crawler',
      license='AGPL',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['chaoflow','chaoflow.testing'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
