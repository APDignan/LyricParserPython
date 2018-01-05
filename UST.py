import PREFIX as prefix
import OTO as oto
import utauGen
from ParserException import ParserException
# UST.py: Contains the main functionality for the UST. Separates the ust into 2 parts:
#           1. settings: contains general information about the voicebank.
#           2. notes: array of note objects that contain the information about each note.

class Ust:
    def __init__(self, ustPath = None):
        #saves the path to the temp ust
        self.__ustPath = ustPath
        #settings are saved in the settings dictionary (key = setting attribute). keys are stored in a list to preserve order
        self.__settings = dict()
        self.__settingsKeys = list()
        #note list; holds the notes within the ust
        self.__notes = list()
        #stores whether utau included a prev and/or next note
        self.__hasPrev = False
        self.__hasNext = False
        #saves the initial note number of the first non-prev note.
        self.__startValue = -1
        #inits the ust and above variables
        if ustPath is not None:
            self.__readUst(ustPath)

    # allows easy access to the voicebank's location
    @property
    def voiceDir(self):
       return self.__settings['VoiceDir']

    @property
    def ustPath(self):
        return self.__ustPath

    @property
    def notes(self):
        return self.__notes

    @property
    def hasPrev(self):
        return self.__hasPrev

    @property
    def hasNext(self):
        return self.__hasNext

    @property
    def settings(self):
        return self.__settings

    @property
    def settingKeys(self):
        return self.__settingsKeys

    @property
    def startValue(self):
        return self.__startValue
    @startValue.setter
    def startValue(self, inStart):
        self.__startValue = inStart

    #reads the ust passed it and parses all of the data
    def __readUst(self, ustPath):
        # stateFlag is used to determine what data to expect. readUst has the following states:
        #       1. version: Version tag + val; read the version info and go to settings
        #       2. settings: Found the settings tag, so read in the setting params and values until we find a "[#XXXX]"
        #       3. notes: Found a note, so begin reading in note data. Add a new note whenever we reach a "[#XXXX]" or finish

        stateFlag = 'version'
        lineCount = 1
        ustFile = ""
        # stores the current note data
        currNote = note()
        try:
            with open(self.__ustPath, "r") as ustFile:
                for line in ustFile:
                    # first line should be [#VERSION], so skip it and then store the version info. Then go to settings
                    if stateFlag == 'version' and line[:-1] != '[#VERSION]':
                        self.__settings['[#VERSION]'] = line[:-1]
                        stateFlag = 'settings'
                    # read in the settings info; ignore [#SETTING] and as long as we don't find another tag, add the setting
                    # to our settings dictionary and list (for maintaining order)
                    elif stateFlag == 'settings':
                        if line[0:2] != '[#':
                            self.__settingsKeys.append(line[:line.find('=')])
                            self.__settings[line[:line.find('=')]] = line[line.find('=') + 1 : -1]
                        # if we've found a new tag, signal the notes flag
                        elif line[:-1] != '[#SETTING]' and line[0:2] == '[#':
                            stateFlag = 'notes'
                            # if we're given a previous note, flag the ust and mark the next note as non-editable (see note)
                            if line[:-1] == '[#PREV]':
                                self.__hasPrev = True
                                currNote.canEdit = False
                                currNote.state = "prev"
                            # otherwise the note was the first note. Store its initial note number
                            else:
                                self.__startValue = getNoteNumber(line[:-1])
                    # read notes until we reach the end of the temp ust. read note params until we find a new note tag, which
                    # we then add the note to the note list and create a new one.
                    elif stateFlag == 'notes':
                        # store the note we've been making when we reach a new one. If we havnen't found the first true note,
                        # save its note number
                        if line[0:2] == '[#':
                            if self.__startValue == -1:
                                self.__startValue = getNoteNumber(line[:-1])

                            # add the note to the list and create a new note. If the note is the "next" note, flag it as non-editable
                            self.__notes.append(currNote)
                            currNote = note()
                            if line[:-1] == '[#NEXT]':
                                self.__hasNext = True
                                currNote.canEdit = False
                                currNote.state = "next"
                        # otherwise store the note data into the current note object. Set override to true to allow us to
                        # edit the prev/next notes
                        else:
                            currNote.setProperty(line[:line.find('=')], line[line.find('=')+1:-1], True)

                # if the ust had no notes, don't add the the final note.
                if currNote.length is not None:
                    self.__notes.append(currNote)
                lineCount+= 1

        except Exception as err:
            raise ParserException("ERROR: (Importing UST) UST could not be processed during state %s. See line %i in the UST." % (stateFlag, lineCount)) \
                if lineCount > 0 else ParserException("ERROR: (Finding UST) Could not open UST at %s" % self.__ustPath)
        finally:
            ustFile.close()
    # closeUst: given a file location, write the current ust file to it. You'll want to use the ustPath initially passed
    # into it to rewrite the current ust file.
    def closeUst(self, fileName):
        errState = 0
        noteCount = 1
        currNote = ""
        subNote = ""
        setting = ""
        try:
            outFile = open(fileName, 'w')
            checkPitches = open("pitches.txt", "w")

            # write the version and setting information using the settingsKey list for order
            outFile.write('[#VERSION]\n' + self.__settings['[#VERSION]'] + '\n' + '[#SETTING]\n')
            checkPitches.write('[#VERSION]\n' + self.__settings['[#VERSION]'] + '\n' + '[#SETTING]\n')
            errState = 1
            for setting in self.__settingsKeys:
                outFile.write(setting + '=' + self.__settings[setting] + '\n')
                checkPitches.write(setting + '=' + self.__settings[setting] + '\n')

            # get the index to label the notes as well as the list of parameters that had split data
            currentIndex = self.__startValue
            splitProperties = ['PBW', 'PBY', 'Envelope', '@alias', 'Flags']

            errState = 2
            # for each note, write either the note number or the prev/next tags if it was the prev/next note.

            for currNote in self.__notes:
                for subNote in currNote.subNotes:
                    if currNote.state == "prev" and self.__hasPrev:
                        outFile.write('[#PREV]\n')
                        checkPitches.write('[#PREV]\n')
                    elif currNote.state == "next" and self.__hasNext:
                        outFile.write('[#NEXT]\n')
                        checkPitches.write('[#NEXT]\n')
                    else:
                        outFile.write(convertNoteNumber(currentIndex) + '\n')
                        checkPitches.write(convertNoteNumber(currentIndex) + '\n')
                        currentIndex += 1

                    # for each parameter in the note, write the parameter. Any paramter in splitProperties has its properties
                    # reformatted for the ust
                    for property in subNote.getPropertiesKeys():
                        outFile.write(property + '=')
                        checkPitches.write(property + '=')
                        # if property in splitProperties:
                        #     currProperty = ""
                        #     for val in subNote.getProperty(property):
                        #         currProperty = (currProperty + val) if property == 'Flags' else (currProperty + val + ',')
                        #     outFile.write((currProperty + '\n') if property == 'Flags' else (currProperty[:-1] + '\n'))
                        #     checkPitches.write("For lyric %s and property %s I got %s\n" %(subNote.lyric, property, subNote.getProperty(property)))
                        # else:
                        outFile.write(subNote.getProperty(property) + '\n')
                        checkPitches.write(subNote.getProperty(property) + '\n')
                    noteCount += 1

            checkPitches.close()

        except Exception as err:
            if errState == 0:
                raise ParserException("ERROR: (Writing UST|Open File/Version) Either could not open \"dictionary.txt\" or could not write Version line.")
            elif errState == 1:
                raise ParserException("ERROR: (Writing UST|Settings) Could not write setting %s = %s." %(setting, str(self.__settings[setting])))
            elif errState == 2:
                raise ParserException("ERROR: (Writing UST|Notes) Could not write note %i# %s from %s." %(noteCount, subNote.lyric, currNote.lyric))
        finally:
            outFile.close()



    # testing function: changes all lyrics in the selected notes to newLyric
    def changeAllLyrics(self, newLyric):
        for n in self.__notes:
            n.setProperty("Lyric", newLyric)

    # inserts a note into the ust. Trying to insert before or on a prev/next note will place it within the bounds of the ust
    def insertNote(self, inNote, index = -1):
        # if you don't specifiy where to insert the note or try to insert it at or behind the next note, place it at the end.
        if index == -1 or index == len(self.__notes) - 1 or index == len(self.__notes):
            if self.__hasNext:
                self.__notes.insert(len(self.__notes) - 1, inNote)
            else:
                self.__notes.append(inNote)
        elif index == 0:
            if self.__hasPrev:
                self.__notes.insert(1, inNote)
            else:
                self.__notes.insert(0, inNote)
        elif index > 0 and index < len(self.__notes):
                self.__notes.insert(index, inNote)

        if self.__startValue == -1:
            self.__startValue = 0 if (len(self.__notes) > 0 and not self.__hasPrev) else 1


    # DO NOT TRUST, EVIL
    def deleteNote(self, index):
        if (index == 0 and self.__notes[0].state != "prev") or (index == len(self.__notes) - 1 and self.__notes[-1].state != "next") or (index > 0 and index < len(self.__notes)):
            self.__notes.remove(self.__notes[index])

    # get the note at the index inIndex within the ust; includes prev if unless specified
    def getNoteIndex(self, inIndex, usePrev = False):
        return (inIndex + self.__startValue + 1) if (self.__hasPrev and usePrev == True) else inIndex + self.__startValue

    # gets the ust's Length discounting prev and next notes. If you want total size use len(Ust.size)
    def getUstLength(self):
        size = len(self.__notes)
        if self.__hasPrev:
            size -= 1

        return size - 1 if self.__hasNext else size

    # replace either a given note exNote or a note at index with inNote.
    def replaceNote(self, inNote, index = -1, exNote = None):
        if index == -1 and exNote == None:
            print("ERROR: No parameters passed")
        elif index == -1 and exNote in self.__notes:
            self.__notes[self.__notes.index(exNote)] = inNote
        elif exNote == None and index > -1 and index < len(self.notes):
            self.__notes[index] = inNote

    # determines if the ust has a setting inSetting
    def hasSetting(self, inSetting):
        return True if inSetting in self.__settingsKeys else False

    # gets the setting value related to inSetting if it exists.
    def getSetting(self, inSetting):
        return self.__settings[inSetting] if inSetting in self.__settings else None

    # sets a setting given an inValue
    def setSetting(self, inSetting, inValue):
        if inSetting not in self.__settingsKeys:
            self.__settingsKeys.append(inSetting)

        self.__settings[inSetting] = inValue

    # copy's the contents of another ust file to the current one. Useful for intermediate editing. By default copys all
    # notes but passing a parameter will only copy the prev and next notes if they exist
    def copyUst(self, inUst, copyNotes = True):
        self.__settings = inUst.settings
        self.__settingsKeys = inUst.settingKeys
        self.__ustPath = inUst.ustPath
        self.__hasNext = inUst.hasNext
        self.__hasPrev = inUst.hasPrev
        self.__startValue = inUst.startValue

        if copyNotes == True:
            self.__notes = inUst.notes
        else:
            if self.__hasPrev:
                self.__notes.append(inUst.notes[0])

            if self.__hasNext:
                self.__notes.append(inUst.notes[-1])





# note: contains the data of a single note from the ust. All properties and values are stored in a dictionary, and the
# property keys are stored in a list to maintain the order they were read from. canEdit flags a note as prev/next,
# preventing them from being edited by setProperty() by default.
class note:
    # by default just creates an empty note, but passing default = True will create a note with predetermined values.
    # One can define some of these values using the proper parameters.
    def __init__(self, default = False, length = "480", lyric = 'a', pitch = "60"):
        self.__properties = dict()
        self.__propertiesKeys = list()
        self.__syllables = list()
        self.__subNotes = list()
        self.__tempLen = 0
        self.__canEdit = True
        # used to define a note as prev/next, but besides that can be used for anything else.
        self.__state = "note"
        self.__parentLyric = ""
        self.__startConst = ""
        self.__vowel = ""
        self.__endConst = ""

        # sets default properties
        if default == True:
            genericProperties = {'Length': length, 'Lyric': lyric, 'NoteNum': pitch, 'Intensity': "100",
                                 'Modulation': "0", "PBS" : "0", "PBW" : "0", "PBY": "0", "VBR": "0"}

            for property in genericProperties:
                self.setProperty(property, genericProperties[property])


    # getProperty: returns the value of a specified property (inProperty). Otherwise returns None
    def getProperty(self, inProperty):
        if inProperty in self.__properties:
            return self.__properties[inProperty]

        return None

    # setProperty: given a property inProperty, set the value to val. If a note is flagged to not be edited via canEdit,
    # passing the override parameter will allow the program to edit it.
    def setProperty(self, inProperty, val, override = None):

        # # parameters that I've found stores a list of values. May be subjet to change
        # splitOnComma = ['PBW', 'PBY', 'PBS', 'VBR', 'Envelope', '@alias']

        # only edits the note if an override value was passed or if the note was not flagged
        if override is not None or self.canEdit:

            # adds the param to the note if it wasn't added already.
            if inProperty not in self.__propertiesKeys:
                self.__propertiesKeys.append(inProperty)

            self.__properties[inProperty] = val

            # # if the param splits on commas, split it.
            # if inProperty in splitOnComma:
            #     self.__properties[inProperty] = val.split(',')
            # # if we take in the Flags param, separate the flags whenever a number preceeds a letter
            # elif inProperty == 'Flags':
            #     tempStr = ''
            #     self.__properties[inProperty] = list()
            #     for c in val:
            #         if len(tempStr) > 0 and tempStr[-1].isdigit() and c.isalpha():
            #             self.__properties[inProperty].append(tempStr)
            #             tempStr = c
            #         else:
            #             tempStr += c
            #     self.__properties[inProperty].append(tempStr)
            # otherwise we have a normal property that we can just add to the dictionary
            # else:


    # sets a property without splitting anything. Used for copying data from one note to another.
    def setPropertyLazy(self, inProperty, val, override = None):
        if override is not None or self.canEdit:
            if inProperty not in self.__propertiesKeys:
                self.__propertiesKeys.append(inProperty)

            self.__properties[inProperty] = val

    #Getters and setters. Use the get/setProperty methods to get/set specific properties (just to make things easier)
    @property
    def length(self):
        return self.getProperty("Length")
    @length.setter
    def length(self, inLength):
        self.setProperty("Length", inLength)

    @property
    def lyric(self):
        return self.getProperty("Lyric")
    @lyric.setter
    def lyric(self, inLyric):
        self.setProperty("Lyric", inLyric)

    # pitch can be retrieved either as their numeric value or the note/octave pair. Any param for flag will get the
    # latter, while no param will get the former.
    @property
    def pitch(self):
        return self.getProperty("NoteNum")
    # pitch setter that can take in either a string or an int. Stores the pitch as an int.
    @pitch.setter
    def pitch(self, inNote):
        if inNote[0].isdigit():
            self.setProperty("NoteNum", str(inNote))
        else:
            self.setProperty("NoteNum", str(utauGen.noteToInt(inNote)))

    @property
    def strPitch(self):
        return utauGen.intToNote(int(self.getProperty("NoteNum")))

    @property
    def intensity(self):
        return self.getProperty("Intensity")
    @intensity.setter
    def intensity(self, inIntensity):
        self.setProperty("Intensity", inIntensity)

    @property
    def modulation(self):
        return self.getProperty("Modulation")
    @modulation.setter
    def modulation(self, inModulation):
        self.setProperty("Modulation", inModulation)

    @property
    def canEdit(self):
        return self.__canEdit
    @canEdit.setter
    def canEdit(self, inEdit):
        self.__canEdit = inEdit

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, inState):
        self.__state = inState

    @property
    def syllables(self):
        return self.__syllables
    @syllables.setter
    def syllables(self, inSyllable):
        self.__syllables = inSyllable

    @property
    def subNotes(self):
        return self.__subNotes
    @subNotes.setter
    def subNotes(self, inNotes):
        for tempNote in inNotes:
            self.__subNotes.append(tempNote)

    @property
    def tempLen(self):
        return self.__tempLen
    @tempLen.setter
    def tempLen(self, inLen):
        self.__tempLen = inLen

    @property
    def parentLyric(self):
        return self.__parentLyric
    @parentLyric.setter
    def parentLyric(self, inLyric):
        self.__parentLyric = inLyric

    @property
    def startConst(self):
        return self.__startConst
    @startConst.setter
    def startConst(self, inStartConst):
        self.__startConst = inStartConst

    @property
    def vowel(self):
        return self.__vowel
    @vowel.setter
    def vowel(self, inVowel):
        self.__vowel = inVowel

    @property
    def endConst(self):
        return self.__endConst
    @endConst.setter
    def endConst(self, inEndConst):
        self.__endConst = inEndConst

    # gets the last vowel for a subNote.
    @property
    def lastVowel(self):
        return self.vowel if self.endConst == "" else ""

    # gets the vowel at the beginning of a note
    @property
    def VBeginning(self):

        return self.vowel if self.startConst == "" else ""

    # # split a lyric on it's vowel and returns the split lyric
    # @property
    # def splitLyric(self):
    #     oneCharVowels = ['a', 'e', 'i', 'o', 'u', 'E', '9', '3', '@', 'A', 'I', 'O', '8', 'Q', '6', 'x', '&']
    #     twoCharVowels = ['9l', '0l', '8n', '0r']
    #     threeCharVowels = ['1ng', 'Ang']
    #
    #     myList = list()
    #
    #     if self.lyric[0:1] in oneCharVowels:
    #         myList = [self.lyric[0:1], self.lyric[1:]]
    #     elif len(self.lyric) > 1 and self.lyric[0:2] in twoCharVowels:
    #         myList = [self.lyric[0:2], self.lyric[2:]]
    #     elif len(self.lyric) > 2 and self.lyric[0:3] in threeCharVowels:
    #         myList = [self.lyric[0:3], self.lyric[3:]]
    #
    #     return myList

    # returns the propertiesKeys for iteration
    def getPropertiesKeys(self):
        return self.__propertiesKeys

    def printNote(self):
        for property in self.__propertiesKeys:
            print(property + "=" + str(self.__properties[property]))


# converts a note tag to an int. ex: [#0123] => 123
def getNoteNumber(inNum):
    if inNum == '[#0000]':
        return 0

    tempNum = inNum[2:-1]
    while tempNum[0] == 0:
        tempNum = tempNum[1:]

    return int(tempNum)

# converts an int to a note number tag. ex: 123 => [#0123]
def convertNoteNumber(inNum):
    if inNum < 0 or inNum > 9999:
        return None
    return '[#' + ('0' * (4 - len(str(inNum)))) + str(inNum) + ']'


# copies the content of one note to another. does NOT copy state or canEdit properties.
def copyNote(inNote, lyric=None, location=""):
    newNote = note()

    for property in inNote.getPropertiesKeys():
        newNote.setPropertyLazy(property, inNote.getProperty(property))

    if lyric is not None:
        newNote.lyric = lyric


    if "PBS" not in inNote.getPropertiesKeys():
        newNote.setPropertyLazy("PBS", "0")

    if "PBY" not in inNote.getPropertiesKeys():
        newNote.setPropertyLazy("PBY", "0")

    if "PBW" not in inNote.getPropertiesKeys():
        newNote.setPropertyLazy("PBW", "0")

    if "VBR" not in inNote.getPropertiesKeys():
        newNote.setPropertyLazy("VBR", "0")

    # newNote.setProperty("PBS", "0")
    # newNote.setProperty("PBY", "0")
    # newNote.setProperty("PBW", "0")

    return newNote







