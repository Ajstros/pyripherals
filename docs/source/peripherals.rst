peripherals
======================

The :py:mod:`pyripherals.peripherals` subpackage contains a few base controllers and several specific controllers for different peripherals. The base controllers are used to reduce code repetition as many peripherals use common communication methods. Specific peripheral classes that use these communication methods are derived from the more general base classes.

Base Controllers
--------------------------
.. automodule:: pyripherals.peripherals.I2CController
    :members:

.. automodule:: pyripherals.peripherals.SPIController
    :members:

.. automodule:: pyripherals.peripherals.SPIFifoDriven
    :members:

Extends I2CController
--------------------------
.. automodule:: pyripherals.peripherals.TCA9555
    :members:

.. automodule:: pyripherals.peripherals.UID_24AA025UID
    :members:

.. automodule:: pyripherals.peripherals.DAC53401
    :members:

.. automodule:: pyripherals.peripherals.TMF8801
    :members:


Extends SPIController
--------------------------
.. automodule:: pyripherals.peripherals.ADS8686
    :members:


Extends SPIFifoDriven
--------------------------
.. automodule:: pyripherals.peripherals.DAC80508
    :members:

.. automodule:: pyripherals.peripherals.AD5453
    :members:


Miscellaneous
---------------
.. automodule:: pyripherals.peripherals.DDR3
    :members:

.. automodule:: pyripherals.peripherals.AD7961
    :members:

.. automodule:: pyripherals.peripherals.ADCDATA
    :members:

