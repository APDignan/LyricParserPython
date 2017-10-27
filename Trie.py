from TrieNode import trieNode

class trie:

    def __init__(self):
        self.dictionary = trieNode()

    def insertWord(self, inWord, syllables):
        if len(inWord) <= 0:
            return

        currNode = self.dictionary
        while len(inWord) > 0:
            currNode = currNode.addBranch(inWord, syllables)
            inWord = inWord[1:]

    def getWord(self, inWord):
        node = self.__getWordHelper(inWord)
        if node is not None:
            return node.getSyllables()

        return ""

    def __getWordHelper(self, inWord):
        if len(inWord) <= 0:
            return None

        currNode = self.dictionary
        while len(inWord) > 0:
            if currNode.hasBranch(inWord[0]):
                currNode = currNode.getDictionary()[inWord[0]]
                inWord = inWord[1:]
            else:
                return None

        if currNode.getSyllables():
            return currNode

        return None

    def printTrie(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        word = ''
        self.printTrieHelper(word, alphabet, self.dictionary)

    def printTrieHelper(self, word, alphabet, node):
        if node.getSyllables():
            print(word + ':' + str(node.getSyllables()))
        for l in alphabet:
            if node.hasBranch(l):
                self.printTrieHelper(word + l, alphabet, node.getDictionary()[l])

    def printTrieToFile(self, fileName):
        fout = open(fileName, "w")
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        word = ''
        self.printTrieToFileHelper(word, alphabet, self.dictionary, fout)
        fout.close()

    def printTrieToFileHelper(self, word, alphabet, node, file):
        if node.getSyllables():
            self.writeSyllablesToFile(word, node, file)
        for l in alphabet:
            if node.hasBranch(l):
                self.printTrieToFileHelper(word + l, alphabet, node.getDictionary()[l], file)

    def writeSyllablesToFile(self, word, node, file):
        syllables = node.getSyllables()[0]
        index = 1

        while index < len(node.getSyllables()):
            syllables = syllables + '|' + node.getSyllables()[index]
            index+= 1

        file.write("_" + word + ": " + syllables + '\n')


    def setWordPreference(self, inWord, syllables):
        node = self.__getWordHelper(inWord)
        if node is not None:
            node.setPreference(syllables)


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



