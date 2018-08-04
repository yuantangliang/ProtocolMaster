import struct

import numpy as np


class BinaryEncoder(object):
    def __init__(self):
        self.data = ""

    def encode_str(self, str):
        self.data += str

    def encode_short(self, nb):
        self.data += struct.pack("@h", nb)

    def encode_int(self, nb):
        self.data += struct.pack("@i", nb)

    def encode_nparray_short(self, nparray):
        nparray = np.round(nparray)
        nparray = nparray.astype(np.int32)
        self.data += self._encode_nparray(nparray, "@h")

    def encode_nparray_byte(self, nparray):
        nparray = np.round(nparray)
        nparray = nparray.astype(np.int32)
        self.data += self._encode_nparray(nparray, "@b")

    def encode_nparray_int(self, nparray):
        nparray = np.round(nparray)
        nparray = nparray.astype(np.int32)
        self.data += self._encode_nparray(nparray, "@i")

    def encode_char(self, nb):
        self.data += struct.pack("@b", nb)

    def _encode_nparray(self, nparray, fmt):
        shape = nparray.shape
        if len(shape) == 2:
            nparray = nparray.reshape(1, 1, shape[0], shape[1])
        elif len(shape) == 3:
            nparray = nparray.reshape(1, shape[0], shape[1], shape[2])
        elif len(shape) == 1:
            nparray = nparray.reshape(1, 1, 1, shape[0])
        str1 = str()
        for three_dim_array in nparray:
            for two_dim_array in three_dim_array:
                for one_dim_array in two_dim_array:
                    for item in one_dim_array:
                        try:
                            data = struct.pack(fmt, item)
                            str1 += data
                        except:
                            print "error: encode  %d" % (item)
        return str1

    def get_binary_data(self, size=None):
        if size is not None:
            padding = size - len(self.data)
            self.data += padding * chr(0)
        return self.data
