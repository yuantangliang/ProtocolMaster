# encoding:utf-8
import struct


def checksum(*args):
    """
    1的ascii码为49
    >>> data = '123'
    >>> checksum(data)
    150
    """
    sum_value = 0
    for data in args:
        for byte in data:
            sum_value += struct.unpack("@B", byte)[0]
            sum_value &= 0xFF  # 强制截断
    return sum_value


def find_head(buff, start, head):
    """
    >>> buff = "1234567123"
    >>> find_head(buff, 0, '2')
    1
    >>> find_head(buff, 2, '2')
    8
    >>> find_head(buff, 2, '9')
    -1
    """
    pos = buff[start:].find(head)
    if -1 == pos:
        return pos
    return pos + start


class Protocol(object):

    @staticmethod
    def create_frame(self, *args, **kwargs):
        pass

    def get_frame_length(self):
        pass

    def is_have_full_frame(self, data):
        pass

    def get_mess_bytes_length(self):
        pass

_all_protocols = dict()


def protocol_register(media_class):
    global _all_protocols
    _all_protocols[media_class.__name__] = media_class
    return media_class


def protocol_create(name):
    from ..user_exceptions import FoundClassException
    protocol_class = _all_protocols(name)
    if protocol_class is None:
        raise FoundClassException(name)
    return protocol_class()



