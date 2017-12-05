# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parserUi.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView
import main
from main import parser, missingNote

class mainWindow(object):
    def setupUi(self, MainWindow):
        self.myParser = parser()
        self.myDictionary = list()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(869, 687)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 871, 601))
        self.tabWidget.setObjectName("tabWidget")
        self.tabMain = QtWidgets.QWidget()
        self.tabMain.setObjectName("tabMain")
        self.tableWidget = QtWidgets.QTableWidget(self.tabMain)
        self.tableWidget.setGeometry(QtCore.QRect(30, 30, 790, 491))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(197)
        self.tabWidget.addTab(self.tabMain, "")
        self.tabError = QtWidgets.QWidget()
        self.tabError.setObjectName("tabError")
        self.btnUpdateErrors = QtWidgets.QPushButton(self.tabError)
        self.btnUpdateErrors.setGeometry(QtCore.QRect(200, 510, 111, 28))
        self.btnUpdateErrors.setObjectName("pushButton")
        self.btnUpdateErrors.clicked.connect(self.addWordsToDictionary)
        self.tblMissingWords = QtWidgets.QTableWidget(self.tabError)
        self.tblMissingWords.setGeometry(QtCore.QRect(40, 40, 771, 431))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblMissingWords.sizePolicy().hasHeightForWidth())
        self.tblMissingWords.setSizePolicy(sizePolicy)
        self.tblMissingWords.setStatusTip("")
        self.tblMissingWords.setDragDropOverwriteMode(True)
        self.tblMissingWords.setObjectName("tblMissingWords")
        self.tblMissingWords.setColumnCount(3)
        self.tblMissingWords.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblMissingWords.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblMissingWords.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblMissingWords.setHorizontalHeaderItem(2, item)
        self.tblMissingWords.horizontalHeader().setDefaultSectionSize(220)
        self.pushButton_2 = QtWidgets.QPushButton(self.tabError)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 510, 191, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.addWordsToDictionaryAndUpdate)
        self.tabWidget.addTab(self.tabError, "")
        self.tabDictionary = QtWidgets.QWidget()
        self.tabDictionary.setObjectName("tabDictionary")
        self.btnDictionarySearch = QtWidgets.QPushButton(self.tabDictionary)
        self.btnDictionarySearch.setGeometry(QtCore.QRect(520, 490, 93, 28))
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
        self.tblDictionary.horizontalHeader().setDefaultSectionSize(250)
        self.tblDictionary.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.btnDictionaryAdd = QtWidgets.QPushButton(self.tabDictionary)
        self.btnDictionaryAdd.setGeometry(QtCore.QRect(690, 490, 93, 28))
        self.btnDictionaryAdd.setObjectName("btnDictionaryAdd")
        self.ltxtDictionaryInput = QtWidgets.QLineEdit(self.tabDictionary)
        self.ltxtDictionaryInput.setGeometry(QtCore.QRect(80, 490, 341, 22))
        self.ltxtDictionaryInput.setObjectName("ltxtDictionaryInput")
        self.tabWidget.addTab(self.tabDictionary, "")
        self.btnConfirm = QtWidgets.QPushButton(self.centralwidget)
        self.btnConfirm.setGeometry(QtCore.QRect(140, 610, 93, 28))
        self.btnConfirm.setObjectName("btnConfirm")
        self.btnConfirm.clicked.connect(self.closeUST)
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setGeometry(QtCore.QRect(560, 610, 93, 28))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.clicked.connect(self.closeWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 869, 26))
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
        self.menuFile.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LyricParser"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NoteNum"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Lyric"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Word Found"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Syllable"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("MainWindow", "Parser"))
        self.btnUpdateErrors.setText(_translate("MainWindow", "Update Dictionary"))
        item = self.tblMissingWords.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Word"))
        item = self.tblMissingWords.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Length"))
        item = self.tblMissingWords.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Syllables"))
        self.pushButton_2.setText(_translate("MainWindow", "Update Dictionary and Parse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError), _translate("MainWindow", "Errors"))
        self.btnDictionarySearch.setText(_translate("MainWindow", "Search"))
        item = self.tblDictionary.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Word"))
        item = self.tblDictionary.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Syllables"))
        item = self.tblDictionary.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Length"))
        self.btnDictionaryAdd.setText(_translate("MainWindow", "Add Word(s)"))
        self.ltxtDictionaryInput.setText(_translate("MainWindow", "Here is some Text"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDictionary), _translate("MainWindow", "Dictionary"))
        self.btnConfirm.setText(_translate("MainWindow", "Confirm"))
        self.btnCancel.setText(_translate("MainWindow", "Cancel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSettings.setText(_translate("MainWindow", "Close"))

    def loadDictionary(self):
        print("My parser is %s and my trie is %s" %(self.myParser, self.myParser.myTrie))
        with open("dictionary.txt") as myFile:
            for line in myFile:
                addWordToTrie(line, self.myParser.myTrie)
        myFile.close()

    def checkWord(self):
        inWord = self.ltxtDictionaryInput.text().lower()
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
            inserts = list()
            for i in pronunciations:
                inserts.append(inWord)
                inserts.append(i)
                inserts.append(str(len(i.split(":"))))

            print(str(inserts))
            if len(inserts) > 2:
                self.tblDictionary.setRowCount(len(inserts) / 3)
                count = 0
                groupCount = 0
                for insert in inserts:
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(insert)
                    self.tblDictionary.setItem(count, groupCount, item)
                    groupCount += 1
                    if groupCount > 2:
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
            self.tblMissingWords.setRowCount(len(self.myParser.missingWords))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError), "Errors (" + str(len(self.myParser.missingWords)) + ")")
            count = 0
            for missing in self.myParser.missingWords:
                missingList = missing.listData()
                for i in range (0, 3):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(missingList[i])
                    self.tblMissingWords.setItem(count, i, item)
                count += 1

        self.updateParserTable()

    def updateParserTable(self):
        self.tableWidget.setRowCount(len(self.myParser.myUst.notes))
        count = 0
        groupCount = 0
        for note in self.myParser.myUst.notes:
            inserts = [str(count), note.lyric, note.parentLyric]
            for insert in inserts:
                item = QtWidgets.QTableWidgetItem()
                item.setText(insert)
                self.tableWidget.setItem(count, groupCount, item)
                groupCount += 1

            sylls = ""
            for subNote in note.subNotes:
                sylls = sylls + "," + subNote.lyric if sylls != "" else subNote.lyric

            #if note.lyric == "R" and len(note.subNotes) == 1:
            #    sylls = "R"

            item = QtWidgets.QTableWidgetItem()
            item.setText(sylls)
            self.tableWidget.setItem(count, 3, item)
            groupCount = 0
            count += 1

    def addWordsToDictionary(self):
        # self.testPrinting()
        rowCount = self.tblMissingWords.rowCount()
        for i in range(0, rowCount):
            inSyll = self.tblMissingWords.item(i, 2).text()
            print("Testing %s with length %i" %(inSyll, self.myParser.missingWords[i].numSylls))
            if len(inSyll) > 0 and len(inSyll.split(":")) == self.myParser.missingWords[i].numSylls:
                print("We're gonna add %s it to the dicitonary for %s" %(self.myParser.missingWords[i].lyric, inSyll))
                self.myParser.missingWords[i].fixedSylls = inSyll
                self.myParser.myTrie.insertWord(self.myParser.missingWords[i].lyric, [inSyll])
                self.tblMissingWords.removeRow(i)

        if self.tblMissingWords.rowCount() > 0:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                  "Errors (" + str(self.tblMissingWords.rowCount()) + ")")
        else:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                      "Errors")

    def addWordsToDictionaryAndUpdate(self):
        # self.testPrinting()
        rowCount = self.tblMissingWords.rowCount()
        delCount = 0
        for i in range(0, rowCount):
            inSyll = self.tblMissingWords.item(i - delCount, 2).text()
            if len(inSyll) > 0 and len(inSyll.split(":")) == self.myParser.missingWords[i].numSylls:
                self.myParser.missingWords[i].fixedSylls = inSyll.split(":") if len(inSyll.split(":")) > 1 else inSyll
                self.myParser.myTrie.insertWord(self.myParser.missingWords[i].lyric, [inSyll])
                self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                self.tblMissingWords.removeRow(i - delCount)
                delCount += 1
            elif len(inSyll) == 0:
                tempSylls = self.myParser.getSyllables(self.myParser.myTrie.getWord(self.myParser.missingWords[i].lyric), self.myParser.missingWords[i].numSylls)
                if tempSylls is not None:
                    self.myParser.missingWords[i].fixedSylls = tempSylls
                    self.myParser.parseFixedVCCV(self.myParser.missingWords[i])
                    self.tblMissingWords.removeRow(i - delCount)
                    delCount += 1

        if self.tblMissingWords.rowCount() > 0:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                  "Errors (" + str(self.tblMissingWords.rowCount()) + ")")
        else:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError),
                                      "Errors")

        self.updateParserTable()

    def testPrinting(self):
        rowCount = self.tblMissingWords.rowCount()
        colCount = self.tblMissingWords.columnCount()
        for i in range(0, rowCount):
            for j in range(0, colCount):
                print("At %i, %i I got %s" %(i, j, self.tblMissingWords.item(i, j).text()))

    def closeUST(self):
        self.myParser.finishPlugin()
        self.myParser.myTrie.printTrieToFile("dictionary.txt")
        window.close()

    def closeWindow(self):
        self.myParser.myTrie.printTrieToFile("dictionary.txt")
        window.close()


class myApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =  mainWindow()
        self.ui.setupUi(self)
        # self.ui.loadDictionary()
        self.ui.parseUST()
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

