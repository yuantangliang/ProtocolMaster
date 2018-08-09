# encoding:utf-8
from tools.converter import str2hexstr, hexstr2str
from PyQt4.QtCore import pyqtSignal, QObject


class Device(QObject):
    device_update = pyqtSignal()

    def __init__(self, address):
        super(Device, self).__init__()
        self.send_count = 0
        self.receive_count = 0
        self.address = address

    def get_summary(self):
        if 0 == self.send_count:
            rate = 1
        else:
            rate = float(self.receive_count)/self.send_count
        info = "send {0},receive {1},rate {2}%".format(self.send_count,
                                                       self.receive_count,
                                                       rate*100)
        return info

    def add_send_count(self):
        self.send_count += 1
        self.device_update.emit()

    def add_receive_count(self):
        self.receive_count += 1
        self.device_update.emit()

    def get_hex_string_address(self):
        return str2hexstr(self.address)

devices = None


def get_all_device():
    global devices
    if devices is None:
        devices = list()
        for address in ["00001802050362"]:
            devices.append(Device(hexstr2str(address)))
    return devices


def find_device_by_address(address):
    for device in devices:
        if device.address == address:
            return device
    return None

