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
        LoveQ_Download_Assistant.resize(710, 446)
        self.saveDirLabel = QtWidgets.QLabel(LoveQ_Download_Assistant)
        self.saveDirLabel.setGeometry(QtCore.QRect(90, 60, 61, 16))
        self.saveDirLabel.setObjectName("saveDirLabel")
        self.saveDirEdit = QtWidgets.QLineEdit(LoveQ_Download_Assistant)
        self.saveDirEdit.setGeometry(QtCore.QRect(160, 60, 321, 20))
        self.saveDirEdit.setObjectName("saveDirEdit")
        self.saveDirBtn = QtWidgets.QPushButton(LoveQ_Download_Assistant)
        self.saveDirBtn.setGeometry(QtCore.QRect(490, 60, 31, 23))
        self.saveDirBtn.setObjectName("saveDirBtn")
        self.startDateEdit = QtWidgets.QDateEdit(LoveQ_Download_Assistant)
        self.startDateEdit.setGeometry(QtCore.QRect(130, 110, 110, 22))
        self.startDateEdit.setObjectName("startDateEdit")
        self.endDateEdit = QtWidgets.QDateEdit(LoveQ_Download_Assistant)
        self.endDateEdit.setGeometry(QtCore.QRect(390, 110, 110, 22))
        self.endDateEdit.setObjectName("endDateEdit")
        self.downloadBtn = QtWidgets.QPushButton(LoveQ_Download_Assistant)
        self.downloadBtn.setGeometry(QtCore.QRect(250, 200, 75, 23))
        self.downloadBtn.setObjectName("downloadBtn")
        self.startDateLabel = QtWidgets.QLabel(LoveQ_Download_Assistant)
        self.startDateLabel.setGeometry(QtCore.QRect(60, 110, 61, 21))
        self.startDateLabel.setObjectName("startDateLabel")
        self.endDateLabel = QtWidgets.QLabel(LoveQ_Download_Assistant)
        self.endDateLabel.setGeometry(QtCore.QRect(320, 120, 54, 12))
        self.endDateLabel.setObjectName("endDateLabel")
        self.downloadProgressBar = QtWidgets.QProgressBar(LoveQ_Download_Assistant)
        self.downloadProgressBar.setGeometry(QtCore.QRect(120, 420, 353, 23))
        self.downloadProgressBar.setProperty("value", 0)
        self.downloadProgressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.downloadProgressBar.setTextVisible(True)
        self.downloadProgressBar.setInvertedAppearance(False)
        self.downloadProgressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.downloadProgressBar.setObjectName("downloadProgressBar")
        self.consoleTextEdit = QtWidgets.QTextEdit(LoveQ_Download_Assistant)
        self.consoleTextEdit.setGeometry(QtCore.QRect(0, 240, 691, 171))
        self.consoleTextEdit.setObjectName("consoleTextEdit")

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

