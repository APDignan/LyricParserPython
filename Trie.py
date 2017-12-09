from ParserException import ParserException

# trie: dictionary of trieNodes; key = letter, val = trieNode. trieNode contains syllables when at a complete word
class trie:

    # init
    def __init__(self):
        self.dictionary = trieNode()

    # insert a word into the trie with its syllables
    def insertWord(self, inWord, syllables):
        if len(inWord) <= 0:
            return

        currNode = self.dictionary
        # starting at the head, traverse the trie, adding nodes whereever needed. Once we reach the last character, add syll.
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
        alphabet = '\'abcdefghijklmnopqrstuvwxyz'
        node = self.__getWordHelper(inSubWord, ignore=True)
        if node is not None:
            subTrieData = list()
            self.getSubTrieHelper(inSubWord, alphabet, node, subTrieData)
            return subTrieData


    def getSubTrieHelper(self, word, alphabet, node, subTrieData):
        if node.syllables:
            for syll in node.syllables:
                subTrieData.append(word)
                subTrieData.append(str(syll))
                subTrieData.append(str(len(syll.split(":"))))
        for l in alphabet:
            if node.hasBranch(l):
                self.getSubTrieHelper(word + l, alphabet, node.dictionary[l], subTrieData)

    # debugging: prints the trie to the screen.
    def printTrie(self):
        # list of applicable paths.
        alphabet = '\'abcdefghijklmnopqrstuvwxyz'
        word = ''
        self.printTrieHelper(word, alphabet, self.dictionary)

    # goes through each branch in order and prints the word and syllable to the screen
    def printTrieHelper(self, word, alphabet, node):
        if node.syllables:
            print(word + ':' + str(node.syllables))
        for l in alphabet:
            if node.hasBranch(l):
                self.printTrieHelper(word + l, alphabet, node.dictionary[l])

    # same thing as printTrie but writes the trie to a file
    def printTrieToFile(self, fileName):
        fout = open(fileName, "w")
        alphabet = '\'abcdefghijklmnopqrstuvwxyz'
        word = ''
        try:
            self.printTrieToFileHelper(word, alphabet, self.dictionary, fout)
        except Exception as err:
            raise ParserException("ERROR: (Writing Dicitonary) Could not write word %s to dictionary." %word)
        finally:
            fout.close()

    # same thing as printTrieHelper except it writes to a file
    def printTrieToFileHelper(self, word, alphabet, node, file):
        if node.syllables:
            self.writeSyllablesToFile(word, node, file)
        for l in alphabet:
            if node.hasBranch(l):
                self.printTrieToFileHelper(word + l, alphabet, node.dictionary[l], file)

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
                    print("Testing %s when I have syllables %s" %(testSyll, self.dictionary[inChar[0]].syllables))
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

# testTrie = trie()
# testTrie.insertWord("hello", "he:lO")
# testTrie.insertWord("world", 'w3,3ld')
# testTrie.insertWord("in", "i,in")
# testTrie.insertWord("insert", 'i,in:s3,3t')
#
# print("My trie: ")
# testTrie.printTrie()
#
# print("hello gets " + str(testTrie.getWord("hello")))
# #print(testTrie.getWord("in"))
# print("insert gets " + str(testTrie.getWord("insert")))
# print("Hello gets " + str(testTrie.getWord("Hello")))
# print("Balloon gets " + str(testTrie.getWord("Balloon")))



