from lib.tryToxic import *
from lib.toxModels import *
from lib.configControll import *
from lib.cryptClass import *
from ui.main import *
from PyQt4 import Qt
from lib.toxUiHandler import toxUiHandler
from lib.configUiHandler import configUiHandler

class toxThread(QtCore.QThread):
  """
  Let the tox-Class run in a seperate thread and handling events betwen tox and gui.
  """
  updateUiUserList = QtCore.pyqtSignal(list)
  clickToxFriend = QtCore.pyqtSignal(str)
  incomingFriendFile = QtCore.pyqtSignal(int,int,float,str)
  incomingFriendRequest = QtCore.pyqtSignal(str,str)
  incomingFriendMessage = QtCore.pyqtSignal(int,str)
  incomingGroupMessage = QtCore.pyqtSignal(int,int,str) 
  incomingGroupInvite = QtCore.pyqtSignal(int,str)
  incomingNameChange = QtCore.pyqtSignal(int,str)
  incomingStatusChange = QtCore.pyqtSignal(int,int)
  incomingOnlineStatus = QtCore.pyqtSignal(int,bool)
  incomingStatusMessageChange = QtCore.pyqtSignal(int,str)
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
  def __init__(self,app, parent=None):
    QtGui.QWidget.__init__(self, parent)
    logger.debug("|GUI| Init Gui")
    self.app=app

    self.msgBox = QtGui.QMessageBox()
    self.msgBox.addButton(QtGui.QMessageBox.Yes)
    self.msgBox.addButton(QtGui.QMessageBox.No)
    
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.setEnabled(True)
    
    self.encryptionObject = None
    self.configUiHandler = configUiHandler(self.ui)
    if self.configUiHandler.encryptionObject is not None:
      self.encryptionObject = self.configUiHandler.encryptionObject
    #instance message-handler, thread, tryToxic itself..
    self.toxMessagesHandler = toxMessageHandler(self.encryptionObject)
    self.toxThread = toxThread()
    if self.encryptionObject is not None:
      self.tryToxic = ToxTry(self.encryptionObject.key,self.toxThread)
    else:
      self.tryToxic = ToxTry("",self.toxThread)
    self.toxThread.tryToxic = self.tryToxic
    self.toxThread.start()
    self.toxUiHandler = toxUiHandler(self.ui, self.tryToxic,self.toxMessagesHandler,self.toxThread)
    #set ui-data 
    self.ui.toxTryUsername.setText(self.tryToxic.name)
    self.setWindowTitle("tryToxic :: "+self.tryToxic.name)
    self.ui.toxTryStatusMessage.setText(self.tryToxic.statusMessage)
    self.ui.toxTryId.setText(self.tryToxic.pubKey)
    #self.generateDnsId(self.tryToxic.pubKey)
    self.tryToxic.updateToxUserObjects()
    self.toxUiHandler.updateToxUsersGuiList(self.tryToxic.toxUserList)
    
    
    
    self.configUiHandler.updateConfigListUi(True)
    self.configUiHandler.passPhraseChanged.connect(self.onPassPhraseChanged)
   
   
  def onPassPhraseChanged(self,encryptionObject):
    self.encryptionObject=encryptionObject
    if encryptionObject is not None:
      self.tryToxic.passPhrase=encryptionObject.key
    else:
      self.tryToxic.passPhrase=""
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
      
