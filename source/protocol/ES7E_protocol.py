# encoding:utf-8
from protocol import Protocol, protocol_register
from protocol import checksum, find_head
from codec import BinaryEncoder, BinaryDecoder
from tools.converter import hexstr2str, str2hexstr

ES7E_HEAD = chr(0x7e)


class DIDSetAddress(object):
    def encode(self, encoder):
        encoder.encode_byte(0x13)
        encoder.encode_byte(0x00)

    def decode(self, decoder):
        pass


class DIDSwitchReverse(object):
    """
    """

    def __init__(self, data=None):
        self.data = data

    def encode(self, encoder):
        encoder.encode_byte(0x18)
        encoder.encode_byte(0xc0)
        encoder.encode_byte(0x01)
        encoder.encode_byte(self.data)

    def decode(self, decoder):
        decoder.decode_str(54) # did
        self.address = decoder.decode_str(7)[::-1]


#设置地址 7E 00 00 00 00 00 00 00 00 00 05 01 01 00 00 00 85
#四路开关执行器翻转报文：7E 01 00 00 00 36 0D 0C 00 06 05 07 18 C0 01 0F C8

@protocol_register
class ES7EProtocol(Protocol):
    """
    >>> encoder = BinaryEncoder()
    >>> protocol = ES7EProtocol(DIDSwitchReverse(0x0f))
    >>> encoder.encode_object(protocol)
    >>> str2hexstr(encoder.get_data())
    '7E 01 00 00 00 36 0D 0C 00 06 05 07 18 C0 01 0F C8'
    """

    @staticmethod
    def create_frame(*args, **kwargs):
        protocol = ES7EProtocol()
        #protocol.address = args[0]
        protocol.did_unit = args[1]
        # if kwargs.has_key("cmd"):
        #     protocol.cmd = kwargs["cmd"]
        return protocol

    def __init__(self, did_unit=None):
        self.src_address = chr(0x1) + chr(0) + chr(0) + chr(0)
        self.dst_address = chr(0x36) + chr(0x0d) + chr(0x0c) + chr(0x00)
        self.serial = 0x06
        self.length = 0x05
        self.cmd = 0x7
        self.did_unit = did_unit

    def encode(self, encoder):
        encoder.encode_str(ES7E_HEAD)
        encoder.encode_str(self.src_address)
        encoder.encode_str(self.dst_address)
        encoder.encode_byte(self.serial)
        encoder.encode_byte(self.length)
        encoder.encode_byte(self.cmd)
        encoder.encode_object(self.did_unit)
        encoder.encode_byte(checksum(encoder.get_data()))


    def decode(self, decoder):
        decoder.decode_str(1)
        self.address = decoder.decode_str(6)[::-1]
        decoder.decode_str(1)
        self.cmd = decoder.decode_str(1)
        self.length = decoder.decode_byte()
        if self.length > 30:
            did_data = decoder.decode_str(self.length)
            did_decoder = BinaryDecoder()
            did_decoder.set_data(did_data)
            self.did_unit = did_decoder.decoder_for_object(DIDSwitchReverse)

    @staticmethod
    def find_frame_in_buff(data):
        """
        >>> receive_str ="fe fe 7E 36 0D 0C 00 01 00 00 00 86 05 07 12 C0 01 00 33"
        >>> receive_data = hexstr2str(receive_str)
        >>> protocol =  ES7EProtocol()
        >>> protocol.find_frame_in_buff(receive_data)
        (True, 2, 17)
        >>> receive_data = hexstr2str("68 10 01 02 03 04 05 ")
        >>> protocol.find_frame_in_buff(receive_data)
        (False, 0, 0)
        """
        start_pos = 0
        found = 0
        while start_pos < (len(data) - 11):
            start_pos = find_head(data, start_pos, ES7E_HEAD)
            if start_pos == -1:
                break
            frame_data = data[start_pos:]

            if len(frame_data) < 10:
                break

            data_len = ord(frame_data[10])

            if data_len + 12 > len(frame_data):
                start_pos += 1
                continue
            if ord(frame_data[11+data_len])  != checksum(frame_data[0:data_len+10]):
                start_pos += 1
                continue
            found = 1
            break

        if found:
            return True, start_pos, data_len+12
        else:
            return False, 0, 0





