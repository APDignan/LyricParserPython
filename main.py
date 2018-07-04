import sys
from UST import Ust, note, copyNote
from PREFIX import prefixMap, prefixMapItem
from OTO import Oto, OtoLine
import utauGen
import traceback
from Trie import trie
import os
from os import listdir
from os.path import isfile, join
from ParserException import ParserException


# parser class: Used by the UI to contain all of the information from UTAU, including the UST, Oto.ini, and prefix.map files.
class parser():
    def __init__(self):
        self.__myUst = None
        self.__myOto = None
        self.__myPMap = None
        self.__myTrie = dict()
        self.__trieList = list()
        self.__selectedTrie = "English"
        self.__isParsed = False
        self.__fullLen = False
        self.__blendVowels = False
        self.__ENG_VVBlend = False
        self.__startSymbol = "-"
        self.__endSymbol = "-"

        # Loads dictionaries into the parser; searches dictionary folder for any .txt files to read in
        dictionaryLocation = listdir(join(os.getcwd(), "dictionary"))
        for item in dictionaryLocation:
            if isfile(join(join(os.getcwd(), "dictionary"), item)):
                fname = item[:-4]
                self.getTrieStruct[fname] = trie(fname, join(join(os.getcwd(), "dictionary"), item))

                # any .txt files are opened and read; if there's an order parameter then save it, then create the trie
                testOrder = False
                with open(join(join(os.getcwd(), "dictionary"), item)) as myFile:
                    self.__selectedTrie = fname
                    self.__trieList.append(fname)
                    for line in myFile:
                        if not testOrder:
                            testOrder = True
                            if line[0:5] == "order":
                                self.getTrieStruct[fname].printOrder = line[6:-1]
                        else:
                            self.addWordToTrie(line)
                myFile.close()
            else:
                print("Couldn't find file at %s" % join(join(os.getcwd(), "dictionary"), item))

        # read in the settings from the .txt file
        settingsDict = dict()
        with open("settings.txt") as settingsFile:
            for line in settingsFile:
                if len(line) > 0 and "=" in line and len(line.split("=")) == 2:
                    settingsDict[line.split("=")[0]] = line.split("=")[1][:-1]
                elif len(line) > 0 and len(line.split(" ")) == 2:
                    settingsDict[line.split(" ")[0]] = line.split(" ")[1][:-1]

        # sets any settings
        if "fulllen" in settingsDict and settingsDict["fulllen"] == "true":
            self.fullLen = True

        if "blendvowels" in settingsDict and settingsDict["blendvowels"] == "true":
            self.blendVowels = True

        if "blendengvowels" in settingsDict and settingsDict["blendengvowels"] == "true":
            self.ENG_VVBlend = True

        if "defaultdictionary" in settingsDict and settingsDict["defaultdictionary"] in self.getTrieStruct:
            self.selectedTrie = settingsDict["defaultdictionary"]
        else:
            self.selectedTrie = None

        self.__startSymbol = settingsDict["startSymbol"] if "startSymbol" in settingsDict and len(settingsDict["startSymbol"]) > 0 else "-"

        self.__startSymbol = settingsDict["endSymbol"] if "endSymbol" in settingsDict and len(settingsDict["endSymbol"]) > 0 else "-"

        settingsFile.close()

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

    # gets and sets the currently selected trie
    @property
    def myTrie(self):
        # if self.__selectedTrie in self.__myTrie:
        # print("Current trie is " + self.__selectedTrie);
        return self.__myTrie[self.__selectedTrie]
    @myTrie.setter
    def myTrie(self, inTrie):
        # if self.__selectedTrie in self.__myTrie:
        self.__myTrie[self.__selectedTrie] = inTrie

    # gets the trie dictionary
    @property
    def getTrieStruct(self):
        return self.__myTrie

    @property
    def isParsed(self):
        return self.__isParsed
    @isParsed.setter
    def isParsed(self, inParsed):
        self.__isParsed = inParsed

    @property
    def fullLen(self):
        return self.__fullLen
    @fullLen.setter
    def fullLen(self, inFullLen):
        self.__fullLen = inFullLen

    @property
    def blendVowels(self):
        return self.__blendVowels
    @blendVowels.setter
    def blendVowels(self, inBlendVowels):
        self.__blendVowels = inBlendVowels

    @property
    def ENG_VVBlend(self):
        return self.__ENG_VVBlend
    @ENG_VVBlend.setter
    def ENG_VVBlend(self, inBlendVowels):
        self.__ENG_VVBlend = inBlendVowels

    @property
    def startSymbol(self):
        return self.__startSymbol
    @startSymbol.setter
    def startSymbol(self, inStartSymbol):
        self.__startSymbol = inStartSymbol

    @property
    def endSymbol(self):
        return self.__endSymbol
    @endSymbol.setter
    def endSymbol(self, inEndSymbol):
        self.__endSymbol = inEndSymbol

    @property
    def selectedTrie(self):
        return self.__selectedTrie
    @selectedTrie.setter
    def selectedTrie(self, inSelectedTrie):
        self.__selectedTrie = inSelectedTrie

    @property
    def trieList(self):
        return self.__trieList
    @trieList.setter
    def trieList(self, inTrieList):
        self.__trieList = inTrieList

    @property
    def missingWords(self):
        return self.__missingWords
    @missingWords.setter
    def missingWords(self, inMissing):
        self.__missingWords.append(inMissing)


    # initial execution to load all of the data into the parser object.
    def run(self):
        # Try to open the Ust, Oto.ini, and prefix.map files.
        myErr = 2
        try:

            self.myUst = Ust(sys.argv[1])
            myErr = 3
            if self.myOto is None:
                self.myOto = Oto(self.myUst.voiceDir)
            myErr = 4
            if self.myPMap is None:
                self.myPMap = prefixMap(self.myUst.voiceDir)

            try:
                self.parseVCCV()
            except ParserException as err:
                print(err.myMsg)
                traceback.print_exc()
            except Exception as err:
                traceback.print_exc()

        except ParserException as pErr:
            print(pErr.myMsg)
        except Exception as err:
            if myErr == 1:
                print("ERROR: Either this plugin is being run outside of UTAU, or no UST file was found.")
            elif myErr == 2:
                print("ERROR: Could not process UST file.")
            elif myErr == 3:
                print("ERROR: Could not process Oto.ini.")
            elif myErr == 4:
                print("ERROR: Could not process prefix.map.")


    # on completion of execution, parser writes the current Trie to dictionary.txt and overrites the UST.
    def finishPlugin(self):
        errState = 0
        try:
            if self.isParsed:
                self.myUst.closeUst(self.myUst.ustPath)
        except ParserException as pErr:
            raise pErr
        except Exception as err:
            raise ParserException("ERROR: Could not finish ending plugin procedures given an err %s" %err)


    # adds a line from the dictionary.txt file to the Trie with their syllables
    def addWordToTrie(self, inStr):
        "_word: syll"
        halfIndex = inStr.find(':')

        if halfIndex > 1:
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
    def parseVCCV(self):

        index = 0
        lastNote = -1
        currNote = ""

        try:
            # loop through each note in the ust
            for currNote in self.myUst.notes:
                # tempLen = the length the note has available to it rather than it's original length.
                currNote.tempLen = currNote.length

                # ignores any prev/next notes and sets their subnotes to the lyric.
                if currNote.state == "prev" or currNote.state == "next":
                    currNote.subNotes = [copyNote(currNote, location="prev/next")]
                    currNote.parentLyric = currNote.lyric + " (" + currNote.state + ")"
                # if the note has a valid lyric and hasn't been parsed yet, try to parse it
                elif len(currNote.lyric) > 0 and currNote.state != 'done' and currNote.state != 'MIA':
                    lyric = currNote.lyric.lower()
                    tempSylls = self.getSyllables(self.myTrie.getWord(lyric), 1)

                    # if our lyric doesn't end with a "-", isn't a rest, and is in the trie, it's a single syllable word.
                    if lyric[-1] != '-' and self.notRest(lyric):
                        if tempSylls is not None:
                            self.createVCCVNotes(currNote, tempSylls)
                            lastNote = index
                            currNote.parentLyric = lyric
                        # otherwise if the note's lyric is not in the dictionary, add it to the missingWords list and set it to MIA
                        else:
                            self.missingWords = missingNote(inLyric=lyric, inNumSylls=1, inStartNote=index, inRange=1)
                            lastNote = index
                            currNote.state = "MIA"
                            currNote.subNotes = [copyNote(currNote, location="missingLyric")]

                    # if our note's lyric is "-" then it's an extender, so try to extend the previous true note if it's not MIA.
                    elif lyric == '-' and self.myUst.notes[lastNote].state != "prev":
                        if self.myUst.notes[lastNote].state == "MIA" or lastNote < 0:
                            currNote.state = "MIA"
                            currNote.subNotes = [copyNote(currNote, location="missingExtender")]
                            # add the missing note to the missingWords list for the user to look through in the UI
                            if lastNote > -1:
                                self.missingWords = missingNote(inLyric="-", inNumSylls=0, inStartNote=index, inRange= 1, inLastNote=(self.missingWords[-1].startNote + self.missingWords[-1].range - 1))
                            else:
                                self.missingWords = missingNote(inLyric="-", inNumSylls=1, inStartNote=index, inRange= 1)

                        else:
                            self.extendVCCVNote(self.myUst.notes[lastNote], currNote)
                            currNote.parentLyric = self.myUst.notes[lastNote].parentLyric + " (-)"
                            lastNote = index

                    # if the lyric ends with "-" then we have a multiple-syllable word.
                    elif lyric[-1] == '-':
                        counter = 0
                        numSylls = 0
                        currLyric = ""

                        # loop through ust until we find the end of the word. Count non-rest and non-extender notes as syllables.
                        while index + counter < len(self.myUst.notes) and self.myUst.notes[index + counter].state != "next" and (self.myUst.notes[index + counter].lyric[-1] == '-' or self.isRest(self.myUst.notes[index + counter].lyric)):
                            if self.myUst.notes[index + counter].lyric != '-' and self.notRest(self.myUst.notes[index + counter].lyric):
                                currLyric = currLyric + self.myUst.notes[index + counter].lyric[:-1]
                                numSylls += 1
                            counter += 1

                        # checks if we ended because we found the last syllable. if so add it to the string
                        if index + counter < len(self.myUst.notes) and self.myUst.notes[index + counter]. state != "next" and self.myUst.notes[index + counter].lyric != '-' and self.notRest(self.myUst.notes[index + counter].lyric):
                            currLyric = currLyric + self.myUst.notes[index + counter].lyric
                            numSylls += 1
                            counter+= 1

                        currLyric = currLyric.lower()

                        # if the word we found was in the dictionary with the right number of syllables, format the notes used
                        tempSylls = self.getSyllables(self.myTrie.getWord(currLyric), numSylls)
                        if tempSylls is not None:
                            noteIndex = index
                            inCounter = 0
                            syllNum = 0

                            # loop through each of the notes we found
                            while inCounter < counter:
                                # if the note was not a rest or an extender put the ith syllable in it
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


                        # If the word is missing, add it to the missingWords list and set the notes to MIA so they don't get parsed
                        else:
                            self.missingWords = missingNote(inLyric=currLyric, inNumSylls=numSylls, inStartNote = index, inRange = counter)
                            inCounter = 0
                            while inCounter < counter:
                                if self.notRest(self.myUst.notes[index + inCounter].lyric):
                                    self.myUst.notes[index + inCounter].state = "MIA"
                                self.myUst.notes[index + inCounter].subNotes = [copyNote(self.myUst.notes[index + inCounter], location="missingMulti")]
                                inCounter += 1

                    # Otherwise the note should be a rest
                    else:
                        if len(currNote.lyric) == 0:
                            currNote.lyric = "R"
                        currNote.subNotes = [copyNote(currNote, location="Rest")]
                        currNote.parentLyric = "R"

                index += 1

        except ParserException as pErr:
            raise pErr
        except Exception as err:
            raise ParserException("ERROR: (Parsing VCCV Lyrics) Could not parse lyric %i# : %s. Rose error %s" %(index, currNote.lyric, err))

    # parseFixedVCCV: parses the notes specified by the user if they gave the proper syllables
    def parseFixedVCCV(self, inMissingNote, fullClear=False):

        # get the relevant notes: prevNote and currNote for pre-editing and endNote and nextNote for post-editing
        prevNote = self.myUst.notes[inMissingNote.startNote - 1]
        currNote = self.myUst.notes[inMissingNote.startNote]
        endNote = self.myUst.notes[inMissingNote.startNote + inMissingNote.range - 1]
        nextNote = self.myUst.notes[inMissingNote.startNote + inMissingNote.range] if inMissingNote.startNote + inMissingNote.range < len(self.myUst.notes) else None

        if currNote.state != "prev" and currNote.state != "next" and currNote.state != "noNext":
            currNote.state = ""

        # if the numSylls is 0, then we have a stand-alone "-". Extend it based on the previous note
        if inMissingNote.numSylls == 0:
            # fully clear the note if we're updating the UST from the parser tab
            if fullClear:
                self.myUst.notes[inMissingNote.startNote].subNotes.clear()

            self.clearNote(currNote)
            self.extendVCCVNote(self.myUst.notes[inMissingNote.lastNote], currNote)
            currNote.parentLyric = self.myUst.notes[inMissingNote.lastNote].parentLyric + " (-)"

            # only parse the notes fully if they're being fixed from the errors tab
            if self.isParsed:
                self.fixPrevNote(prevNote, currNote)
                self.fixNextNote(currNote, nextNote)

        # otherwise if numSylls is 1 then it's a single note. Create the note.
        elif inMissingNote.numSylls == 1 and inMissingNote.lyric != "-":
            #fully clear the note if we're updating the UST from the parser tab
            if fullClear:
                self.myUst.notes[inMissingNote.startNote].subNotes.clear()

            self.clearNote(currNote)
            self.createVCCVNotes(currNote, inMissingNote.fixedSylls)

            currNote.parentLyric = inMissingNote.lyric

            if self.isParsed:
                self.fixPrevNote(prevNote, currNote)
                self.fixNextNote(currNote, nextNote)


        # finally the note must have more than one syllable, so parse it as a multi-syllable word
        else:
            index = inMissingNote.startNote
            syllNum = 0
            lastNote = -1

            # loop through the notes given by the missing note's range
            while index < inMissingNote.startNote + inMissingNote.range:
                # if it's not an extender or a rest, create a note using the syllNumth syllable.
                if self.myUst.notes[index].state != "prev" and self.myUst.notes[index].state != "next":
                    self.myUst.notes[index].state = ""

                # fully clear the note if we're updating the UST from the parser tab
                if fullClear:
                    self.myUst.notes[index].subNotes.clear()

                self.clearNote(self.myUst.notes[index])

                # if the lyric is not a rest or extender, place the ith syllabe in it
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

            # Only format the notes if we've already parsed the ust
            if self.isParsed:
                index = inMissingNote.startNote + 1
                self.fixPrevNote(prevNote, currNote)
                while index < inMissingNote.startNote + inMissingNote.range:
                    self.formatNotes(self.myUst.notes[index - 1], self.myUst.notes[index])
                    index += 1
                self.fixNextNote(endNote, nextNote)


    # when fixing currNote we have to remove the prior note's "-" and vowel ending if it's there and reformat the notes
    def fixPrevNote(self, prevNote, currNote):
        if prevNote.subNotes[-1].lyric[-1] == self.endSymbol:
            prevNote.subNotes[-1].lyric = prevNote.subNotes[-1].lyric[:-1]

            if prevNote.subNotes[-1].lastVowel != "" and len(prevNote.subNotes) > 1:
                tempNotes = prevNote.subNotes[:-1]
                prevNote.subNotes.clear()
                prevNote.subNotes = tempNotes

        self.formatNotes(prevNote, currNote)

    # when fixing currNote we need to update any CCV beginnings and "-" symbols before we reformat them
    def fixNextNote(self, currNote, nextNote):
        if nextNote is not None and nextNote.state != "MIA" and nextNote.subNotes[0].lyric[0] == '_':
            nextNote.subNotes[0].lyric = currNote.subNotes[-1].lyric + nextNote.subNotes[0].lyric[2:]
            tempNotes = currNote.subNotes[:-1]
            currNote.subNotes.clear()
            currNote.subNotes = tempNotes

        if nextNote is not None and nextNote.state != "MIA" and nextNote.subNotes[0].lyric[0] == self.startSymbol:
            nextNote.subNotes[0].lyric = nextNote.subNotes[0].lyric[1:]

        self.formatNotes(currNote, nextNote)

    # # given a syllable of a word, break it up into it's individual parts
    # def createVCCVNotes(self, inNote, syllables):
    #     counter = 0
    #     # loop on the syllables (divided by commas). The first note should be a copy of the original note
    #     # while the rest should be generic to not copy the pitchbends
    #     for syllable in syllables.split(","):
    #         if counter == 0:
    #             tempNote = copyNote(inNote, syllable, location="VCCVNote")
    #         else:
    #             tempNote = note(True, lyric=syllable, pitch=inNote.pitch)
    #
    #         # add the note with the syllable to the current note's subNotes
    #         inNote.subNotes = [tempNote]
    #         if inNote.syllables is None:
    #             inNote.syllables = list()
    #         inNote.syllables = inNote.syllables.append(syllable)
    #         counter += 1

    # create a VCCV Note based on the syllables given
    def createVCCVNotes(self, inNote, syllables, update=False):

        # split the syllables based on the format C*"("V*")"C*
        if "(" in syllables and ")" in syllables:
            syllableParts = [syllables[:syllables.index("(")], syllables[syllables.index("(") + 1:syllables.index(")")], syllables[syllables.index(")") + 1:]]
            tempNotes = list()
            tempNotes.append(copyNote(inNote, syllableParts[0] + syllableParts[1], location="VCCVNote"))

            # if we have an ending consonant, add the VC portion
            if len(syllableParts[2]) > 0:
                tempNotes.append(note(True, lyric=syllableParts[1] + syllableParts[2], pitch=inNote.pitch))

            inNote.subNotes.clear()
            inNote.subNotes = tempNotes

            inNote.startConst = syllableParts[0]
            inNote.vowel = syllableParts[1]
            inNote.endConst = syllableParts[2]
        # split the syllables based on the format CV,VC (only when reading directly from parser
        elif update:
            syllList = syllables.split(",")
            tempNotes = list()
            if len(syllList) > 0:
                for syll in syllList:
                    if len(tempNotes) == 0 and len(syll) > 0:
                        tempNotes.append(copyNote(inNote, syll, location="VCCVNoteUpdateUST"))
                    elif len(syll) > 0:
                        tempNotes.append(note(True, lyric=syll, pitch=inNote.pitch))

                inNote.subNotes = tempNotes



    # Extends a note currNote based off of the previous note's lyric.
    # Cases:
    #   1. Lyric = CV (kla)
    #       [kla] [-] => [kla] [a]
    #   2. Lyric = CVC (kla,ak)
    #       [[kla],[ak]] [-] => [kla] [[a], [ak]]
    def extendVCCVNote(self, prevNote, currNote):
        # list of vowels words can end with.

        if prevNote.vowel != "":

            # set the current note's subnotes to the previous note's vowel + the previous note's subnotes[1:]
            currNote.subNotes = [copyNote(currNote, prevNote.vowel, location="ExtendVCCV")]
            currNote.subNotes = prevNote.subNotes[1:]

            # remove all but the first subnote from prevNote
            tempNote = prevNote.subNotes[0]
            prevNote.subNotes.clear()
            prevNote.subNotes = [tempNote]

            # set all of the consonant info
            currNote.startConst = ""
            currNote.vowel = prevNote.vowel
            currNote.endConst = prevNote.endConst
            prevNote.endConst = ""

            # set pitches
            for myNote in currNote.subNotes:
                myNote.pitch = str(currNote.pitch)


    # Given the previous note and current note, converts the lyric from Psuedo VCCV (CV,VC only) to VCCV. Includes adding "-"
    # to beginning and ends of notes, adding VV and V C transitions, and parsing CCV and VCC samples. All parsing is based
    # on what's in the user's Oto.
    def formatNotes(self, prevNote, currNote):

        errState = 0

        # if the current note is none, prevnote is the last note in the UST. in this case create a dummy note to represent the "VC -" portion
        # of the note to add on to the end of the ust.
        if currNote is None and prevNote.state != "MIA" and self.myUst.hasNext == False and prevNote == self.myUst.notes[-1] and self.myUst.notes[-1].state != "noNext":
            currNote = note(True, lyric="R", pitch=str(prevNote.pitch))
            currNote.subNotes = [copyNote(currNote, location="formatNotes")]
            currNote.state = "noNext"
            self.myUst.notes.append(currNote)

        try:
            #gets the prefix and suffix of the current note
            myPrefix = self.myPMap.getPrefixValue(currNote.strPitch).prefix if self.myPMap.getPrefixValue(currNote.strPitch).prefix is not None else ""
            mySuffix = self.myPMap.getPrefixValue(currNote.strPitch).suffix if self.myPMap.getPrefixValue(currNote.strPitch).suffix is not None else ""

            errState = 1

            # if the previous and current notes are valid, try formatting them based on the selected dictionary
            if self.notRest(prevNote.lyric, prevNote.state) and self.notRest(currNote.lyric, currNote.state) and prevNote.state != "prev":
                prevVC = prevNote.vowel + prevNote.endConst
                currCV = currNote.startConst + currNote.vowel

                # 8n, 9l, Ang
                # See if there are any VV or even VCV matches; if so add them and remove the previous note's ending
                if len(prevVC) > 0 and len(currCV) > 0 and self.checkOto(prevVC + currCV, myPrefix, mySuffix) is not None and currNote.lyric != "-":
                    currNote.subNotes[0].lyric = prevVC + currCV
                    if len(prevNote.subNotes) > 1:
                        del prevNote.subNotes[-1]
                    currNote.state = "VV"

                # if we're using english, have selected ENG_VVBlend, and have differing vowels between the prevnad currnotes
                # try to blend the vowels
                elif self.ENG_VVBlend and len(prevVC) > 0 and len(currCV) > 0 and prevVC != currCV and prevVC == prevNote.vowel and currCV == currNote.vowel:
                    if len(prevVC) == 1:
                        myConst = 'y'
                        if prevVC == 'o':
                            myConst = 'w'
                        elif prevVC == '3':
                            myConst = 'r'

                        prevNote.subNotes = [
                            note(True, lyric=prevVC + " " + myConst, pitch=prevNote.subNotes[-1].pitch)]
                        currNote.subNotes[0].lyric = myConst + currNote.subNotes[0].lyric
                        currNote.startConst = myConst

                    elif len(prevVC) == 2:
                        myConst = prevVC[-1]
                        currNote.subNotes[0].lyric = myConst + currNote.subNotes[0].lyric
                        currNote.startConst = myConst

                    elif len(prevVC) == 3:
                        currNote.subNotes[0].lyric = "_" + currNote.subNotes[0].lyric

                # Format any "V C" like blending for the previous note
                elif len(prevVC) > 0 and len(currNote.startConst) > 0:
                    tempCC = currNote.startConst

                    # get the largest consonant from currnote that we have a "V C" recording in the oto
                    while len(tempCC) > 0 and self.checkOto(prevVC + " " + tempCC, myPrefix, mySuffix) is None:
                        tempCC = tempCC[:-1]

                    if len(tempCC) > 0 and len(prevNote.subNotes) == 1:
                        prevNote.subNotes = [
                            note(True, lyric=prevVC + " " + tempCC, pitch=prevNote.subNotes[-1].pitch)]

                    # otherwise just replace the previous ending with this
                    elif len(tempCC) > 0:
                        prevNote.subNotes[-1].lyric = prevVC + " " + tempCC

                # try blending vowels with previous note consonants to make it sound better
                if self.blendVowels:
                    myLastConst = prevNote.endConst

                    if myLastConst == "t" or myLastConst == "d":
                        myLastConst = "dd"

                    if (len(myLastConst) == 1 or myLastConst == "dd") and currNote.startConst == "" and self.checkOto(myLastConst + currNote.subNotes[0].lyric, myPrefix,
                                                               mySuffix) is not None and self.checkOto(prevNote.subNotes[-1].lyric[:-1] + " " + myLastConst, myPrefix, mySuffix) is not None:
                        currNote.startConst = myLastConst
                        prevNote.endConst = ""
                        currNote.subNotes[0].lyric = myLastConst + currNote.subNotes[0].lyric
                        prevNote.subNotes[-1].lyric = prevNote.subNotes[-1].lyric[:-1] + " " + myLastConst

            # add any ending dashes because the currnote is a rest
            elif self.isRest(currNote.lyric, currNote.state) and self.notRest(prevNote.lyric, prevNote.state) and prevNote.state != "prev":
                prevVC = prevNote.vowel + prevNote.endConst

                if len(prevNote.subNotes) == 1 and prevVC == prevNote.vowel:
                    prevNote.subNotes = [note(True, lyric=prevNote.vowel + self.__endSymbol, pitch=prevNote.subNotes[-1].pitch)]
                else:
                    prevNote.subNotes[-1].lyric = prevNote.subNotes[-1].lyric + self.__endSymbol

            errState = 2

            # Try seeing if the note's CV and VC portions have been parsed and, if not, parse them
            # First test if the first subNote (always the psuedoVCCV CV) is in the oto. If not, then test it should be a CCV to be parsed
            if self.checkOto(currNote.subNotes[0].lyric, myPrefix, mySuffix) is None:
                # if we start with at least 2 consonants and we're a valid note, then add the "proper" CCV notes
                if len(currNote.startConst) > 1 and self.notRest(currNote.lyric, currNote.state):
                    tempLyric = currNote.startConst if self.notRest(prevNote.lyric, prevNote.state) else self.__startSymbol + currNote.startConst
                    prevNote.subNotes = [note(True, lyric=tempLyric, pitch=prevNote.subNotes[-1].pitch)]
                    prevNote.subNotes[-1].state = "ccbeginning"
                    currNote.subNotes[0].lyric = "_" + currNote.subNotes[0].lyric[len(currNote.startConst) - 1:]

            errState = 3

            # Then test the second half of the note; test if it's in the oto and if not, try to parse it as a VCC
            # loop until you find a VC that works, then do old one to take 1ng into account
            if len(currNote.endConst) > 0 and self.notRest(currNote.subNotes[-1].lyric, currNote.state) and self.checkOto(currNote.subNotes[-1].lyric, myPrefix, mySuffix) is None:
                self.findCCEnding(currNote, myPrefix, mySuffix)

            errState = 4

            # add the "-" symbol to notes if the previous note is a rest or if the current lyric is a vowel following a non VV transition
            if self.isRest(prevNote.subNotes[-1].lyric, prevNote.state) and currNote.state != "next":
                if self.notRest(currNote.subNotes[0].lyric, currNote.state) and currNote.subNotes[0].lyric[0] != "_":
                    currNote.subNotes[0].lyric = self.__startSymbol + currNote.subNotes[0].lyric

            elif self.notRest(currNote.subNotes[0].lyric, currNote.state) and currNote.state != "next":
                if currNote.startConst == "" and currNote.lyric != "-" and (currNote.state != "VV"):
                    currNote.subNotes[0].lyric = self.__startSymbol + currNote.subNotes[0].lyric

            errState = 5

            # if prevNote was the last note in the ust, set up the dummy note to have the prevNote's last subNote.
            if currNote.state == "noNext":
                currNote.subNotes.clear()
                currNote.subNotes = [prevNote.subNotes.pop(-1)]
                currNote.length = "480"

            self.getSizes(prevNote, currNote)

        except ParserException as pErr:
            raise pErr
        except Exception as err:
            if errState == 0:
                raise ParserException("ERROR: (formattingNotes|getting prefix.map vals) Could not get prefix values for note \"%s\" with err: %s" %(currNote.subNotes, err))
            elif errState == 1:
                raise ParserException("ERROR: (formattingNotes|performing prevNote functions) Could not parse previous note \"%s\" with curr note \"%s\" with err: %s" %(prevNote.lyric, currNote.lyric, err))
            # elif errState == 2:
            #     raise ParserException("ERROR: (formattingNotes|currentNote CV) Could not parse current note \"%s\" CV section \"%s\" with err: %s" %(currNote.lyric, currNote.syllables[0], err))
            elif errState == 3:
                raise ParserException(
                    "ERROR: (formattingNotes|currentNote VC) Could not parse current note \"%s\" VC section \"%s\" with err: %s" % (
                    currNote.lyric, currNote.subNotes[-1].lyric, err))
            elif errState == 4:
                raise ParserException("ERROR: (formattingNotes|Adding \"-\") Could not add \"-\" to currNote \"%s\" with prevNote \"%s\" and err %s" %(currNote.subNotes[0], prevNote.subNotes[-1], err))
            else:
                raise ParserException("ERROR: (formattingNotes|Unknown Error with getSizes) Could not do getSizes with currNote \"%s\" and prevNote \"%s\" with err %s" %(currNote.lyric, prevNote.lyric, err))


    # get the CC endings of a note by splitting it's VCC into VC1-, C1C2-, C3...
    def findCCEnding(self, currNote, myPrefix, mySuffix):
        # initialize by splitting the VC on it's last character
        noteSplit = [currNote.vowel + currNote.endConst[:-1], currNote.endConst[-1]]
        foundVCC = False

        # loop through each possibility starting with the longest VC possible. If we don't find in our oto
        # the entire breakdown, then try the next largest possibility, otherwise set it to MIA.
        while len(noteSplit[0]) > 0 and not foundVCC:
            found = self.findCCEndingRecHelper(noteSplit[0], noteSplit[1], currNote, myPrefix, mySuffix)

            # if we didn't get the correct VCC breakdown, change noteSplit's values to the next largest possible one
            if found is None:
                noteSplit[1] = noteSplit[0][-1] + noteSplit[1]
                noteSplit[0] = noteSplit[0][:-1]

            # otherwise set the currNote's subnotes to what we got and exit th eloop
            else:
                currNote.subNotes.clear()
                currNote.subNotes = found
                foundVCC = True

        # if we failed, set the last note's subNote to MIA, which really doesn't do anything
        if not foundVCC:
            currNote.subNotes[-1].state = "MIA"


    # not really recursive, but helps find the CC ending. Tries to find valid breakdowns of the VCC ending, starting with
    # the largest possibilities. If it doesn't find a valid breakdown for the given front/back, return none.
    def findCCEndingRecHelper(self, front, back, currNote, myPrefix, mySuffix):

        tempList = [currNote.subNotes[0]]

        # loops through the VC, checking to find the largest correct VC- until we get to the end. If we exhaust all
        # optinos, return None. Otherwise return the successful VCC breakdown.
        while len(front) > 0:

            #if we found a valid front portion, add it to the tempList
            if self.checkOto(front, myPrefix, mySuffix) is not None:
                tempList.append(note(default=True, lyric=front, pitch=currNote.pitch))

                # if we completed the VCC, return the final note, otherwise test the rest of the characters we have left
                if back == "":
                    return tempList
                else:
                    tempList[-1].lyric = tempList[-1].lyric + self.__endSymbol
                    # front = front[len(currNote.vowel):] + back if front[0:len(currNote.vowel)] == currNote.vowel else front[1:] + back
                    front = front[1:] + back
                    back = ""
            # if front was not valid, remove the last character and add it to back
            else:
                back = front[-1] + back
                front = front[:-1]

        return None

    # sets the sizes for the previous note's subnotes depending on the oto and the current note.
    def getSizes(self, prevNote, currNote):

        sum = 0
        myPrefix = ""
        mySuffix = ""
        index = len(prevNote.subNotes) - 1
        errState = 0

        try:
            inCounter = 0

            # loop through all except the first subNote. Sets lengths based on the preutterance.
            while index > 0:

                # if you're the last subnote, get the nextnote's first subnote's lyric as well as the prefix and suffix data from that note
                if index == len(prevNote.subNotes) - 1:
                    if self.notRest(currNote.lyric, currNote.state):
                        currLyric = currNote.subNotes[0].lyric
                        myPrefix = self.myPMap.getPrefixValue(currNote.strPitch).prefix if self.myPMap.getPrefixValue(currNote.strPitch).prefix is not None else ""
                        mySuffix = self.myPMap.getPrefixValue(currNote.strPitch).suffix if self.myPMap.getPrefixValue(currNote.strPitch).suffix is not None else ""
                    else:
                        currLyric = None

                # otherwise if you're an other subnote, set currLyric to the previous subnote's lyric and  get the prefixmap data
                else:
                    currLyric = prevNote.subNotes[index+1].lyric
                    myPrefix = self.myPMap.getPrefixValue(prevNote.strPitch).prefix if self.myPMap.getPrefixValue(prevNote.strPitch).prefix is not None else ""
                    mySuffix = self.myPMap.getPrefixValue(prevNote.strPitch).suffix if self.myPMap.getPrefixValue(prevNote.strPitch).suffix is not None else ""


                # Time to set sizes: if the currLryc was not a rest, the set the current subnote's length to it's preutterance
                if currLyric is not None and self.checkOto(currLyric, myPrefix, mySuffix) is not None:
                    prevNote.subNotes[index].length = str(int(float(self.checkOto(currLyric, myPrefix, mySuffix).preutterance)))

                # otherwise if the currLyric is a rest:
                elif currLyric is None and self.isRest(currNote.lyric) and currNote.state != "noNext":

                    # if the current rest is large enough (>1920), increase prevNote's last note by a fixed amount and
                    # adjust the tempLen's of currNote and PrevNote to the new values
                    if int(currNote.length) > (960 * 2):
                        prevNote.subNotes[index].length = "990"
                        currNote.tempLen = str(int(currNote.length) - int(prevNote.subNotes[index].length) + 30)
                        prevNote.tempLen = str(int(prevNote.tempLen) + int(prevNote.subNotes[index].length) - 30)

                    # otherwise add about half of the rest to prevNote.
                    else:
                        prevNote.subNotes[index].length = str(30 + ((int(currNote.length) - sum) // 2)) if int(currNote.length) > 60 or len(currNote.subNotes) == 1  else "30"
                        currNote.tempLen = str(int(currNote.length) - int(prevNote.subNotes[index].length) + 30)
                        prevNote.tempLen = str(int(prevNote.tempLen) + int(prevNote.subNotes[index].length) - 30)

                # otherwise just give a default length of 60
                else:
                    prevNote.subNotes[index].length = "60" if int(prevNote.subNotes[index].length) > 120 else "30"

                sum += int(prevNote.subNotes[index].length)
                index -= 1


            errState = 1

            # once the initial sizes have been calculated besides the first subNote in prevNote, if we have one more note but no room to fit it,
            # divide the notes equally within the length
            if sum >= int(prevNote.tempLen) and len(prevNote.subNotes) > 1 and self.notRest(prevNote.subNotes[0].lyric, prevNote.state):
                sum = 0

                # loop through each subnote and give it an equal amount of space.
                for myNote in prevNote.subNotes:
                    myNote.length = str(int(prevNote.tempLen) // len(prevNote.subNotes))
                    sum += int(myNote.length)

                # add any extra space to the first note.

                if int(prevNote.subNotes[0].length) + (int(prevNote.tempLen) - sum) > 0:
                    prevNote.subNotes[0].length = str(int(prevNote.subNotes[0].length) + (int(prevNote.tempLen) - sum))

            # otherwise if we have at least one more note and there's room, add it with the remaining space
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
            if self.fullLen:
                # if the final subnote is valid, not a V C, and is not a cc beginning, try to adjust it's length
                if self.notRest(prevNote.lyric, prevNote.state) and self.notRest(currNote.lyric, currNote.state) and len(prevNote.lyric) > 1 and ' ' not in prevNote.subNotes[-1].lyric and (self.checkOto(prevNote.subNotes[-1].lyric, myPrefix, mySuffix) is not None and prevNote.subNotes[-1].state != "ccbeginning"):
                        # fullLen is equal to the length of the area within the consonant block beyond the preutterance line.
                        fullLen = int(float(self.checkOto(prevNote.subNotes[-1].lyric, myPrefix, mySuffix).consonant)) - int(float(self.checkOto(prevNote.subNotes[-1].lyric, myPrefix, mySuffix).preutterance))

                        # if that area doubled is still less than the CV's length, then add the fullLen length to the last note and subtract it from the first
                        if fullLen * 2 <= int(prevNote.subNotes[0].length):
                            prevNote.subNotes[0].length = str(int(prevNote.subNotes[0].length) - fullLen)
                            prevNote.subNotes[-1].length = str(int(prevNote.subNotes[-1].length) + fullLen)

                        # otherwise if the first subnote's length is less than fullLen but the last subnote's length + 60
                        # and doubled is less than the first subnote's length, then take 60 length from the first note and give it to the note.
                        elif int(prevNote.subNotes[0].length) < fullLen and (int(prevNote.subNotes[-1].length) + 60) * 2 <= int(prevNote.subNotes[0].length):
                            prevNote.subNotes[0].length = str(int(prevNote.subNotes[0].length) - 60)
                            prevNote.subNotes[-1].length = str(int(prevNote.subNotes[-1].length) + 60)

            errState = 3

            # any CCbeginning notes have their pitches set to their parent lyric's pitch
            if currNote.subNotes[0].lyric[0] == "_" and len(prevNote.subNotes) > 1:
                prevNote.subNotes[-1].pitch = currNote.subNotes[0].pitch

            # if the current note is next, adjust it's length if need be.
            if currNote.state == "next" or currNote.state == "restEnd":
                currNote.subNotes[0].setProperty("Length", currNote.tempLen, True)

            if currNote.state == "noNext":
                prevNote.subNotes = [currNote.subNotes[0]]
                self.myUst.notes.pop(-1)


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

    # determines if a note is a rest
    def isRest(self, inLyric, state=None):
        if inLyric == 'R' or inLyric == 'r' or (state == 'MIA'):
            return True
        return False

    # checks the oto's cache to see if we've looked up a word already, and if not, add's it before retrieving it.
    def checkOto(self, inLyric, prefix, suffix):
        # sees if the lyric info is in our cache; if not then try adding it
        if self.myOto.checkDict(inLyric, prefix, suffix) is None:
            self.myOto.setLyricInDict(inLyric, prefix, suffix)

        # retrieve whatever was in the cache
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

    # clears a MIA note; if it had any CCV notes at the end preserve them
    def clearNote(self, inNote):
        if len(inNote.subNotes) <= 1:
            inNote.subNotes.clear()
        else:
            tempNote = inNote.subNotes[1:]
            inNote.subNotes.clear()
            inNote.subNotes = tempNote

# missingNote: class to store data on notes that could not be found during parsing.
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



