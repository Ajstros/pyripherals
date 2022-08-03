"""Module containing general functions useful to interfaces.

Abe Stroschein, ajstroschein@stthomas.edu

Lucas Koerner, koer2434@stthomas.edu
"""

import matplotlib.pyplot as plt
import time
import numpy as np
from scipy.fft import rfft
from scipy.signal.windows import hann
import datetime
import sys
import yaml
import os
import h5py

home_dir = os.path.join(os.path.expanduser('~'), '.pyripherals')
DEFAULT_CONFIGS = {
    'endpoint_max_width': 32,
    'fpga_bitfile_path': None,
    'ep_defines_path': None,
    'registers_path': None,
    'frontpanel_path': 'C:/Program Files/Opal Kelly/FrontPanelUSB',
}


def create_yaml(overwrite=False):
    """Create a default config.yaml file."""

    if not os.path.exists(home_dir):
        os.mkdir(home_dir)

    file_path = os.path.join(home_dir, 'config.yaml')

    if os.path.exists(file_path) and not overwrite:
        print('File already exists, run "create_yaml(overwrite=True)" to overwrite the file.')
        return None

    with open(file_path, mode='w') as file:
        yaml.dump(DEFAULT_CONFIGS, file)
    
    print(f'YAML created at {file_path}')
    return DEFAULT_CONFIGS


def rev_lookup(dd, val):
    key = next(key for key, value in dd.items() if value == val)
    return key

def bin(s):
    return str(s) if s<=1 else bin(s>>1) + str(s&1)

def test_bit(int_type, offset):
    mask = 1 << offset
    return ((int_type & mask) >> offset)

def gen_mask(bit_pos):

    if not hasattr(bit_pos, '__iter__'):
        bit_pos = [bit_pos]

    mask = sum([(1 << b) for b in bit_pos])
    return mask


def reverse_bits(number, bit_width=8):
    """Return an integer with the reversed bits of the input number."""

    reversed_number = 0
    for i in range(bit_width):
        reversed_number <<= 1
        reversed_number |= number & 0b1
        number >>= 1
    return reversed_number


def count_bytes(num):
    """Count the number of bytes in a number."""

    bytes = 0
    if (num == 0):  # if the number equals 0
        return 1
    while (num != 0):  # bit shift 8 bits (byte)
        num >>= 8
        bytes += 1
    return bytes


def int_to_list(integer, byteorder='little', num_bytes=None):
    """Convert an integer into a list of integers 1 byte long.

    Parameters
    ----------
    integer : int
        The integer to convert.
    byteorder : str
        Either 'little' for little Endian (LSB first) or 'big' for big Endian
        (MSB first).
    num_bytes : int
        The number of bytes to convert the number into. None means the
        function will return the minimum number of bytes necessary to
        represent the number.
    """

    list_int = []

    while integer != 0:
        # Take the least significant byte and append it to the list, then shift the integer right 1 byte.
        byte = integer % 2**(8)
        list_int.append(byte)
        integer >>= 8

    # In case integer began at 0.
    if len(list_int) == 0:
        list_int.append(0)

    if num_bytes is not None:
        # User entered a number of bytes
        # Check if the integer fits into the given number of bytes
        if num_bytes < len(list_int):
            return False
        else:
            # Fill the list with 0 for remaining bytes
            for i in range(num_bytes - len(list_int)):
                # Can append to the end because the list will be reversed in the return
                list_int.append(0)

    if byteorder == 'little':
        return list_int
    elif byteorder == 'big':
        return list_int[::-1]
    else:
        print(f'Unknown byteorder "{byteorder}", using "little" instead')
        return list_int


def int_to_custom_signed(data, num_bits):
    """Return the given integer in two's complement form in the given number of bits.
    
    Invert all bits (in num_bits), add 1 (only keeping num_bits).

    Parameters
    ----------
    data : int or list(int) or np.ndarray(int)
        The binary data to apply two's complement to.
    num_bits : int
        The number of bits the number is represented in. This is important
        for knowing how many bits to keep in the end.

    Returns
    -------
    twos_data : int or np.ndarray(int)
        The two's complement conversion of the data with num_bits.

    Examples
    --------
    >>>int_to_custom_signed(-5, 16)
    65531
    >>>int_to_custom_signed([-5, 5], 16)
    array([65531, 5])
    >>>int_to_custom_signed(np.array([-5, 5]), 16)
    array([65531, 5])
    """

    if type(data) is np.ndarray:
        # Use bitwise_or to invert bits, then add one, then use bitwise_and to keep only num_bits, allowing the rest to overflow out.
        twos_data = np.where(data & (1 << num_bits - 1), np.bitwise_and(np.bitwise_xor(np.abs(data), 2**num_bits - 1) + 1, 2 ** num_bits - 1), data).astype(int)
    elif type(data) is list:
        data = np.array(data)
        # Use bitwise_or to invert bits, then add one, then use bitwise_and to keep only num_bits, allowing the rest to overflow out.
        twos_data = np.where(data & (1 << num_bits - 1), np.bitwise_and(np.bitwise_xor(np.abs(data), 2**num_bits - 1) + 1, 2 ** num_bits - 1), data).astype(int)
    elif np.issubdtype(type(data), np.integer):
        # Use bitwise_or to invert bits, then add one, then use bitwise_and to keep only num_bits, allowing the rest to overflow out.
        twos_data = np.bitwise_and(np.bitwise_xor(np.abs(data), 2**num_bits - 1) + 1, 2 ** num_bits - 1) if data & (1 << num_bits - 1) else data
        twos_data = int(twos_data)

    return twos_data


def custom_signed_to_int(data, num_bits):
    """Return the Python int form of a two's complement integer in the given number of bits.
    
    Invert all bits (in num_bits), add 1 (only keeping num_bits).

    Parameters
    ----------
    data : int or list(int) or np.ndarray(int)
        The binary data to apply two's complement to.
    num_bits : int
        The number of bits the number is represented in. This is important
        for knowing how many bits to keep in the end.

    Returns
    -------
    int_data : int or np.ndarray(int)
        The two's complement conversion of the data with num_bits.

    Examples
    --------
    >>>custom_signed_to_int(65531, 16)
    -5
    >>>custom_signed_to_int([65531, 5], 16)
    array([-5,  5])
    >>>custom_signed_to_int(np.array([65531, 5]), 16)
    array([-5,  5])
    """

    if type(data) is np.ndarray:
        # Use bitwise_or to invert bits, then add one, then use bitwise_and to keep only num_bits, allowing the rest to overflow out. Multiply by -1 to get the negative integer version.
        int_data = np.where(data & (1 << num_bits - 1), np.bitwise_and(np.bitwise_xor(
            np.abs(data), 2**num_bits - 1) + 1, 2 ** num_bits - 1) * -1, data).astype(int)
    elif type(data) is list:
        data = np.array(data)
        # Use bitwise_or to invert bits, then add one, then use bitwise_and to keep only num_bits, allowing the rest to overflow out. Multiply by -1 to get the negative integer version.
        int_data = np.where(data & (1 << num_bits - 1), np.bitwise_and(np.bitwise_xor(
            np.abs(data), 2**num_bits - 1) + 1, 2 ** num_bits - 1) * -1, data).astype(int)
    elif np.issubdtype(type(data), np.integer):
        # Use bitwise_or to invert bits, then add one, then use bitwise_and to keep only num_bits, allowing the rest to overflow out. Multiply by -1 to get the negative integer version.
        int_data = np.bitwise_and(np.bitwise_xor(np.abs(
            data), 2**num_bits - 1) + 1, 2 ** num_bits - 1) * -1 if data & (1 << num_bits - 1) else data
        int_data = int(int_data)

    return int_data


def to_voltage(data, num_bits, voltage_range, use_twos_comp=False):
    """Convert the binary read data into a float voltage.

    We use the bit-width of the data and the voltage range of the channel
    to determine the voltage per bit. Then we multiply the binary data by
    that voltage for the total voltage.

    Arguments
    ---------
    data : int or list(int) or np.ndarray(np.integer)
        The binary voltage data.
    voltage_range : int
        The total voltage range (peak-to-peak) used for the data.
    use_twos_comp : bool
        True if the given data is in two's complement form, False otherwise.

    Returns
    -------
    float or np.ndarray of float : voltage(s) represented by the given binary data.
    """

    bit_voltage = voltage_range / (2 ** num_bits)
    if use_twos_comp:
        twos_data = twos_comp(data=data, num_bits=num_bits)
        data = np.where(np.array(data) >= (1 << num_bits - 1), -1 * twos_data, twos_data)

    if type(data) is np.ndarray:
        voltage = data * bit_voltage
    elif type(data) is list:
        voltage = np.array(data) * bit_voltage
    elif np.issubdtype(type(data), np.integer):
        voltage = data * bit_voltage
    else:
        raise TypeError(f'to_voltage data expected np.integer, list, or np.ndarray type, got {type(data)}')

    return voltage


def from_voltage(voltage, num_bits, voltage_range, with_negatives=False):
    """Convert the float/int voltage into binary data.

    We use the bit-width and voltage range to determine the voltage per bit.
    Then we divide the voltage by the bit-voltage and round to an integer to
    find the binary data representation.

    Arguments
    ---------
    voltage : np.integer or np.floating or np.ndarray of those
        The voltage data to convert.
    num_bits : int
        The number of bits to convert the voltage data to. Maximum 64.
    voltage_range : int
        The total voltage range (peak-to-peak) used for the voltage.
    with_negatives : bool
        True to convert the voltage with full negative at 0x0, zero at half
        scale, and full positive at full scale, False otherwise.

    Returns
    -------
    np.ndarray of int or int : binary version of voltage data. Scalar int returned if voltage was a scalar.
    """

    if num_bits > 32:
        raise ValueError(f'from_voltage num_bits={num_bits} greater than maximum 32')

    bit_voltage = voltage_range / (2 ** num_bits)

    if type(voltage) is np.ndarray:
        data = (voltage // bit_voltage).astype(int)
    elif type(voltage) is list:
        data = (np.array(voltage) // bit_voltage).astype(int)
    elif np.issubdtype(type(voltage), np.integer) or np.issubdtype(type(voltage), np.floating):
        data = int(voltage // bit_voltage)
    else:
        raise TypeError(f'from_voltage voltage expected np.integer, np.floating, list, or np.ndarray type, got {type(voltage)}')

    if with_negatives:
        data = twos_comp(data=data, num_bits=num_bits)

    # Since this system may overflow to 0 on the maximum value, we limit any
    # input voltages of maximum to full-scale.
    if type(voltage) is int or type(voltage) is float:
        # Keep scalar voltage from converting to 0d array by only using np.where on arrays
        data = 2 ** num_bits - 1 if voltage == voltage_range else int(data)
    else:
        # Use an array
        # Note that this only catches maximum values without negatives, since with negatives the maximum is halved
        data = np.where(voltage == voltage_range, 2 ** num_bits - 1, data)

    return data


def get_timestamp():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


def calc_impedance(v_in, v_out, resistance):
    """Calculate the impedance of an unknown component.
    
    It is assumed the voltage source is connect in series with both the resistor and the unknown component.

    Arguments
    ---------
    v_in : list(int or float)
        The sinusoidal voltage source in the circuit.
    v_out : list(int or float)
        The output voltage across the unknown component.
    resistance : int or float
        The resistance of the resistor in the circuit in Ohms.

    Returns
    -------
    numpy.ndarray : the array of impedances calculated.
    """

    current = np.subtract(v_in, v_out) / resistance

    window = hann(len(v_out), sym=False)
    w_v_out = window * v_out
    w_current = window * current

    impedance_calc = np.divide(rfft(w_v_out), rfft(w_current))
    
    return impedance_calc

def get_memory_usage():
    """Get a sorted list of the objects and their sizes."""

    # These are the usual ipython objects, including this one you are creating
    ipython_vars = ['In', 'Out', 'exit', 'quit', 'get_ipython', 'ipython_vars']

    return sorted([(x, sys.getsizeof(globals().get(x))) for x in dir() if not x.startswith(
        '_') and x not in sys.modules and x not in ipython_vars], key=lambda x: x[1], reverse=True)

def create_filter_coefficients(fc, output_scale=0x2000, 
                        output_offset=0x0000, fs=5e6):
    from scipy.signal import butter, zpk2sos
    from numfi import numfi
    
    order = 4  # eventually order could be an input parameter however the code is 
    word_length = 32
    num_frac = 29
    den_frac = 30
    scale_frac = 31

    class Integer(int):
        ''' same as an int except prints as hex with 8 characters (32 bit wide)
            https://stackoverflow.com/questions/39095294/override-repr-or-pprint-for-int
        '''
        def __repr__(self):
            num_hex_characters = 8
            return "{0:#0{1}x}".format(self, num_hex_characters+2)

    def print_get_int(fix_pt, debug_print=False):
        # print the fixed point value and also return as an 
        # overriden int with a __repr__ method that prints in hex 
        val = Integer(int(t.base_repr(base=2)[0],2))
        if debug_print:
            print(val)
        return val

    if (fc == 'passthru') or (fc == 'passthrough'):
        k = 1
        sos = np.matrix([[1,0,0,1,0,0], 
                         [1,0,0,1,0,0]])
    else: # for any integer cutoff frequency 
        (z,p,k) = butter(order, fc/(fs/2), output='zpk')
        sos = zpk2sos(z,p,1)

    coeffs = {}
    coeff_idx = 0
    # gain of filter scale 1 (coeff_idx 0)
    t = numfi(-k, 1, word_length, scale_frac, fixed=True)
    coeffs[coeff_idx] = print_get_int(t)
    coeff_idx += 1

    for r in range(np.shape(sos)[0]):
        for c in range(np.shape(sos)[1]):
            if (r == 1) and (c == 0):
                coeff_idx = 9 # advance to the second sos stage 
            if c < 2:
                frac_val = num_frac
            if c > 3:
                frac_val = den_frac
            t = numfi(sos[r,c], 1, word_length, frac_val, fixed=True)
            if c!=3:
                coeffs[coeff_idx] = print_get_int(t)
                coeff_idx+=1

    # coefficients 7,8 are scale2, scale3 which are 1 
    scale2_scale3_values = 1
    t = numfi(scale2_scale3_values, 1, word_length, scale_frac, fixed=True)
    coeffs[7] = print_get_int(t)
    coeffs[8] = print_get_int(t)

    coeffs[15] = Integer((output_offset << 14) + output_scale)

    return coeffs


def read_h5(data_dir, file_name, chan_list=[0]):
    """ Read in h5 data and return the time and adc_data for the channels in
    input list

    Arguments
    ---------
    data_dir (string): directory of h5 file
    file_name (string): file name (must include extension)
    chan_list (list of ints): adc channels to return
    
    Returns
    -------
    (numpy.ndarray) time
    (dicionary of numpy.ndarrays) adc data
    """

    SAMPLE_PERIOD = 1 / 5e6

    data_name = os.path.join(data_dir, file_name)
    adc_data = {}
    with h5py.File(data_name, "r") as file:
        dset = file["adc"]
        t = np.arange(len(dset[0, :])) * SAMPLE_PERIOD
        for ch in chan_list:
            adc_data[ch] = dset[ch, :].astype(np.uint16)
    return t, adc_data


def plt_uniques(data, ax=None, block=True):
    """Plot only the first and last of each group of unique data points to save time and memory.

    Parameters
    ----------
    data : np.ndarray
        Data to plot. Must be at least 1 dimensional
    ax : matplotlib.axes._subplots.AxesSubplot
        The axes to plot the data on.
    block : bool
        Whether to block when showing the plot. Used in plt.show(block=block).
    """

    if type(data) is not np.ndarray:
        raise TypeError(f'plt_uniques expected data of type np.ndarray but got {type(data)}')

    if len(data.shape) < 1:
        raise Exception(f'plt_uniques expected data.shape >= 1 but data.shape is {data.shape}')

    if ax is None:
        # No axis provided, create new
        fig, ax = plt.subplots()

    if len(data.shape) > 1:
        # Call recursively until we can plot a line. All lines will end up on the same plot.
        for d in data:
            plt_uniques(data=d, ax=ax, block=False)
        plt.show(block=block)

    else:
        # len(data.shape) == 1, we can plot as normal
        # Get indices of first appearance of unique values
        uniques, indices = np.unique(data, return_index=True)
        # Get indices from just before unique values to get first and last of each group of unique values
        indices = np.append(indices, indices - 1)
        # Add last index so full data is plotted
        indices = np.append(indices, len(data) - 1)

        # Sort data for plotting and remove negative indices (-1 from unique at 0)
        indices = np.sort(indices[indices >= 0])
        # Grab data at indices
        unique_data = data[indices]

        ax.plot(indices, unique_data)
        plt.show(block=block)
