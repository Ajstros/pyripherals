"""Unit test for the utils module.

Abe Stroschein, ajstroschein@stthomas.edu
"""

# Uncomment this and either pip uninstall pyripherals or enter a venv that
# does not have pyripherals installed. Run the test from the unit_tests folder
# to run the test on your cloned version of the repo instead of a pip install.
import os, sys
sys.path.insert(0, os.path.abspath('../../src'))

import pytest
import numpy as np
from pyripherals.utils import from_voltage, to_voltage

pytestmark = [pytest.mark.usable, pytest.mark.no_fpga]

@pytest.mark.parametrize('data, num_bits, voltage_range, use_twos_comp, expected', [
    [0, 16, 5, False, 0],
    [0, 16, 5, True, 0],
    [0xFFFF, 16, 5, False, 5],
    [0xFFFF, 16, 5, True, -1 * 5 / (2 ** 16)],
    [[i for i in range(0x3FFF + 1)], 14, 5, False, np.array([i * 5 / (2 ** 14) for i in range(0x3FFF + 1)])],
    [[i for i in range(0xFFFF + 1)], 16, 5, False, np.array([i * 5 / (2 ** 16) for i in range(0xFFFF + 1)])],
    [[i for i in range(0xFFFF + 1)], 16, 5, True, np.array([np.int16(i) * 5 / (2 ** 16) for i in range(0xFFFF + 1)])],
    [np.array([i for i in range(0x3FFF + 1)]), 14, 5, False, np.array([i * 5 / (2 ** 14) for i in range(0x3FFF + 1)])],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, False, np.array([i * 5 / (2 ** 16) for i in range(0xFFFF + 1)])],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, True, np.array([np.int16(i) * 5 / (2 ** 16) for i in range(0xFFFF + 1)])],
])
def test_to_voltage(data, num_bits, voltage_range, use_twos_comp, expected):
    tolerance = 0.001

    if type(data) is list:
        difference = np.abs(np.array(to_voltage(data=data, num_bits=num_bits, voltage_range=voltage_range, use_twos_comp=use_twos_comp)) - expected)
    else:
        difference = np.abs(to_voltage(data=data, num_bits=num_bits, voltage_range=voltage_range, use_twos_comp=use_twos_comp) - expected)

    if type(difference) is np.ndarray:
        assert all(difference < tolerance)
    else:
        assert difference < tolerance

@pytest.mark.parametrize('expected, num_bits, voltage_range, with_negatives, voltage', [
    [0, 16, 5, False, 0],
    [0, 16, 5, True, 0],
    [0xFFFF, 16, 5, False, 5],
    [0xFFFF, 16, 5, True, -1 * 5 / (2 ** 16)],
    [np.array([i for i in range(0x3FFF + 1)]), 14, 5, False, [i * 5 / (2 ** 14) for i in range(0x3FFF + 1)]],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, False, [i * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, True, [np.int16(i) * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
    [np.array([i for i in range(0x3FFF + 1)]), 14, 5, False, np.array([i * 5 / (2 ** 14) for i in range(0x3FFF + 1)])],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, False, np.array([i * 5 / (2 ** 16) for i in range(0xFFFF + 1)])],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, True, np.array([np.int16(i) * 5 / (2 ** 16) for i in range(0xFFFF + 1)])],
])
def test_from_voltage(expected, num_bits, voltage_range, with_negatives, voltage):
    tolerance = 0.001

    from_voltage_value = from_voltage(voltage=voltage, num_bits=num_bits, voltage_range=voltage_range, with_negatives=with_negatives)

    if type(voltage) is list:
        difference = np.abs(np.array(from_voltage_value) - expected)
    else:
        difference = np.abs(from_voltage_value - expected)

    if type(difference) is np.ndarray:
        assert all(difference < tolerance)
    else:
        assert difference < tolerance

    # We expect an scalar int if we gave a scalar int or float, otherwise an array.
    if type(voltage) is int or type(voltage) is float:
        assert type(from_voltage_value) is int
    else:
        assert type(from_voltage_value) is np.ndarray

def test_voltage_conversion():
    tolerance = 0.001

    voltage_in = np.array([i / 100 for i in range(500 + 1)])
    difference = np.abs(to_voltage(from_voltage(voltage=voltage_in, num_bits=16, voltage_range=5, with_negatives=False), num_bits=16, voltage_range=5, use_twos_comp=False) - voltage_in)
    if type(difference) is np.ndarray:
        assert all(difference < tolerance)
    else:
        assert difference < tolerance

    data_in = np.array([i for i in range(0xFFFF + 1)])
    difference = np.abs(from_voltage(to_voltage(data=data_in, num_bits=16, voltage_range=5, use_twos_comp=False), num_bits=16, voltage_range=5, with_negatives=False) - data_in)
    if type(difference) is np.ndarray:
        assert all(difference < tolerance)
    else:
        assert difference < tolerance
