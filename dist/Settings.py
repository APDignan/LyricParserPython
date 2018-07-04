# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlogSettings(object):
    def setupUi(self, dlogSettings):
        dlogSettings.setObjectName("dlogSettings")
        dlogSettings.resize(420, 158)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlogSettings)
        self.buttonBox.setGeometry(QtCore.QRect(60, 110, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.ckbxFullLen = QtWidgets.QCheckBox(dlogSettings)
        self.ckbxFullLen.setGeometry(QtCore.QRect(30, 30, 301, 20))
        self.ckbxFullLen.setObjectName("ckbxFullLen")
        self.ckbxBlendVowels = QtWidgets.QCheckBox(dlogSettings)
        self.ckbxBlendVowels.setGeometry(QtCore.QRect(30, 60, 281, 20))
        self.ckbxBlendVowels.setObjectName("ckbxBlendVowels")
        self.btnSaveSettings = QtWidgets.QPushButton(dlogSettings)
        self.btnSaveSettings.setGeometry(QtCore.QRect(30, 110, 93, 28))
        self.btnSaveSettings.setObjectName("btnSaveSettings")

        self.retranslateUi(dlogSettings)
        self.buttonBox.accepted.connect(dlogSettings.accept)
        self.buttonBox.rejected.connect(dlogSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(dlogSettings)

    def retranslateUi(self, dlogSettings):
        _translate = QtCore.QCoreApplication.translate
        dlogSettings.setWindowTitle(_translate("dlogSettings", "Settings"))
        self.ckbxFullLen.setText(_translate("dlogSettings", "Extend endings based on Consonant Field"))
        self.ckbxBlendVowels.setText(_translate("dlogSettings", "Blend Vowels with consonants"))
        self.btnSaveSettings.setText(_translate("dlogSettings", "Save Settings"))

