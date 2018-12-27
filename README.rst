flit6
=====

Cross-compat ``flit install``. Flit doesn't support Python 2 at all, but authors of
cross-compat libs might still want to use flit's packaging_ for the simplicity. After
``pip install flit6`` you can use ``flit install`` on Python 2 in your CI, with
``flit whatever else`` working as usual on Python 3.

I did not port any of ``flit`` itself. This project merely subprocesses a Python 3
build of your project, and then installs the generated distribution into the Python 2
environment. That requires flit_ to exist in the ``python3`` runtime, for build. An
example of how to set it up the yaml for travis-ci can be seen here_.


dev
---

Clone the repo and then:

.. code-block:: bash

   $ pip install pytest pytest-mock
   $ pytest

To generate a release, use ``python setup.py bdist_wheel --universal``. Upload with twine_.


.. _flit: https://flit.readthedocs.io/en/latest/
.. _packaging: https://flit.readthedocs.io/en/latest/pyproject_toml.html
.. _twine: https://twine.readthedocs.io/en/latest/
.. _here: https://github.com/wimglenn/pytest-raisin/blob/432b55c838a10b2c885b3f33efdaee39df18504c/.travis.yml#L22-L24
