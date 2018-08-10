# -*- coding: utf-8 -*-

from media_option_example import Ui_ChannelDialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui


class EsUserOptionsDialog(QDialog):
    def __init__(self):
        super(EsUserOptionsDialog, self).__init__()
        self.options = []
        self.setModal(True)
        self.ok_func = None
        self.vlayout = None
        self.group_widget =None
        self.widget_list =[]

    def setup_ui(self):
        #self.resize(237, 298)
        self.vlayout = QVBoxLayout()
        self.vlayout.setSpacing(20)
        self.config_groups = QtGui.QGroupBox(self.group_widget)
        self.config_layout = QtGui.QGridLayout(self.config_groups)
        self.config_layout.setHorizontalSpacing(20)
        self.config_layout.setVerticalSpacing(10)
        for i,option in enumerate(self.options):
            combobox = QtGui.QComboBox(self.config_groups)
            combobox.addItems(option.get_options())
            combobox.setCurrentIndex(option.select_id)
            self.widget_list.append(combobox)
            self.config_layout.addWidget(combobox, i, 1, 1, 1)
            label = QtGui.QLabel(self.config_groups)
            size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
            label.setSizePolicy(size_policy)
            label.setText(option.label_text)
            self.config_layout.addWidget(label, i, 0, 1, 1)

        self.vlayout.addWidget(self.config_groups)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.vlayout.addWidget(self.buttonBox)
        self.setLayout(self.vlayout)

    def set_options(self, options):
        self.options = options
        self.setup_ui()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def set_ok_function(self, func):
        self.ok_func = func

    def accept(self):
        if self.ok_func is not None:
            self.ok_func(self.get_user_options())
        self.hide()

    def reject(self):
        self.hide()

    def get_user_options(self):
        for i, widget in enumerate(self.widget_list):
            self.options[i].select_id = widget.currentIndex()
        return self.options

dialog = None


def get_user_options(options, ok_select):
    global dialog
    dialog = EsUserOptionsDialog()
    dialog.set_options(options)
    dialog.set_ok_function(ok_select)
    dialog.show()


