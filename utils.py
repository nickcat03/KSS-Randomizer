#Utility functions

import binascii
import os
import sys

#Self explanatory...
def write_bytes_to_file(file, data, address):
	file.seek(address)
	file.write(data)
     
	hex_data = ''.join(format(byte, '02X') for byte in data)
	print("Wrote " + hex_data + " to " + hex(address))

#Windows and Unix have different file pathing formats. This to make sure each OS gets the correct filepath
def convert_file_path_format(filepath):
    if os.name == 'nt':
        filepath = filepath.replace('/',chr(92))
        return filepath
    else:
        return filepath

def remove_brackets(value):
	value = str(value)
	value = value.strip("[")
	value = value.strip("]")
	value = value.strip("'")
	return value

def hex_string_to_bytes(hex_string, desired_length):
    # Strip any leading '0x' if present
    hex_string = hex_string.lstrip('0x')

    # Make hex string even
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string

    # Calculate the number of bytes in the hex string
    num_bytes = len(hex_string) // 2

    # If the number of bytes is less than the desired length, pad with zeros at the beginning
    if num_bytes < desired_length:
        hex_string = '0' * (2 * (desired_length - num_bytes)) + hex_string

    # Convert the hex string to bytes
    return bytes.fromhex(hex_string)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)