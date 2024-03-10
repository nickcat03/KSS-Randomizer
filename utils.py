#Utility functions

import binascii
import os

#Self explanatory...
def writeBytesToFile(file,data,address,bytes):
	file.seek(address)
	file.write(data)
	print("Wrote " + str(data) + " to " + str(address))

#Windows and Unix have different file pathing formats. This to make sure each OS gets the correct filepath
def convert_file_path_format(filepath):
    if os.name == 'nt':
        filepath = filepath.replace('/','\\')
    else:
        return filepath

def removeBrackets(value):
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
