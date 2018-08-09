# encoding:utf-8


class FoundClassException(Exception):
    def __init__(self, class_name):
        err = "can not find register class,please check your spell or write your plug".format(class_name)
        Exception.__init__(self, err)
        self.class_name = class_name
