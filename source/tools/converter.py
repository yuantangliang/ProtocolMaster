# encoding:utf-8
import struct


def hexstr2str(string):
    """
    >>> data = " 0x31  0x32  0x33 "
    >>> hexstr2str(data)
    '123'
    """
    string = string.strip()
    hex_data = ""
    print string
    for byte in string.split(" "):
        if byte is '':
            continue
        for i in range(0, len(byte), 2):
            hex_data += struct.pack("@B", int(byte[i:i+2], 16))
    return hex_data


def str2hexstr(string):
    des = ""
    for byte in string:
        des += "%02x" %(ord(byte))
        des += " "
    return des.strip().upper()


def str2bytearray(string):
    array = bytearray()
    for x in string:
        array += x
    return array


def bytearray2str(bytes):
    out = ""
    for x in bytes:
        out += chr(x)
    return out

