"""Integration test for calculating impedance.

Requires host computer only. Uses these functions:
- interfaces.interfaces.DDR3.make_sine_wave
- interfaces.utils.calc_impedance
- interfaces.utils.from_voltage
- interfaces.utils.to_voltage

Abe Stroschein, ajstroschein@stthomas.edu
January 2022
"""

import imp
import pytest
import numpy as np
from scipy.fft import rfftfreq
from pyripherals.core import FPGA
from pyripherals.peripherals.DDR3 import DDR3
from pyripherals.utils import from_voltage, to_voltage, calc_impedance

pytestmark = [pytest.mark.usable, pytest.mark.no_fpga]

# Fixtures


# Tests


def test_calc_impedance():
    # Works best at high frequencies
    # TODO: add more test data (loop through)

    accepted_error = 0.06  # Accepting +/-6% error (calculated by 6% of magnitude being allowed for real and imaginary parts)
    # Expected according to https://www.multisim.com/content/iosH7R4mMVBJ4s2L7RcdvK/impedance-analyzer-test/open/
    # expected = complex(0, -1000)  # Expecting 0 - 1000j Ohms impedance
    expected = complex(0, -10)

    resistor = 1000  # 1000 Ohm resistor
    # freq = 1000  # Frequency in Hertz
    freq = 100000  # Frequency in Hertz
    amp_in = 1
    # amp_out = 0.7072
    amp_out = 0.01
    dac80508_offset = 0x8000
    t = np.arange(0,
              DDR3.UPDATE_PERIOD * DDR3.SAMPLE_SIZE,
              DDR3.UPDATE_PERIOD)

    # Input 1V amplitude at 1KHz
    amp_in_code = from_voltage(voltage=amp_in,
                            num_bits=16,
                            voltage_range=2.5,
                            with_negatives=False)
    v_in_codes, freq_in_calc = DDR3.make_sine_wave(amplitude=amp_in_code,
                                                frequency=freq,
                                                offset=dac80508_offset)
    v_in = to_voltage(data=v_in_codes,
                    num_bits=16,
                    voltage_range=2.5,
                    use_twos_comp=False)

    # Output 0.7072V amplitude at 1KHz
    # These values according to MultiSim simulation at
    # https://www.multisim.com/content/iosH7R4mMVBJ4s2L7RcdvK/impedance-analyzer-test/open/
    amp_out_code = from_voltage(voltage=amp_out,
                                num_bits=16,
                                voltage_range=2.5,
                                with_negatives=False)
    v_out_codes, freq_out_calc = DDR3.make_sine_wave(amplitude=amp_out_code,
                                                    frequency=freq,
                                                    offset=dac80508_offset)
    v_out = to_voltage(data=v_out_codes,
                    num_bits=16,
                    voltage_range=2.5,
                    use_twos_comp=False)

    # 90 degrees behind for about -1000j Ohms impedance -> 1/4 period
    # Period in seconds
    period = 1 / freq_in_calc
    shift_amt = int(((1/4) * period) // (t[1] - t[0]))
    new_len = min(len(v_in), len(v_out)) - shift_amt
    v_in = v_in[-new_len:]
    v_out = v_out[:new_len]
    t = t[:new_len]

    # Remove offset before transform
    v_in = [x - 1.25 for x in v_in]
    v_out = [x - 1.25 for x in v_out]

    # We need to cut off the signals so they appear periodic for the transform
    # max_time = t[-1]
    max_time = t[int(len(t) / 100)]
    num_complete_periods = max_time // period
    target_time = period * num_complete_periods
    end_index = int(target_time / DDR3.UPDATE_PERIOD)
    t = t[:end_index]
    v_in = v_in[:end_index]
    v_out = v_out[:end_index]

    # import matplotlib.pyplot as plt
    # plt.plot(t, v_in)
    # plt.plot(t, v_out)
    # plt.xlim(0, 0.014)
    # plt.ylim(-1.01, 1.01)
    # plt.show()

    # Calculate frequencies from time
    x_frequencies = rfftfreq(len(t), t[1] - t[0])

    # Calculate impedance
    impedance_calc = calc_impedance(v_in=v_in, v_out=v_out, resistance=resistor)
    # plt.plot(x_frequencies, abs(impedance_calc))
    # plt.show()
    # Find nearest frequency to frequency we sent in v_in
    i = 0
    for f in x_frequencies:
        if f < freq_in_calc:
            i += 1
        else:
            break
    # Get impedance at that frequency
    z = impedance_calc[i]
    print(f'Got {z} at frequency {x_frequencies[i]}\nExpected {expected} at frequency {freq}')
    from scipy.fft import rfft
    z_non_window = np.divide(rfft(v_out), rfft(np.subtract(v_out, v_in) / resistor))
    print(f'Non-window calculation: {z_non_window[i]}')
    for i2 in range(len(x_frequencies)):
        if x_frequencies[i2] > freq_in_calc * 2 * np.pi:
            break
    print(f'Radians impedance calc: {impedance_calc[i2]}\nNon-window radians calc: {z_non_window[i2]}')
    error = accepted_error * np.abs(z)
    real_upper_bound = expected.real + error
    real_lower_bound = expected.real - error
    imag_upper_bound = expected.imag + error
    imag_lower_bound = expected.imag - error
    assert real_lower_bound < z.real < real_upper_bound
    assert imag_lower_bound < z.imag < imag_upper_bound
