Tests
=================

:py:mod:`pyripherals` uses `pytest <https://docs.pytest.org/en/7.1.x/>`_ for its tests. pytest can be installed with pip.

.. code-block:: python

    >>> pip install pytest

All tests are available in the `tests folder on the GitHub <https://github.com/Ajstros/pyripherals/tree/main/python/tests>`_
All automated and working tests can be run with the "usable" marker. To run the tests clone the repository and navigate into the repository. 

.. code-block:: python

    >>> py -m pytest -m usable

More specific marks are available for different setups. Simply replace "usable" with one of the following markers in the command above.

* no_fpga: use if you do not have an FPGA connected

* fpga_only: use if you have an FPGA connected

* usable: all working automated tests; requires an FPGA and connected peripherals which is very specific to our lab
