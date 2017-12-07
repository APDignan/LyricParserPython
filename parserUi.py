# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parserUi.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QHeaderView
import main
from main import parser, missingNote

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 20, 331, 191))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))



class mainWindow(object):
    def setupUi(self, MainWindow):
        self.myParser = parser()
        self.myDictionary = list()
        self.originalParse = list()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(870, 687)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 871, 601))
        self.tabWidget.setObjectName("tabWidget")
        self.tabMain = QtWidgets.QWidget()
        self.tabMain.setObjectName("tabMain")
        self.tblParserOutput = QtWidgets.QTableWidget(self.tabMain)
        self.tblParserOutput.setGeometry(QtCore.QRect(30, 30, 790, 491))
        self.tblParserOutput.setObjectName("tblParserOutput")
        self.tblParserOutput.setColumnCount(4)
        self.tblParserOutput.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblParserOutput.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblParserOutput.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblParserOutput.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblParserOutput.setHorizontalHeaderItem(3, item)
        self.tblParserOutput.horizontalHeader().setDefaultSectionSize(197)
        self.tblParserOutput.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.btnParse = QtWidgets.QPushButton(self.tabMain)
        self.btnParse.setGeometry(QtCore.QRect(470, 532, 93, 28))
        self.btnParse.setObjectName("btnParse")
        self.btnParse.clicked.connect(self.handleParseButton)
        self.cmbLanguageSetting = QtWidgets.QComboBox(self.tabMain)
        self.cmbLanguageSetting.setGeometry(QtCore.QRect(240, 535, 171, 22))
        self.cmbLanguageSetting.setObjectName("cmbLanguageSetting")
        self.cmbLanguageSetting.addItem("")
        self.tabWidget.addTab(self.tabMain, "")
        self.tabError = QtWidgets.QWidget()
        self.tabError.setObjectName("tabError")
        self.btnUpdateDictionary = QtWidgets.QPushButton(self.tabError)
        self.btnUpdateDictionary.setGeometry(QtCore.QRect(200, 510, 111, 28))
        self.btnUpdateDictionary.setObjectName("btnUpdateDictionary")
        self.btnUpdateDictionary.clicked.connect(self.addWordsToDictionary)
        self.tblErrors = QtWidgets.QTableWidget(self.tabError)
        self.tblErrors.setGeometry(QtCore.QRect(40, 40, 771, 431))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblErrors.sizePolicy().hasHeightForWidth())
        self.tblErrors.setSizePolicy(sizePolicy)
        self.tblErrors.setStatusTip("")
        self.tblErrors.setDragDropOverwriteMode(True)
        self.tblErrors.setObjectName("tblErrors")
        self.tblErrors.setColumnCount(3)
        self.tblErrors.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblErrors.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblErrors.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblErrors.setHorizontalHeaderItem(2, item)
        self.tblErrors.horizontalHeader().setDefaultSectionSize(220)
        self.tblErrors.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.btnUpdateDictionaryAndParse = QtWidgets.QPushButton(self.tabError)
        self.btnUpdateDictionaryAndParse.setGeometry(QtCore.QRect(500, 510, 191, 28))
        self.btnUpdateDictionaryAndParse.setObjectName("btnUpdateDictionaryAndParse")
        self.btnUpdateDictionaryAndParse.clicked.connect(self.addWordsToDictionaryAndUpdate)
        self.tabWidget.addTab(self.tabError, "")
        self.tabDictionary = QtWidgets.QWidget()
        self.tabDictionary.setObjectName("tabDictionary")
        self.btnDictionarySearch = QtWidgets.QPushButton(self.tabDictionary)
        self.btnDictionarySearch.setGeometry(QtCore.QRect(470, 500, 93, 28))
        self.btnDictionarySearch.setObjectName("btnDictionarySearch")
        self.btnDictionarySearch.clicked.connect(self.checkWord)
        self.tblDictionary = QtWidgets.QTableWidget(self.tabDictionary)
        self.tblDictionary.setGeometry(QtCore.QRect(40, 20, 771, 431))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblDictionary.sizePolicy().hasHeightForWidth())
        self.tblDictionary.setSizePolicy(sizePolicy)
        self.tblDictionary.setStatusTip("")
        self.tblDictionary.setDragDropOverwriteMode(True)
        self.tblDictionary.setObjectName("tblDictionary")
        self.tblDictionary.setColumnCount(3)
        self.tblDictionary.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblDictionary.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblDictionary.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblDictionary.setHorizontalHeaderItem(2, item)
        self.tblDictionary.horizontalHeader().setDefaultSectionSize(257)
        self.tblDictionary.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.btnDictionaryAdd = QtWidgets.QPushButton(self.tabDictionary)
        self.btnDictionaryAdd.setGeometry(QtCore.QRect(720, 500, 93, 28))
        self.btnDictionaryAdd.setObjectName("btnDictionaryAdd")
        self.btnDictionaryAdd.clicked.connect(self.openDicitonaryDialog)
        self.ltxtDictionaryInput = QtWidgets.QLineEdit(self.tabDictionary)
        self.ltxtDictionaryInput.setGeometry(QtCore.QRect(80, 500, 341, 22))
        self.ltxtDictionaryInput.setText("")
        self.ltxtDictionaryInput.setObjectName("ltxtDictionaryInput")
        self.btnDictionaryUpdate = QtWidgets.QPushButton(self.tabDictionary)
        self.btnDictionaryUpdate.setGeometry(QtCore.QRect(595, 500, 93, 28))
        self.btnDictionaryUpdate.setObjectName("btnDictionaryUpdate")
        self.btnDictionaryUpdate.clicked.connect(self.updateDictionary)
        self.tabWidget.addTab(self.tabDictionary, "")
        self.btnConfirm = QtWidgets.QPushButton(self.centralwidget)
        self.btnConfirm.setGeometry(QtCore.QRect(200, 605, 93, 28))
        self.btnConfirm.setObjectName("btnConfirm")
        self.btnConfirm.clicked.connect(self.closeUST)
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setGeometry(QtCore.QRect(580, 605, 93, 28))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.clicked.connect(self.closeWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 870, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.mnuSaveDictionary = QtWidgets.QAction(MainWindow)
        self.mnuSaveDictionary.setObjectName("mnuSaveDictionary")
        self.mnuSaveDictionary.triggered.connect(self.saveDictionary)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.mnuSaveDictionary)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LyricParser"))
        item = self.tblParserOutput.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NoteNum"))
        item = self.tblParserOutput.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Lyric"))
        item = self.tblParserOutput.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Word Found"))
        item = self.tblParserOutput.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Syllable"))
        self.btnParse.setText(_translate("MainWindow", "Parse UST"))
        self.cmbLanguageSetting.setItemText(0, _translate("MainWindow", "English VCCV"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("MainWindow", "Parser"))
        self.btnUpdateDictionary.setText(_translate("MainWindow", "Update Dictionary"))
        item = self.tblErrors.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Word"))
        item = self.tblErrors.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Length"))
        item = self.tblErrors.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Syllables"))
        self.btnUpdateDictionaryAndParse.setText(_translate("MainWindow", "Update Dictionary and Parse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError), _translate("MainWindow", "Errors"))
        self.btnDictionarySearch.setText(_translate("MainWindow", "Search"))
        item = self.tblDictionary.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Word"))
        item = self.tblDictionary.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Syllables"))
        item = self.tblDictionary.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Length"))
        self.btnDictionaryAdd.setText(_translate("MainWindow", "Add Word(s)"))
        self.btnDictionaryUpdate.setText(_translate("MainWindow", "Update"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDictionary), _translate("MainWindow", "Dictionary"))
        self.btnConfirm.setText(_translate("MainWindow", "Confirm"))
        self.btnCancel.setText(_translate("MainWindow", "Cancel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSettings.setText(_translate("MainWindow", "Close"))
        self.mnuSaveDictionary.setText(_translate("MainWindow", "Save Dictionary"))

    # loads the dictionary file into the parser
    def loadDictionary(self):
        with open("dictionary.txt") as myFile:
            for line in myFile:
                self.myParser.addWordToTrie(line)
        myFile.close()

    # used by search button on the dictionary page. Checks if the word given is in the dictionary, and puts any syllables
    # in the grid. If the word ends with "-" looks up any words that start with the substring.
    def checkWord(self):
        inWord = self.ltxtDictionaryInput.text().lower()
        self.myDictionary.clear()

        # if the word ends with a "-", look up all of the words that start with the substring and put them on the grid
        if len(inWord) < 100 and inWord[-1] == "-" and inWord != "-":
            inWord = inWord[:-1]
            inserts = self.myParser.myTrie.getSubTrie(inWord)
            # loop through each word and insert them into the grid
            if len(inserts) > 2:
                self.tblDictionary.setRowCount(len(inserts) / 3)
                count = 0
                groupCount = 0
                tempDictionaryItem = list()
                for insert in inserts:
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(insert)
                    self.tblDictionary.setItem(count, groupCount, item)
                    tempDictionaryItem.append(insert)

                    # insert the data into the grid once we've found each part of the row
                    groupCount += 1
                    if groupCount > 2:
                        self.myDictionary.append(dictionaryItem(tempDictionaryItem[0], tempDictionaryItem[1], tempDictionaryItem[2]))
                        tempDictionaryItem = list()
                        groupCount = 0
                        count += 1
        # if the word exists put it in the dictionary table
        elif len(inWord) < 100 and self.myParser.myTrie.getWord(inWord) != "":
            pronunciations = self.myParser.myTrie.getWord(inWord)
            inserts = list()
            for i in pronunciations:
                inserts.append(inWord)
                inserts.append(i)
                inserts.append(str(len(i.split(":"))))
            if len(inserts) > 2:
                self.tblDictionary.setRowCount(len(inserts) / 3)
                count = 0
                groupCount = 0
                tempDictionaryItem = list()
                for insert in inserts:
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(insert)
                    self.tblDictionary.setItem(count, groupCount, item)
                    tempDictionaryItem.append(insert)
                    groupCount += 1
                    if groupCount > 2:
                        self.myDictionary.append(dictionaryItem(tempDictionaryItem[0], tempDictionaryItem[1], tempDictionaryItem[2]))
                        tempDictionaryItem = list()
                        groupCount = 0
                        count += 1
        else:
            self.tblDictionary.setRowCount(0)

    # used on init. Converts lyrics to the psuedo VCCV syntax and puts them in the UST. Any errors are triggered here.
    def parseUST(self):
        # go through each note and try to find the lyric in the dictionary
        self.myParser.run()

        # any missing words are stored in parser.missingWords. Add all missing words to the Error tab and mark the number of errors
        if len(self.myParser.missingWords) > 0:
            self.tblErrors.setRowCount(len(self.myParser.missingWords))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError), "Errors (" + str(len(self.myParser.missingWords)) + ")")
            count = 0
            for missing in self.myParser.missingWords:
                missingList = missing.listData()
                for i in range (0, 3):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(missingList[i])
                    self.tblErrors.setItem(count, i, item)
                count += 1

        self.updateParserTable()

    # updates the parser grid based on the current state of the UST
    def updateParserTable(self):
        self.tblParserOutput.setRowCount(len(self.myParser.myUst.notes))
        count = 0
        groupCount = 0
        # loop through each note in the UST
        for note in self.myParser.myUst.notes:
            inserts = [str(count), note.lyric, note.parentLyric]

            # add the index, the lyric, and the lyric found in the grid
            for insert in inserts:
                item = QtWidgets.QTableWidgetItem()
                item.setText(insert)
                self.tblParserOutput.setItem(count, groupCount, item)
                groupCount += 1

            # concatenate the syllables to the psuedo VCCV format
            sylls = ""
            for subNote in note.subNotes:
                sylls = sylls + "," + subNote.lyric if sylls != "" else subNote.lyric

            # add the row into the group
            item = QtWidgets.QTableWidgetItem()
            item.setText(sylls)
            self.tblParserOutput.setItem(count, 3, item)
            groupCount = 0
            count += 1

    # used by the updateDictionary button on the Errors page. Adds whatever fixes the user made into the dictionary if they're valid
    def addWordsToDictionary(self):
        rowCount = self.tblErrors.rowCount()
        # for each row check if the user tried to fix the word If they did and the word fits, put it in the dictionary
        for i in range(0, rowCount):
            inSyll = self.tblErrors.item(i, 2).text()
            if len(inSyll) > 0 and len(inSyll.split(":")) == self.myParser.missingWords[i].numSylls:
                self.myParser.missingWords[i].fixedSylls = inSyll
                self.myParser.myTrie.insertWord(self.myParser.missingWords[i].lyric, [inSyll])
                self.tblErrors.removeRow(i)

        # update the Errors tab with the current number of errors
        if self.tblErrors.rowCount() > 0:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                  "Errors (" + str(self.tblErrors.rowCount()) + ")")
        else:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                      "Errors")

    # used by the "Update Dictionary and Parse" button on the Errors tab. In addition to adding the word into the dictionary,
    # update the UST wherever the missing word originated.
    def addWordsToDictionaryAndUpdate(self):
        rowCount = self.tblErrors.rowCount()
        delCount = 0

        # loop through each row in the errors page. If the user tried to fix a word then insert it into the dictionary
        # and fix whatever note triggered the error
        for i in range(0, rowCount):
            inSyll = self.tblErrors.item(i - delCount, 2).text()
            if len(inSyll) > 0 and len(inSyll.split(":")) == self.myParser.missingWords[i].numSylls:
                self.myParser.missingWords[i].fixedSylls = inSyll.split(":") if len(inSyll.split(":")) > 1 else inSyll
                self.myParser.myTrie.insertWord(self.myParser.missingWords[i].lyric, [inSyll])
                self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                self.tblErrors.removeRow(i - delCount)
                delCount += 1
            # if no fix was made, then see if the word was added either through the dictionary or an earlier note in the
            # function. If so update the note based on what's in the dictionary.
            elif len(inSyll) == 0:
                tempSylls = self.myParser.getSyllables(self.myParser.myTrie.getWord(self.myParser.missingWords[i].lyric), self.myParser.missingWords[i].numSylls)
                if tempSylls is not None:
                    self.myParser.missingWords[i].fixedSylls = tempSylls
                    self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                    self.tblErrors.removeRow(i - delCount)
                    delCount += 1

        # update the Error tab text with the number of errors
        if self.tblErrors.rowCount() > 0:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                  "Errors (" + str(self.tblErrors.rowCount()) + ")")
        else:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                      "Errors")

        # update the parser grid based
        self.updateParserTable()

    # used to update any words in the dictionary that had their pronunciation changed
    def updateDictionary(self):
        rowCount = self.tblDictionary.rowCount()

        # loops through each row. If the row doesn't equal the original, try to parse the input
        for index in range(0, rowCount):
            item = self.tblDictionary.item(index, 1).text()
            # split the input on "|" to split any multiple definitions
            if item != self.myDictionary[index].pronunciation:
                inserts = item.split("|")
                # if the insert at 0 doesn't equal the previous pronunciation then replace it
                if inserts[0] != self.myDictionary[index].pronunciation:
                    self.myParser.myTrie.updateWord(self.myDictionary[index].word,
                                                    self.myDictionary[index].pronunciation, inserts[0])
                # add any additional pronunciations to the dictionary
                if len(inserts) > 1:
                    self.myParser.myTrie.insertWord(self.myDictionary[index].word, inserts[1:])

        self.checkWord()

    # used for the "Parse" button on the parser tab. Final parsing for the UST.
    def handleParseButton(self):
        index = self.cmbLanguageSetting.currentIndex()

        if index == 0:
            # updates the Ust with any changes the user made on the Parser page
            self.updateUst()
            # formats the notes into the VCCV format
            self.formatVCCVNotes()
            self.myParser.isParsed = True

    # updates the UST based on whatever the user changed on the parser tab. Changes to syllables replaces the note's syllables
    # while changing the lyric updates the lyric.
    def updateUst(self):

        canParse = -1
        # loop through all of the notes besides the perv and next notes
        for i in range(1, self.tblParserOutput.rowCount()):
            # canParse used to prevent reformatting multi-syllable notes, so ignore them and the last "next" note.
            if i >= canParse and self.myParser.myUst.notes[i].state != "next":

                # get the user's word, syllables, and the note's original syllables
                inWord = self.tblParserOutput.item(i, 2).text()
                inSyllables = self.tblParserOutput.item(i, 3).text()
                tempSyll = ""
                for note in self.myParser.myUst.notes[i].subNotes:
                    tempSyll = tempSyll + note.lyric + ","

                # if the syllables do not equal the original syllables, replace them
                if inSyllables != tempSyll[:-1]:
                    self.myParser.myUst.notes[i].subNotes.clear()
                    self.myParser.createVCCVNotes(self.myParser.myUst.notes[i], inSyllables)
                # otherwise if the word does not match the original lyric, reparse the note.
                elif inWord != self.originalParse[i]:
                    index = i
                    numSylls = 0
                    totalLen = 0
                    finalLyric = ""
                    endLoop = True
                    # loop through the notes until you reach the end or find a non-rest lyric that doesn't end with "-".
                    # any non-rest lyrics have their lyrics added to the finalLyric and are counted for # syllables
                    while index < self.tblParserOutput.rowCount() - 1 and endLoop:
                        currLyric = self.tblParserOutput.item(index, 2).text()
                        if len(currLyric) > 0:
                            if currLyric != "-" and currLyric.lower() != 'r':
                                numSylls += 1
                                finalLyric = finalLyric + currLyric[:-1] if currLyric[-1] == "-" else finalLyric + currLyric
                                if currLyric[-1] != "-" and currLyric.lower() != 'r':
                                    endLoop = False

                            index += 1
                            totalLen += 1

                    # create a missingNote object to format the information for fixing the notes
                    myMissingNote = missingNote(inLyric = finalLyric, inNumSylls= numSylls, inStartNote=index - totalLen, inRange= totalLen)

                    # if the finalLyric is an actual word and we were able to find a valid pronunciation, parse it
                    if finalLyric != "" and self.myParser.getSyllables(
                            self.myParser.myTrie.getWord(finalLyric), numSylls) is not None:
                        myMissingNote.fixedSylls = self.myParser.getSyllables(self.myParser.myTrie.getWord(finalLyric), numSylls)
                        self.myParser.parseFixedVCCV(myMissingNote, fullClear=True)
                    # otherwise treat it like a mixxing word
                    else:
                        self.myParser.missingWords.append(myMissingNote)

                    # prevent editing notes until we reach the end of the current lyric
                    canParse = index


    # dialog used to import any words for the dictionary
    def openDicitonaryDialog(self):
        myDialog = dictionaryDialog()
        myDialog.exec_()
        txt = myDialog.plainTextEdit.toPlainText()
        for line in txt.split("\n"):
            if len(line) > 0 and line[0] == "_":
                line = line + "\n"
                self.myParser.addWordToTrie(line)
            elif len(line) > 0:
                splitLine = line.split(" ")
                self.myParser.myTrie.insertWord(splitLine[0], splitLine[1].split("|"))

    # formats the nots for the parser
    def formatVCCVNotes(self):
        for i in range(1, len(self.myParser.myUst.notes)):
            self.myParser.formatNotes(self.myParser.myUst.notes[i-1], self.myParser.myUst.notes[i])

        self.updateParserTable()

    # testing function, ignore
    def testPrinting(self):
        rowCount = self.tblErrors.rowCount()
        colCount = self.tblErrors.columnCount()
        for i in range(0, rowCount):
            for j in range(0, colCount):
                print("At %i, %i I got %s" %(i, j, self.tblErrors.item(i, j).text()))

    # on finishing the UST, overrite the UST and dictionary files.
    def closeUST(self):
        self.myParser.finishPlugin()
        self.myParser.myTrie.printTrieToFile("dictionary.txt")
        window.close()

    # saves the current dictionary to the dictionary file
    def saveDictionary(self):
        self.myParser.myTrie.printTrieToFile("dictionary.txt")

    # on closing the window just save the dictionary
    def closeWindow(self):
        self.saveDictionary()
        window.close()

# dialog used to import user data
class dictionaryDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

# main app; parses the ust and initializes all of the tables
class myApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =  mainWindow()
        self.ui.setupUi(self)
        # self.ui.loadDictionary()
        self.ui.parseUST()
        for i in range(0, self.ui.tblParserOutput.rowCount()):
            self.ui.originalParse.append(self.ui.tblParserOutput.item(i, 2).text())
        self.show()

# used to store the data regarding the initial data stored in the dictionary
class dictionaryItem():
    def __init__(self, inWord = None, inPronunciation = None, inNumSylls = 0):
        self.__word = inWord
        self.__pronunciation = inPronunciation
        self.__numSylls = inNumSylls

    @property
    def word(self):
        return self.__word
    @word.setter
    def word(self, inWord):
        self.__word = inWord

    @property
    def pronunciation(self):
        return self.__pronunciation
    @pronunciation.setter
    def pronunciation(self, inPronunciation):
        self.__pronunciation = inPronunciation

    @property
    def numSylls(self):
        return self.__numSylls
    @numSylls.setter
    def numSylls(self, inNumSylls):
        self.__numSylls = inNumSylls


# opens app
testApp = QApplication(sys.argv)
window = myApp()
window.show()
sys.exit(testApp.exec_())
