flit6
=====

Cross-compat ``flit install``. Flit doesn't support Python 2 at all, but authors of
cross-compat libs might still want to use flit's packaging for the simplicity. After
``pip install flit6`` you can use ``flit install`` on Python 2 in your CI, with
``flit whatever else`` working as usual on Python 3.

I did not port any of ``flit`` itself. This project merely subprocesses a Python 3
build of your distribution, and then installs the generated release in the Python 2
environment. That requires flit_ to exist in the ``python3`` runtime, for build.


dev
---

Clone the repo and then:

.. code-block:: bash

   $ pip install pytest pytest-mock
   $ pytest

To generate a release, use ``python setup.py bdist_wheel --universal``. Upload with twine_.


.. _flit: https://flit.readthedocs.io/en/latest/
.. _twine: https://twine.readthedocs.io/en/latest/
