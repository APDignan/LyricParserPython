from os import listdir
from os.path import isfile, join
from ParserException import ParserException

# OTO.py: contains two classes (Oto and OtoLine) to help parse and manipulate oto data from a voicebank

# Oto: the main encapsulator for the data. Using the voicebank's path, it creates a list of OtoLines, which each contain
# a line from the oto with the data set to corresponding variables.
class Oto:
    # init
    def __init__(self, bankPath):
        # __otoList: contains the oto data. Each element is an OtoLine instance
        self.__otoList = list()
        self.__myDict = dict()

        # searches for oto.ini files. First checks any folders within the voicebank to see if there are any oto.ini files.
        # if it finds any, it accumulates a list of paths for each oto.ini file. It also adds the oto in the main folder.
        otoCount = 1
        errState = 0
        currOto = ""
        line = ""
        dir = ""
        try:
            dirs = [d for d in listdir(bankPath) if not isfile(join(bankPath, d))]
            otoDirs = list()
            for d in dirs:
                if isfile(join(join(bankPath, d), "oto.ini")):
                    otoDirs.append(join(join(bankPath, d), "oto.ini"))
            if isfile(join(bankPath, "oto.ini")):
                otoDirs.append(join(bankPath, "oto.ini"))

            errState = 1

            # for each oto.ini file it found, we build the otoList based on each line within the oto.
            for dir in otoDirs:
                with open(dir, "r") as currOto:
                    for line in currOto:
                        self.__otoList.append(OtoLine(line))
                        otoCount += 1
                currOto.close()

        except Exception as err:
            raise ParserException("ERROR: (Reading Oto.ini Files) Error when looking for Oto.ini at %s. Make sure all Oto.ini files are in your voicebank's folder" %dir) \
                if errState == 0 else ParserException("ERROR: (Importing Oto.ini) In Oto %s could not parse line %i:  %s" %(dir, otoCount, line))
        finally:
            currOto.close()


    # debugging function. Number of lines may be one less than what utau says (0 indexing?)
    def printOto(self):
        print("Here is my oto with %i lines" %len(self.__otoList))
        for line in self.__otoList:
            line.printTest()

    # sees if a certain alias exists within the oto (with an optional suffix). If so, return the otoLine it came from.
    def getOtoLine(self, alias, prefix=None, suffix=None):
        # get a temp alias based on whether a suffix was specified

        searchAlias = alias if prefix is None else (prefix + alias)
        searchAlias = searchAlias if suffix is None else (searchAlias + suffix)

        # look for the line. If you find it, return the otoLine instance.
        for line in self.__otoList:
            if line.alias == searchAlias:
                return line

        return None

    # sees if an otoline was stored in the cache. Return it, otherwise return None
    def checkDict(self, inLyric, prefix, suffix):
        if prefix + inLyric + suffix in self.__myDict:
            return self.__myDict[prefix + inLyric + suffix]

        return None

    # put an otoline in our cache on the given sound, prefix, and suffix.
    def setLyricInDict(self, inLyric, prefix, suffix):
        if prefix + inLyric + suffix not in self.__myDict:
            self.__myDict[prefix + inLyric + suffix] = self.getOtoLine(inLyric, prefix, suffix)

# otoLine: contains the information stored in a single line of oto. The data is then stored as private variables that
# can be accessed through property-defined getters and setters
class OtoLine:
    def __init__(self, inLine):
        # create a list containing the individual components of the oto line
        tempList = self.parseOtoLine(inLine)
        # verify that the oto has 7 parameters. If it does, set the data to the proper variable
        if len(tempList) == 7:
            self.__sourceWav = tempList[0]
            self.__alias = tempList[1]
            self.__offset = tempList[2]
            self.__consonant = tempList[3]
            self.__cutoff = tempList[4]
            self.__preutterance = tempList[5]
            self.__overlap = tempList[6]
        else:
            print("Error: Incorrect number of parameters for otoLine: %s. Expected 7, found %i" % (str(tempList), len(tempList)))

# Getter and Setter Section
    @property
    def sourceWav(self):
        return self.__sourceWav
    @sourceWav.setter
    def sourceWav(self, inSourceWav):
        self.__sourceWav = inSourceWav

    @property
    def alias(self):
        return self.__alias
    @alias.setter
    def alias(self, inAlias):
        self.__alias = inAlias

    @property
    def offset(self):
        return self.__offset
    @offset.setter
    def offset(self, inOffset):
        self.__offset = inOffset

    @property
    def consonant(self):
        return self.__consonant
    @consonant.setter
    def consonant(self, inConsonant):
        self.__consonant = inConsonant

    @property
    def cutoff(self):
        return self.__cutoff
    @cutoff.setter
    def cutoff(self, inCutoff):
        self.__cutoff = inCutoff

    @property
    def preutterance(self):
        return self.__preutterance
    @preutterance.setter
    def preutterance(self, inPreutterance):
        self.__preutterance = inPreutterance

    @property
    def overlap(self):
        return self.__overlap
    @overlap.setter
    def overlap(self, inOverlap):
        self.__overlap = inOverlap
# /Getter and Setter Section

    # parseOtoLine: given an oto line (inStr), splits the string into a list containing the important bits of information
    # sound.wav=alias,offset,cutoff,consonant,preutterance,overlap
    def parseOtoLine(self, inStr):
        tempList = []
        tempList.append(inStr[:inStr.find('=')])
        tempList = tempList + inStr[inStr.find('=')+1:-1].split(",")
        return tempList

    # debugging test: prints the otoLine in the normal oto format.
    def printTest(self):
        print(self.sourceWav + '=' + self.alias + "," + self.offset + "," + self.cutoff + "," + self.consonant + "," + self.preutterance + "," + self.overlap)


