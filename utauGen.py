
# utauGen.py: General functions that are useful for multiple files.

# noteToInt: converts a note (C4, E2, F#5) to their numeric counterpart for iteration. Can be called for w/e though
def noteToInt(note):
    myFile = open("utauGen.txt", "a")
    myFile.write("I have %s, the result is: " %note)
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # if the note is valid, return the numeric counterpart, otherwise return -1 for failure
    if note[:-1] in notes and int(note[-1:]) > 0 and int(note[-1:]) < 8:
        myFile.write("%i (success)\n" %(((notes.index(note[:-1])) + (int(note[-1:]) - 1) * 12) + 24))
        myFile.close()
        return ((notes.index(note[:-1])) + (int(note[-1:]) - 1) * 12) + 24
    else:
        myFile.write("-1 (failure)\n")
        myFile.close()
        return -1

# intToNote: converts an integer to their note counterpart.
def intToNote(inValue):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # if the int is valid, return the note counterpart, otherwise return -1 for failure
    inValue = inValue - 24
    if int(inValue) >= 0 and int(inValue) <= 95:
        return str(notes[inValue % len(notes)]) + str(((inValue // len(notes)) + 1))
    else:
        return -1



