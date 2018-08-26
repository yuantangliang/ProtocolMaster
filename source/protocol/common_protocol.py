

class DataFragment(object):

    def length(self):
        return 0;


class ConstDataFragment(object):
    def __init__(self, name, data):
        self.data = data
        self.name = name

    def length(self):
        return len(self.data)


class ChoiceDataFragment(object):

    def __init__(self):
        pass


class StatisticsDataFragment(object):

    @staticmethod
    def create_length_statistics(name, depends):
        pass

    @staticmethod
    def create_cs_statistics(name, depends):
        pass

    def __init__(self,name, depends):
        self.name = name
        self.depends = depends


class FixedLengthDataFragment(object):

    def __init__(self, name, length, default_value):
        self.name = name
        self.length = length
        self.default_value = default_value


class VariableDataFragment(object):
    def __init__(self, name, depends):
        self.name = name
        self.depends = depends


# receive_str+="68 10 01 02 03 04 05 06 07  81 16 90 1F 96 00 55 55 05 2C 00 55 55 05 2C 00 00 00 00 00 00 00 00 00 26 16"
class CJT188Protocol(object):

    def __init__(self):
        self.name = "CJT188"
        self.fragments = []
        self.add_fragment(ConstDataFragment("head", chr(0x68)))
        self.add_fragment(ConstDataFragment("type", chr(0x01)))
        self.add_fragment(FixedLengthDataFragment("address", 7, chr(0xaa) * 7))
        self.add_fragment(FixedLengthDataFragment("cmd", 1, chr(0x02)))
        self.add_fragment(StatisticsDataFragment.create_length_statistics("length", 1, ("didunit",)))
        self.add_fragment(VariableDataFragment("didunit", "length"))
        self.add_fragment(StatisticsDataFragment.create_cs_statistics("cs", 1, ("head", "type", "address", "cmd", "didunit")))
        self.add_fragment(ConstDataFragment("tail", chr(0x16)))



    def add_fragment(self, fragment):
        self.fragments.append(fragment)
