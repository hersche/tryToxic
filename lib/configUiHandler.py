from PyQt4 import QtGui
from lib.header import *
from lib.configControll import *
class configUiHandler(QtCore.QObject):
  passPhraseChanged = QtCore.pyqtSignal(object)
  saveMessagesChanged = QtCore.pyqtSignal(str)
  def __init__(self, ui):
    QtCore.QObject.__init__(self)
    self.ui = ui
    self.configList = staticConfigTools.updateConfigListData()
    self.encryptionObject = None
    self.logMessages = True
    self.filterConfig(self.configList)
    self.updateConfigListUi(True)

    self.ui.createConfig.clicked.connect(self.onCreateConfig)
    self.ui.saveConfig.clicked.connect(self.onSaveConfig)
    self.ui.deleteConfig.clicked.connect(self.onDeleteConfig)
    self.ui.configList.itemClicked.connect(self.onConfigItemClick)
  def updateConfigListUi(self, selectFirst=False, name=""):
    """
    Just update the config ui
    """
    self.ui.configList.clear()
    i = 0
    for config in self.configList:
        self.ui.configList.addItem(config.key)
        if config.key == name:
            self.ui.configList.setCurrentRow(i)
            self.onConfigItemClick(self.ui.configList.currentItem())
        i += 1
    if selectFirst:
        self.ui.configList.setCurrentRow(0)
        self.onConfigItemClick(self.ui.configList.currentItem())

  def filterConfig(self, configList):
    for config in configList:
      if config.key.lower() == "encrypted" and self.encryptionObject is None:
          logger.debug(tr("Found encryption in config. Init Module with value " + config.value))
          if self.encryptionObject is None and config.value.lower() != "none":
            pw, ok = QtGui.QInputDialog.getText(None, tr("Password"), tr("Enter Password"), QtGui.QLineEdit.Password)
            if ok:
              pin, ok2 = QtGui.QInputDialog.getText(None, tr("Pin"), tr("Secure your password once more with a pin. This could be a simple nr between 1-100. Leafe empty for no one."), QtGui.QLineEdit.Password)
              if ok2:
                self.encryptionObject = cm(scm.getMod(config.value), pw)
              else:
                self.encryptionObject = cm(scm.getMod(config.value), pw)
      elif config.key.lower() == "filehandlerloglevel":
        logger.removeHandler(fh)
        fh.setLevel(staticConfigTools.getLoggerLevel(config.key))
        logger.addHandler(fh)
      elif config.key.lower() == "consolehandlerloglevel":
        logger.removeHandler(ch)
        ch.setLevel(staticConfigTools.getLoggerLevel(config.value))
        logger.addHandler(ch)
      elif config.key.lower() == "logmessages":
        if config.value.lower() != "true":
          self.logMessages = False

  def onConfigItemClick(self, item):
    for config in self.configList:
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
        pw, ok = QtGui.QInputDialog.getText(None, tr("Password"), tr("Enter Password"), QtGui.QLineEdit.Password)
        if ok:
          staticConfigTools.createConfig(self.ui.configKey.text(), self.ui.configValue.text())
          newCryptManager = cm(scm.getMod(self.ui.configValue.text()), pw)
          self.encryptionObject = newCryptManager
          self.passPhraseChanged.emit(newCryptManager)
      elif key == "logMessages":
       self.saveMessagesChanged.emit(self.ui.configValue.text())
      staticConfigTools.createConfig(self.ui.configKey.text(), self.ui.configValue.text())
      self.configList = staticConfigTools.updateConfigListData()
      self.updateConfigListUi()
  def onSaveConfig(self):
    """
    Save a configuration in db.
    """
    cI = self.ui.configList.currentItem()
    if cI is not None:
      ciText = cI.text()
      outOk = True
      for config in self.configList:
        if config.key == ciText:
          key = self.ui.configKey.text()
          key = key.lower()
          config.save(self.ui.configKey.text(), self.ui.configValue.text())
          if key == "encrypted":
            if self.ui.configValue.text() != "None":
              pw, ok = QtGui.QInputDialog.getText(None, tr("Password"), tr("Enter Password"), QtGui.QLineEdit.Password)
              outOk = ok
              if ok:
                mod = scm.getMod(self.ui.configValue.text())
                if mod is not None:
                  nCm = cm(scm.getMod(self.ui.configValue.text()), pw)
            else:
              nCm = None
            if outOk:
              self.passPhraseChanged.emit(nCm)
              self.encryptionObject = nCm
          elif key == "logMessages":
            self.saveMessagesChanged.emit(self.ui.configValue.text())
      self.configList = staticConfigTools.updateConfigListData()
  def onDeleteConfig(self):
    """
    Delete a config-object from db
    """
    cm = self.ui.configList.currentItem()
    success = False
    for config in self.configList:
        if cm is not None and config.key == cm.text():
            config.delete()
            success = True
    if not success:
        logger.error(tr("Config") + " " + tr("could not") + " be " + tr("saved"))
    else:
        self.configList = staticConfigTools.updateConfigListData()
        self.updateConfigListUi(True)
