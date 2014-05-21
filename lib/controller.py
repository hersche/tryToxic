from lib.tryToxic import ToxTry
from ui.main import *
from PyQt4 import QtCore, QtGui
from lib.toxUiHandler import toxUiHandler
from lib.toxModels import toxMessageHandler
from lib.cryptClass import scm
from lib.configUiHandler import configUiHandler
from lib.header import tr

class toxThread(QtCore.QThread):
  """
  Let the tox-Class run in a seperate thread and handling events betwen tox and gui.
  """
  updateUiUserList = QtCore.pyqtSignal(list)
  clickToxFriend = QtCore.pyqtSignal(str)
  incomingFriendFile = QtCore.pyqtSignal(int, int, float, str)
  incomingFriendRequest = QtCore.pyqtSignal(str, str)
  incomingFriendMessage = QtCore.pyqtSignal(int, str)
  incomingGroupMessage = QtCore.pyqtSignal(int, int, str)
  incomingGroupInvite = QtCore.pyqtSignal(int, str)
  incomingNameChange = QtCore.pyqtSignal(int, str)
  incomingStatusChange = QtCore.pyqtSignal(int, int)
  incomingOnlineStatus = QtCore.pyqtSignal(int, bool)
  incomingStatusMessageChange = QtCore.pyqtSignal(int, str)
  incomingGroupNameChange = QtCore.pyqtSignal()
  connectToDHT = QtCore.pyqtSignal(int)
  disconnectToDHT = QtCore.pyqtSignal(int)
  def __init__(self):
    QtCore.QThread.__init__(self)
    self.tryToxic = None
  def run(self):
    """
    Run the thread
    """
    self.tryToxic.loop()

  def quit(self):
    """
    Quit the thread
    """
    self.tryToxic.kill()
    self.exit(0)
class mainController(QtGui.QMainWindow):
  """
  The big big main-class. It's the gui and handler for gui, which is in active connection with tryToxic in toxThread.
  @TODO needs to get more lite - methods could go to another class too, to get better overview of code.
  """
  def __init__(self, app, parent=None):
    QtGui.QWidget.__init__(self, parent)
    self.app = app
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # Starting with encryption
    self.encryptionObject = None
    self.configUiHandler = configUiHandler(self.ui)
    if self.configUiHandler.encryptionObject is not None:
      self.encryptionObject = self.configUiHandler.encryptionObject

    # instance message-handler, thread, tryToxic itself..
    self.toxMessagesHandler = toxMessageHandler(self.encryptionObject, self.configUiHandler.logMessages)
    self.toxThread = toxThread()
    if self.encryptionObject is not None:
      self.tryToxic = ToxTry(self.encryptionObject.key, self.toxThread)
    else:
      self.tryToxic = ToxTry("", self.toxThread)
    self.toxThread.tryToxic = self.tryToxic
    self.toxThread.start()
    self.setWindowTitle("tryToxic :: " + self.tryToxic.name)
    # start toxUiHandler
    self.toxUiHandler = toxUiHandler(self.ui, self.tryToxic, self.toxMessagesHandler, self.toxThread)

    self.toxUiHandler.appNotify.connect(self.onAppNotify)
    self.configUiHandler.passPhraseChanged.connect(self.onPassPhraseChanged)
    self.configUiHandler.saveMessagesChanged.connect(self.onSaveMessagesChanged)

  def onAppNotify(self):
    logger.info("recive notify!")
    self.app.alert(self, 4000)

  def onSaveMessagesChanged(self, yesNo):
    yesNo = yesNo.lower()
    if yesNo != "true":
      self.toxMessagesHandler.saveMessages = False
      self.tryToxic.toxMessagesHandler.saveMessages = False
    else:
      self.toxMessagesHandler.saveMessages = True
      self.tryToxic.toxMessagesHandler.saveMessages = True


  def onPassPhraseChanged(self, encryptionObject):
    """
    When configUiHandler came to the point, he has to change passPhrase, he informs the mainclass (for compatibility)
    but also tryToxic over it's new passPhrase.
    """
    self.encryptionObject = encryptionObject
    if encryptionObject is not None:
      self.tryToxic.passPhrase = encryptionObject.key
    else:
      self.tryToxic.passPhrase = ""
    scm.migrateEncryptionData(encryptionObject, self.toxMessagesHandler)
    self.tryToxic.saveLocalData()
  def closeEvent(self, event):
    """
    Programm should get closed? We're informed here
    """
    reply = QtGui.QMessageBox.question(self, tr('Really leave tryToxic?'),
        tr("Are you sure to quit?"), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    if reply == QtGui.QMessageBox.Yes:
      self.toxThread.quit()
      event.accept()
    else:
      event.ignore()

