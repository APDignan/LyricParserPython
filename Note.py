class Note:
    def __init__(self):
        self.order = list()
        self.params = dict()
        self.syllables = list()
        self.value = ""

    def insertParam(self, inParam):
        equalIndex = inParam.find('=')

class Syllable:
    def __init__(self, syll):
        self.syll = syll
        self.length = 0
        self.preutterance = 0
        self.overlap = 0
        self.prefix = ""
        self.suffix = ""


