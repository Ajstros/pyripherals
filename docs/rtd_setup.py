"""Set up for Read the Docs build.

Need to create a YAML with the correct path to Registers.xlsx so RTD can find it.
"""

import os

home_dir = os.path.join(os.path.expanduser('~'), '.pyripherals')
config_path = os.path.join(home_dir, 'config.yaml')

doc_configs = {
    'endpoint_max_width': 32,
    'fpga_bitfile_path': None,
    'ep_defines_path': None,
    'registers_path': './python/Registers.xlsx',
    'frontpanel_path': 'C:/Program Files/Opal Kelly/FrontPanelUSB',
}

print('home_dir:', home_dir)
print('config_path:', config_path)

os.mkdir(home_dir)
with open(config_path, 'w') as file:
    file.write(doc_configs)
