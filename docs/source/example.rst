Example
============

One example of using :py:mod:`pyripherals` is an impedance analyzer which calculates the impedance of an unknown
component. For this example you will need an Opal Kelly XEM7310 FPGA connected to your computer as well as a
`DAC80508 <https://www.ti.com/product/DAC80508>`_ and `ADS8686 <https://www.ti.com/product/ADS8686S>`_
connected to the FPGA. The pin connections between the FPGA and these peripherals are as follows:

DAC80508

* SDI - L3

* SDO - K3

ADS8686

* SDI - P2

* SDOA - N5

* SDOB - N2

Also download the `top_level_module.bit <https://github.com/Ajstros/pyripherals/blob/main/examples/top_level_module.bit>`_
bitfile, `ep_defines <https://github.com/Ajstros/pyripherals/blob/main/examples/ep_defines.v>`_, `Registers.xlsx <https://github.com/Ajstros/pyripherals/blob/main/python/Registers.xlsx>`_, and the `impedance_analyzer.py <https://github.com/Ajstros/pyripherals/blob/main/examples/impedance_analyzer.py>`_
Python file from the GitHub. Change the BITFILE_PATH constant in impedance_analyzer.py to the path of
top_level_module.bit on your computer. Read through the documentation included in impedance_analyzer.py
to understand the other constants you can change as well as the setup of the circuit. You can then run
impedance_analyzer.py.

This will send a test voltage across the unknown impedance with the DDR3 and the DAC80508 and read it back
using the DDR3 and the ADS8686. With the known resistor's value, the current is calculated to be used with
the read voltage to calculate the impedance.