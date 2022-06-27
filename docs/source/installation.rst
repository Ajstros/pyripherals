Installation
=================================

Quick Start
--------------
1. Install with pip (see :ref:`installation_pip` section)

To use an FPGA and peripherals:


2. Download `FrontPanel <https://pins.opalkelly.com/downloads>`_ from OpalKelly (see :ref:`installation_fpga` section)

3. Download `Registers.xlsx <https://github.com/Ajstros/pyripherals/blob/main/python/Registers.xlsx>`_ and add unsupported peripherals (see :ref:`installation_peripherals` section)

4. Create config.yaml with :py:meth:`pyripherals.utils.create_yaml` and edit (see :ref:`installation_yaml` section)


.. _installation_pip:

pip
-----------

:py:mod:`pyripherals` can be installed using pip.

.. code-block:: console

    pip install pyripherals

.. _installation_fpga:

FPGA
------------
To use the FPGA class with an Opal Kelly FrontPanel-supported device, you will also need to download the `FrontPanel SDK <https://pins.opalkelly.com/downloads>`_ from Opal Kelly. If you are using a MAC see the :ref:`mac_ok_setup` section.
You will also need to update the config.yaml file. See the :ref:`installation_yaml` section and example.

.. _installation_peripherals:

Peripherals
--------------------
To use peripherals, you will need FrontPanel (see :ref:`installation_fpga` section) as well as the `Registers.xlsx <https://github.com/Ajstros/pyripherals/blob/main/python/Registers.xlsx>`_ spreadsheet with register information for all supported peripherals, available on the `GitHub <https://github.com/Ajstros/pyripherals>`_.
Update the config.yaml file with the path to `Registers.xlsx <https://github.com/Ajstros/pyripherals/blob/main/python/Registers.xlsx>`_ (see :ref:`installation_yaml` section).
If you are using a peripheral not currently supported by :py:mod:`pyripherals`, see the :ref:`New Peripheral Guide <new_peripheral_guide>`.

.. _installation_yaml:

YAML Configuration
-----------------------
:py:mod:`pyripherals` uses a config.yaml file to customize paths to needed files and other user-configurable options.
To start, install the package (see :ref:`installation_pip` section), and open a Python shell. You can then
import :py:meth:`pyripherals.utils.create_yaml` and run it like below.

.. code-block:: python

    >>> from pyripherals.utils import create_yaml
    >>> create_yaml()
    YAML created at C:/Users/username/.pyripherals

From there, you can configure the options available by editing the config.yaml file created at the path given
after running :py:meth:`pyripherals.utils.create_yaml`. An example YAML is shown below.

.. code-block:: yaml

    endpoint_max_width: 32
    ep_defines_path: C:/Users/username/my_project/ep_defines.v
    fpga_bitfile_path: C:/Users/username/my_project/top_level_module.bit
    frontpanel_path: C:/Program Files/Opal Kelly/FrontPanelUSB
    registers_path: C:/Users/username/my_project/Registers.xlsx

.. _mac_ok_setup:

Opal Kelly Setup on MAC
-----------------------
The _ok.so shared library needs to be able to "find" the libokFrontPanel.dylib. Navigate to the FrontPanel API directory: e.g. frontpanel/API/Python3/ and check where _ok.so is searching for libokFrontPanel.dylib using otool.

.. code-block:: console 

    $ otool -L _ok.so

This output indicates that the Python import of ok will fail since libok is one directory up. Change this using install_name_tool.

.. code-block:: console 

    $ install_name_tool -change libokFrontPanel.dylib /fullpath/to/libokFrontPanel/libokFrontPanel.dylib _ok.so

