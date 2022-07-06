"""Unit test for the utils module.

Abe Stroschein, ajstroschein@stthomas.edu
"""

import pytest
import numpy as np
from pyripherals.utils import from_voltage, to_voltage

pytestmark = [pytest.mark.usable, pytest.mark.no_fpga]

@pytest.mark.parametrize('data, num_bits, voltage_range, use_twos_comp, expected', [
    [0, 16, 5, False, 0],
    [0, 16, 5, True, 0],
    [0xFFFF, 16, 5, False, 5],
    [0xFFFF, 16, 5, True, 2.5],
    [[i for i in range(0x3FFF + 1)], 14, 5, False, [i * 5 / (2 ** 14) for i in range(0x3FFF + 1)]],
    [[i for i in range(0xFFFF + 1)], 16, 5, False, [i * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
    [[i for i in range(0xFFFF + 1)], 16, 5, True, [np.int16(i) * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
    [np.array([i for i in range(0x3FFF + 1)]), 14, 5, False, [i * 5 / (2 ** 14) for i in range(0x3FFF + 1)]],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, False, [i * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, True, [np.int16(i) * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
])
def test_to_voltage(data, num_bits, voltage_range, use_twos_comp, expected):
    match = np.abs(to_voltage(data=data, num_bits=num_bits, voltage_range=voltage_range, use_twos_comp=use_twos_comp) - expected) < 0.001
    if type(match) is np.ndarray:
        assert all(match)
    else:
        assert match

@pytest.mark.parametrize('expected, num_bits, voltage_range, with_negatives, voltage', [
    [0, 16, 5, False, 0],
    [0, 16, 5, True, 0],
    [0xFFFF, 16, 5, False, 5],
    [0xFFFF, 16, 5, True, 2.5],
    [[i for i in range(0x3FFF + 1)], 14, 5, False, [i * 5 / (2 ** 14) for i in range(0x3FFF + 1)]],
    [[i for i in range(0xFFFF + 1)], 16, 5, False, [i * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
    [[i for i in range(0xFFFF + 1)], 16, 5, True, [np.int16(i) * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
    [np.array([i for i in range(0x3FFF + 1)]), 14, 5, False, [i * 5 / (2 ** 14) for i in range(0x3FFF + 1)]],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, False, [i * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
    [np.array([i for i in range(0xFFFF + 1)]), 16, 5, True, [np.int16(i) * 5 / (2 ** 16) for i in range(0xFFFF + 1)]],
])
def test_from_voltage(expected, num_bits, voltage_range, with_negatives, voltage):
    match = np.abs(from_voltage(voltage=voltage, num_bits=num_bits, voltage_range=voltage_range, with_negatives=with_negatives) - expected) < 0.001
    if type(match) is np.ndarray:
        assert all(match)
    else:
        assert match

def test_voltage_conversion():
    voltage_in = np.array([i / 100 for i in range(500 + 1)])
    match = np.abs(to_voltage(from_voltage(voltage=voltage_in, num_bits=16, voltage_range=5, with_negatives=False), num_bits=16, voltage_range=5, use_twos_comp=False) - voltage_in) < 0.001
    if type(match) is np.ndarray:
        assert all(match)
    else:
        assert match

    data_in = np.array([i for i in range(0xFFFF + 1)])
    match = np.abs(from_voltage(to_voltage(data=data_in, num_bits=16, voltage_range=5, use_twos_comp=False), num_bits=16, voltage_range=5, with_negatives=False) - data_in) < 0.001
    if type(match) is np.ndarray:
        assert all(match)
    else:
        assert match
