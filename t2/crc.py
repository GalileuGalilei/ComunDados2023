def crc(data, polynomial):
    # Pad the data with zeros to match the length of the polynomial
    data += ['0'] * (len(polynomial) - 1)

    # Perform CRC calculation
    for i in range(len(data) - len(polynomial) + 1):
        if data[i] == '0':
            continue

        for j in range(len(polynomial)):
            data[i + j] = str(int(data[i + j]) ^ int(polynomial[j]))

    # Return the CRC trailer (remainder)
    return data[-(len(polynomial) - 1):]


def verify_crc(data, polynomial):
    # Pad the data with zeros to match the length of the polynomial
    data += ['0'] * (len(polynomial) - 1)

    # Perform CRC calculation
    for i in range(len(data) - len(polynomial) + 1):
        if data[i] == '0':
            continue

        for j in range(len(polynomial)):
            data[i + j] = str(int(data[i + j]) ^ int(polynomial[j]))

    # Check if the remainder (CRC trailer) is zero
    return all(bit == '0' for bit in data[-(len(polynomial) - 1):])
