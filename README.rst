flit6
=====

Cross-compat ``flit install``.

``pip install flit6`` allows you to use ``flit install`` on Python 2, and ``flit whatever else`` on Python 3.

Requires ``flit``_ to exist in the python3 runtime, for build.


dev
---

Clone the repo and then:

.. code-block:: bash

   $ pip install pytest pytest-mock
   $ pytest

To generate a release, use ``python setup.py bdist_wheel --universal``. Upload with ``twine_``.


.. _flit: https://flit.readthedocs.io/en/latest/
.. _twine: https://twine.readthedocs.io/en/latest/
