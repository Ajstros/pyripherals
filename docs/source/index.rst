.. pyripheral documentation master file, created by
   sphinx-quickstart on Sat Feb 19 12:21:09 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyripheral's documentation!
===========================================

.. image:: ../../paper/JOSS_diagram.drawio.png
   :alt: Fig. 1: On the left, the Pyripherals module abstracts registers to enable user code to easily read and write to peripherals. Pyripherals and the FPGA code share a file ep_defines.v that defines the addresses of endpoints so that the transport of messages from the host computer through the FPGA and to the correct peripherals is managed. On the right, is an example hardware setup supported by Pyripherals. An FPGA module (Opal Kelly) with a Python API to the USB interface has various types of communication controllers in the FPGA logic and is wired to peripheral chips that sit on a custom circuit board. The chips include analog-to-digital converters (ADCs), digital-to-analog converters (DACs), and a unique identification chip (UID). The example user code reads the serial number of the UID chip using get_serial_number(). Pyripherals constructs the message using the address of the serial number register from the Registers.xslx spreadsheet. The message is then routed to the appropriate communication controller using the controller addresses defined in the ep_defines.v file and by the user code which provides the controller/bus name at initialization of the UID instance. Pyripherals formats messages for each type of communication protocol. In the user code example, the UID chip is connected to the I2CDAQ bus and has messages routed through the I2C0 communication controller such that the UID Python class inherits from a parent I2CController class.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   core
   peripherals
   utils
   register_index_guide
   endpoint_definitions_guide
   new_peripheral_guide
   tests
   example


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
