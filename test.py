def hex_string_to_bytes(hex_string, desired_length):
    # Strip any leading '0x' if present
    hex_string = hex_string.lstrip('0x')

    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string

    # Calculate the number of bytes in the hex string
    num_bytes = len(hex_string) // 2

    # If the number of bytes is less than the desired length, pad with zeros at the beginning
    if num_bytes < desired_length:
        hex_string = '0' * (2 * (desired_length - num_bytes)) + hex_string

    print(hex_string)

    # Convert the hex string to bytes
    return bytes.fromhex(hex_string)

# Example usage:
hex_string = "0x03"
desired_length = 1
result = hex_string_to_bytes(hex_string, desired_length)
print(result)
hex_data = ''.join(format(byte, '02X') for byte in result)
print(hex_data)