from lib.toxTry import *
from lib.toxModels import *
from lib.cryptClass import *
from ui.main import *
singleView = False
singleViewId = -1
#the whole gui...
class toxThread(QtCore.QThread):
 def __init__(self,ui,tmh,tt):
  QtCore.QThread.__init__(self)
  self.tt = tt
 def run(self):
    self.tt.loop()
class Gui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        logger.debug("|GUI| Init Gui")
        self.passPhrase = ""
        self.encryptionObject = None
        self.updateConfigListData()
        if self.encryptionObject is not None and self.encryptionObject.name is not "None":
            pw, okCancel = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
            self.passPhrase = self.encryptionObject.setKey(pw)
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.tmc = toxController("","")
        self.tmh = toxMessageHandler(self.encryptionObject)
        self.tt = ToxTry(self.ui,self.tmh,self.passPhrase)
        self.toxThread = toxThread(self.ui,self.tmh,self.tt)
        #self.updateToxUserList()
        self.toxThread.start()
        self.updateConfigListUi()
        self.ui.configList.itemClicked.connect(self.onConfigItemClick)
        #config-Actions
        self.ui.createConfig.clicked.connect(self.onCreateConfig)
        self.ui.saveConfig.clicked.connect(self.onSaveConfig)
        self.ui.deleteConfig.clicked.connect(self.onDeleteConfig)
        
        
    def updateConfigListUi(self,selectFirst=False,name=""):
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
        logger.debug("|Models| Update configList")
        self.configlist = []
        c2.execute('select * from config;') 
        for row in c2.fetchall():
            self.configlist.append(Config(row[0], row[1], row[2]))
        for config in self.configlist:
            #elif config.key.lower()== "singleviewcname":
                #singleViewName = config.value
            if config.key.lower()== "encrypted" and self.encryptionObject is None:
                logger.debug("Found encryption in config. Init Module with value "+config.value)
                if self.encryptionObject is None:
                    logger.error("create init-eo")
                    self.encryptionObject = cm(scm.getMod(config.value), "encryptionInit")
            elif config.key == "lang" or config.key == "language":
                if os.path.isfile("lang/"+config.value):
                    self.lang="lang/"+config.value
                elif os.path.isfile("lang/"+config.value+".qm"):
                    self.lang="lang/"+config.value+".qm"
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
        if self.ui.configKey.text() == "encrypted" and self.ui.configValue.text() != "None":
            pw, ok = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
            if ok:
              Config.createConfig(self.ui.configKey.text(), self.ui.configValue.text())
              newCryptManager = cm(scm.getMod(self.ui.configValue.text()),pw)
              scm.migrateEncryptionData(newCryptManager, self.tmh)
              self.encryptionObject=newCryptManager
              self.tt.passPhrase = newCryptManager.key
              self.tt.saveLocalData()
        else:
            Config.createConfig(self.ui.configKey.text(), self.ui.configValue.text())
        self.updateConfigListData()
        self.updateConfigListUi()
    def onSaveConfig(self):
        cI = self.ui.configList.currentItem()
        if cI is not None:      ciText = cI.text()
        outOk = True
        for config in self.configlist:
            if config.key == ciText:
                config.save(self.ui.configKey.text(), self.ui.configValue.text())
                if self.ui.configKey.text() == "encrypted":
                    if self.ui.configValue.text() != "None":
                      #logger.error("not none but "+self.ui.configValue.text())
                      #self.tmh.
                      pw, ok = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
                      outOk=ok 
                      if ok:
                        mod = scm.getMod(self.ui.configValue.text())
                        if mod is not None:
                          nCm = cm(scm.getMod(self.ui.configValue.text()), pw)
                          self.tt.passPhrase = nCm.key
                          self.tt.saveLocalData()
                    else:
                      nCm = None
                    if outOk:
                      scm.migrateEncryptionData(nCm, self.tmh)
                      self.encryptionObject = nCm
        self.updateConfigListData()
    def onDeleteConfig(self):
        cm = self.ui.configList.currentItem()
        success = False
        for config in self.configlist:
            if cm is not None and config.key == cm.text():
                config.delete()
                success = True
        if not success:
            logger.error(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
        else:
            self.updateConfigList(True)
 