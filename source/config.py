# encoding:utf-8
import ConfigParser
import os
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ESConfig(object):
    """
    >>> config = ESConfig.get_instance()
    >>> config.set_device_file(u"中文路径")
    >>> config.get_device_file()
    u'中文路径'
    """
    config = None
    @staticmethod
    def get_instance():
        if ESConfig.config is None:
            ESConfig.config = ESConfig("config.ini")
        return ESConfig.config

    def __init__(self, filename):
        self.cfg = ConfigParser.ConfigParser()
        self.file_name = filename
        if not os.path.exists(filename):
            self.cfg.add_section("global")
            self.cfg.set("global","device_file", "")
            self.sync2file()
        self.cfg.readfp(codecs.open(filename,"r",encoding="utf-8"))

    def get_device_file(self):
        return self.cfg.get("global", "device_file")

    def set_device_file(self, file_name):
        self.cfg.set("global", "device_file", file_name)
        self.sync2file()

    def sync2file(self):
        with codecs.open(self.file_name, "w", encoding="utf-8") as f:
            self.cfg.write(f)
