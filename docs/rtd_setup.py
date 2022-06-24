"""Set up for Read the Docs build.

Need to create a YAML with the correct path to Registers.xlsx so RTD can find it.
"""

import os

home_dir = os.path.join(os.path.expanduser('~'), '.pyripherals')
config_path = os.path.join(home_dir, 'config.yaml')

doc_configs = '''endpoint_max_width: 32
ep_defines_path: none
fpga_bitfile_path: none
frontpanel_path: none
registers_path: /python/Registers.xlsx'''

print('home_dir:', home_dir)
print('config_path:', config_path)
print(os.path.exists('/python/Registers.xlsx'))
print(os.path.abspath('/python/Registers.xlsx'))

os.mkdir(home_dir)
with open(config_path, 'w') as file:
    file.write(doc_configs)
