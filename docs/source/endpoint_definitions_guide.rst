.. _endpoint-definitions-guide:

Endpoint Definitions Guide
========================================================

The Endpoint definitions Verilog file, often shortened to “ep_defines.v,” defines Opal Kelly FrontPanel Endpoint addresses and bits as Verilog parameters. These parameters can then be used when instantiating controllers in Verilog as well as over USB from a host using Python. For the host to use the Endpoint information, it must be written according to the guide.

The lines in ep_defines.v are split into two categories: addresses and bit indices.

.. _ep-defines-guide-addresses:

Addresses
------------------------------

Address definitions store the address and bit width of the Endpoint. The general structure is as follows.

.. code-block:: verilog

    `define {CHIPNAME}_{ENDPOINT_NAME}{_GEN_ADDR} 8’h{ADDRESS} // bit_width={BIT_WIDTH} addr_step={ADDR_STEP}

Each piece of this definition is explained below.

.. code-block:: verilog

    `define // the macro used to declare a parameter in Verilog

- **CHIPNAME:** the name of the chip this Endpoint belongs to. This is the chip the Endpoint will be found under when using the :py:meth:`~pyripherals.core.Endpoint.get_chip_endpoints` method. This name MUST NOT have any underscores in it because pyripheral uses the first underscore in this line to separate the chip name from the Endpoint name.

- **ENDPOINT_NAME:** the name of the Endpoint. This will be the dictionary key paired with the Endpoint object holding the data defined on this line. Underscores are allowed in this name.

- **_GEN_ADDR:** an optional phrase added after the Endpoint name that tells pyripheral to increment this Endpoint’s address when :py:meth:`~pyripherals.core.Endpoint.advance_endpoints` is called on a group containing this Endpoint.

- **8’h:** declaration of an 8 bit hexadecimal value before the address. If your address is more than 8 bits, change the 8 to that value. Ex. 16 bit address would be 16’h.

- **ADDRESS:** the hexadecimal address value for this Endpoint. This is the value the parameter will hold in the Verilog.

- **//:** start of the comment part of this line. The Verilog parameter only holds the address, but the pyripheral Endpoint object will also hold the bit_width, which is defined in the comment.

- **bit_width=:** the prefix for defining the bit width.

- **BIT_WIDTH:** the decimal integer value of the bit width of the Endpoint.

- **addr_step=:** the prefix for defining the address step of the Endpoint.

- **ADDR_STEP:** the integer value to add to the Endpoint's address when incrementing with :py:meth:`~pyripherals.core.Endpoint.advance_endpoints`.

.. _ep-defines-guide-bit-indices:

Bit Indices
------------------------------

Bit index definitions store the bit, associated address, and bit width of the Endpoint. The general structure is as follows.

.. code-block:: verilog

    `define {CHIPNAME}_{ENDPOINT_NAME}{_GEN_BIT} {BIT} // addr={ADDRESS} bit_width={BIT_WIDTH}

Each piece of this definition is explained below.

.. code-block:: verilog

    `define // the macro used to declare a parameter in Verilog

- **CHIPNAME:** the name of the chip this Endpoint belongs to. This is the chip the Endpoint will be found under when using the :py:meth:`~pyripherals.core.Endpoint.get_chip_endpoints` method. This name MUST NOT have any underscores in it because pyripheral uses the first underscore in this line to separate the chip name from the Endpoint name.

- **ENDPOINT_NAME:** the name of the Endpoint. This will be the dictionary key paired with the Endpoint object holding the data defined on this line. Underscores are allowed in this name.

- **_GEN_BIT:** an optional phrase added after the Endpoint name that tells pyripheral to increment this Endpoint’s lower bit index by its bit width when :py:meth:`~pyripherals.core.Endpoint.advance_endpoints` is called on a group containing this Endpoint.

- **BIT:** the decimal lower bit index for this Endpoint. This is the value the parameter will hold in the Verilog.

- **//:** start of the comment part of this line. The Verilog parameter only holds the address, but the pyripheral Endpoint object will also hold the bit_width, which is defined in the comment.

- **addr=:** the prefix for defining the associated address for pyripheral.

- **ADDRESS:** the address associated with the bit index for this Endpoint. While the Verilog parameter will only store the bit defined in this line, the pyripheral Endpoint object will also store the address and bit width defined in the comment. The address can either be a hexadecimal address value with prefix “0x” or the group and Endpoint name of an address Endpoint (see :ref:`ep-defines-guide-addresses` section). Ex. 0x04 or GP_WIRE_IN.

- **bit_width=:** the prefix for defining the bit width for pyripheral.

- **BIT_WIDTH:** the decimal value of the bit width of the Endpoint. If the _GEN_BIT suffix is added, then pyripheral will add this value to the lower bit index of the Endpoint when incrementing a group containing this Endpoint.

File
------------------------------

Using the above formats, enter the Endpoints each on separate lines in a Verilog file. The order of the Endpoints does not matter. Endpoints can have the same name if they have different chip names. For example, “GP_WIRE_IN” and “MEM_WIRE_IN” both have the Endpoint name “WIRE_IN” but have different chip names “GP” and “MEM,” which is allowed. Because pyripheral uses comments to extract extra information about the Endpoints, any other comments must be put on their own line, which pyripheral will ignore.

Alternatively, enter the information in an Excel spreadsheet copy of this `template <https://github.com/Ajstros/pyripherals/blob/main/examples/ep_defines_sheet_template.xlsx>`_. Each row should be a different Endpoint. Each column is explained below. Check the “Generated Line” column for any possible errors, then use the :py:meth:`~pyripherals.core.Endpoint.excel_to_defines` method to create a Verilog file from the spreadsheet. For reference, here is an `example spreadsheet <https://github.com/Ajstros/pyripherals/blob/main/examples/ep_defines_sheet_example.xlsx>`_ and an example of the `Verilog file <https://github.com/Ajstros/pyripherals/blob/main/examples/ep_defines_example.v>`_ generated from it.

- **Chip Name:** CHIPNAME (see :ref:`ep-defines-guide-bit-indices` section) from above.

    - *Note: recall that the chip name in each Endpoint definition line MUST NOT have underscores*

- **Endpoint Name:** ENDPOINT_NAME (see :ref:`ep-defines-guide-bit-indices` section) from above.

- **Address (hex):** ADDRESS (see :ref:`ep-defines-guide-bit-indices` section) from above.

- **Bit:** BIT (see :ref:`ep-defines-guide-bit-indices` section) from above. Leave empty if defining an Endpoint holding an address only.

- **Bit Width:** BIT_WIDTH (see :ref:`ep-defines-guide-bit-indices` section) from above

- **GEN_BIT:** _GEN_BIT (see :ref:`ep-defines-guide-bit-indices` section) from above. Enter True or False.

- **GEN_ADDR:** _GEN_ADDR (see :ref:`ep-defines-guide-bit-indices` section) from above. Enter True or False.

- **Address Step:** ADDR_STEP (see :ref:`ep-defines-guide-bit-indices` section) from above. Leave empty to default to 1.

- **Generated Name:** automatically generated chip name with Endpoint name. Since this is the name the “Address (hex)” column needs when referencing another Endpoint, referencing this cell allows you to have any future name changes to the address Endpoint reflected in the “Address (hex)” column of any Endpoint referencing it.

- **Generated Line:** the line that will be written for this Endpoint in the Endpoint definitions Verilog file when :py:meth:`~pyripherals.core.Endpoint.excel_to_defines` is called.

Usage
------------------------------

Once your Endpoint definitions file is complete, you can include the parameters you just named in your Verilog containing the Opal Kelly Endpoints themselves by adding the line below to that file. Replace “ep_defines.v” with whatever you named your Endpoint definitions file.

.. code-block:: verilog

    `include “ep_defines.v”

To retrieve the Endpoints through pyripheral, use the :py:meth:`~pyripherals.core.Endpoint.get_chip_endpoints` method.
