# encoding:utf-8


class FifoBuffer(object):
    """
    >>> buff = FifoBuffer()
    >>> buff.receive('123')
    >>> buff.peek(4)
    '123'
    >>> buff.read(1)
    '1'
    >>> buff.peek(2)
    '23'
    """

    def __init__(self):
        self.buff = ""

    def receive(self, data):
        self.buff += data

    def peek(self, length):
        length = min(length, len(self.buff))
        return self.buff[0:length]

    def read(self, length):
        data = self.peek(length)
        assert length >= 0, "length must be greater then 0"
        if length == 0:
            return ""

        if len(self.buff) <= length:
            self.buff = ""
        else:
            self.buff = self.buff[length:]
        return data
