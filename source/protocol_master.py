# encoding:utf-8
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from protocol_master_ui import Ui_MainWindow
from device.device import get_all_device, find_device_by_address
from session import SessionSuit
from protocol.CJT188_protocol import DIDReadMeter,CJT188Protocol
from protocol.DL645_protocol import DIDReadAddress,DIDRealTimeMeterData
from tools.converter import str2hexstr, hexstr2str
from protocol.codec import BinaryDecoder,BinaryEncoder


class EsMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(EsMainWindow, self).__init__()
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0,350)
        self.tableWidget.setColumnWidth(1,350)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        devices = get_all_device()
        self.tableWidget.setRowCount(len(devices))
        for i, device in enumerate(devices):
            widget = QTableWidgetItem(device.get_hex_string_address())
            self.tableWidget.setItem(i, 0, widget)
            device.device_update.connect(self.sync_to_ui)
        self.send_idx = 0
        self.devices = devices
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_next_device)
        self.is645 = False
        self.session = SessionSuit.create_188_suit()
        self.session.data_ready.connect(self.protocol_handle)

    def sync_to_ui(self):
        for i, device in enumerate(self.devices):
            widget = QTableWidgetItem(device.get_summary())
            self.tableWidget.setItem(i, 1, widget)

    def read_next_device(self):
        device = self.devices[self.send_idx]
        device.add_send_count()
        self.send_idx += 1
        self.send_idx %= len(self.devices)
        self.sync_to_ui()
        if self.is645:
            self.session.send_data(hexstr2str(str(self.convertAddressLineEdit.text())), DIDRealTimeMeterData(device.address))
        else:
            self.session.send_data(device.address, DIDReadMeter())

    def eventFilter(self, source, event):
        if source == self.video_label and event.type() == QEvent.MouseButtonPress:
            return True
        else:
            return QMainWindow.eventFilter(self, source, event)

    def start(self):
        self.timer.start(7000)

    def stop(self):
        self.timer.stop()

    def read_convert_address(self):
        self.session.send_data(chr(0xaa)*6, None, cmd=0x13)

    def is645Taggle(self, is645):
        self.is645 = is645
        self.session.close()
        if self.is645:
            self.session = SessionSuit.create_645_suit()
        else:
            self.session = SessionSuit.create_188_suit()
        self.session.data_ready.connect(self.protocol_handle)

    def protocol_handle(self, protocol):
        if self.is645:
            if protocol.cmd == chr(0x93):
                self.convertAddressLineEdit.setText(str2hexstr(protocol.address))
            if protocol.cmd == chr(0x91):
                device = find_device_by_address(protocol.did_unit.address)
                if device is not None:
                    device.add_receive_count()
                else:
                    print "receive from unknown device,device is not found", str2hexstr(protocol.did_unit.address)
        else:
            device = find_device_by_address(protocol.address)
            if device is not None:
                device.add_receive_count()
            else:
                print "receive from unknown device,device is not found"


def protocol_master_run():
    app = QApplication(sys.argv)
    ex = EsMainWindow()
    print QApplication.desktop().width(), QApplication.desktop().height()
    ex.move((QApplication.desktop().width() - ex.width()) / 2, (QApplication.desktop().height() - ex.height()) / 2);
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    protocol_master_run()
