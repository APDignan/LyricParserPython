from os import listdir
from os.path import isfile, join
import utauGen as ustGen
from ParserException import ParserException
# PREFIX.py: contains two classes (prefixMap and prefixMapItem) to store data from the prefix map.

# prefixMap: main encapsulation of the prefix.map data. Data is stored in a dictionary as a prefixMapItem (see below) that
# contains the prefix and suffix for each given note
class prefixMap:
    # init: tries to load the prefix map from the voicebank. If it finds one populate the pMap, otherwise set it to None
    def __init__(self, bankPath):
        self.__pMap = dict()
        if isfile(join(bankPath, "prefix.map")):
            self.__processMap(join(bankPath, "prefix.map"))
        else:
            # print("The voicebank you have selected either does not have a prefix map or has an incorrectly named one.")
            self.__blankMap()

    # processMap: given the prefix.map's path, populate the prefixMap with the data from each note
    def __processMap(self, mapPath):
        # tempStr stores a temporary string (note/prefix/suffix)
        tempStr = ""
        # tempList stores each line's data
        tempList = list()
        inMap = ""
        lineCount = 1

        # open the prefix map and loop through each line
        try:
            with open(mapPath, 'r') as inMap:
                for line in inMap:
                    # in the line, add characters to tempStr until you find a tab (break). Then, add the str to your tempList
                    # and continue. If we reach a tab while tempStr is empty, the prefix is missing, so set it to None.
                    for c in line:
                        if c != "\t":
                            tempStr += c
                        else:
                            if len(tempStr) > 0:
                                tempList.append(tempStr)
                                tempStr = ""
                            else:
                                tempList.append(None)
                    # get the suffix. If there was no suffix, add none to the list
                    if len(tempStr) > 0 and tempStr != '\n':
                        tempList.append(tempStr[:-1])
                    else:
                        tempList.append(None)

                    # set up the relation for the note in the prefixMap. If prefix or suffix are empty, set them to None.
                    self.__pMap[tempList[0]] = prefixMapItem(prefix = tempList[1], suffix = tempList[2])
                    # reset values
                    tempList = list()
                    tempStr = ""
                    lineCount+= 1

        except Exception as err:
            raise ParserException("ERROR: (Reading Prefix.map) Could not read line %i" %lineCount)
        finally:
            inMap.close()

    def __blankMap(self):
        for i in range(24, 107):
            currNote = ustGen.intToNote(i)
            self.__pMap[currNote] = prefixMapItem()

    # printPrefixMap: debugging, prints the prefix map for each note
    def printPrefixMap(self):
        for keys in self.__pMap:
            print("Key: %s Values: %s %s" %(keys, self.__pMap[keys].prefix, self.__pMap[keys].suffix))

    def printPrefixMapToFile(self, inFile):
        for keys in self.__pMap:
            inFile.write("Key: %s Values: %s %s\n" %(keys, self.__pMap[keys].prefix, self.__pMap[keys].suffix))

    # getPrefixValues: gets the prefix and suffix from the list with the given key. Returns a prefixMapItem
    def getPrefixValue(self, key):
        if key in self.__pMap:
            return self.__pMap[key]

        return prefixMapItem()

    # getRangePrefixVlaues: gets prefix values for all items between the start and end parameter. Order does not matter as
    # long as they are within C1 and B7.
    def getPrefixValuesOverRange(self, start, end):
        # convert start and end to the integer counterparts. Swap them if startValue is larger than endValue
        startValue = ustGen.noteToInt(start)
        endValue = ustGen.noteToInt(end)

        if startValue > endValue:
            startValue, endValue = endValue, startValue

        # set up a dictionary to return to the user
        tempDict = dict()

        # double check that the start and end points are both valid, then populate the tempDict with the values from pMap
        if startValue >= 24 and endValue <= 107:
            while startValue <= endValue:
                if ustGen.intToNote(startValue) in self.__pMap:
                    tempDict[ustGen.intToNote(startValue)] = self.__pMap[ustGen.intToNote(startValue)]
                startValue += 1
        else:
            print("Range Error: Tried to start at %s and end at %s" %(start, end))

        # return the dictionary
        return tempDict

    # generateNoteRange: Get's a list containing all of the notes within a given range inclusively.
    # Can be used for sorting prefix map.
    def generateNoteRange(self, start, end):
        startValue = ustGen.noteToInt(start)
        endValue = ustGen.noteToInt(end)

        if startValue > endValue:
            startValue, endValue = endValue, startValue

        tempList = list()

        if startValue >= 24 and endValue <= 107:
            while startValue <= endValue:
                tempList.append(ustGen.intToNote(startValue))
                startValue += 1
        else:
            print("Range Error: Tried to start at %s and end at %s" %(start, end))


#prefixMapItem: used to hold the prefix and suffix data within the prefixMap in a clean manner. Pretty much just two values.
class prefixMapItem:

    def __init__(self, prefix = None, suffix = None):
        self.__prefix = prefix
        self.__suffix = suffix

    @property
    def prefix(self):
        return self.__prefix
    @prefix.setter
    def prefix(self, inPrefix):
        self.__prefix = inPrefix

    @property
    def suffix(self):
        return self.__suffix
    @suffix.setter
    def suffix(self, inSuffix):
        self.__suffix = inSuffix
