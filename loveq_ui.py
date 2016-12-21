# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loveq.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoveQ_Download_Assistant(object):
    def setupUi(self, LoveQ_Download_Assistant):
        LoveQ_Download_Assistant.setObjectName("LoveQ_Download_Assistant")
        LoveQ_Download_Assistant.resize(690, 277)
        self.saveDirLabel = QtWidgets.QLabel(LoveQ_Download_Assistant)
        self.saveDirLabel.setGeometry(QtCore.QRect(81, 40, 54, 16))
        self.saveDirLabel.setObjectName("saveDirLabel")
        self.saveDirEdit = QtWidgets.QLineEdit(LoveQ_Download_Assistant)
        self.saveDirEdit.setGeometry(QtCore.QRect(141, 40, 431, 20))
        self.saveDirEdit.setObjectName("saveDirEdit")
        self.saveDirBtn = QtWidgets.QPushButton(LoveQ_Download_Assistant)
        self.saveDirBtn.setGeometry(QtCore.QRect(579, 39, 41, 23))
        self.saveDirBtn.setObjectName("saveDirBtn")
        self.startDateEdit = QtWidgets.QDateEdit(LoveQ_Download_Assistant)
        self.startDateEdit.setGeometry(QtCore.QRect(140, 80, 88, 21))
        self.startDateEdit.setObjectName("startDateEdit")
        self.endDateEdit = QtWidgets.QDateEdit(LoveQ_Download_Assistant)
        self.endDateEdit.setGeometry(QtCore.QRect(410, 80, 88, 21))
        self.endDateEdit.setObjectName("endDateEdit")
        self.downloadBtn = QtWidgets.QPushButton(LoveQ_Download_Assistant)
        self.downloadBtn.setGeometry(QtCore.QRect(550, 78, 70, 25))
        self.downloadBtn.setObjectName("downloadBtn")
        self.startDateLabel = QtWidgets.QLabel(LoveQ_Download_Assistant)
        self.startDateLabel.setGeometry(QtCore.QRect(80, 80, 54, 21))
        self.startDateLabel.setObjectName("startDateLabel")
        self.endDateLabel = QtWidgets.QLabel(LoveQ_Download_Assistant)
        self.endDateLabel.setGeometry(QtCore.QRect(350, 80, 54, 21))
        self.endDateLabel.setObjectName("endDateLabel")
        self.consoleTextEdit = QtWidgets.QTextEdit(LoveQ_Download_Assistant)
        self.consoleTextEdit.setGeometry(QtCore.QRect(0, 150, 691, 101))
        self.consoleTextEdit.setReadOnly(True)
        self.consoleTextEdit.setObjectName("consoleTextEdit")
        self.statusLabel = QtWidgets.QLabel(LoveQ_Download_Assistant)
        self.statusLabel.setGeometry(QtCore.QRect(10, 256, 111, 20))
        self.statusLabel.setText("")
        self.statusLabel.setObjectName("statusLabel")

        self.retranslateUi(LoveQ_Download_Assistant)
        QtCore.QMetaObject.connectSlotsByName(LoveQ_Download_Assistant)

    def retranslateUi(self, LoveQ_Download_Assistant):
        _translate = QtCore.QCoreApplication.translate
        LoveQ_Download_Assistant.setWindowTitle(_translate("LoveQ_Download_Assistant", "LoveQ_Download_Assistant"))
        self.saveDirLabel.setText(_translate("LoveQ_Download_Assistant", "保存路径:"))
        self.saveDirBtn.setText(_translate("LoveQ_Download_Assistant", "..."))
        self.downloadBtn.setText(_translate("LoveQ_Download_Assistant", "Download"))
        self.startDateLabel.setText(_translate("LoveQ_Download_Assistant", "起始日期:"))
        self.endDateLabel.setText(_translate("LoveQ_Download_Assistant", "结束日期:"))

