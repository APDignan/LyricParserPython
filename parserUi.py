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

# dialog box for accepting input for the dictionary
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

# dialog box for the settings options
class Ui_dlogSettings(object):
    def setupUi(self, dlogSettings):
        dlogSettings.setObjectName("dlogSettings")
        dlogSettings.resize(435, 224)

        self.buttonBox = QtWidgets.QDialogButtonBox(dlogSettings)
        self.buttonBox.setGeometry(QtCore.QRect(60, 180, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.ckbxFullLen = QtWidgets.QCheckBox(dlogSettings)
        self.ckbxFullLen.setGeometry(QtCore.QRect(30, 20, 335, 20))
        self.ckbxFullLen.setObjectName("ckbxFullLen")

        self.ckbxBlendVowels = QtWidgets.QCheckBox(dlogSettings)
        self.ckbxBlendVowels.setGeometry(QtCore.QRect(30, 50, 311, 20))
        self.ckbxBlendVowels.setObjectName("ckbxBlendVowels")

        self.ckbxBlendEngVowels = QtWidgets.QCheckBox(dlogSettings)
        self.ckbxBlendEngVowels.setGeometry(QtCore.QRect(30, 80, 311, 20))
        self.ckbxBlendEngVowels.setObjectName("ckbxBlendVowels")

        self.ltxtStartSymbol = QtWidgets.QLineEdit(dlogSettings)
        self.ltxtStartSymbol.setGeometry(QtCore.QRect(30, 110, 61, 22))
        self.ltxtStartSymbol.setText("")
        self.ltxtStartSymbol.setObjectName("ltxtStartSymbol")

        self.lblStartSymbol = QtWidgets.QLabel(dlogSettings)
        self.lblStartSymbol.setGeometry((QtCore.QRect(110,110,74,16)))

        self.ltxtEndSymbol = QtWidgets.QLineEdit(dlogSettings)
        self.ltxtEndSymbol.setGeometry(QtCore.QRect(30, 140, 61, 22))
        self.ltxtEndSymbol.setText("")
        self.ltxtEndSymbol.setObjectName("ltxtEndSymbol")

        self.lblEndSymbol = QtWidgets.QLabel(dlogSettings)
        self.lblEndSymbol.setGeometry((QtCore.QRect(110, 140, 81, 16)))

        self.btnSaveSettings = QtWidgets.QPushButton(dlogSettings)
        self.btnSaveSettings.setGeometry(QtCore.QRect(30, 180, 93, 28))
        self.btnSaveSettings.setObjectName("btnSaveSettings")
        self.btnSaveSettings.clicked.connect(self.saveSettings)

        self.retranslateUi(dlogSettings)

        self.buttonBox.accepted.connect(dlogSettings.accept)
        self.buttonBox.rejected.connect(dlogSettings.reject)

        QtCore.QMetaObject.connectSlotsByName(dlogSettings)

    def retranslateUi(self, dlogSettings):
        _translate = QtCore.QCoreApplication.translate
        dlogSettings.setWindowTitle(_translate("dlogSettings", "Settings"))
        self.ckbxFullLen.setText(_translate("dlogSettings", "Extend VC endings based on the oto's Consonant field"))
        self.ckbxBlendVowels.setText(_translate("dlogSettings", "Blend Vowels using the previous note's VC Ending"))
        self.ckbxBlendEngVowels.setText(_translate("dlogSettings", "(English) Blend Vowels missing VV transitions"))
        self.lblStartSymbol.setText(_translate("dlogSettings", "Start Symbol"))
        self.lblEndSymbol.setText(_translate("dlogSettings", "End Symbol"))
        self.btnSaveSettings.setText(_translate("dlogSettings", "Save Settings"))

    # saveSettings: saves the currently selected settings by writing to the settings.txt file
    def saveSettings(self):

        tempList = list()
        settingsList = list()

        # gets the original settings to maintain order
        with open("settings.txt", "r") as settingsFile:
            for line in settingsFile:
                tempList.append(line)
        settingsFile.close()

        # loops through each setting that was set and writes them to the file
        with open("settings.txt", "w") as settingsFile:
            for item in tempList:
                if "fulllen" in item:
                    settingsFile.write("fulllen=true\n") if self.ckbxFullLen.isChecked() else settingsFile.write(
                        "fulllen=false\n")
                    settingsList.append("fulllen")
                elif "blendvowels" in item:
                    settingsFile.write(
                        "blendvowels=true\n") if self.ckbxBlendVowels.isChecked() else settingsFile.write(
                        "blendvowels=false\n")
                    settingsList.append("blendvowels")
                elif "blendengvowels" in item:
                    settingsFile.write(
                        "blendengvowels=true\n") if self.ckbxBlendEngVowels.isChecked() else settingsFile.write(
                        "blendengvowels=false\n")
                    settingsList.append("blendengvowels")
                elif "startSymbol" in item:
                    settingsFile.write("startSymbol=" + self.ltxtStartSymbol.text() + "\n")
                    settingsList.append("startSymbol")
                elif "endSymbol" in item:
                    settingsFile.write("endSymbol=" + self.ltxtEndSymbol.text() + "\n")
                    settingsList.append("endSymbol")
                elif len(item) > 2:
                    settingsFile.write(item)

            if "fulllen" not in settingsList:
                settingsFile.write("fulllen=true\n") if self.ckbxFullLen.isChecked() else settingsFile.write(
                    "fulllen=false\n")
            if "blendvowels" not in settingsList:
                settingsFile.write(
                    "blendvowels=true\n") if self.ckbxBlendVowels.isChecked() else settingsFile.write(
                    "blendvowels=false\n")
            if "blendengvowels" not in settingsList:
                settingsFile.write(
                    "blendengvowels=true\n") if self.ckbxBlendEngVowels.isChecked() else settingsFile.write(
                    "blendengvowels=false\n")
            if "startSymbol" not in settingsList:
                settingsFile.write("startSymbol=" + self.ltxtStartSymbol.text() + "\n")
            if "endSymbol" not in settingsList:
                settingsFile.write("endSymbol=" + self.ltxtEndSymbol.text() + "\n")




        settingsFile.close()

# the main window of the UI
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
        self.btnParse.setGeometry(QtCore.QRect(480, 532, 93, 28))
        self.btnParse.setObjectName("btnParse")
        self.btnParse.clicked.connect(self.handleParseButton)

        self.cmbLanguage = QtWidgets.QComboBox(self.tabMain)
        self.cmbLanguage.setGeometry(QtCore.QRect(90, 535, 171, 22))
        self.cmbLanguage.setObjectName("cmbLanguage")
        self.cmbLanguage.addItem("")
        self.cmbLanguage.currentIndexChanged.connect(self.parseUST)
        self.cmbLanguageSetting = QtWidgets.QComboBox(self.tabMain)
        self.cmbLanguageSetting.setGeometry(QtCore.QRect(280, 535, 171, 22))
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
        self.ltxtDictionaryInput.returnPressed.connect(self.checkWord)

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

        # self.menuHelp = QtWidgets.QMenu(self.menubar)
        # self.menuHelp.setObjectName("menuHelp")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.triggered.connect(self.closeWindow)

        self.mnuSaveDictionary = QtWidgets.QAction(MainWindow)
        self.mnuSaveDictionary.setObjectName("mnuSaveDictionary")
        self.mnuSaveDictionary.triggered.connect(self.saveDictionary)

        self.mnuSetDefaultDictionary = QtWidgets.QAction(MainWindow)
        self.mnuSetDefaultDictionary.setObjectName("MnuSetDefaultDictionary")
        self.mnuSetDefaultDictionary.triggered.connect(self.setDefaultDictionary)

        self.mnuSettings = QtWidgets.QAction(MainWindow)
        self.mnuSettings.setObjectName("mnuSettings")
        self.mnuSettings.triggered.connect(self.openSettingsDialog)

        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.mnuSettings)
        self.menuFile.addAction(self.mnuSaveDictionary)
        self.menuFile.addAction(self.mnuSetDefaultDictionary)

        self.menubar.addAction(self.menuFile.menuAction())
        # self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # sets text and stuff, mostly pre-generated
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

        self.cmbLanguage.setItemText(0, _translate("MainWindow", "(Select Language)"))
        self.cmbLanguageSetting.setItemText(0, _translate("MainWindow", "VCCV"))
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
        # self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSettings.setText(_translate("MainWindow", "Close"))
        self.mnuSaveDictionary.setText(_translate("MainWindow", "Save Dictionary"))
        self.mnuSetDefaultDictionary.setText(_translate("MainWindow", "Set Current Dictionary As Default"))
        self.mnuSettings.setText(_translate("MainWindow", "Settings"))

    # used on init. Converts lyrics to the psuedo VCCV syntax and puts them in the UST. Any errors are triggered here.
    def parseUST(self):
        # go through each note and try to find the lyric in the dictionary
        self.myParser.selectedTrie = self.myParser.trieList[self.cmbLanguage.currentIndex() - 1] if self.cmbLanguage.currentIndex() > 0 else ""


        if self.cmbLanguage.currentIndex() > 0:
            self.myParser.missingWords.clear()
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
            else:
                self.tblErrors.setRowCount(0)
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError), "Errors")

            self.updateParserTable()
            self.myParser.isParsed = False

        # store the current parsing of the ust to check for updates
        self.originalParse.clear()
        for i in range(0, self.tblParserOutput.rowCount()):
            self.originalParse.append(self.tblParserOutput.item(i, 2).text())

    # used for the "Parse" button on the parser tab. Final parsing for the UST.
    def handleParseButton(self):
        index = self.cmbLanguageSetting.currentIndex()

        if index == 0:
            # updates the Ust with any changes the user made on the Parser page
            self.btnParse.setEnabled(False)
            try:

                self.updateUst()
                # formats the notes into the VCCV format
                if self.myParser.isParsed:
                    for i in range (1, len(self.myParser.myUst.notes)):
                        self.myParser.getSizes(self.myParser.myUst.notes[i-1], self.myParser.myUst.notes[i])

                    # change subnotes to whatever's there and update sizes
                else:
                    self.formatVCCVNotes()
                    self.myParser.isParsed = True
            except Exception as err:
                raise err
            finally:
                self.btnParse.setEnabled(True)

    # updates the UST based on whatever the user changed on the parser tab. Changes to syllables replaces the note's syllables
    # while changing the lyric updates the lyric.
    def updateUst(self):

        canParse = -1
        # loop through all of the notes besides the perv and next notes
        for i in range(1, self.tblParserOutput.rowCount()):

            # canParse used to prevent reformatting multi-syllable notes, so ignore them and the last "next" note.
            if i >= canParse and self.myParser.myUst.notes[i].state != "next":
                # get the user's word, syllables, and the note's original syllables
                inWord = self.tblParserOutput.item(i, 2).text().lower()
                inSyllables = self.tblParserOutput.item(i, 3).text()
                tempSyll = ""

                for note in self.myParser.myUst.notes[i].subNotes:
                    tempSyll = tempSyll + note.lyric + ","

                # if the syllables do not equal the original syllables, replace them
                if inSyllables != tempSyll[:-1]:
                    self.myParser.myUst.notes[i].subNotes.clear()
                    self.myParser.createVCCVNotes(self.myParser.myUst.notes[i], inSyllables, update=True)

                # otherwise if the word does not match the original lyric, reparse the note.
                elif i < len(self.originalParse) and inWord != self.originalParse[i].lower() and \
                                self.myParser.myUst.notes[i].state != 'extended' and \
                                self.myParser.myUst.notes[i].state != "noNext":
                    index = i
                    numSylls = 0
                    totalLen = 0
                    finalLyric = ""
                    endLoop = True

                    # loop through the notes until you reach the end or find a non-rest lyric that doesn't end with "-".
                    # any non-rest lyrics have their lyrics added to the finalLyric and are counted for # syllables
                    while index < self.tblParserOutput.rowCount()and endLoop:
                        currLyric = self.tblParserOutput.item(index, 2).text()
                        if len(currLyric) > 0:
                            if currLyric != "-" and currLyric.lower() != 'r':
                                numSylls += 1
                                finalLyric = finalLyric + currLyric[:-1] if currLyric[
                                                                                -1] == "-" else finalLyric + currLyric
                                if currLyric[-1] != "-" and currLyric.lower() != 'r':
                                    endLoop = False

                            index += 1
                            totalLen += 1

                    finalLyric = finalLyric.lower()

                    # create a missingNote object to format the information for fixing the notes
                    myMissingNote = missingNote(inLyric=finalLyric, inNumSylls=numSylls,
                                                inStartNote=index - totalLen, inRange=totalLen)

                    # if the finalLyric is an actual word and we were able to find a valid pronunciation, parse it
                    if finalLyric != "" and self.myParser.getSyllables(
                            self.myParser.myTrie.getWord(finalLyric), numSylls) is not None:
                        myMissingNote.fixedSylls = self.myParser.getSyllables(
                            self.myParser.myTrie.getWord(finalLyric), numSylls)
                        self.myParser.parseFixedVCCV(myMissingNote, fullClear=True)
                    # otherwise treat it like a mixxing word
                    else:
                        self.myParser.missingWords.append(myMissingNote)

                    # prevent editing notes until we reach the end of the current lyric
                    canParse = index

        self.updateParserTable()

    # formats the notes for the parser
    def formatVCCVNotes(self):
        # print("Formatting VCCV notes")
        for i in range(1, len(self.myParser.myUst.notes)):
            if i == len(self.myParser.myUst.notes) - 1 and self.myParser.myUst.hasNext == False and self.myParser.myUst.notes[-1].state != "MIA" and self.myParser.isRest(self.myParser.myUst.notes[-1].lyric):
                self.myParser.myUst.notes[-1].state = "restEnd"
            self.myParser.formatNotes(self.myParser.myUst.notes[i - 1], self.myParser.myUst.notes[i])

        # if we have the last note in the entire ust, update the final note and add an extra note as an ending note
        if self.myParser.myUst.hasNext == False and self.myParser.myUst.notes[-1].state != "MIA" and not self.myParser.isRest(self.myParser.myUst.notes[-1].lyric):
            self.myParser.formatNotes(self.myParser.myUst.notes[-1], None)

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

    # used by search button on the dictionary page. Checks if the word given is in the dictionary, and puts any syllables
    # in the grid. If the word ends with "-" looks up any words that start with the substring.
    def checkWord(self):
        inWord = self.ltxtDictionaryInput.text().lower()

        self.myDictionary.clear()

        # if the word ends with a "-", look up all of the words that start with the substring and put them on the grid
        if len(inWord) > 0 and len(inWord) < 100 and inWord[-1] == "-" and inWord != "-":
            inWord = inWord[:-1]
            inserts = self.myParser.myTrie.getSubTrie(inWord)

            # loop through each word and insert them into the grid
            if inserts is not None and len(inserts) > 2:
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

            else:
                self.tblDictionary.setRowCount(0)

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

    # used by the updateDictionary button on the Errors page. Adds whatever fixes the user made into the dictionary if they're valid
    def addWordsToDictionary(self):
        rowCount = self.tblErrors.rowCount()
        delCount = 0

        # for each row check if the user tried to fix the word If they did and the word fits, put it in the dictionary
        for i in range(0, rowCount):
            inSyll = self.tblErrors.item(i - delCount, 2).text()
            if len(inSyll) > 0 and len(inSyll.split(":")) == self.myParser.missingWords[i].numSylls:
                self.myParser.missingWords[i].fixedSylls = inSyll
                self.myParser.myTrie.insertWord(self.myParser.missingWords[i].lyric, [inSyll])
                self.tblErrors.removeRow(i - delCount)
                delCount += 1

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
        tempMissingWords = list()

        # loop through each row in the errors page. If the user tried to fix a word then insert it into the dictionary
        # and fix whatever note triggered the error
        for i in range(0, rowCount):
            inSyll = self.tblErrors.item(i - delCount, 2).text()
            oldDelCount = delCount

            # if the syllables included equals the number of the missing syllables, update the UST, add the word to the dictionary
            # and remove the word from the error tab
            if len(inSyll) > 0 and len(inSyll.split(":")) == self.myParser.missingWords[i].numSylls:
                self.myParser.missingWords[i].fixedSylls = inSyll.split(":") if len(inSyll.split(":")) > 1 else inSyll
                self.myParser.myTrie.insertWord(self.myParser.missingWords[i].lyric, [inSyll])
                self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                self.tblErrors.removeRow(i - delCount)
                delCount += 1

            # if no fix was made, then see if the word was added either through the dictionary or an earlier note in the
            # function. If so update the note based on what's in the dictionary.
            elif len(inSyll) == 0:
                if self.myParser.missingWords[i].lyric == "-" and self.myParser.myUst.notes[self.myParser.missingWords[i].lastNote].state != 'MIA':
                    self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                    self.tblErrors.removeRow(i - delCount)
                    self.myParser.myUst.notes[self.myParser.missingWords[i].lastNote].state = 'extended'
                    delCount += 1
                else:
                    tempSylls = self.myParser.getSyllables(self.myParser.myTrie.getWord(self.myParser.missingWords[i].lyric), self.myParser.missingWords[i].numSylls)
                    if tempSylls is not None:
                        self.myParser.missingWords[i].fixedSylls = tempSylls
                        self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                        self.tblErrors.removeRow(i - delCount)
                        delCount += 1

            # if we didn't delete anything, keep the missing word
            if delCount == oldDelCount:
                tempMissingWords.append(self.myParser.missingWords[i])

        # update the Error tab text with the number of errors
        if self.tblErrors.rowCount() > 0:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                  "Errors (" + str(self.tblErrors.rowCount()) + ")")
        else:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                      "Errors")

        # update the parser grid based
        self.myParser.missingWords.clear()
        for missingWord in tempMissingWords:
            self.myParser.missingWords = missingWord

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


    # opens the settings dialog, showing the current selections and then saving any changes
    def openSettingsDialog(self):
        mySettings = settingsDialog()
        if self.myParser.fullLen == True:
            mySettings.ckbxFullLen.setChecked(True)

        if self.myParser.blendVowels == True:
            mySettings.ckbxBlendVowels.setChecked(True)

        if self.myParser.ENG_VVBlend == True:
            mySettings.ckbxBlendEngVowels.setChecked(True)

        mySettings.ltxtStartSymbol.setText(self.myParser.startSymbol)
        mySettings.ltxtEndSymbol.setText(self.myParser.endSymbol)

        mySettings.exec_()

        if mySettings.result() == 1:
            if mySettings.ckbxFullLen.isChecked():
                self.myParser.fullLen = True
            else:
                self.myParser.fullLen = False

            if mySettings.ckbxBlendVowels.isChecked():
                self.myParser.blendVowels = True
            else:
                self.myParser.blendVowels = False

            if mySettings.ckbxBlendEngVowels.isChecked():
                self.myParser.ENG_VVBlend = True
            else:
                self.myParser.ENG_VVBlend = False

            self.myParser.startSymbol = mySettings.ltxtStartSymbol.text()
            self.myParser.endSymbol = mySettings.ltxtEndSymbol.text()

    # dialog used to import any words for the dictionary
    def openDicitonaryDialog(self):
        myDialog = dictionaryDialog()
        myDialog.exec_()

        # if the dialog returned "OK", add any words found to the dictionary
        if myDialog.result() == 1:
            txt = myDialog.plainTextEdit.toPlainText()
            dictionaryList = list()
            currWord = ""

            # loop through each line in the textbox
            for line in txt.split("\n"):

                # add line formatted as "_word: def1|def2|..."
                if len(line) > 0 and line[0] == "_":
                    line = line + "\n"
                    currWord = line[1:].split(" ")
                    currWord = currWord[0][:-1]
                    self.myParser.addWordToTrie(line)

                # add line formatted as "word def1|def2|... or word: def1|def2|..."
                elif len(line) > 0:
                    splitLine = line.split(" ")
                    if splitLine[0][-1] == ":":
                        splitLine[0] = splitLine[0][:-1]

                    self.myParser.myTrie.insertWord(splitLine[0], splitLine[1].split("|"))
                    currWord = splitLine[0]

                # add the words added to the dictionary list to add to the dictionary table
                syllList = line.split(" ")
                if len(syllList) > 1:
                    syllList = syllList[1].split("|")
                    for syll in syllList:
                        dictionaryList.append(currWord)
                        dictionaryList.append(syll.split("\n")[0])
                        dictionaryList.append(str(len(syll.split(":"))))

            self.myDictionary.clear()

            # if we added at least one word, update the dictionary table with the words added
            if len(dictionaryList) > 2:
                self.tblDictionary.setRowCount(len(dictionaryList) / 3)
                count = 0
                groupCount = 0
                tempDictionaryList = list()

                # loop through each item in our list and add them to the table
                for insert in dictionaryList:
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(insert)
                    self.tblDictionary.setItem(count, groupCount, item)
                    tempDictionaryList.append(insert)
                    groupCount += 1

                    if groupCount > 2:
                        self.myDictionary.append(dictionaryItem(tempDictionaryList[0], tempDictionaryList[1], tempDictionaryList[2]))
                        tempDictionaryList.clear()
                        groupCount = 0
                        count += 1

    # saves the current dictionary to the dictionary file
    def saveDictionary(self):
        if self.myParser.selectedTrie in self.myParser.trieList:
            self.myParser.myTrie.printTrieToFile()

    def setDefaultDictionary(self):

        tempList = list()

        with open("settings.txt", "r") as settingsFile:
            for line in settingsFile:
                tempList.append(line)
        settingsFile.close()

        with open("settings.txt", "w") as settingsFile:
            for item in tempList:
                if "defaultdictionary" not in item:
                    settingsFile.write(item)

            if self.cmbLanguage.currentIndex() > 0:
                settingsFile.write("defaultdictionary " + self.myParser.trieList[
                    self.cmbLanguage.currentIndex() - 1] + "\n")

        settingsFile.close()

    # testing function, ignore
    def testPrinting(self):
        rowCount = self.tblErrors.rowCount()
        colCount = self.tblErrors.columnCount()
        for i in range(0, rowCount):
            for j in range(0, colCount):
                print("At %i, %i I got %s" %(i, j, self.tblErrors.item(i, j).text()))

    # on finishing the UST, overwrite the UST and dictionary files.
    def closeUST(self):
        self.myParser.finishPlugin()
        for trie in self.myParser.getTrieStruct:
            self.myParser.getTrieStruct[trie].printTrieToFile()

        window.close()

    # on closing the window just save the dictionary
    def closeWindow(self):
        window.close()

# dialog used to import user data
class dictionaryDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

class settingsDialog(QDialog, Ui_dlogSettings):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

# main app; parses the ust and initializes all of the tables
class myApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =  mainWindow()
        self.ui.setupUi(self)

        for item in self.ui.myParser.trieList:
            self.ui.cmbLanguage.addItem(item)

            if item == self.ui.myParser.selectedTrie:
                self.ui.cmbLanguage.setCurrentIndex(self.ui.cmbLanguage.findText(item, QtCore.Qt.MatchFixedString))

        # self.ui.parseUST()
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
if __name__ == "__main__":
    testApp = QApplication(sys.argv)
    window = myApp()
    window.show()
    sys.exit(testApp.exec_())
