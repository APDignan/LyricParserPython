import sys
from Trie import trie

def run():
    myTrie = trie()
    with open("in.txt") as myFile:
        for line in myFile:
            addWordToTrie(line, myTrie)

    myTrie.setWordPreference("the", "dhE")
    myTrie.printTrie()
    myTrie.printTrieToFile("out.txt")
    myFile.close()

def addWordToTrie(str, myTrie):
    "_word: syll"
    halfIndex = str.find(':')

    if halfIndex >= 0:
        word = str[1:halfIndex]
        syllables = str[halfIndex + 2:-1]
        myTrie.insertWord(word, syllables)

run()








run()