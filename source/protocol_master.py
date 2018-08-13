# encoding:utf-8
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from protocol_master_ui import Ui_MainWindow
from device.device import get_all_device, find_device_by_address
from session import SessionSuit
from protocol.CJT188_protocol import DIDReadMeter,CJT188Protocol
from protocol.DL645_protocol import DIDReadAddress,DIDRealTimeMeterData, DL645Protocol
from protocol.ES7E_protocol import DIDSwitchReverse
from tools.converter import str2hexstr, hexstr2str
from protocol.codec import BinaryDecoder,BinaryEncoder
from ui.media_option_ui import get_user_options
from config import ESConfig
from serial import SerialException
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class EsMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(EsMainWindow, self).__init__()
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0,350)
        self.tableWidget.setColumnWidth(1,350)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_next_device)

        self.is645 = False
        self.session = SessionSuit.create_188_suit()
        self.session.data_ready.connect(self.protocol_handle)
        self.show_media_config(self.session.media)

        self.switch_session = SessionSuit.create_7E_suit()
        self.switch_timer = QTimer()
        self.switch_timer.setSingleShot(True)
        self.switch_timer.timeout.connect(self.switch_reverse)
        self.switch_session.media.open()

        action = QAction(u"通信参数", self)
        action.setShortcut("Ctrl+R")
        action.triggered.connect(self.show_communication_media)
        self.menuSet.addAction(action)
        self.toolbar.addAction(action)

        action = QAction(u"通断串口参数", self)
        action.setShortcut("Ctrl+R")
        action.triggered.connect(self.show_switch_media)
        self.menuSet.addAction(action)
        self.toolbar.addAction(action)

        action = QAction(u"导入设备", self)
        action.triggered.connect(self.import_device_list)
        self.menuDevice.addAction(action)
        self.toolbar.addAction(action)

        devices = get_all_device(ESConfig.get_instance().get_device_file())
        self.devices = devices
        self.sync_device_to_ui()
        self.send_idx = 0

    def switch_reverse(self):
        self.switch_session.send_data("789841", DIDSwitchReverse(0x08))

    def show_switch_media(self):
        self.show_media_config(self.switch_session.media)

    def show_communication_media(self):
        self.show_media_config(self.session.media)

    @staticmethod
    def show_media_config(media):
        def ok_button_press(select_options):
            media.set_media_options(select_options)
        options = media.get_media_options()
        get_user_options(options, ok_button_press)

    def import_device_list(self):
        file_name = QFileDialog.getOpenFileName(directory=ESConfig.get_instance().get_device_file())
        file_name = unicode(file_name.toUtf8(), 'utf-8', 'ignore')
        ESConfig.get_instance().set_device_file(file_name)
        self.devices = get_all_device(file_name)
        self.sync_device_to_ui()

    def sync_device_to_ui(self):
        devices = self.devices
        self.tableWidget.setRowCount(len(devices))
        for i, device in enumerate(devices):
            widget = QTableWidgetItem(device.get_hex_string_address())
            self.tableWidget.setItem(i, 0, widget)
            device.device_update.connect(self.sync_status_to_ui)
        self.send_idx = 0

    def sync_status_to_ui(self):
        for i, device in enumerate(self.devices):
            widget = QTableWidgetItem(device.get_summary())
            self.tableWidget.setItem(i, 1, widget)

    def read_next_device(self):
        device = self.devices[self.send_idx]
        device.add_send_count()
        self.send_idx += 1
        self.send_idx %= len(self.devices)
        self.sync_status_to_ui()
        if self.is645:
            self.session.send_data(hexstr2str(str(self.convertAddressLineEdit.text())), DIDRealTimeMeterData(device.address))
        else:
            self.session.send_data(device.address, DIDReadMeter())
        value = random.randrange(0, 1000)
        self.switch_timer.start(1200+value)

    def eventFilter(self, source, event):
        if source == self.video_label and event.type() == QEvent.MouseButtonPress:
            return True
        else:
            return QMainWindow.eventFilter(self, source, event)

    def start(self):
        if len(self.devices) == 0:
            QMessageBox.information(self, u"导入设备", u"轮抄需要首先导入设备列表")
            return
        self.read_next_device()
        self.timer.start(int(float(str(self.readMeterSpanLineEdit.text()))*1000))

    def stop(self):
        self.timer.stop()

    def read_convert_address(self):
        if self.is645:
            self.session.send_data(chr(0xaa)*6, None, cmd=0x13)

    def is645Taggle(self, is645):
        self.is645 = is645
        if self.is645:
            self.session.protocol_cls = DL645Protocol
        else:
            self.session.protocol_cls = CJT188Protocol

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
