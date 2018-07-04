

# has 3 main parts:
#   1. creates a list of dictionaries, each containing the note data.
#   2. compares notes with the one that follows, and if a "-" should be added create a new note using a dictionary and
#      add it to the insertList
#   3. write the notes to the ust file, giving priority to any note in the insertList list whose index equals the current note
def ustReadTest():
    # list of dictionaries that contains the note data
    noteList = list()
    # list of dictionaries that represent notes that we'll add back into the ust
    insertList = list()
    # storage dictionary for reading in notes
    tempDict = None
    # outfile
    outFile = open("outust.ust", "w")

    # loop through the ust file
    with open(sys.argv[1], "r") as ustFile:
        for line in ustFile:
            paramList = ""

            # if the line is a note, create a dictionary and set the value of "index" to it's tag "[#XXXXX]
            if "[#" in line and line != "[#VERSION]" and line != "[#SETTINGS]":
                # if we'd started a note already, add the parameter list to it and add it to the noteList list
                if tempDict is not None:
                    tempDict["params"] = paramList
                    noteList.append(tempDict)
                tempDict = dict()
                tempDict["index"] = line[:-1]
            # we're within the current note, so add the parameter to the dictionary. Add it to a param list str to maintain order
            elif tempDict is not None and "[#" not in line:
                paramList = line.split("=")[0] if paramList == "" else paramList + "," + line.split("=")[0]
                tempDict[line.split("=")[0]] = line.split("=")[1][:-1]
            # otherwise we've found one of the tags before the note that we don't care about, so just write them to the file
            else:
                outFile.write(line[:-1])

    index = 0
    # Here we see where we need to add notes. Loop from the first note to the second to last note
    while index > len(noteList) - 2:
        # get the lyrics from the the note index points to and the next note
        currLyric = noteList[index]["lyric"]
        nextLyric = noteList[index +1]["lyric"]
        # if the current lyric is not a rest and the next note is a rest, create a "-" note
        # could make it so that it only creates a note if the rest is big enough to have a "-"
        if len(currLyric) > 0 and not isRest(currLyric) and isRest(nextLyric):
            # add an empty dictionary to the insertlist list
            insertList.append(dict())
            # use the "index" key as an identifier to know where the note should go
            insertList[-1]["index"] = noteList[index + 1]["index"]
            # add the rest of the notable parameters
            insertList[-1]["lyric"] = "-"
            insertList[-1]["pitch"] = noteList[index + 1]["pitch"]
            # adjust the size of the next note and the inserted note so that there's no change in the length of the ust
            # this can be whatever size you want, just doing half for example
            tempLen = int(noteList[index + 1]["length"])
            insertList[-1]["length"] = str(tempLen / 2)
            noteList[index+1]["length"] = str(tempLen - int(insertList[-1]["length"]))

    index = 0
    # finally, write the ust. the pre-note info was written before, so we just need to write out the notes
    while index < len(noteList):
        outNote = noteList[index]
        # whenever we find a note in the insertNote list, use that instead of the next note in noteList
        # we only move on once there aren't any notes left in insertList or if the next insertList note's index
        # does not equal the current note's index
        if len(insertList) > 0 and noteList[index]["index"] == insertList[0]["index"]:
            outFile.write("[#INSERT]")
            outNote = insertList.pop(0)
        else:
            outFile.write(outNote["index"] + "\n")
            index += 1

        # get the parameter list and write them to the ust in order
        paramList = outNote["params"].split(",")
        for param in paramList:
            outFile.write(param + "=" + outNote[param] + "\n")


    outFile.close()

def isRest(lyric):
    return (lyric == "R" or lyric == "r")