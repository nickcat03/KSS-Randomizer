#Utility functions

import binascii
import os
import sys

#Self explanatory...
def writeBytesToFile(file,data,address,bytes):
	file.seek(address)
	file.write(data)
	print("Wrote " + str(data) + " to " + str(address))

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

def hex_string_to_bytes(hex_string):
    # Strip any leading '0x' if present
    hex_string = hex_string.lstrip('0x')

    # Ensure the length of the hex string is even
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string
    print(hex_string)

    # Convert the hex string to bytes
    return bytes.fromhex(hex_string)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)