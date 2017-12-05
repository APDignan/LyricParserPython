# used to hold the messages of any errors that occur
class ParserException(Exception):
    def __init__(self, myMsg = None):
        self.myMsg = myMsg