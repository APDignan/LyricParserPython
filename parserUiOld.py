# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parserUi.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView
from Trie import trie

class mainWindow(object):
    def setupUi(self, MainWindow):
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
        self.pushButton = QtWidgets.QPushButton(self.tabError)
        self.pushButton.setGeometry(QtCore.QRect(200, 510, 111, 28))
        self.pushButton.setObjectName("pushButton")
        self.tblDictionary_2 = QtWidgets.QTableWidget(self.tabError)
        self.tblDictionary_2.setGeometry(QtCore.QRect(40, 40, 771, 431))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblDictionary_2.sizePolicy().hasHeightForWidth())
        self.tblDictionary_2.setSizePolicy(sizePolicy)
        self.tblDictionary_2.setStatusTip("")
        self.tblDictionary_2.setDragDropOverwriteMode(True)
        self.tblDictionary_2.setObjectName("tblMissingWords")
        self.tblDictionary_2.setColumnCount(3)
        self.tblDictionary_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblDictionary_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblDictionary_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblDictionary_2.setHorizontalHeaderItem(2, item)
        self.tblDictionary_2.horizontalHeader().setDefaultSectionSize(220)
        self.pushButton_2 = QtWidgets.QPushButton(self.tabError)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 510, 191, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.addTab(self.tabError, "")
        self.tabDictionary = QtWidgets.QWidget()
        self.tabDictionary.setObjectName("tabDictionary")
        self.txtDictionaryInput = QtWidgets.QPlainTextEdit(self.tabDictionary)
        self.txtDictionaryInput.setGeometry(QtCore.QRect(110, 490, 351, 31))
        self.txtDictionaryInput.setObjectName("txtDictionaryInput")
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
        self.tblDictionary.horizontalHeader().setDefaultSectionSize(220)
        self.tblDictionary.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.btnDictionaryAdd = QtWidgets.QPushButton(self.tabDictionary)
        self.btnDictionaryAdd.setGeometry(QtCore.QRect(690, 490, 93, 28))
        self.btnDictionaryAdd.setObjectName("btnDictionaryAdd")
        self.tabWidget.addTab(self.tabDictionary, "")
        self.btnConfirm = QtWidgets.QPushButton(self.centralwidget)
        self.btnConfirm.setGeometry(QtCore.QRect(140, 610, 93, 28))
        self.btnConfirm.setObjectName("btnConfirm")
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setGeometry(QtCore.QRect(560, 610, 93, 28))
        self.btnCancel.setObjectName("btnCancel")
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
        self.tabWidget.setCurrentIndex(2)
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
        self.pushButton.setText(_translate("MainWindow", "Update Dictionary"))
        item = self.tblDictionary_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Word"))
        item = self.tblDictionary_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Length"))
        item = self.tblDictionary_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Syllables"))
        self.pushButton_2.setText(_translate("MainWindow", "Update Dictionary and Parse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabError), _translate("MainWindow", "Errors"))
        self.txtDictionaryInput.setPlainText(_translate("MainWindow", "Here is some text"))
        self.btnDictionarySearch.setText(_translate("MainWindow", "Search"))
        item = self.tblDictionary.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Word"))
        item = self.tblDictionary.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Syllables"))
        item = self.tblDictionary.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Length"))
        self.btnDictionaryAdd.setText(_translate("MainWindow", "Add Word(s)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDictionary), _translate("MainWindow", "Dictionary"))
        self.btnConfirm.setText(_translate("MainWindow", "Confirm"))
        self.btnCancel.setText(_translate("MainWindow", "Cancel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSettings.setText(_translate("MainWindow", "Close"))

    def loadDictionary(self):
        self.myTrie = trie()
        with open("dictionary.txt") as myFile:
            for line in myFile:
                addWordToTrie(line, self.myTrie)
        print("Done reading in dicitonary")

    def checkWord(self):
        inWord = self.txtDictionaryInput.toPlainText().lower()
        print("Checking with inWord %s. Got %s" %(inWord, self.myTrie.getWord(inWord)))
        if len(inWord) < 100 and self.myTrie.getWord(inWord) != "":
            # self.tblDictionary = QtWidgets.QTableWidget(self.tabDictionary)
            size = self.tblDictionary.rowCount()
            self.tblDictionary.setRowCount(size + 1)
            inserts = [inWord, str(self.myTrie.getWord(inWord)[0]), str(len(self.myTrie.getWord(inWord)[0].split(":")))]
            count = 0
            for insert in inserts:
                item = QtWidgets.QTableWidgetItem()
                item.setText(insert)
                self.tblDictionary.setItem(size, count, item)
                count += 1


class myApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =  mainWindow()
        self.ui.setupUi(self)
        self.ui.loadDictionary()
        self.show()

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

