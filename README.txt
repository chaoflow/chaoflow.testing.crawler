Introduction
============

The purpose of chaoflow.testing.crawler is to find tests in your package and
run them along with tests in files you explicitly define.

Tests are found in the following files:

- all .py files that are part of (subpackages of) your package, i.e. files that
  you can import with ``import``
- all .txt files that have a corresponding .py file
- all files you excplicitly specify

All tests found can be run individually, e.g. with zc.recipe.testrunner.


Using the test crawler
======================

In order to use the test crawler for your package, you only need to copy one
file and declare the dependency on chaoflow.testing.crawler in your setup.py.

Drop this file into your package root and adapt the files list to explicitly
specify test files that are not found otherwise, tests.py_::

  # chaoflow.testing.crawler.tests.py
  #
  # You can simply copy this file to your package and adjust it to your needs

  from chaoflow.testing.crawler import create_test_suite

  # File to test, relative to the package root
  # all .py files are found
  # all .txt files with corresponding .py file are found
  files = [
          'README.txt'
          ]

  # We assume that this modules is in the root of your package
  pkgname = __name__[:-6]

  test_suite = create_test_suite(pkgname, files)

.. _tests.py: http://github.com/chaoflow/chaoflow.testing.crawler/blob/master/src/chaoflow/testing/crawler/tests.py



Declare the dependency in setup.py::

  setup(...
        extras_require={
            'test': [
                'interlude',
                'chaoflow.testing.ipython',
                'chaoflow.testing.crawler',
                ],
            },
        )

If interlude is available, ``interlude.interact`` will be available as
``interact`` in your test environment.

If chaoflow.testing.ipython is available, ``ipshell`` will be available as
``ipshell`` in your test environment.

example buildout.cfg using chaoflow.testing.crawler and zc.recipe.testrunner::

  [buildout]
  develop = .
  parts = test py

  [test]
  recipe = zc.recipe.testrunner
  eggs = chaoflow.testing.crawler [test]

  [py]
  recipe = zc.recipe.egg
  interpreter = py
  eggs = ${test:eggs}


After buildout, you can run your tests using ``./bin/test``.
Run ``./bin/test --list-tests`` to get a list of all registered tests and see
``./bin/test --help`` for further information.


License
=======

chaoflow.testing.crawler is licensed under LGPLv3. Please let me know if this
presents a problem for you.
