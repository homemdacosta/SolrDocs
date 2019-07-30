# Import configuration Parser
from configparser import SafeConfigParser
import sys

parser = SafeConfigParser()
parser.read('config.ini')

def set_configuration (section='file_location', option = 'path', value=''):
    parser.set(section, option, value)
    # Writing our configuration file to 'config.ini'
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)

def get_configuration (section='file_location', option = 'path'):
    return parser.get(section, option)