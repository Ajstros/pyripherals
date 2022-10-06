---
title: 'Pyripherals: A Python Package for Communicating with Peripheral Electronic Devices'
tags:
  - Python
  - instrument control
  - data acquisition
  - electrical engineering
  - physics
  - experiments
authors:
  - name: Abraham Stroschein
    orcid: 0000-0001-9412-2049
    affiliation: 1
  - name: Ian Delgadillo Bonequi
    orcid: 
    affiliation: 1
  - name: Lucas J. Koerner
    orcid: 0000-0002-7236-7202
    affiliation: 1
affiliations:
 - name: Department of Electrical and Computer Engineering, University of St. Thomas
   index: 1
date: 1 August 2022
bibliography: paper.bib
---

# Statement of Need
We are developing a data acquisition system (DAQ) for real-time feedback that uses FPGA-based control of and acquisition from various electronic chips, or peripherals. Because these peripherals communicate over multiple protocols (SPI, I2C, LVDS) through an FPGA, we designed *pyripherals* to organize and abstract registers, the communication protocol, and the host computer interface to each communication controller. The software and firmware are designed for Opal Kelly FPGA modules, yet the Python developments are generally useful for organizing the data fields of electronic chips, especially for communication.

Data from a register is accessed with the address of the register and the bit indices of the data field, but users will often refer to the data field by its name, which *pyripherals* retains as a dictionary key. When passed the location of the data field, parameterized functions automatically format the data or command as required by the communication interface used by the peripheral. The assembled message is passed to the appropriate hardware controller responsible for low-level communication with the peripheral. In this solution, the addressing, bit indexing, and formatting are handled by *pyripherals* before the message is sent over the Opal Kelly FrontPanel API to a hardware-level communication controller on an Opal Kelly FPGA [@opalkelly.comFrontPanel], which handles low-level communication with the desired peripheral.

This DAQ system and the *pyripherals* software are crucial components of a digital feedback amplifier being developed for ion channel electrophysiology [@koernerDigitalFeedbackAmplifier2022a] and more generally comprise an open-source system for microsecond latency real-time feedback experiments. Similar DAQ systems [@leibrandtOpenSourceDigital2015; @yuPerformanceLimitationsFPGAbased2018] create MHz bandwidth servos for physics experiments but these works do not expose the host software. Many Python packages for lab automation and electrical instrument control have been developed [@allanBlueskyAheadMultiFacility2019; @casagrandeInstrumentKit; @jermainPyMeasure] yet do not support real-time control. In our system, the FPGA controller fills a need for microsecond level latency by interfacing directly to analog-to-digital converters and digital-to-analog converters while *pyripherals* organizes the configuration of these chips. The *pyripherals* software can be expanded to control and read data from other electronic sensors, such as accelerometers, and is currently in use in our lab with a time-of-flight depth sensor (AMS TMF8801) for rapid readout of photon return time histograms. Similar to *pyripherals*, the Python package *registerMap* [@smileyRegisterMap] creates a framework for register map organization in embedded systems. However, it lacks the interconnection between register data and hardware communication controller offered by *pyripherals*. The Opal Kelly XEM7310 FPGA that we use for communication controllers to demonstrate *pyripherals* is common in research environments which allows other labs to accelerate their development of FPGA to electronic chip interfaces using *pyripherals*.

# Summary

## Registers

*pyripherals* reads an Excel spreadsheet that holds the name, address, lower bit index, upper bit index, and bit width of each data field. Different peripherals can be separated into different sheets within the register index. The table below shows an example sheet for a peripheral named “TestPeripheral”.

| Name          | Hex Address | Default Value | Bit Width | Bit Index (High) | Bit Index (Low) |
| ------------- | ----------- | ------------- | --------- | ---------------- | --------------- |
| INPUT         | 0x00        | 0xf           | 4         | 3                | 0               |
| OUTPUT        | 0x00        | 0x0           | 4         | 7                | 4               |
| CONFIG        | 0x01        | 0xff          | 8         | 7                | 0               |
| ID            | 0x01        | 0x0           | 8         | 15               | 8               |

- Name = name of the data field chosen by the user. This is how the register will be accessed in Python.
- Hex Address = address of the register on the chip as given by its datasheet. Must be formatted as a hexadecimal number with "0x" prefix.
- Default Value = the default value of the register as given by the chip's datasheet.
- Bit Width = the number of bits in the data field.
- Bit Index (High) = the bit index of the upper end of the data field in the register. Ex. in a 32-bit register where the data field is located in the last 4 bits of the register, Bit Index (High) would be 31.
- Bit Index (Low) = the bit index of the lower end of the data field in the register. Ex. in a 32-bit register where the data field is located in the last 4 bits of the register, Bit Index (Low) would be 28.

*pyripherals* then reads the spreadsheet, referred to as a register index in the documentation, and returns a dictionary of name-Register pairs using the `Register.get_chip_registers` static method. The example below retrieves the register index from the table above.

```python
>>> TestPeripheral_regs = Register.get_chip_registers('TestPeripheral')
```

Each `Register` object holds all values from the spreadsheet for the data field it represents. A guide for [creating a register index](https://pyripherals.readthedocs.io/en/latest/register_index_guide.html) is located in the documentation. An example register is shown below. 

```python
>>> print(TestPeripheral_regs['INPUT']) 
0x0[0:3] 
>>> TestPeripheral_regs['INPUT'].__dict__ 
{'address': 0, 'default': 15, 'bit_index_high': 3, 'bit_index_low': 0,
'bit_width': 4}
```

The `Register` abstraction of *pyripherals* allows user code to refer to data fields using only their names. The spreadsheet organization of data fields allows for user-friendly editing and sharing of data field information without the need to change user code. Specific applications include communicating with microcontrollers or development boards like Arduino as well as accessing data using SPI or I2C controllers. 

*pyripherals* uses `Registers` to assemble messages for SPI [@srotOverviewSPIController] and I2C [@DesignresourcesHDLComponentsI2CController]
communication interfaces using parameterized commands in classes for [SPI](https://pyripherals.readthedocs.io/en/latest/peripherals.html#pyripherals.peripherals.SPIController.SPIController), [hardware-timed SPI](https://pyripherals.readthedocs.io/en/latest/peripherals.html#pyripherals.peripherals.SPIFifoDriven.SPIFifoDriven), and [I2C](https://pyripherals.readthedocs.io/en/latest/peripherals.html#pyripherals.peripherals.I2CController.I2CController). Communication specific to an individual peripheral is available in its subclass. A full list of [peripherals with classes](https://pyripherals.readthedocs.io/en/latest/peripherals.html) in *pyripherals* can be found in the documentation.

## Endpoints

For our research, *pyripherals* is paired with hardware controllers instantiated on an Opal Kelly FPGA. These controllers send communication signals to the chips connected to the FPGA. To interact with these controllers, *pyripherals* uses the Opal Kelly FrontPanel API for bidirectional communication over USB between a host computer and the FPGA using addressable endpoints.  

*pyripherals* reads FrontPanel endpoint addresses and bit indices from a Verilog definition file. This Verilog file requires a [naming system](https://pyripherals.readthedocs.io/en/latest/endpoint_definitions_guide.html) described in the documentation and associates peripherals with a specific hardware controller instantiation. A complete guide to [creating an endpoint definitions file](https://pyripherals.readthedocs.io/en/latest/endpoint_definitions_guide.html) is in the documentation. If the TestPeripheral is a DAC, it might have a "WRITE_IN" register to hold the data written in by the user to be output as a voltage. If multiple TestPeripherals are being used, the Verilog Opal Kelly endpoints to connect with it may be instantiated in a generate loop. This means there is a set interval between the addresses of different instantiations of the Verilog endpoints. The first instance could have an address of 0x4, with an interval of 7 between each instance. To access this information on the Python side, the Verilog instantiation of the endpoint must use a parameter defined according to the *pyripherals* syntax in a separate definitions file. The line below shows an example that defines an endpoint named “WRITE_IN” that belongs to peripheral “TestPeripheral” with an address of 0x04 (8'h04 is the Verilog syntax for an 8-bit hexadecimal number 0x04) and a bit_width of 32 that adds 7 to the address every time it is advanced.

```verilog
`define TestPeripheral_WRITE_IN_GEN_ADDR 8'h04 // bit_width=32 addr_step=7
```

The naming convention for endpoints depends on whether they contain contain addresses or bit indices. The above example contains an address. Each is demonstrated below with curly brackets {} indicating placeholders to be completed by the user. More information on the syntax and meaning of these lines is available in the [endpoint definitions guide](https://pyripherals.readthedocs.io/en/latest/endpoint_definitions_guide.html).

Addresses: 

```verilog
`define {CHIPNAME}_{ENDPOINT_NAME}{_GEN_ADDR} {hexadecimal address}
// bit_width={bit_width} addr_step={addr_step}
```

Bit Indices: 

```verilog
`define {CHIPNAME}_{ENDPOINT_NAME}{_GEN_BIT} {decimal bit index}
// addr={address or endpoint name} bit_width={bit_width}
```

*Note: the above comments must be placed on the same line as the `define. They are split here for readability.*

For multiple units of the same chip, each chip class has a `create_chips` method which instantiates a specified number of chips, incrementing the endpoint addresses and bit indices according to the GEN_ADDR, GEN_BIT, bit_width, and addr_step parameters above.

Once created, the user can read the endpoint definitions file with `Endpoint.get_chip_endpoints`
which returns a dictionary of name-Endpoint pairs. An example using the “TestPeripheral_WRITE_IN” endpoint from earlier is shown below. 

```python
>>> TestPeripheral_eps = Endpoint.get_chip_endpoints(chip_name='TestPeripheral') 
>>> print(TestPeripheral_eps['WRITE_IN']) 
0x4[None:None] 
>>> TestPeripheral_eps['WRITE_IN'].__dict__ 
{'address': 4, 'bit_index_low': None, 'bit_index_high': None, 'bit_width': 32,
'gen_bit': False, 'gen_address': False, 'addr_step': 7} 
```

Using the `Endpoint` class in *pyripherals* makes Verilog parameters used to instantiate Opal Kelly endpoints available in Python. This means the user does not have to manually match them in each language; when the user changes the value of an endpoint in the definitions file, the change is reflected in both the Python and Verilog code.

## FPGA Data Acquisition Code
Our FPGA code for use with *pyripherals* is available at [https://github.com/lucask07/covg_fpga/](https://github.com/lucask07/covg_fpga/). It is written for the Opal Kelly XEM7310 FPGA and supports I2C, SPI, and LVDS communication with a DDR for data buffering. An example use of this code is an [impedance analyzer](https://pyripherals.readthedocs.io/en/latest/example.html) using a DAC80508 digital-to-analog converter [@dac80508] and an ADS8686 analog-to-digital converter [@ads8686] communicating over SPI.

## Links

Documentation is available  at [https://pyripherals.readthedocs.io/en/latest/index.html](https://pyripherals.readthedocs.io/en/latest/index.html) and the GitHub is available at [https://github.com/Ajstros/pyripherals](https://github.com/Ajstros/pyripherals). *pyripherals* is available for install from pip at [https://pypi.org/project/pyripherals/](https://pypi.org/project/pyripherals/).

# Current Research
*pyripherals* was developed under an NIH-funded project to create a digital ion channel amplifier at the University of St. Thomas where it is being used to communicate with and control an FPGA-based data acquisition system for real-time feedback.


# Acknowledgements
*pyripherals* was developed under the National Institutes of Health (NIH) R15 grant R15NS116907 to PI L. J. Koerner. 

# References
