from lib.tryToxic import *
from lib.toxModels import *
from lib.configControll import *
from lib.cryptClass import *
from ui.main import *
from PyQt4 import Qt
from lib.toxUiHandler import toxUiHandler

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
    self.passPhrase = ""
    self.app=app
    self.encryptionObject = None
    self.msgBox = QtGui.QMessageBox()
    self.msgBox.addButton(QtGui.QMessageBox.Yes)
    self.msgBox.addButton(QtGui.QMessageBox.No)
    self.updateConfigListData()
    if self.encryptionObject is not None and self.encryptionObject.name is not "None":
        pw, okCancel = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
        self.passPhrase = self.encryptionObject.setKey(pw)
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.setEnabled(True)
    
    #instance message-handler, thread, tryToxic itself..
    self.toxMessagesHandler = toxMessageHandler(self.encryptionObject)
    self.toxThread = toxThread()
    self.tryToxic = ToxTry(self.passPhrase,self.toxThread)
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
    self.updateConfigListUi(True)
    
    #config-Actions
    self.ui.createConfig.clicked.connect(self.onCreateConfig)
    self.ui.saveConfig.clicked.connect(self.onSaveConfig)
    self.ui.deleteConfig.clicked.connect(self.onDeleteConfig)
    self.ui.configList.itemClicked.connect(self.onConfigItemClick)
      
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
      
  #down here it's just config-stuff   
  def updateConfigListUi(self,selectFirst=False,name=""):
    """
    Just update the config ui
    """
    self.ui.configList.clear()
    i=0
    for config in self.configlist:
        self.ui.configList.addItem(config.key)
        if config.key == name:
            self.ui.configList.setCurrentRow(i)
            self.onConfigItemClick(self.ui.configList.currentItem())
        i+=1
    if selectFirst:
        self.ui.configList.setCurrentRow(0)
        self.onConfigItemClick(self.ui.configList.currentItem())
  def updateConfigListData(self):
    """
    update the list of config-data-objects 
    """
    logger.debug("|Models| Update configList")
    self.configlist = []
    dbCursor.execute('select * from config;') 
    for row in dbCursor.fetchall():
        self.configlist.append(Config(row[0], row[1], row[2]))
    for config in self.configlist:
        if config.key.lower()== "encrypted" and self.encryptionObject is None:
            logger.debug(tr("Found encryption in config. Init Module with value "+config.value))
            if self.encryptionObject is None:
                self.encryptionObject = cm(scm.getMod(config.value), "encryptionInit")
        elif config.key == "fileHandlerLogLevel":
          logger.removeHandler(fh)
          fh.setLevel(staticConfigTools.getLoggerLevel(config.key))
          logger.addHandler(fh)
        elif config.key == "consoleHandlerLogLevel":
          logger.removeHandler(ch)
          ch.setLevel(staticConfigTools.getLoggerLevel(config.value))
          logger.addHandler(ch)
  def onConfigItemClick(self, item):
    for config in self.configlist:
        if config.key == item.text():
            self.ui.configKey.setText(config.key)
            self.ui.configValue.setText(config.value)
              
  #-------------
  # config-Actions
  #--------------
  def onCreateConfig(self):
      # @TODO select the created!
      key = self.ui.configKey.text()
      key = key.lower()
      if key == "encrypted" and self.ui.configValue.text() != "None":
          pw, ok = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
          if ok:
            Config.createConfig(self.ui.configKey.text(), self.ui.configValue.text())
            newCryptManager = cm(scm.getMod(self.ui.configValue.text()),pw)
            scm.migrateEncryptionData(newCryptManager, self.toxMessagesHandler)
            self.encryptionObject=newCryptManager
            self.tryToxic.passPhrase = newCryptManager.key
            self.tryToxic.saveLocalData()
      else:
          Config.createConfig(self.ui.configKey.text(), self.ui.configValue.text())
      self.updateConfigListData()
      self.updateConfigListUi()
  def onSaveConfig(self):
    """
    Save a configuration in db.
    """
    cI = self.ui.configList.currentItem()
    if cI is not None:      ciText = cI.text()
    outOk = True
    for config in self.configlist:
        if config.key == ciText:
            key = self.ui.configKey.text()
            key = key.lower()
            config.save(self.ui.configKey.text(), self.ui.configValue.text())
            if key == "encrypted":
                if self.ui.configValue.text() != "None":
                  pw, ok = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
                  outOk=ok 
                  if ok:
                    mod = scm.getMod(self.ui.configValue.text())
                    if mod is not None:
                      nCm = cm(scm.getMod(self.ui.configValue.text()), pw)
                      self.tryToxic.passPhrase = nCm.key
                      self.tryToxic.saveLocalData()
                else:
                  nCm = None
                if outOk:
                  scm.migrateEncryptionData(nCm, self.toxMessagesHandler)
                  self.encryptionObject = nCm
    self.updateConfigListData()
  def onDeleteConfig(self):
    """
    Delete a config-object from db
    """
    cm = self.ui.configList.currentItem()
    success = False
    for config in self.configlist:
        if cm is not None and config.key == cm.text():
            config.delete()
            success = True
    if not success:
        logger.error(tr("Config")+" "+tr("could not")+" be "+tr("saved"))
    else:
        self.updateConfigListData()
        self.updateConfigListUi(True)
