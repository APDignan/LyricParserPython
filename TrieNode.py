
class trieNode:

    def __init__(self, syll=None):
        self.dictionary = dict()
        self.syllables = list()
        if syll is not None:
            self.syllables.append(syll)

    #Given a string, create a new branch; if we're at the end of the string add the syllables
    #return the node we made
    def addBranch(self, inChar, syll):
        if len(inChar) == 1:
            if inChar not in self.dictionary:
                self.dictionary[inChar[0]] = trieNode(syll)
            else:
                if syll not in self.syllables:
                    self.dictionary[inChar[0]].setSyllables(syll)
        else:
            if inChar[0] not in self.dictionary:
                self.dictionary[inChar[0]] = trieNode()

        return self.dictionary[inChar[0]]

    def hasBranch(self, inChar):
        if inChar in self.dictionary:
            return True

        return False

    def getDictionary(self):
        return self.dictionary

    def getSyllables(self):
        return self.syllables

    def setSyllables(self, syllables):
        self.syllables.append(syllables)

    def setPreference(self, inSyllables):
        index = 0
        contin = True
        while index < len(self.syllables) and contin:
            if(self.syllables[index] == inSyllables):
                self.syllables[0], self.syllables[index] = self.syllables[index], self.syllables[0]
                contin = False

            index += 1




