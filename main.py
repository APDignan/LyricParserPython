import sys
from UST import Ust, note, copyNote
from PREFIX import prefixMap, prefixMapItem
from OTO import Oto, OtoLine
import utauGen
import traceback
from Trie import trie
from ParserException import ParserException

#pyinstaller --onefile -F --dist C:\Users\Andrew\UTAU\plugins\PythonTest2 parserUi.py

# main execution of parser. Imports the following:
#   1. English Dictionary from dictionary.txt into Trie.myTrie (see Trie.py)
#   2. Ust .temp file from sys.argv[1] into UST.myUst (see UST.py)
#   3. Ust's bank's oto using the voiceDir in myUst to OTO.myOto (see OTO.py)
#   4. Ust's bank's prefix map using myUst.voiceDir into PREFIX.myPMap (see PREFIX.py)
# if everything was successfully imported, try to parse the ust.

class parser():
    def __init__(self):
        self.__myUst = None
        self.__myOto = None
        self.__myPMap = None
        self.__myTrie = trie()
        with open("dictionary.txt") as myFile:
            for line in myFile:
                self.addWordToTrie(line)
        myFile.close()
        self.__missingWords = list()

    @property
    def myUst(self):
        return self.__myUst
    @myUst.setter
    def myUst(self, inUst):
        self.__myUst = inUst

    @property
    def myOto(self):
        return self.__myOto
    @myOto.setter
    def myOto(self, inOto):
        self.__myOto = inOto

    @property
    def myPMap(self):
        return self.__myPMap
    @myPMap.setter
    def myPMap(self, inPMap):
        self.__myPMap = inPMap

    @property
    def myTrie(self):
        return self.__myTrie

    @myTrie.setter
    def myTrie(self, inTrie):
        self.__myTrie = inTrie


    @property
    def missingWords(self):
        return self.__missingWords

    @missingWords.setter
    def missingWords(self, inMissing):
        self.__missingWords.append(inMissing)


    def run(self):
        # load dictionary into the Trie.
        myErr = 0
        try:
            myErr = 1
            # testFile = open(sys.argv[1])
            myErr = 2
            self.myUst = Ust(sys.argv[1])
            myErr = 3
            self.myOto = Oto(self.myUst.voiceDir)
            myErr = 4
            self.myPMap = prefixMap(self.myUst.voiceDir)

            try:
                self.parseVCCV()
            except ParserException as err:
                print(err.myMsg)
                traceback.print_exc()
            except Exception as err:
                traceback.print_exc()
                input("Press ENTER to Continue...")

        except ParserException as pErr:
            print(pErr.myMsg)
        except Exception as err:
            if myErr == 0:
                print("ERROR: \"dictionary.txt\" has either been moved or deleted. Please replace dictionary.txt in this folder.")
            elif myErr == 1:
                print("ERROR: Either this plugin is being run outside of UTAU, or no UST file was found.")
            elif myErr == 2:
                print("ERROR: Could not process UST file.")
            elif myErr == 3:
                print("ERROR: Could not process Oto.ini.")
            elif myErr == 4:
                print("ERROR: Could not process prefix.map.")

            input("Press ENTER to Continue...")

    def finishPlugin(self):
        errState = 0
        try:
            self.myTrie.printTrieToFile("dictionary.txt")
            self.myUst.closeUst(self.myUst.ustPath)
        except ParserException as pErr:
            raise pErr
        except Exception as err:
            raise ParserException("ERROR: Could not finish ending plugin procedures given an err %s" %err)



    def addWordToTrie(self, inStr):
        "_word: syll"
        halfIndex = inStr.find(':')

        if halfIndex >= 0:
            word = inStr[1:halfIndex]
            syllables = inStr[halfIndex + 2:-1].split("|")
            self.myTrie.insertWord(word, syllables)

    # given a ust, parses each note using the dictionary from myTrie and voicebank settings in myOto and myPMap
    # loops through each note and tries to see if the word is in the dictionary. Special cases:
    #   1. Word not in Dictionary => Treat note like a Rest (except for extending notes)
    #   2. 1 syllable word in Dictionary => get the syllables and set them to the current note's syllable field
    #   3. note = - => extend the previous note by removing all but the first subNote and setting note to the prevNote's vowel + it's subNotes[1:]
    #   4. multi-syllable word => looks through the ust until it reaches a note that is not a rest or ends with "-". Accumulates the lyrics on the
    #      notes into the word to parse. Parses each note within the word and sets their flag to "done" so that we pass over them. Also takes into account
    #      rests (if notes pass over a rest) and "-" (extends previous syllable determined by notes with letters in them"
    # for each note, go to formatNote to convert the psudeo VCCV to VCCV
    def parseVCCV(self):
        prevNote = ""

        # myFile = open("checking.txt", "w")
        # missingFile = open("missing.txt", 'w')

        index = 0
        lastNote = -1
        currNote = ""
        try:
            for currNote in self.myUst.notes:
                # tempLen = the length the note has available to it rather than it's original length.
                currNote.tempLen = currNote.length
                # if the note is either a prev note or next note, don't try to parse it and just add itself to its subNotes
                if currNote.state == "prev" or currNote.state == "next":
                    currNote.subNotes = [currNote]
                    currNote.parentLyric = currNote.lyric + " (" + currNote.state + ")"
                # if the note has a valid lyric and hasn't been parsed yet, try to parse it
                elif len(currNote.lyric) > 0 and currNote.state != 'done' and currNote.state != 'MIA':
                    lyric = currNote.lyric.lower()
                    # if lyric == "/" and self.myUst.notes[index-1].lyric == "-":
                    #     lyric = "-"
                    #     currNote.lyric = "-"
                    # if our lyric doesn't end with a "-", isn't a rest, and is in the trie, it's a single syllable word.
                    tempSylls = self.getSyllables(self.myTrie.getWord(lyric), 1)
                    if lyric[-1] != '-' and self.notRest(lyric) and tempSylls is not None:
                        self.createVCCVNotes(currNote, tempSylls)
                        lastNote = index
                        currNote.parentLyric = lyric
                    # otherwise if the note's lyric is not in the dictionary, write it to a file and set it to MIA
                    elif self.notRest(lyric) and lyric[-1] != '-' and tempSylls is None:
                        # def __init__(self, inLyric = None, inNumSylls = None, inFixedSylls = "", inStartNote = 0, inRange = 0):
                        self.missingWords = missingNote(inLyric=lyric, inNumSylls=1, inStartNote = index, inRange = 1)
                        currNote.state = "MIA"
                        currNote.subNotes = [copyNote(currNote)]
                    # if our note's lyric is "-" then it's an extender, so try to extend the previous true note if it's not MIA.
                    elif lyric == '-' and lastNote > -1:
                        if self.myUst.notes[index-1].state == "MIA":
                            currNote.state = "MIA"
                            currNote.subNotes = [copyNote(currNote)]
                            self.missingWords = missingNote(inLyric="-", inNumSylls=0, inStartNote=index, inRange= 1, inLastNote=(self.missingWords[-1].startNote + self.missingWords[-1].range - 1))
                        else:
                            self.extendVCCVNote(self.myUst.notes[lastNote], currNote)
                            currNote.parentLyric = self.myUst.notes[lastNote].parentLyric + " (-)"
                            lastNote = index
                    # if the lyric ends with "-" then we have a multiple-syllable word.
                    elif lyric[-1] == '-':
                        counter = 0
                        numSylls = 0
                        currLyric = ""

                        # loop through ust while we haven't reached the end, while the note is not the next note, and while either the notes end with "-" or is a rest (need to end on word that has no dashes
                        # if the note is not "-" or a rest then we count it as a syllable. Concatenate the letters to the word that we'll test
                        while index + counter < len(self.myUst.notes) and self.myUst.notes[index + counter].state != "next" and (self.myUst.notes[index + counter].lyric[-1] == '-' or self.isRest(self.myUst.notes[index + counter].lyric)):
                            if self.myUst.notes[index + counter].lyric != '-' and self.notRest(self.myUst.notes[index + counter].lyric):
                                currLyric = currLyric + self.myUst.notes[index + counter].lyric[:-1]
                                numSylls += 1
                            counter += 1

                        # checks if we ended becasue we found the last syllable. if so add it to the string
                        if index + counter < len(self.myUst.notes) and self.myUst.notes[index + counter]. state != "next" and self.myUst.notes[index + counter].lyric != '-' and self.notRest(self.myUst.notes[index + counter].lyric):
                            currLyric = currLyric + self.myUst.notes[index + counter].lyric
                            numSylls += 1
                            counter+= 1

                        currLyric = currLyric.lower()

                        # if the word we found was in the dictionary with the right number of syllables
                        tempSylls = self.getSyllables(self.myTrie.getWord(currLyric), numSylls)
                        if tempSylls is not None:
                            noteIndex = index
                            inCounter = 0
                            syllNum = 0
                            # loop through each of the notes we found
                            while inCounter < counter:
                                # if the note is a syllable by having some characters, parse the syllNum syllable
                                if self.myUst.notes[index + inCounter].lyric != "-" and self.notRest(self.myUst.notes[index + inCounter].lyric):
                                    self.createVCCVNotes(self.myUst.notes[index + inCounter], tempSylls[syllNum])
                                    syllNum += 1
                                    self.myUst.notes[index + inCounter].parentLyric = currLyric
                                    noteIndex = index + inCounter
                                    lastNote = noteIndex


                                # otherwise if we found an extender, then extend the previous note
                                elif self.myUst.notes[index + inCounter].lyric == "-":
                                    self.extendVCCVNote(self.myUst.notes[noteIndex], self.myUst.notes[index + inCounter])
                                    self.myUst.notes[index + inCounter].parentLyric = currLyric + " (-)"
                                    noteIndex = index + inCounter
                                    lastNote = noteIndex
                                # finally it must be a rest, so treat it as such
                                else:
                                    self.myUst.notes[index + inCounter].subNotes = [self.myUst.notes[index + inCounter]]

                                # set the word's state to done so that we don't try to parse it's syllables
                                self.myUst.notes[index + inCounter].state = "done"
                                inCounter += 1
                        # If the word is missing, print it and set all notes within the ust to MIA if it's not a rest
                        else:
                            #def __init__(self, inLyric = None, inNumSylls = None, inFixedSylls = "", inStartNote = 0, inRange = 0):
                            self.missingWords = missingNote(inLyric=currLyric, inNumSylls=numSylls, inStartNote = index, inRange = counter)
                            inCounter = 0
                            while inCounter < counter:
                                if self.notRest(self.myUst.notes[index + inCounter].lyric):
                                    self.myUst.notes[index + inCounter].state = "MIA"
                                self.myUst.notes[index + inCounter].subNotes = [copyNote(self.myUst.notes[index + inCounter])]
                                inCounter += 1
                    # If the lyric is 0, set it to a rest
                    elif len(currNote.lyric) == 0:
                        currNote.lyric = "R"
                        currNote.subNotes = [copyNote(currNote)]
                        currNote.parentLyric = "R"
                    # Otherwise the note should be a rest
                    else:
                        currNote.subNotes = [copyNote(currNote)]
                        currNote.parentLyric = "R"

                # Format the note if it's not a prev.note (No lyric to parse, all size changes are done to the previous note)
                if currNote.state != "prev":
                    self.formatNotes(self.myUst.notes[index-1], currNote)
                index += 1
        except ParserException as pErr:
            raise pErr
        except Exception as err:
            raise ParserException("ERROR: (Parsing VCCV Lyrics) Could not parse lyric %i# : %s. Rose error %s" %(index, currNote.lyric, err))

    # parseFixedVCCV: parses the notes specified by the user if they gave the proper syllables
    def parseFixedVCCV(self, inMissingNote):
        # set the state of the note to nothing to allow editing

        prevNote = self.myUst.notes[inMissingNote.startNote - 1]
        currNote = self.myUst.notes[inMissingNote.startNote]
        endNote = self.myUst.notes[inMissingNote.startNote + inMissingNote.range - 1]
        nextNote = self.myUst.notes[inMissingNote.startNote + inMissingNote.range]

        print("Fixing %s" %inMissingNote.lyric)

        currNote.state = ""
        # if the numSylls is 0, then we have a stand-alone "-". Extend it based on the previous note
        if inMissingNote.numSylls == 0:
            self.clearNote(currNote)
            self.extendVCCVNote(self.myUst.notes[inMissingNote.lastNote], currNote)
            currNote.parentLyric = self.myUst.notes[inMissingNote.lastNote].parentLyric + " (-)"
            # self.formatNotes(prevNote, currNote)
            self.fixPrevNote(prevNote, currNote)
            self.fixNextNote(currNote, nextNote)
        # otherwise if numSylls is 1 then it's a single note. Create the note.
        elif inMissingNote.numSylls == 1 and inMissingNote.lyric != "-":
            self.clearNote(currNote)
            self.createVCCVNotes(currNote, inMissingNote.fixedSylls)
            currNote.parentLyric = inMissingNote.lyric
            self.fixPrevNote(prevNote, currNote)
            self.fixNextNote(currNote, nextNote)
            # self.formatNotes(prevNote, currNote)
        # finally the note must have more than one syllable, so parse it as a multi-syllable word
        else:
            index = inMissingNote.startNote
            syllNum = 0
            lastNote = -1
            # loop through the notes given by the missing note's range
            # 31 < 34
            # 32 < 34
            # 33 < 34
            while index < inMissingNote.startNote + inMissingNote.range:
                # if it's not an extender or a rest, create a note using the syllNumth syllable.
                self.myUst.notes[index].state = ""
                self.clearNote(self.myUst.notes[index])
                if self.myUst.notes[index].lyric != "-" and self.notRest(self.myUst.notes[index].lyric):
                    self.createVCCVNotes(self.myUst.notes[index], inMissingNote.fixedSylls[syllNum])
                    syllNum += 1
                    self.myUst.notes[index].parentLyric = inMissingNote.lyric
                    lastNote = index
                # if the note is an extender, extend the last note that wasn't a rest. Don't go to the next syllable
                elif self.myUst.notes[index].lyric == "-":
                    self.extendVCCVNote(self.myUst.notes[lastNote], self.myUst.notes[index])
                    self.myUst.notes[index].parentLyric = inMissingNote.lyric + " (-)"
                    lastNote = index
                # finally we must have a rest, so just do the subnote thing
                else:
                    self.myUst.notes[index].subNotes = [self.myUst.notes[index]]

                index+= 1

            index = inMissingNote.startNote + 1
            self.fixPrevNote(prevNote, currNote)
            while index < inMissingNote.startNote + inMissingNote.range:
                self.formatNotes(self.myUst.notes[index - 1], self.myUst.notes[index])
                index += 1
            self.fixNextNote(endNote, nextNote)



    def fixPrevNote(self, prevNote, currNote):
        if prevNote.subNotes[-1].lyric[-1:] == "-":
            prevNote.subNotes[-1].lyric = prevNote.subNotes[-1].lyric[:-1]
            print("prevNote now ends with %s" %prevNote.subNotes[-1].lyric)
            if prevNote.subNotes[-1].lastVowel != "":
                if len(prevNote.subNotes) > 1:
                    tempNotes = prevNote.subNotes[:-1]
                    prevNote.subNotes.clear()
                    prevNote.subNotes = tempNotes

        self.formatNotes(prevNote, currNote)

    # give currNote any
    def fixNextNote(self, currNote, nextNote):
        if nextNote.state != "MIA" and nextNote.subNotes[0].lyric[0] == '_':
            nextNote.subNotes[0].lyric = currNote.subNotes[-1].lyric + nextNote.subNotes[0].lyric[2:]
            tempNotes = currNote.subNotes[:-1]
            currNote.subNotes.clear()
            currNote.subNotes = tempNotes

        if nextNote.state != "MIA" and nextNote.subNotes[0].lyric[0] == '-':
            nextNote.subNotes[0].lyric = nextNote.subNotes[0].lyric[1:]

        # currNote.printNote()
        # nextNote.printNote()
        self.formatNotes(currNote, nextNote)

        # index = inMissingNote.startNote + inMissingNote.range
        # if self.isRest(self.myUst.notes[index]):
        #     self.formatNotes(self.myUst.notes[index - 1], self.myUst.notes[index])


            # while inCounter < counter:
            #     # if the note is a syllable by having some characters, parse the syllNum syllable
            #     if self.myUst.notes[index + inCounter].lyric != "-" and self.notRest(
            #             self.myUst.notes[index + inCounter].lyric):
            #         self.createVCCVNotes(self.myUst.notes[index + inCounter], tempSylls[syllNum])
            #         syllNum += 1
            #         self.myUst.notes[index + inCounter].parentLyric = currLyric
            #         noteIndex = index + inCounter
            #         lastNote = noteIndex
            #
            #
            #     # otherwise if we found an extender, then extend the previous note
            #     elif self.myUst.notes[index + inCounter].lyric == "-":
            #         self.extendVCCVNote(self.myUst.notes[noteIndex], self.myUst.notes[index + inCounter])
            #         self.myUst.notes[index + inCounter].parentLyric = currLyric + " (-)"
            #         noteIndex = index + inCounter
            #         lastNote = noteIndex
            #     # finally it must be a rest, so treat it as such
            #     else:
            #         self.myUst.notes[index + inCounter].subNotes = [self.myUst.notes[index + inCounter]]
            #
            #     # set the word's state to done so that we don't try to parse it's syllables
            #     self.myUst.notes[index + inCounter].state = "done"
            #     inCounter += 1






    # given a syllable of a word, break it up into it's individual parts
    def createVCCVNotes(self, inNote, syllables):
        counter = 0
        # loop on the syllables (divided by commas). The first note should be a copy of the original note
        # while the rest should be generic to not copy the pitchbends
        for syllable in syllables.split(","):
            if counter == 0:
                tempNote = copyNote(inNote, syllable)
            else:
                tempNote = note(True, lyric=syllable, pitch=inNote.pitch)

            # add the note with the syllable to the current note's subNotes
            inNote.subNotes = [tempNote]
            if inNote.syllables is None:
                inNote.syllables = list()
            inNote.syllables = inNote.syllables.append(syllable)
            counter += 1


    # Extends a note currNote based off of the previous note's lyric.
    # Cases:
    #   1. Lyric = CV (kla)
    #       [kla] [-] => [kla] [a]
    #   2. Lyric = CVC (kla,ak)
    #       [[kla],[ak]] [-] => [kla] [[a], [ak]]
    def extendVCCVNote(self, prevNote, currNote):
        # list of vowels words can end with.
        availableVowels = ['a', 'e', 'i', 'o', 'u', 'E', '9', '3', '@', 'A', 'I', 'O', '8', 'Q', '6', 'x', '9l', '8n', 'Ang']

        prevVowel = prevNote.subNotes[0].lastVowel

        # double checks that the previous note has a vowel. If so make the currNote's subNotes equal to the vowel \
        # and all but the first of prevNote's subNotes. Set prevNote's subNotes to just it's first subNote (CV or V)
        if prevVowel != "" and prevVowel in availableVowels:
            currNote.subNotes = [copyNote(currNote, prevVowel)]
            currNote.subNotes = prevNote.subNotes[1:]
            tempNote = prevNote.subNotes[0]
            prevNote.subNotes.clear()
            prevNote.subNotes = [tempNote]

            #Loop through the notes and fix the pitches
            for myNote in currNote.subNotes:
                myNote.pitch = str(currNote.pitch)

    # Given the previous note and current note, converts the lyric from Psuedo VCCV (CV,VC only) to VCCV. Includes adding "-"
    # to beginning and ends of notes, adding VV and V C transitions, and parsing CCV and VCC samples. All parsing is based
    # on what's in the user's Oto.
    def formatNotes(self, prevNote, currNote):

        errState = 0

        try:
            #gets the prefix and suffix of the current note
            myPrefix = self.myPMap.getPrefixValue(currNote.strPitch).prefix if self.myPMap.getPrefixValue(currNote.strPitch).prefix is not None else ""
            mySuffix = self.myPMap.getPrefixValue(currNote.strPitch).suffix if self.myPMap.getPrefixValue(currNote.strPitch).suffix is not None else ""

            errState = 1
            # Start with checking the previous note; if it has a Vowel, try to either add a V C, VV, or V - note.
            if self.notRest(prevNote.lyric, prevNote.state) and prevNote.subNotes[-1].lastVowel != "":
                lastVowel = prevNote.subNotes[-1].lastVowel

                # If the current note is not a rest, we want to see if we can add a V C or a VV.
                if self.notRest(currNote.lyric, currNote.state) and prevNote.state != "prev":
                    # if we have a consonant, add a V C note
                    if len(currNote.subNotes[0].CCBeginning) > 0:
                        tempCC = currNote.subNotes[0].CCBeginning

                        # see what the longest V C sample is for our consonant (ex. get V sk instead of just V s)
                        while len(tempCC) > 0 and self.checkOto(lastVowel + " " + tempCC, myPrefix, mySuffix) is None:
                            tempCC = tempCC[:-1]

                        # If we found a CC that works and the previous vowel is a single character (not 0r/1ng), create a new note for it
                        if len(tempCC) > 0 and (len(lastVowel) == 1):
                            prevNote.subNotes = [note(True, lyric=lastVowel + " " + tempCC, pitch=prevNote.subNotes[-1].pitch)]
                        # otherwise just replace the previous ending with this
                        elif len(tempCC) > 0:
                            prevNote.subNotes[-1].lyric = lastVowel + " " + tempCC
                    # otherwise currNote starts with a vowel, so see if you can add a VV. If not, try using consonants to merge them
                    else:
                        # if the last lyric was not "-" and we have a VV, add it
                        if self.checkOto(lastVowel + currNote.subNotes[0].lyric, myPrefix, mySuffix) is not None and currNote.lyric != '-':
                            currNote.subNotes[0].lyric = lastVowel + currNote.subNotes[0].lyric
                        # otherwise if the last lyric's vowel and current lyric do not match, try to fix it.
                        elif lastVowel != currNote.subNotes[0].lyric:
                            if len(lastVowel) == 1:
                                myConst = 'y'
                                if lastVowel == 'o':
                                    myConst = 'w'
                                elif lastVowel == '3':
                                    myConst = 'r'
                                prevNote.subNotes = [note(True, lyric=lastVowel + " " + myConst, pitch=prevNote.subNotes[-1].pitch)]
                                currNote.subNotes[0].lyric = myConst + currNote.subNotes[0].lyric
                            elif len(lastVowel) == 2:
                                myConst = lastVowel[-1]
                                currNote.subNotes[0].lyric = myConst + currNote.subNotes[0].lyric
                            elif len(lastVowel) == 3:
                                currNote.subNotes[0].lyric = "_" + currNote.subNotes[0].lyric

                # if we are a rest, add the vowel ending to the previous one
                elif prevNote.state != "prev":
                    if len(lastVowel) > 1:
                        prevNote.subNotes[-1].lyric = prevNote.subNotes[-1].lyric + "-"
                    else:
                        prevNote.subNotes = [note(True, lyric=lastVowel + "-", pitch=prevNote.subNotes[-1].pitch)]
            # otherwise if currNote is a rest we need to add a "-"
            elif self.notRest(prevNote.lyric, prevNote.state) and self.isRest(currNote.lyric, currNote.state):
                prevNote.subNotes[-1].lyric = prevNote.subNotes[-1].lyric + "-"

            errState = 2

            # Try seeing if the note's CV and VC portions have been parsed and, if not, parse them
            # First test if the first subNote (always the psuedoVCCV CV) is in the oto. If not, then test it should be a CCV to be parsed
            if self.checkOto(currNote.subNotes[0].lyric, myPrefix, mySuffix) is None:
                # if we start with at least 2 consonants and we're a valid note, then add the "proper" CCV notes
                if len(currNote.subNotes[0].CCBeginning) > 1 and self.notRest(currNote.lyric, currNote.state):
                    tempLyric = currNote.subNotes[0].CCBeginning if self.notRest(prevNote.lyric, prevNote.state) else "-" + currNote.subNotes[0].CCBeginning
                    prevNote.subNotes = [note(True, lyric=tempLyric, pitch=prevNote.subNotes[-1].pitch)]
                    prevNote.subNotes[-1].state = "ccbeginning"
                    currNote.subNotes[0].lyric = "_" + currNote.subNotes[0].lyric[len(currNote.subNotes[0].CCBeginning) - 1:]

            errState = 3
            # Then test the second half of the note; test if it's in the oto and if not, try to parse it as a VCC
            if len(currNote.subNotes) == 2 and self.notRest(currNote.subNotes[1].lyric, currNote.state) and self.checkOto(currNote.subNotes[1].lyric, myPrefix, mySuffix) is None:
                self.findCCEnding(currNote, myPrefix, mySuffix)

            errState = 4
            # adding "-" to beginning of valid notes; consider cleaning this up
            #if ((isRest(prevNote.subNotes[-1].lyric) or (prevNote.state == 'MIA' and len(prevNote.subNotes) == 1)) and notRest(currNote.lyric, currNote.state)) or (currNote.subNotes[0].VBeginning != "" and prevNote.subNotes[-1].lastVowel != currNote.subNotes[0].VBeginning):

            if self.isRest(prevNote.subNotes[-1].lyric, prevNote.state):
                if self.notRest(currNote.subNotes[0].lyric, currNote.state) and currNote.subNotes[0].lyric[0] != "_":
                    currNote.subNotes[0].lyric = "-" + currNote.subNotes[0].lyric
            elif self.notRest(currNote.subNotes[0].lyric, currNote.state):
                if currNote.subNotes[0].VBeginning != "" and (prevNote.subNotes[-1].lastVowel == "" or prevNote.subNotes[-1].lastVowel[0] != currNote.subNotes[0].VBeginning):
                    currNote.subNotes[0].lyric = "-" + currNote.subNotes[0].lyric

            # if self.isRest(prevNote.subNotes[-1].lyric, prevNote.state) and self.notRest(currNote.subNotes[0].lyric, currNote.state):
            #     currNote.subNotes[0].lyric = "-" + currNote.subNotes[0].lyric
            #
            # elif self.notRest(currNote.subNotes[0].lyric, prevNote.state) and currNote.subNotes[0].VBeginning != "" and (prevNote.subNotes[-1].lastVowel == "" or len(prevNote.subNotes[-1].lastVowel) > 0 and prevNote.subNotes[-1].lastVowel[0] != currNote.subNotes[0].VBeginning):
            #     currNote.subNotes[0].lyric = "-" + currNote.subNotes[0].lyric

            errState = 5
            # update the sizes of the subnotes
            self.getSizes(prevNote, currNote)
        except ParserException as pErr:
            raise pErr
        except Exception as err:
            if errState == 0:
                raise ParserException("ERROR: (formattingNotes|getting prefix.map vals) Could not get prefix values for note \"%s\" with err: %s" %(currNote.subNotes, err))
            elif errState == 1:
                raise ParserException("ERROR: (formattingNotes|performing prevNote functions) Could not parse previous note \"%s\" with curr note \"%s\" with err: %s" %(prevNote.lyric, currNote.lyric, err))
            elif errState == 2:
                raise ParserException("ERROR: (formattingNotes|currentNote CV) Could not parse current note \"%s\" CV section \"%s\" with err: %s" %(currNote.lyric, currNote.syllables[0], err))
            elif errState == 3:
                raise ParserException(
                    "ERROR: (formattingNotes|currentNote VC) Could not parse current note \"%s\" VC section \"%s\" with err: %s" % (
                    currNote.lyric, currNote.syllables[-1], err))
            elif errState == 4:
                raise ParserException("ERROR: (formattingNotes|Adding \"-\") Could not add \"-\" to currNote \"%s\" with prevNote \"%s\" and err %s" %(currNote.subNotes[0], prevNote.subNotes[-1], err))
            else:
                raise ParserException("ERROR: (formattingNotes|Unknown Error with getSizes) Could not do getSizes with currNote \"%s\" and prevNote \"%s\" with err %s" %(currNote.lyric, prevNote.lyric, err))

    # finds the CC ending of a given currNote given what's in the oto
    def findCCEnding(self, currNote, myPrefix, mySuffix):

        # splits the note's lyric into two parts: noteSplit[0] = V and noteSplit[1] = C (inz -> ["i", "nz"]
        # sets up a tempList of notes to add back to currNote
        noteSplit = currNote.subNotes[1].splitLyric
        tempList = list()
        tempList.append(currNote.subNotes[0])

        # if the vowel is longer than one character and the VC is not in the oto, add the vowel to the new subNotes list and replace it with the last char
        # ex: [0r, th] => (0r-) [r, th]
        if len(noteSplit[0]) > 1 and self.checkOto(str(noteSplit[0]) + str(noteSplit[1]), myPrefix, mySuffix) is None:
            tempList.append(copyNote(currNote, str(noteSplit[0]) + '-'))
            noteSplit[0] = noteSplit[0][1:]

        # while we have at least some consonant left to test and the entire list together is not in the oto, add the first half plus the first char in
        # the second half to the tempList and shift the first character in the right to the left.
        # ex: [i, nz] -> (in-) [n, z]
        while len(noteSplit[1]) > 0 and self.checkOto(str(noteSplit[0]) + str(noteSplit[1]), myPrefix, mySuffix) is None:
            tempList.append(copyNote(currNote, str(noteSplit[0]) + str(noteSplit[1])[0:1] + "-"))
            noteSplit[0] = noteSplit[1][0]
            noteSplit[1] = noteSplit[1][1:]

        # if we added at least one thing then we "fixed" the CC (we add whatever's left to keep things consistant). Then replace the current note's subNOtes with tempList.
        if len(tempList) > 1:
            if len(noteSplit[1]) > 0:
                tempList.append(copyNote(currNote, noteSplit[0] + noteSplit[1]))
            currNote.subNotes.clear()
            currNote.subNotes = tempList

    # size should be size of next preutterance
    # if subNotes[0].length > 480, set all subNotes' velocity to 80, otherwise if < 480, set all to 150

    # sets the sizes for the previous note depending on the oto and the current note based off of the prior subNote's preutterance
    def getSizes(self, prevNote, currNote):

        counter = 0
        sum = 0
        myPrefix = ""
        mySuffix = ""
        currLyric = ""
        index = len(prevNote.subNotes) - 1
        errState = 0

        try:
            inCounter = 0

            # loop through all except the first note. Sets lengths based on the preutterance.
            while index > 0:
                # if you're the last note, get the first note in the next note's lyric as well as the prefix and suffix data from that note
                if index == len(prevNote.subNotes) - 1:
                    if self.notRest(currNote.lyric, currNote.state):
                        currLyric = currNote.subNotes[0].lyric
                        myPrefix = self.myPMap.getPrefixValue(currNote.strPitch).prefix if self.myPMap.getPrefixValue(currNote.strPitch).prefix is not None else ""
                        mySuffix = self.myPMap.getPrefixValue(currNote.strPitch).suffix if self.myPMap.getPrefixValue(currNote.strPitch).suffix is not None else ""
                    else:
                        currLyric = None
                # otherwise if you're any note, set currLyric to the previous lyric and  get the prefixmap data
                else:
                    currLyric = prevNote.subNotes[index+1].lyric
                    myPrefix = self.myPMap.getPrefixValue(prevNote.strPitch).prefix if self.myPMap.getPrefixValue(prevNote.strPitch).prefix is not None else ""
                    mySuffix = self.myPMap.getPrefixValue(prevNote.strPitch).suffix if self.myPMap.getPrefixValue(prevNote.strPitch).suffix is not None else ""

                # if the previous note was not a rest, get the preutterance
                if currLyric is not None and self.checkOto(currLyric, myPrefix, mySuffix) is not None:
                    prevNote.subNotes[index].length = str(int(float(self.checkOto(currLyric, myPrefix, mySuffix).preutterance)))
                # otherwise grow the previous note.
                elif currLyric is not None and self.checkOto(currLyric, myPrefix, mySuffix) is not None:
                    prevNote.subNotes[index].length = "30"
                # otherwise if the currentLyric is a rest:
                elif currLyric is None and self.isRest(currNote.lyric):
                    # if note is at least twice as long as a half note, take at most a half note + some.
                    if int(currNote.length) > (960 * 2):
                        prevNote.subNotes[index].length = "990"
                        currNote.tempLen = str(int(currNote.length) - int(prevNote.subNotes[index].length) + 30)
                        prevNote.tempLen = str(int(prevNote.tempLen) + int(prevNote.subNotes[index].length) - 30)
                        # prevNote.subNotes[index].length, currNote.length, currNote.tempLen))
                    # otherwise get about half of it. Try to check for any CC's
                    else:
                        prevNote.subNotes[index].length = str(30 + ((int(currNote.length) - sum) // 2)) if int(currNote.length) > 60 or len(currNote.subNotes) == 1  else "30"
                        currNote.tempLen = str(int(currNote.length) - int(prevNote.subNotes[index].length) + 30)
                        prevNote.tempLen = str(int(prevNote.tempLen) + int(prevNote.subNotes[index].length) - 30)
                else:
                    prevNote.subNotes[index].length = "60" if int(prevNote.subNotes[index].length) > 120 else "30"

                sum += int(prevNote.subNotes[index].length)
                index -= 1


            errState = 1
            # if we have one more note but no room to fit it, divide the notes equally within the length
            if sum >= int(prevNote.tempLen) and len(prevNote.subNotes) > 1 and self.notRest(prevNote.subNotes[0].lyric, prevNote.state):
                sum = 0
                # divide the available space betwee the notes
                for myNote in prevNote.subNotes:
                    myNote.length = str(int(prevNote.tempLen) // len(prevNote.subNotes))
                    sum += int(myNote.length)

                prevNote.subNotes[0].length = str(int(prevNote.subNotes[0].length) + (int(prevNote.tempLen) - sum))
            # otherwise if we have at least one more note, add it with the remaining space
            elif sum < int(prevNote.tempLen):
                if prevNote.state != 'prev':
                    prevNote.subNotes[0].length = str(int(prevNote.tempLen) - sum)
                else:
                    prevNote.subNotes[0].setProperty("Length", str(int(prevNote.tempLen) - sum), True)


            # to fix: dealing with notes on rest notes
            for note in prevNote.subNotes:
                if int(prevNote.tempLen) > 480:
                    note.setProperty("Velocity", "80")
                elif int(prevNote.tempLen) < 480:
                    note.setProperty("Velocity", "150")

            errState = 2

            # try to fix sizes of things if we have room
            # "full length" = consonant - preutterance
            # or (prevNote.subNotes[-1].lastConst != "" and currNote.subNotes[0].lyric[0] != "_")
            if self.notRest(prevNote.lyric, prevNote.state) and self.notRest(currNote.lyric, currNote.state) and len(prevNote.lyric) > 1 and ' ' not in prevNote.subNotes[-1].lyric:
                if self.checkOto(prevNote.subNotes[-1].lyric, myPrefix, mySuffix) is not None and prevNote.subNotes[-1].state != "ccbeginning":
                    fullLen = int(float(self.checkOto(prevNote.subNotes[-1].lyric, myPrefix, mySuffix).consonant)) - int(float(self.checkOto(prevNote.subNotes[-1].lyric, myPrefix, mySuffix).preutterance))
                    if fullLen * 2 <= int(prevNote.subNotes[0].length):
                        prevNote.subNotes[0].length = str(int(prevNote.subNotes[0].length) - fullLen)
                        prevNote.subNotes[-1].length = str(int(prevNote.subNotes[-1].length) + fullLen)
                    elif int(prevNote.subNotes[0].length) < fullLen and (int(prevNote.subNotes[0].length) + 60) * 2 <= int(prevNote.subNotes[0].length):
                        prevNote.subNotes[0].length = str(int(prevNote.subNotes[0].length) - 60)
                        prevNote.subNotes[-1].length = str(int(prevNote.subNotes[-1].length) + 60)

            errState = 3
            if currNote.state == "next":
                currNote.subNotes[0].setProperty("Length", currNote.tempLen, True)

        except Exception as err:
            if errState == 0:
                raise ParserException("ERROR: (getSizes|initial Size Adjust) Failed to update sizes with prevNote \"%s\" and currNote \"%s\" on note %i#: \"%s\" with err %s" %(prevNote.lyric, currNote.lyric, index, prevNote.subNotes[index].lyric, err))
            elif errState == 1:
                raise ParserException("ERROR: (getSizes|CV Size Adjust) Failed to update the size of the first note with prevNote \"%s\" and currNote \"%s\" on note \"%s\" with err %s" % (prevNote.lyric, currNote.lyric, prevNote.subNotes[0].lyric, err))
            elif errState == 2:
                raise ParserException("ERROR: (getSizes|VC Size Adjust) Failed to update the size of the last note with prevNote \"%s\" and currNote \"%s\" on note \"%s\" with err %s" % (prevNote.lyric, currNote.lyric, prevNote.subNotes[-1].lyric, err))
            else:
                raise ParserException("ERROR: (getSizes|fix lasrSize) Failed to adjust the final note's length on note \"%s\" with err %s" %(currNote.lyric, err))

    # gets the syllables of the word given the list of possible syllables from the dictionary.
    # passes the first set of syllables that fits the word
    def getSyllables(self, syllables, numSyllables):
        for syllable in syllables:
            if len(syllable.split(":")) == numSyllables:
                return syllable if numSyllables == 1 else syllable.split(":")

        return None

    # determines if a note is a rest (or MIA)
    def notRest(self, inLyric, state=None):
        if inLyric != 'R' and inLyric != 'r' and (state != 'MIA'):
            return True
        return False

    def isRest(self, inLyric, state=None):
        if inLyric == 'R' or inLyric == 'r' or (state == 'MIA'):
            return True
        return False

    def checkOto(self, inLyric, prefix, suffix):
        if self.myOto.checkDict(inLyric, prefix, suffix) is None:
            self.myOto.setLyricInDict(inLyric, prefix, suffix)

        return self.myOto.checkDict(inLyric, prefix, suffix)

    # (testing function) prints all of the current notes and subnotes to the screen given a ust
    def printVCCVNotes(self):
        counter = 0
        for note in self.myUst.notes:
            print("Note %i: %s" %((counter+1), note.lyric))
            inCounter = 0
            for subNote in note.subNotes:
                print("Subnote %i: %s" %((inCounter+1), subNote.lyric))
                inCounter+= 1
            counter+= 1

    # writes the notes and subnotes in a ust to a file "out.txt"
    def printVCCVNotesOut(self):
        myFile = open("out.txt", 'a')

        counter = 0
        for note in self.myUst.notes:
            myFile.write("Note %i: %s\n" % ((counter + 1), note.lyric))
            inCounter = 0
            for subNote in note.subNotes:
                myFile.write("Subnote %i: %s\n" % ((inCounter + 1), subNote.lyric))
                inCounter += 1
            counter += 1

        myFile.write('\n')

        myFile.close()

    def clearNote(self, inNote):
        if len(inNote.subNotes) == 1:
            inNote.subNotes.clear()
        else:
            tempNote = inNote.subNotes[1:]
            inNote.subNotes.clear()
            inNote.subNotes = tempNote


        # self.missingWords = lyric
        # self.missingWords = "1"
        # self.missingWords = ""
        # currNote.state = "MIA"
        # currNote.subNotes = [copyNote(currNote)]

class missingNote():
    def __init__(self, inLyric = None, inNumSylls = 0, inFixedSylls = "", inStartNote = 0, inRange = 0, inLastNote = -1):
        self.__lyric = inLyric
        self.__numSylls = inNumSylls
        self.__fixedSylls = inFixedSylls
        self.__startNote = inStartNote
        self.__range = inRange
        self.__lastNote = inLastNote

    @property
    def lyric(self):
        return self.__lyric
    @lyric.setter
    def lyric(self, inLyric):
        self.__lyric = inLyric

    @property
    def numSylls(self):
        return self.__numSylls
    @numSylls.setter
    def numSylls(self, inNumSylls):
        self.__numSylls = inNumSylls

    @property
    def fixedSylls(self):
        return self.__fixedSylls
    @fixedSylls.setter
    def fixedSylls(self, inFixedSylls):
        self.__fixedSylls = inFixedSylls

    @property
    def startNote(self):
        return self.__startNote
    @startNote.setter
    def startNote(self, inStartNote):
        self.__startNote = inStartNote

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, inRange):
        self.__range = inRange

    @property
    def lastNote(self):
        return self.__lastNote
    @lastNote.setter
    def lastNote(self, inLastNote):
        self.__lastNote = inLastNote

    def listData(self):
        return [self.lyric, str(self.numSylls), ""]



    # myFile.write("After PrevNote: %s\n" % (prevNote.lyric))
    # inCounter = 0
    # for subNote in prevNote.subNotes:
    #     myFile.write("Subnote %i: %s\n" % ((inCounter + 1), subNote.lyric))
    #     inCounter += 1
    #
    # myFile.write("CurrNote: %s\n" % (currNote.lyric))
    # inCounter = 0
    # for subNote in currNote.subNotes:
    #     myFile.write("Subnote %i: %s\n" % ((inCounter + 1), subNote.lyric))
    #     inCounter += 1
    # for myNote in currNote.subNotes:
    #     myFile.write("\tBefore cc ending I had %s\n" % myNote.lyric)

        # myFile.write("After Sizes\nPrevNote: %s\n" % (prevNote.lyric))
        # inCounter = 0
        # for subNote in prevNote.subNotes:
        #     myFile.write("Subnote %i: %s\n" % ((inCounter + 1), subNote.lyric))
        #     myFile.write("Lyric = %s, length = %s, pitch = %s, convertedPitch = %s\n" % (
        #     subNote.lyric, subNote.length, subNote.pitch, subNote.strPitch))
        #     inCounter += 1
        #
        # myFile.write("CurrNote: %s\n" % (currNote.lyric))
        # inCounter = 0
        # for subNote in currNote.subNotes:
        #     myFile.write("Subnote %i: %s\n" % ((inCounter + 1), subNote.lyric))
        #     myFile.write("Lyric = %s, length = %s, pitch = %s, convertedPitch = %s\n" % (
        #         subNote.lyric, subNote.length, subNote.pitch, subNote.strPitch))
        #     inCounter += 1

        # for subNote in prevNote.subNotes:
        #     myFile.write("Subnote %i: %s\n" % ((inCounter + 1), subNote.lyric))
        #     myFile.write("Lyric = %s, length = %s, pitch = %s, convertedPitch = %s\n" % (
        #         subNote.lyric, subNote.length, subNote.pitch, subNote.strPitch))
        #     inCounter += 1
        #
        # myFile.write("CurrNote: %s\n" % (currNote.lyric))
        # inCounter = 0
        # for subNote in currNote.subNotes:
        #     myFile.write("Subnote %i: %s\n" % ((inCounter + 1), subNote.lyric))
        #     myFile.write("Lyric = %s, length = %s, pitch = %s, convertedPitch = %s\n" % (
        #         subNote.lyric, subNote.length, subNote.pitch, subNote.strPitch))
        #     inCounter += 1


