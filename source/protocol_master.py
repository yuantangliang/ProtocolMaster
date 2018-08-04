import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from protocol_master_ui import Ui_MainWindow


class EsMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(EsMainWindow, self).__init__()
        self.setupUi(self)

    def eventFilter(self, source, event):
        if source == self.video_label and event.type() == QEvent.MouseButtonPress:
            # self.mark_box(event.x(), event.y())
            return True
        else:
            return QMainWindow.eventFilter(self, source, event)


def protocol_master_run():
    app = QApplication(sys.argv)
    ex = EsMainWindow()
    print QApplication.desktop().width(), QApplication.desktop().height()
    ex.move((QApplication.desktop().width() - ex.width()) / 2, (QApplication.desktop().height() - ex.height()) / 2);
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    protocol_master_run()
