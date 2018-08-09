# encoding:utf-8
import os
from PyQt4.QtCore import QObject


class Media(QObject):
    def __init__(self, media_options):
        self.options = {}
        self.user_options = {}
        self.media_options = media_options
        super(Media, self).__init__()

    def open(self):
        pass

    def close(self):
        pass

    def send(self, data):
        pass

    def _receive(self):
        pass

    def get_user_options(self):
        return self.options

    def set_user_options(self, options):
        self.user_options = options

    def get_media_options(self):
        return self.media_options


_all_medias = dict()


def media_register(media_class):
    global _all_protocols
    _all_medias[media_class.__name__] = media_class
    return media_class


def media_create(name):
    from ..user_exceptions import FoundClassException
    media_class = _all_protocols(name)
    if media_class is None:
        raise FoundClassException(name)
    return media_class()






