from ParserException import ParserException

# trie: dictionary of trieNodes; key = letter, val = trieNode. trieNode contains syllables when at a complete word
class trie:

    # init
    def __init__(self, inFileName, inFilePath):
        self.dictionary = trieNode()
        self.__printOrder = list()
        self.__fileName = inFileName
        self.__filePath = inFilePath

    @property
    def printOrder(self):
        return self.__printOrder
    @printOrder.setter
    def printOrder(self, inOrder):
        self.__printOrder = inOrder.split(",")

    @property
    def fileName(self):
        return self.__fileName
    @fileName.setter
    def fileName(self, inFileName):
        self.__fileName = inFileName

    @property
    def filePath(self):
        return self.__filePath
    @filePath.setter
    def filePath(self, inPath):
        self.__filePath = inPath

    # insert a word into the trie with its syllables
    def insertWord(self, inWord, syllables):

        if len(inWord) <= 0:
            return

        currNode = self.dictionary

        # starting at the head, traverse the trie, adding nodes where they're needed. Once we reach the last character, add syll.
        while len(inWord) > 0:
            currNode = currNode.addBranch(inWord, syllables)
            inWord = inWord[1:]

    # get the syllables of inWord from the trie. If it's not in the trie, return ""
    def getWord(self, inWord):
        node = self.__getWordHelper(inWord)
        if node is not None and len(node.syllables) > 0:
            return node.syllables

        return ""

    # determines if the word in is the trie.
    def __getWordHelper(self, inWord, ignore=False):
        if len(inWord) <= 0:
            return None

        currNode = self.dictionary

        # loops through each character of inWord. If we reach a branch that doesn't exist, return None.
        while len(inWord) > 0:
            if currNode.hasBranch(inWord[0]):
                currNode = currNode.dictionary[inWord[0]]
                inWord = inWord[1:]
            else:
                return None

        # verify that we found the word, and return the trieNode that has it's syllables.
        if ignore or currNode.syllables:
            return currNode

        return None

    def updateWord(self, inWord, oldPronunciation, newPronunciation):
        node = self.__getWordHelper(inWord)

        if oldPronunciation in node.syllables:
            if newPronunciation != "":
                node.syllables[node.syllables.index(oldPronunciation)] = newPronunciation
            else:
                node.syllables.remove(oldPronunciation)

    def getSubTrie(self, inSubWord):
        node = self.__getWordHelper(inSubWord, ignore=True)
        if node is not None:
            subTrieData = list()
            self.getSubTrieHelper(inSubWord, self.printOrder, node, subTrieData)
            return subTrieData

    def getSubTrieHelper(self, word, printOrder, node, subTrieData):
        if node.syllables:
            for syll in node.syllables:
                subTrieData.append(word)
                subTrieData.append(str(syll))
                subTrieData.append(str(len(syll.split(":"))))

        counter = 0
        for l in printOrder:
            if node.hasBranch(l):
                self.getSubTrieHelper(word + l, printOrder, node.dictionary[l], subTrieData)
                counter += 1

        if counter < len(node.dictionary):
            for branch in node.dictionary:
                if branch not in printOrder:
                    self.getSubTrieHelper(word + branch, printOrder, node.dictionary[branch], subTrieData)

    # debugging: prints the trie to the screen.
    def printTrie(self):
        # list of applicable paths.
        word = ''
        self.printTrieHelper(word, self.printOrder, self.dictionary)

    # goes through each branch in order and prints the word and syllable to the screen
    def printTrieHelper(self, word, printOrder, node):
        if node.syllables:
            print(word + ':' + str(node.syllables))
        counter = 0
        for l in printOrder:
            if node.hasBranch(l):
                self.printTrieHelper(word + l, printOrder, node.dictionary[l])
                counter += 1

        if counter < len(node.dictionary):
            for branch in node.dictionary:
                if branch not in printOrder:
                    self.printTrieHelper(word + branch, printOrder, node.dictionary[branch])

    # same thing as printTrie but writes the trie to a file
    def printTrieToFile(self):
        fout = open(self.filePath, "w")
        word = ''
        try:
            if len(self.printOrder) > 0:
                tempStr = ""
                for letter in self.printOrder:
                    tempStr = tempStr + letter + ","
                fout.write("order=%s\n" %tempStr[:-1])
            else:
                fout.write("order=\n")
            self.printTrieToFileHelper(word, self.printOrder, self.dictionary, fout)
        except Exception as err:
            raise ParserException("ERROR: (Writing Dicitonary) Could not write word %s to dictionary." %word)
        finally:
            fout.close()

    # same thing as printTrieHelper except it writes to a file
    def printTrieToFileHelper(self, word, printOrder, node, file):
        if node.syllables:
            self.writeSyllablesToFile(word, node, file)

        counter = 0
        for l in printOrder:
            if node.hasBranch(l):
                self.printTrieToFileHelper(word + l, printOrder, node.dictionary[l], file)
                counter += 1

        if counter < len(node.dictionary):
            for branch in node.dictionary:
                if branch not in printOrder:
                    self.printTrieToFileHelper(word + branch, printOrder, node.dictionary[branch], file)

    # formats the syllables to a readable format
    def writeSyllablesToFile(self, word, node, file):
        if len(node.syllables) > 0:
            syllables = node.syllables[0]
            index = 1

            while index < len(node.syllables):
                syllables = syllables + '|' + node.syllables[index]
                index+= 1

            file.write("_" + word + ": " + syllables + '\n')

    # sets a word within syllables to be marked as the one to be used
    def setWordPreference(self, inWord, syllables):
        node = self.__getWordHelper(inWord)
        if node is not None:
            node.setPreference(syllables)

# trieNode: building block of the trie. Has a list of syllables and a dictionary for each letter of the alphabet + '.
class trieNode:

    def __init__(self, syll=None):
        self.__dictionary = dict()
        self.__syllables = list()
        if syll is not None:
            for inSyll in syll:
                self.syllables.append(inSyll)

    # Given a string, create a new branch; if we're at the end of the string add the syllables
    # return the node we made
    def addBranch(self, inChar, syll):
        if len(inChar) == 1:
            if inChar not in self.dictionary:
                self.dictionary[inChar[0]] = trieNode(syll)
            else:
                for testSyll in syll:
                    # print("Testing %s when I have syllables %s" %(testSyll, self.dictionary[inChar[0]].syllables))
                    if testSyll not in self.dictionary[inChar[0]].syllables:
                        self.dictionary[inChar[0]].setSyllables(testSyll)
        else:
            if inChar[0] not in self.dictionary:
                self.dictionary[inChar[0]] = trieNode()

        return self.dictionary[inChar[0]]

    # sees if a character is in the dictionary
    def hasBranch(self, inChar):
        if inChar in self.dictionary:
            return True

        return False

    @property
    def dictionary(self):
        return self.__dictionary

    @property
    def syllables(self):
        return self.__syllables

    def setSyllables(self, syllables):
        self.__syllables.append(syllables)

    # Sets a pronunciation of a word as the default by placing it at the front of the list
    def setPreference(self, inSyllables):
        index = 0
        contin = True
        while index < len(self.syllables) and contin:
            if (self.__syllables[index] == inSyllables):
                self.__syllables[0], self.__syllables[index] = self.__syllables[index], self.__syllables[0]
                contin = False

            index += 1





