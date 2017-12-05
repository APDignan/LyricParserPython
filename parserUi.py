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

    def loadDictionary(self):
        print("My parser is %s and my trie is %s" %(self.myParser, self.myParser.myTrie))
        with open("dictionary.txt") as myFile:
            for line in myFile:
                addWordToTrie(line, self.myParser.myTrie)
        myFile.close()

    def checkWord(self):
        inWord = self.ltxtDictionaryInput.text().lower()
        self.myDictionary.clear()

        if len(inWord) < 100 and inWord[-1] == "-" and inWord != "-":
            inWord = inWord[:-1]
            inserts = self.myParser.myTrie.getSubTrie(inWord)
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
        elif len(inWord) < 100 and self.myParser.myTrie.getWord(inWord) != "":
            # self.tblDictionary = QtWidgets.QTableWidget(self.tabDictionary)
            pronunciations = self.myParser.myTrie.getWord(inWord)
            print(str(pronunciations))
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


            #
            # inserts = [inWord, str(self.myParser.myTrie.getWord(inWord)[0]), str(len(self.myParser.myTrie.getWord(inWord)[0].split(":")))]
            # self.tblDictionary.setRowCount(size + 1)
            # count = 0
            # for insert in inserts:
            #     item = QtWidgets.QTableWidgetItem()
            #     item.setText(insert)
            #     self.tblDictionary.setItem(size, count, item)
            #     count += 1

    def parseUST(self):
        self.myParser.run()

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

    def updateParserTable(self):
        self.tblParserOutput.setRowCount(len(self.myParser.myUst.notes))
        count = 0
        groupCount = 0
        for note in self.myParser.myUst.notes:
            inserts = [str(count), note.lyric, note.parentLyric]
            for insert in inserts:
                item = QtWidgets.QTableWidgetItem()
                item.setText(insert)
                self.tblParserOutput.setItem(count, groupCount, item)
                groupCount += 1

            sylls = ""
            for subNote in note.subNotes:
                sylls = sylls + "," + subNote.lyric if sylls != "" else subNote.lyric

            #if note.lyric == "R" and len(note.subNotes) == 1:
            #    sylls = "R"

            item = QtWidgets.QTableWidgetItem()
            item.setText(sylls)
            self.tblParserOutput.setItem(count, 3, item)
            groupCount = 0
            count += 1

    def addWordsToDictionary(self):
        # self.testPrinting()
        rowCount = self.tblErrors.rowCount()
        for i in range(0, rowCount):
            inSyll = self.tblErrors.item(i, 2).text()
            print("Testing %s with length %i" %(inSyll, self.myParser.missingWords[i].numSylls))
            if len(inSyll) > 0 and len(inSyll.split(":")) == self.myParser.missingWords[i].numSylls:
                print("We're gonna add %s it to the dicitonary for %s" %(self.myParser.missingWords[i].lyric, inSyll))
                self.myParser.missingWords[i].fixedSylls = inSyll
                self.myParser.myTrie.insertWord(self.myParser.missingWords[i].lyric, [inSyll])
                self.tblErrors.removeRow(i)

        if self.tblErrors.rowCount() > 0:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                  "Errors (" + str(self.tblErrors.rowCount()) + ")")
        else:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                      "Errors")

    def addWordsToDictionaryAndUpdate(self):
        # self.testPrinting()
        rowCount = self.tblErrors.rowCount()
        delCount = 0
        for i in range(0, rowCount):
            inSyll = self.tblErrors.item(i - delCount, 2).text()
            if len(inSyll) > 0 and len(inSyll.split(":")) == self.myParser.missingWords[i].numSylls:
                self.myParser.missingWords[i].fixedSylls = inSyll.split(":") if len(inSyll.split(":")) > 1 else inSyll
                self.myParser.myTrie.insertWord(self.myParser.missingWords[i].lyric, [inSyll])
                self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                self.tblErrors.removeRow(i - delCount)
                delCount += 1
            elif len(inSyll) == 0:
                tempSylls = self.myParser.getSyllables(self.myParser.myTrie.getWord(self.myParser.missingWords[i].lyric), self.myParser.missingWords[i].numSylls)
                if tempSylls is not None:
                    self.myParser.missingWords[i].fixedSylls = tempSylls
                    self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                    self.tblErrors.removeRow(i - delCount)
                    delCount += 1

        if self.tblErrors.rowCount() > 0:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                  "Errors (" + str(self.tblErrors.rowCount()) + ")")
        else:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                      "Errors")

        self.updateParserTable()

    def updateDictionary(self):
        rowCount = self.tblDictionary.rowCount()

        for i in self.myDictionary:
            print("Word: %s Pronunciation: %s numSylls: %s" %(i.word, i.pronunciation, i.numSylls))

        for index in range(0, rowCount):
            item = self.tblDictionary.item(index, 1).text()
            if item != self.myDictionary[index].pronunciation:
                print("index = %i: %s did not equal %s's old pronunciation %s" %(index, item, self.myDictionary[index].word, self.myDictionary[index].pronunciation))
                inserts = item.split("|")
                if inserts[0] != self.myDictionary[index].pronunciation:
                    print("Updating %s with insert %s" %(self.myDictionary[index].word, inserts[0]))
                    self.myParser.myTrie.updateWord(self.myDictionary[index].word,
                                                    self.myDictionary[index].pronunciation, inserts[0])
                if len(inserts) > 1:
                    print("Adding to %s: %s" %(self.myDictionary[index].word, inserts[1:]))
                    self.myParser.myTrie.insertWord(self.myDictionary[index].word, inserts[1:])
            else:
                print("Nothing was changed for %s's pronunciation %s" %(self.myDictionary[index].word, self.myDictionary[index].pronunciation))

        self.checkWord()

    def handleParseButton(self):
        index = self.cmbLanguageSetting.currentIndex()

        if index == 0:
            self.parseUST()

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
                print("I got %s" %splitLine)
                self.myParser.myTrie.insertWord(splitLine[0], splitLine[1].split("|"))






    def testPrinting(self):
        rowCount = self.tblErrors.rowCount()
        colCount = self.tblErrors.columnCount()
        for i in range(0, rowCount):
            for j in range(0, colCount):
                print("At %i, %i I got %s" %(i, j, self.tblErrors.item(i, j).text()))

    def closeUST(self):
        self.myParser.finishPlugin()
        self.myParser.myTrie.printTrieToFile("dictionary.txt")
        window.close()

    def saveDictionary(self):
        self.myParser.myTrie.printTrieToFile("dictionary.txt")

    def closeWindow(self):
        self.myParser.myTrie.printTrieToFile("dictionary.txt")
        window.close()

class dictionaryDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

class myApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =  mainWindow()
        self.ui.setupUi(self)
        # self.ui.loadDictionary()
        #self.ui.parseUST()
        self.show()

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

def addWordToTrie(str, myTrie):
    "_word: syll"
    halfIndex = str.find(':')

    if halfIndex >= 0:
        word = str[1:halfIndex]
        syllables = str[halfIndex + 2:-1].split("|")
        myTrie.insertWord(word, syllables)

testApp = QApplication(sys.argv)
window = myApp()
window.show()
sys.exit(testApp.exec_())
