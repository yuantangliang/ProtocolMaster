import struct
import numpy as np


class Encoder(object):
    def __init__(self):
        self.data = ""

    def encode_str(self, str):
        pass

    def encode_char(self, nb):
        pass

    def encode_unsigned_short(self, nb):
        pass

    def encode_int(self, nb):
       pass

    def encode_object(self, nb):
        pass

    def object2data(self):
        pass

    def get_data(self):
        pass


class Decoder(object):
    pass


class BinaryEncoder(Encoder):
    def __init__(self):
        self.data = ""

    def encode_str(self, str):
        self.data += str

    def encode_byte(self, nb):
        self.data += struct.pack("@B", nb)

    def encode_unsigned_short(self, nb):
        self.data += struct.pack("@H", nb)

    def encode_short(self, nb):
        self.data += struct.pack("@h", nb)

    def encode_int(self, nb):
        self.data += struct.pack("@i", nb)

    def encode_object(self, object_data):
        object_data.encode(self)

    def object2data(self, object_data):
        encoder = BinaryEncoder()
        object_data.encode(encoder)
        return encoder.get_data()

    def get_data(self, size=None):
        if size is not None:
            padding = size - len(self.data)
            self.data += padding * chr(0)
        return self.data

    def reset(self):
        self.data = ""


class BinaryDecoder(Decoder):

    def __init__(self, data=None):
        self.data = data

    def decoder_for_object(self, cls, data):
        protocol = cls(self)
        return protocol

    def decode_str(self, length):
        data = self.data[0:length]
        self.data = self.data[length:]
        return data

    def decode_byte(self):
        data = self.decode_str(1)
        return ord(data)

    def set_data(self, data):
        self.data = data