# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sat Mar 29 11:00:51 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1072, 830)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mainTab = QtGui.QTabWidget(self.centralwidget)
        self.mainTab.setGeometry(QtCore.QRect(0, 0, 1041, 791))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTab.sizePolicy().hasHeightForWidth())
        self.mainTab.setSizePolicy(sizePolicy)
        self.mainTab.setObjectName(_fromUtf8("mainTab"))
        self.tab_9 = QtGui.QWidget()
        self.tab_9.setObjectName(_fromUtf8("tab_9"))
        self.toxTryChat = QtGui.QTextEdit(self.tab_9)
        self.toxTryChat.setGeometry(QtCore.QRect(360, 10, 661, 711))
        self.toxTryChat.setFrameShape(QtGui.QFrame.StyledPanel)
        self.toxTryChat.setFrameShadow(QtGui.QFrame.Sunken)
        self.toxTryChat.setReadOnly(True)
        self.toxTryChat.setObjectName(_fromUtf8("toxTryChat"))
        self.toxTrySendText = QtGui.QLineEdit(self.tab_9)
        self.toxTrySendText.setGeometry(QtCore.QRect(360, 730, 561, 21))
        self.toxTrySendText.setObjectName(_fromUtf8("toxTrySendText"))
        self.toxTrySendButton = QtGui.QPushButton(self.tab_9)
        self.toxTrySendButton.setGeometry(QtCore.QRect(930, 730, 91, 24))
        self.toxTrySendButton.setObjectName(_fromUtf8("toxTrySendButton"))
        self.toxTryFriends = QtGui.QListWidget(self.tab_9)
        self.toxTryFriends.setGeometry(QtCore.QRect(10, 160, 291, 261))
        self.toxTryFriends.setObjectName(_fromUtf8("toxTryFriends"))
        self.gridLayoutWidget_5 = QtGui.QWidget(self.tab_9)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 291, 107))
        self.gridLayoutWidget_5.setObjectName(_fromUtf8("gridLayoutWidget_5"))
        self.gridLayout_5 = QtGui.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_25 = QtGui.QLabel(self.gridLayoutWidget_5)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridLayout_5.addWidget(self.label_25, 3, 0, 1, 1)
        self.label_42 = QtGui.QLabel(self.gridLayoutWidget_5)
        self.label_42.setObjectName(_fromUtf8("label_42"))
        self.gridLayout_5.addWidget(self.label_42, 0, 0, 1, 1)
        self.label_43 = QtGui.QLabel(self.gridLayoutWidget_5)
        self.label_43.setObjectName(_fromUtf8("label_43"))
        self.gridLayout_5.addWidget(self.label_43, 4, 0, 1, 1)
        self.toxTryId = QtGui.QLineEdit(self.gridLayoutWidget_5)
        self.toxTryId.setObjectName(_fromUtf8("toxTryId"))
        self.gridLayout_5.addWidget(self.toxTryId, 3, 2, 1, 1)
        self.toxTryUsername = QtGui.QLineEdit(self.gridLayoutWidget_5)
        self.toxTryUsername.setObjectName(_fromUtf8("toxTryUsername"))
        self.gridLayout_5.addWidget(self.toxTryUsername, 0, 2, 1, 1)
        self.toxTryStatus = QtGui.QComboBox(self.gridLayoutWidget_5)
        self.toxTryStatus.setObjectName(_fromUtf8("toxTryStatus"))
        self.toxTryStatus.addItem(_fromUtf8(""))
        self.toxTryStatus.addItem(_fromUtf8(""))
        self.toxTryStatus.addItem(_fromUtf8(""))
        self.gridLayout_5.addWidget(self.toxTryStatus, 4, 2, 1, 1)
        self.label_46 = QtGui.QLabel(self.gridLayoutWidget_5)
        self.label_46.setObjectName(_fromUtf8("label_46"))
        self.gridLayout_5.addWidget(self.label_46, 5, 0, 1, 1)
        self.toxTryStatusMessage = QtGui.QLineEdit(self.gridLayoutWidget_5)
        self.toxTryStatusMessage.setObjectName(_fromUtf8("toxTryStatusMessage"))
        self.gridLayout_5.addWidget(self.toxTryStatusMessage, 5, 2, 1, 1)
        self.label_44 = QtGui.QLabel(self.tab_9)
        self.label_44.setGeometry(QtCore.QRect(10, 140, 101, 16))
        self.label_44.setObjectName(_fromUtf8("label_44"))
        self.label_45 = QtGui.QLabel(self.tab_9)
        self.label_45.setGeometry(QtCore.QRect(10, 430, 111, 16))
        self.label_45.setObjectName(_fromUtf8("label_45"))
        self.toxTryFriendInfos = QtGui.QTextEdit(self.tab_9)
        self.toxTryFriendInfos.setGeometry(QtCore.QRect(10, 450, 291, 131))
        self.toxTryFriendInfos.setDocumentTitle(_fromUtf8(""))
        self.toxTryFriendInfos.setUndoRedoEnabled(False)
        self.toxTryFriendInfos.setReadOnly(True)
        self.toxTryFriendInfos.setObjectName(_fromUtf8("toxTryFriendInfos"))
        self.toxTryNotifications = QtGui.QTextEdit(self.tab_9)
        self.toxTryNotifications.setGeometry(QtCore.QRect(10, 610, 291, 141))
        self.toxTryNotifications.setDocumentTitle(_fromUtf8(""))
        self.toxTryNotifications.setUndoRedoEnabled(False)
        self.toxTryNotifications.setReadOnly(True)
        self.toxTryNotifications.setObjectName(_fromUtf8("toxTryNotifications"))
        self.toxTryNewFriendRequest = QtGui.QPushButton(self.tab_9)
        self.toxTryNewFriendRequest.setGeometry(QtCore.QRect(200, 130, 101, 24))
        self.toxTryNewFriendRequest.setObjectName(_fromUtf8("toxTryNewFriendRequest"))
        self.label_47 = QtGui.QLabel(self.tab_9)
        self.label_47.setGeometry(QtCore.QRect(10, 590, 111, 16))
        self.label_47.setObjectName(_fromUtf8("label_47"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("logo.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainTab.addTab(self.tab_9, icon, _fromUtf8(""))
        self.settings = QtGui.QWidget()
        self.settings.setObjectName(_fromUtf8("settings"))
        self.formLayoutWidget_7 = QtGui.QWidget(self.settings)
        self.formLayoutWidget_7.setGeometry(QtCore.QRect(10, 10, 351, 251))
        self.formLayoutWidget_7.setObjectName(_fromUtf8("formLayoutWidget_7"))
        self.formLayout_7 = QtGui.QFormLayout(self.formLayoutWidget_7)
        self.formLayout_7.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_7.setMargin(0)
        self.formLayout_7.setObjectName(_fromUtf8("formLayout_7"))
        self.label_23 = QtGui.QLabel(self.formLayoutWidget_7)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.formLayout_7.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_23)
        self.configList = QtGui.QListWidget(self.formLayoutWidget_7)
        self.configList.setObjectName(_fromUtf8("configList"))
        self.formLayout_7.setWidget(3, QtGui.QFormLayout.SpanningRole, self.configList)
        self.label_26 = QtGui.QLabel(self.formLayoutWidget_7)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.formLayout_7.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_26)
        self.label_27 = QtGui.QLabel(self.formLayoutWidget_7)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.formLayout_7.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_27)
        self.configKey = QtGui.QLineEdit(self.formLayoutWidget_7)
        self.configKey.setObjectName(_fromUtf8("configKey"))
        self.formLayout_7.setWidget(4, QtGui.QFormLayout.FieldRole, self.configKey)
        self.configValue = QtGui.QLineEdit(self.formLayoutWidget_7)
        self.configValue.setObjectName(_fromUtf8("configValue"))
        self.formLayout_7.setWidget(5, QtGui.QFormLayout.FieldRole, self.configValue)
        self.createConfig = QtGui.QPushButton(self.formLayoutWidget_7)
        self.createConfig.setObjectName(_fromUtf8("createConfig"))
        self.formLayout_7.setWidget(6, QtGui.QFormLayout.LabelRole, self.createConfig)
        self.saveConfig = QtGui.QPushButton(self.formLayoutWidget_7)
        self.saveConfig.setObjectName(_fromUtf8("saveConfig"))
        self.formLayout_7.setWidget(6, QtGui.QFormLayout.FieldRole, self.saveConfig)
        self.deleteConfig = QtGui.QPushButton(self.formLayoutWidget_7)
        self.deleteConfig.setObjectName(_fromUtf8("deleteConfig"))
        self.formLayout_7.setWidget(7, QtGui.QFormLayout.FieldRole, self.deleteConfig)
        self.textEdit = QtGui.QTextEdit(self.settings)
        self.textEdit.setGeometry(QtCore.QRect(380, 10, 501, 251))
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.mainTab.addTab(self.settings, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1072, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.mainTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "tryTox", None))
        self.toxTrySendButton.setText(_translate("MainWindow", "Send", None))
        self.label_25.setText(_translate("MainWindow", "Your ID", None))
        self.label_42.setText(_translate("MainWindow", "Username", None))
        self.label_43.setText(_translate("MainWindow", "Status", None))
        self.toxTryStatus.setItemText(0, _translate("MainWindow", "Online", None))
        self.toxTryStatus.setItemText(1, _translate("MainWindow", "Away", None))
        self.toxTryStatus.setItemText(2, _translate("MainWindow", "Busy", None))
        self.label_46.setText(_translate("MainWindow", "Statusmessage", None))
        self.toxTryStatusMessage.setText(_translate("MainWindow", "I\'m alive!", None))
        self.label_44.setText(_translate("MainWindow", "Friendlist", None))
        self.label_45.setText(_translate("MainWindow", "FriendInfos", None))
        self.toxTryNotifications.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.toxTryNewFriendRequest.setText(_translate("MainWindow", "Add new Friend", None))
        self.label_47.setText(_translate("MainWindow", "Notifications", None))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tab_9), _translate("MainWindow", "ToxTry", None))
        self.label_23.setText(_translate("MainWindow", "Configs", None))
        self.label_26.setText(_translate("MainWindow", "Key", None))
        self.label_27.setText(_translate("MainWindow", "Value", None))
        self.createConfig.setText(_translate("MainWindow", "Create", None))
        self.saveConfig.setText(_translate("MainWindow", "Save", None))
        self.deleteConfig.setText(_translate("MainWindow", "Delete", None))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; text-decoration: underline;\">Avaible Config-Keys</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">* lang / language = language - put the right filename (*.qm in your folder) there</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">* encrypted : 1=CAST, 2=Blowfish, 3=DES3,4=ARC4,5=XOR,6=AES,7=ARC2 (you need to install pycrypto / python3-crypto @ *buntu). Put &quot;None&quot; as value for going back to cleartext. Encryption shouldn\'t need any restart.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Restart is needed after changes!</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.mainTab.setTabText(self.mainTab.indexOf(self.settings), _translate("MainWindow", "Settings", None))

