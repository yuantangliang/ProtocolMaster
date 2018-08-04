class Media(object):
    def __init__(self):
        self.options = {}
        self.user_options = {}

    def send(self, data):
        pass

    def receive(self):
        pass

    def get_options(self):
        return self.options

    def set_options(self, options):
        self.user_options = options


class SerialMedia(Media):
    pass
