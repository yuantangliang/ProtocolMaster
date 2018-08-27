# encoding:utf-8
from media import media_register, Media, MediaOptions, MediaText
import os
from collections import OrderedDict
import serial
from PyQt4.QtCore import QTimer, pyqtSignal
from tools.converter import str2bytearray
from serial import SerialException
import socket
from Queue import Queue
from threading import Thread
from tools.converter import str2bytearray


def receive_from_socket(tcp_media):
    while tcp_media.receiving:
        data = tcp_media.socket.recv(1)
        tcp_media.rcv_queue.put(data)


@media_register
class TCPMedia(Media):

    def __init__(self):
        super(TCPMedia, self).__init__(self._get_all_options())
        self.socket = None
        self.read_timer = QTimer()
        self.read_timer.timeout.connect(self._receive)
        self.read_timer.start(10)
        self.rcv_queue = Queue()
        self.receiving = True
        self.rcv_thread = None

    def open(self):
        if self.socket is None:
            selected_options = self.get_selected_options()
            selected_options["timeout"] = 0
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.connect((selected_options["IP"], int(selected_options["PORT"])))
            self.receiving = True
            self.rcv_thread = Thread(target=receive_from_socket, args=(self,))
            self.rcv_thread.start()
        except socket.error, e:
            print "error happen",e.message
            self.refresh_media_options()
            return False
        return  True

    def _get_all_options(self):
        options = list()
        options.append(MediaText("IP", "127.0.0.1"))
        options.append(MediaText("PORT", "8266", u"端口号"))
        return options

    def refresh_media_options(self):
        self.media_options = self._get_all_options()
        self.load_saved_options()

    def close(self):
        if self.socket is not None:
            self.socket.close()
        if self.rcv_thread is not None and  self.rcv_thread.isAlive():
            self.receiving = False
            self.rcv_thread.join()

    def send(self, data):
        self.socket.send(data)

    def _receive(self):
        data = ""
        while not self.rcv_queue.empty():
            data += self.rcv_queue.get()
        if len(data) > 0:
            self.data_ready.emit(str2bytearray(data))

    def set_media_options(self, options):
        self.read_timer.stop()
        super(TCPMedia, self).set_media_options(options)
        if self.socket is not None:
            self.socket.close()
        self.socket = None
        is_open = self.open()
        self.read_timer.start(10)
        return is_open


if __name__ == "__main__":
    import json
    serial = TCPMedia()
    print json.dumps(serial.get_media_options(), ensure_ascii=False, encoding='UTF-8')