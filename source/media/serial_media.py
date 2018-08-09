# encoding:utf-8
from media import media_register, Media
import os
from collections import OrderedDict
import serial
from PyQt4.QtCore import QTimer, pyqtSignal
from tools.converter import str2bytearray

@media_register
class SerialMedia(Media):
    data_ready = pyqtSignal(bytearray)

    @staticmethod
    def find_possible_port():
        if os.name == 'nt':
            from serial.tools.list_ports_windows import comports
        elif os.name == 'posix':
            from serial.tools.list_ports_posix import comports
        else:
            raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))
        ports  = comports(True)
        outputs = [port.device for port in ports]
        return outputs

    def __init__(self):
        options = OrderedDict()
        options[u"端口号"] = self.find_possible_port()
        options[u"波特率"] = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
        options[u"校验位"] = [u"奇校验", u"偶校验"]
        self.serial = None
        self.read_timer = QTimer()
        self.read_timer.timeout.connect(self._receive)
        self.read_timer.start(10)
        super(SerialMedia, self).__init__(options)

    def open(self):
         if self.serial is None:
            self.serial = serial.Serial(port="COM36", baudrate=2400, parity=serial.PARITY_EVEN, timeout = 0)
         return True

    def close(self):
        self.serial.close()

    def send(self, data):
        self.serial.write(data)

    def _receive(self):
        data = self.serial.read(100)
        if len(data) > 0:
            self.data_ready.emit(str2bytearray(data))


if __name__ == "__main__":
    import json
    serial = SerialMedia()
    print json.dumps(serial.get_media_options(), ensure_ascii=False, encoding='UTF-8')