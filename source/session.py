# encoding:utf-8
from media.serial_media import SerialMedia
from protocol.codec import BinaryEncoder, BinaryDecoder
from protocol.CJT188_protocol import CJT188Protocol, Protocol
from protocol.DL645_protocol import DL645Protocol
from protocol.fifo_buffer import FifoBuffer
from tools.converter import hexstr2str, str2hexstr
from PyQt4.QtCore import QObject, pyqtSignal
from tools.converter import bytearray2str


class SessionSuit(QObject):
    data_ready = pyqtSignal(Protocol)

    @staticmethod
    def create_188_suit():
        media = SerialMedia()
        media.open()
        encoder = BinaryEncoder()
        decoder = BinaryDecoder()
        return SessionSuit(media, encoder, decoder, CJT188Protocol)

    @staticmethod
    def create_645_suit():
        media = SerialMedia()
        media.open()
        encoder = BinaryEncoder()
        decoder = BinaryDecoder()
        return SessionSuit(media, encoder, decoder, DL645Protocol)

    def __init__(self, media, encoder, decoder, protocol_cls):
        media.data_ready.connect(self.handle_receive_data)
        media.open()
        self.media = media
        self.encoder = encoder
        self.decoder = decoder
        self.protocol_cls = protocol_cls
        self.buffer = FifoBuffer()
        super(SessionSuit, self).__init__()

    def handle_receive_data(self, string):
        string = bytearray2str(string)
        assert len(string) > 0
        self.buffer.receive(string)
        data = self.buffer.peek(10000)
        protocol = self.protocol_cls()
        (found, start, length) = protocol.find_frame_in_buff(data)
        if found:
            self.buffer.read(start + length)
            print "rcv", str2hexstr(data[0:start + length])
            frame_data = data[start:start+length]
            self.decoder.set_data(frame_data)
            protocol.decode(self.decoder)
            self.data_ready.emit(protocol)


    def send_data(self, address, data, **kwargs):
        protocol = self.protocol_cls.create_frame(address, data, **kwargs)
        self.encoder.encode_object(protocol)
        data = self.encoder.get_data()
        self.media.send(data)
        print "snd",str2hexstr(data)
        self.encoder.reset()

    def close(self):
        self.media.close()
