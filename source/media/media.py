# encoding:utf-8
import os
from PyQt4.QtCore import QObject
import pickle
from copy import deepcopy


class MediaOptions(object):
    def __init__(self, key, options, label_text=None, show_options=None,select_id=0):
        self.key = key
        self.options = options
        self.select_id = select_id
        if label_text is None:
            label_text = key
        if show_options is None:
            show_options = options
        self.label_text = label_text
        self.show_options = show_options

    def get_options(self):
        return [str(i) for i in self.show_options]


class Media(QObject, object):
    def __init__(self, media_options):
        super(Media, self).__init__()
        self.media_options = media_options
        self.pickle_file_name = ".config_" + self.__class__.__name__ + ".pkl"
        self.load_last_options()

    def load_last_options(self):
        if os.path.exists(self.pickle_file_name):
            with open(self.pickle_file_name, 'rb') as handle:
                media_options = pickle.load(handle)
            for current, last in zip(self.media_options, media_options):
                if current.options == last.options:
                    current.select_id = last.select_id
        self.media_options

    def open(self):
        pass

    def close(self):
        pass

    def send(self, data):
        pass

    def _receive(self):
        pass

    def set_media_options(self, options):
        self.media_options = options
        with open(self.pickle_file_name, 'wb') as handle:
            pickle.dump(options, handle)

    def get_media_options(self):
        return self.media_options

    def get_selected_options(self):
        selected_options = {}
        for option in self.media_options:
            selected_options[option.key] = option.options[option.select_id]
        return selected_options


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






