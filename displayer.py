# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'displayer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Displayer(object):
    def setupUi(self, Displayer):
        Displayer.setObjectName("Displayer")
        Displayer.resize(400, 300)

        self.retranslateUi(Displayer)
        QtCore.QMetaObject.connectSlotsByName(Displayer)

    def retranslateUi(self, Displayer):
        _translate = QtCore.QCoreApplication.translate
        Displayer.setWindowTitle(_translate("Displayer", "Dialog"))

