# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(996, 777)
        MainWindow.setMinimumSize(QtCore.QSize(996, 777))
        MainWindow.setMaximumSize(QtCore.QSize(996, 777))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(840, 100, 141, 591))
        self.layoutWidget.setObjectName("layoutWidget")
        self.Main_buts = QtWidgets.QGridLayout(self.layoutWidget)
        self.Main_buts.setContentsMargins(0, 0, 0, 0)
        self.Main_buts.setObjectName("Main_buts")
        self.but_kdisplay = QtWidgets.QPushButton(self.layoutWidget)
        self.but_kdisplay.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.but_kdisplay.setFont(font)
        self.but_kdisplay.setObjectName("but_kdisplay")
        self.Main_buts.addWidget(self.but_kdisplay, 9, 1, 1, 1)
        self.but_pick = QtWidgets.QPushButton(self.layoutWidget)
        self.but_pick.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.but_pick.setFont(font)
        self.but_pick.setObjectName("but_pick")
        self.Main_buts.addWidget(self.but_pick, 2, 1, 1, 1)
        self.but_back = QtWidgets.QPushButton(self.layoutWidget)
        self.but_back.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.but_back.setFont(font)
        self.but_back.setObjectName("but_back")
        self.Main_buts.addWidget(self.but_back, 7, 1, 1, 1)
        self.but_inspect = QtWidgets.QPushButton(self.layoutWidget)
        self.but_inspect.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.but_inspect.setFont(font)
        self.but_inspect.setObjectName("but_inspect")
        self.Main_buts.addWidget(self.but_inspect, 11, 1, 1, 1)
        self.but_cs2star = QtWidgets.QPushButton(self.layoutWidget)
        self.but_cs2star.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.but_cs2star.setFont(font)
        self.but_cs2star.setObjectName("but_cs2star")
        self.Main_buts.addWidget(self.but_cs2star, 8, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.Main_buts.addWidget(self.pushButton_4, 5, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_9.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")
        self.Main_buts.addWidget(self.pushButton_9, 10, 1, 1, 1)
        self.but_write = QtWidgets.QPushButton(self.layoutWidget)
        self.but_write.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.but_write.setFont(font)
        self.but_write.setObjectName("but_write")
        self.Main_buts.addWidget(self.but_write, 6, 1, 1, 1)
        self.but_select = QtWidgets.QPushButton(self.layoutWidget)
        self.but_select.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.but_select.setFont(font)
        self.but_select.setObjectName("but_select")
        self.Main_buts.addWidget(self.but_select, 0, 1, 1, 1)
        self.main_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.main_text.setGeometry(QtCore.QRect(10, 120, 811, 561))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(15)
        self.main_text.setFont(font)
        self.main_text.setMouseTracking(True)
        self.main_text.setAcceptRichText(False)
        self.main_text.setObjectName("main_text")
        self.but_inspect_2 = QtWidgets.QPushButton(self.centralwidget)
        self.but_inspect_2.setGeometry(QtCore.QRect(680, 50, 139, 50))
        self.but_inspect_2.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.but_inspect_2.setFont(font)
        self.but_inspect_2.setObjectName("but_inspect_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 30, 651, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.text_pwd = QtWidgets.QTextBrowser(self.layoutWidget1)
        self.text_pwd.setObjectName("text_pwd")
        self.horizontalLayout_2.addWidget(self.text_pwd)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Gpus = QtWidgets.QHBoxLayout()
        self.Gpus.setObjectName("Gpus")
        self.ck_gpu0 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ck_gpu0.setObjectName("ck_gpu0")
        self.Gpus.addWidget(self.ck_gpu0)
        self.ck_gpu1 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ck_gpu1.setObjectName("ck_gpu1")
        self.Gpus.addWidget(self.ck_gpu1)
        self.ck_gpu2 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ck_gpu2.setObjectName("ck_gpu2")
        self.Gpus.addWidget(self.ck_gpu2)
        self.ck_gpu3 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ck_gpu3.setObjectName("ck_gpu3")
        self.Gpus.addWidget(self.ck_gpu3)
        self.ck_gpu4 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ck_gpu4.setObjectName("ck_gpu4")
        self.Gpus.addWidget(self.ck_gpu4)
        self.ck_gpu5 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ck_gpu5.setObjectName("ck_gpu5")
        self.Gpus.addWidget(self.ck_gpu5)
        self.ck_gpu6 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ck_gpu6.setObjectName("ck_gpu6")
        self.Gpus.addWidget(self.ck_gpu6)
        self.ck_gpu7 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ck_gpu7.setObjectName("ck_gpu7")
        self.Gpus.addWidget(self.ck_gpu7)
        self.horizontalLayout.addLayout(self.Gpus)
        self.current_gpu = QtWidgets.QTextBrowser(self.layoutWidget1)
        self.current_gpu.setObjectName("current_gpu")
        self.horizontalLayout.addWidget(self.current_gpu)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 996, 22))
        self.menubar.setObjectName("menubar")
        self.menuFuck_Here = QtWidgets.QMenu(self.menubar)
        self.menuFuck_Here.setObjectName("menuFuck_Here")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFuck_Here.menuAction())

        self.retranslateUi(MainWindow)
        self.but_inspect_2.clicked.connect(self.main_text.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ksoft"))
        self.but_kdisplay.setText(_translate("MainWindow", "K_display"))
        self.but_pick.setText(_translate("MainWindow", "Particle Picking"))
        self.but_back.setText(_translate("MainWindow", "Ez_Back Particles"))
        self.but_inspect.setText(_translate("MainWindow", "Undeveloped"))
        self.but_cs2star.setText(_translate("MainWindow", "Cs2Star"))
        self.pushButton_4.setText(_translate("MainWindow", "Inspect Particles"))
        self.pushButton_9.setText(_translate("MainWindow", "Undeveloped"))
        self.but_write.setText(_translate("MainWindow", "Write Particles"))
        self.but_select.setText(_translate("MainWindow", "Select Micrographs"))
        self.main_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu Mono\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.but_inspect_2.setText(_translate("MainWindow", "Clear"))
        self.label_2.setText(_translate("MainWindow", "Current Work Directory:"))
        self.text_pwd.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Gpus :"))
        self.ck_gpu0.setText(_translate("MainWindow", "0"))
        self.ck_gpu1.setText(_translate("MainWindow", "1"))
        self.ck_gpu2.setText(_translate("MainWindow", "2"))
        self.ck_gpu3.setText(_translate("MainWindow", "3"))
        self.ck_gpu4.setText(_translate("MainWindow", "4"))
        self.ck_gpu5.setText(_translate("MainWindow", "5"))
        self.ck_gpu6.setText(_translate("MainWindow", "6"))
        self.ck_gpu7.setText(_translate("MainWindow", "7"))
        self.current_gpu.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.menuFuck_Here.setTitle(_translate("MainWindow", "Fuck Here"))
