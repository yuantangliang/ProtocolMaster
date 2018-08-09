# encoding:utf-8
from protocol import Protocol, protocol_register
from protocol import checksum, find_head
from codec import BinaryEncoder
from tools.converter import hexstr2str, str2hexstr

DL645_HEAD = chr(0x68)
DL645_TAIL = chr(0x16)

class DID_504d(object):
    """
    68+转换器地址+68+01+L+50 4D(倒序+33为8083)+188完整报文（+33）+CS+16
    """
    def __init__(self):
        self.serial = 0

    def encode(self, encoder):
        encoder.encode_byte(0x4d)
        encoder.encode_byte(0x50)

    def decode(self, decoder):
        pass


def data_encrypt(data):
    out = ""
    for byte in data:
        out += chr(ord(byte)+0x33)
    return out

@protocol_register
class DL645Protocol(Protocol):
    """
    >>> encoder = BinaryEncoder()
    >>> protocol = DL645Protocol()
    >>> encoder.encode_object(protocol)
    >>> str2hexstr(encoder.get_data())
    '68 11 11 11 11 11 11 68 01 02 80 83 3C 16'
    """

    def __init__(self):
        self.address = chr(0x11)*6
        self.meter_type = 0x10
        self.cmd = 0x01
        self.length = 0x04
        self.did_unit = DID_504d()
        self.serial = 0x90

    def encode(self, encoder):
        encoder.encode_str(DL645_HEAD)
        encoder.encode_str(self.address)
        encoder.encode_str(DL645_HEAD)
        encoder.encode_byte(self.cmd)
        did_data = encoder.object2data(self.did_unit)
        encoder.encode_byte(len(did_data))
        did_data = data_encrypt(did_data)
        encoder.encode_str(did_data)
        encoder.encode_byte(checksum(encoder.get_data()))
        encoder.encode_str(DL645_TAIL)

    def decode(self, decoder):
        pass

    @staticmethod
    def find_frame_in_buff(data):
        """
        >>> receive_str =" fe fe 68 11 11 11 11 11 11 68 01 02 43 C3 3F 16 "
        >>> receive_data = hexstr2str(receive_str)
        >>> protocol =  DL645Protocol()
        >>> protocol.find_frame_in_buff(receive_data)
        (True, 2, 14)
        >>> receive_data = hexstr2str("68 10 01 02 03 04 05 ")
        >>> protocol.find_frame_in_buff(receive_data)
        (False, 0, 0)
        """
        start_pos = 0
        found = 0
        while start_pos < (len(data) - 11):
            start_pos = find_head(data, start_pos, DL645_HEAD)
            if start_pos == -1:
                break
            frame_data = data[start_pos:]

            if len(frame_data) < 10:
                break

            data_len = ord(frame_data[9])

            if data_len + 12 > len(frame_data):
                start_pos += 1
                continue
            if ord(frame_data[10+data_len])  != checksum(frame_data[0:data_len+10]):
                start_pos += 1
                continue
            if frame_data[11+data_len] != DL645_TAIL:
                start_pos += 1
                continue
            found = 1
            break

        if found:
            return True, start_pos, data_len+12
        else:
            return False, 0, 0





