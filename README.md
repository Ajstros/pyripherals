[![Documentation Status](https://readthedocs.org/projects/pyripherals/badge/?version=latest)](https://pyripherals.readthedocs.io/en/latest/?badge=latest)

`pyripherals` is a Python package for communicating with peripheral ICs. It has a `Register` class to keep track of internal registers, but is most useful when used with a FrontPanel compatible Opal Kelly FPGA. With that, `pyripherals` makes use of the FrontPanel API for Python and Verilog to communicate more easily on common interfaces such as I2C and SPI.

## Quick Start

1. Install with pip

_Note that not all of_ `pyripherals` _will work with Python 3.10_

```
pip install pyripherals
```

To use an FPGA and peripherals:


2. Download [FrontPanel](https://pins.opalkelly.com/downloads) from OpalKelly

3. Download [Registers.xlsx](https://github.com/Ajstros/pyripherals/blob/main/python/Registers.xlsx) from the GitHub

4. Create config.yaml with create_yaml and edit fields as needed

```python
>>> from interfaces.utils import create_yaml
>>> create_yaml()
YAML created at C:/Users/username/.pyripherals
```

See [Installation Guide](https://pyripherals.readthedocs.io/en/latest/installation.html) for more information.

## Documentation
[Documentation](https://pyripherals.readthedocs.io/en/latest/index.html) is hosted on Read the Docs.

## Acknowledgements 

### The FPGA code is dervied from many open-source contributions. 

* The Verilog I2C controller is from OpalKelly [OpalKelly I2CController](https://github.com/opalkelly-opensource/design-resources/tree/main/HDLComponents/I2CController) (MIT License).

* The Verilog AD7961 controller is from Analog Devices and is free to use / redistribute as long as its used with Analog Devices parts (which must be the case since it does not work if connected to other parts). The Verilog is available within the [EVAL-AD7960 evaluation kit software](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/eval-ad7960.html#eb-overview)

* The Verilog [SPI Controller](http://www.opencores.org/projects/spi/) is from OpenCores.org and is authored by Simon Srot (GPL 2.1 or later license). 

* The Verilog wishbone master is written by Dan Gisselquist, Gisselquist Technology LLC. (LGPL, v3) 

* The DDR user interface (ddr_test.v) started with the OpalKelly DDR example provided in the FrontPanel example RAMTester and was significantly modified to support two ports.

### The Python code relies on wonderful open source packages such as:

* numpy
* numfi
* matplotlib
* pandas
* openpyxl
* h5py
* pyyaml
* scipy


## OpalKelly Module Compatibility. 
We have targeted and tested with the [XEM7310-A75 module](https://opalkelly.com/products/xem7310/) (Xilinx Artix-7). We have not tested but anticipate reasonable portability to other USB 3 OpalKelly modules:

* XEM7310MT
* XEM7320
* XEM7305
* XEM7360

## (Approximate) FPGA Block Diagram
This is the block diagram of the [top_level_module.bit bitfile](https://github.com/Ajstros/pyripherals/blob/main/examples/top_level_module.bit)
<p align="center">
<img src="docs/block_diagram/fpga_block_diagram.png" width="700">
