# encoding:utf-8
from media import media_register, Media, MediaOptions
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
        ports = comports(True)
        outputs = [port.device for port in ports]
        return outputs

    def __init__(self, name):
        super(SerialMedia, self).__init__(self.refresh_serial_options(), name)
        self.serial = None
        self.read_timer = QTimer()
        self.read_timer.timeout.connect(self._receive)
        self.read_timer.start(10)

    def open(self):
        if self.serial is None:
            selected_options = self.get_selected_options()
            selected_options["timeout"] = 0
        try:
            self.serial = serial.Serial(**selected_options)
        except serial.SerialException:
            self.media_options = self.refresh_serial_options()
            self.load_last_options()
            print "open serial error"
            return False
        return True

    def refresh_serial_options(self):
        options = list()
        options.append(MediaOptions("port", self.find_possible_port(), u"端口号"))
        options.append(MediaOptions("baudrate", serial.Serial.BAUDRATES, u"波特率"))
        parity_show_option = ['None', 'Even', 'Odd', 'Mark', 'Space']
        parity_options = [serial.PARITY_NONE,serial.PARITY_EVEN,serial.PARITY_ODD,serial.PARITY_MARK,serial.PARITY_SPACE]
        options.append(MediaOptions("parity", parity_options, u"校验位", parity_show_option))
        return options

    def close(self):
        self.serial.close()

    def send(self, data):
        self.serial.write(data)

    def _receive(self):
        if self.serial is not None and self.serial.is_open:
            data = self.serial.read(100)
            if len(data) > 0:
                self.data_ready.emit(str2bytearray(data))

    def set_media_options(self, options):
        self.read_timer.stop()
        super(SerialMedia, self).set_media_options(options)
        if self.serial is not None:
            self.serial.close()
        self.serial = None
        self.open()
        self.read_timer.start(10)


if __name__ == "__main__":
    import json
    serial = SerialMedia()
    print json.dumps(serial.get_media_options(), ensure_ascii=False, encoding='UTF-8')