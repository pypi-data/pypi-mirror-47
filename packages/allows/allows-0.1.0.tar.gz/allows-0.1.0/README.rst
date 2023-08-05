======
Allows
======


.. image:: https://img.shields.io/pypi/v/allows.svg
        :target: https://pypi.python.org/pypi/allows

.. image:: https://img.shields.io/travis/dvndrsn/allows.svg
        :target: https://travis-ci.org/dvndrsn/allows

.. image:: https://readthedocs.org/projects/allows/badge/?version=latest
        :target: https://allows.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/dvndrsn/allows/shield.svg
     :target: https://pyup.io/repos/github/dvndrsn/allows/
     :alt: Updates



Easier mock configuration and assertions in Python using R-spec_-like grammar!

.. code:: python

    allow(my_mock).to(return_value('hi').on_method('wave'))
    allow(my_mock).to(return_value('bye').on_method('wave').when_called_with('see ya'))

    assert my_mock.wave() == 'hi'
    assert my_mock.wave('see ya') == 'bye'

This library is built to wrap and configure Mock, MagicMock and other objects from the built in `unittest.mock`_ available in Python 3.3+.

.. _unittest.mock: https://docs.python.org/3/library/unittest.mock.html

* Free software: MIT license
* Documentation: https://allows.readthedocs.io.


Features
--------

* R-spec_-like grammar for specifing Mock behavior
* Compatible with all Python standard library `unittest.mock`_ Mock (MagicMock, Patch, etc.)
* Stand alone SideEffect builder to model and combine complex side effects

.. _R-spec: https://rspec.info/documentation/3.8/rspec-mocks/

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
