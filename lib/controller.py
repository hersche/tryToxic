from lib.tryToxic import *
from lib.toxModels import *
from lib.configControll import *
from lib.cryptClass import *
from ui.main import *
from PyQt4 import Qt

class toxThread(QtCore.QThread):
 updateUiUserList = QtCore.pyqtSignal(list)
 clickToxFriend = QtCore.pyqtSignal(str)
 incomingFriendRequest = QtCore.pyqtSignal(str,str)
 incomingFriendMessage = QtCore.pyqtSignal(int,str)
 incomingGroupMessage = QtCore.pyqtSignal(str,str,str,str) 
 incomingGroupInvite = QtCore.pyqtSignal(int,str)
 incomingNameChange = QtCore.pyqtSignal(int,str)
 incomingStatusChange = QtCore.pyqtSignal(int,int)
 incomingStatusMessageChange = QtCore.pyqtSignal(int,str)
 incomingGroupNameChange = QtCore.pyqtSignal(toxGroupUser)
 connectToDHT = QtCore.pyqtSignal(int)
 disconnectToDHT = QtCore.pyqtSignal(int)
 def __init__(self,ui,tmh):
  QtCore.QThread.__init__(self)
  self.tryToxic = None
 def run(self):
    self.tryToxic.loop()
class mainController(QtGui.QMainWindow):
    def __init__(self,app, parent=None):
        QtGui.QWidget.__init__(self, parent)
        logger.debug("|GUI| Init Gui")
        self.passPhrase = ""
        self.app=app
        self.lastMessageName=""
        self.lastMessageColor = 3
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
        self.ui.toxTryFriends.setContextMenuPolicy(2)
        addToGrouchat = QtGui.QAction("Add to groupchat", self.ui.toxTryFriends)
        contextDelete = QtGui.QAction("Delete", self.ui.toxTryFriends)
        #self.ui.toxTryFriends.addAction()
        self.ui.toxTryFriends.addAction(contextDelete)
        self.toxMessagesHandler = toxMessageHandler(self.encryptionObject)
        self.toxThread = toxThread(self.ui,self.toxMessagesHandler)
        self.tryToxic = ToxTry(self.ui,self.toxMessagesHandler,self.passPhrase,self.toxThread)
        self.toxThread.tryToxic = self.tryToxic
        self.toxThread.start()
        self.ui.toxTryUsername.setText(self.tryToxic.name)
        self.setWindowTitle("tryToxic :: "+self.tryToxic.name)
        self.ui.toxTryStatusMessage.setText(self.tryToxic.statusMessage)
        self.ui.toxTryId.setText(self.tryToxic.pubKey)
        self.tryToxic.updateToxUserObjects()
        self.updateToxUsersGuiList(self.tryToxic.toxUserList+self.tryToxic.toxGroupUser)
        self.updateConfigListUi(True)
        #config-Actions
        self.ui.createConfig.clicked.connect(self.onCreateConfig)
        self.ui.saveConfig.clicked.connect(self.onSaveConfig)
        self.ui.deleteConfig.clicked.connect(self.onDeleteConfig)
        self.ui.configList.itemClicked.connect(self.onConfigItemClick)
        
        #catching tryToxic-signals
        contextDelete.triggered.connect(self.onDeleteFriend)
        self.toxThread.updateUiUserList.connect(self.updateToxUsersGuiList)
        self.ui.toxTryFriends.itemClicked.connect(self.onClickToxUser)
        self.ui.toxTrySendButton.clicked.connect(self.onSendToxMessage)
        self.ui.toxTrySendText.returnPressed.connect(self.onSendToxMessage)
        self.ui.toxTryStatusMessage.returnPressed.connect(self.onChangeStatusMessage)
        self.ui.toxTryUsername.returnPressed.connect(self.onSaveToxUsername)
        self.ui.toxTryNewFriendRequest.clicked.connect(self.onNewFriendRequest)
        self.ui.toxTryStatus.currentIndexChanged.connect(self.onChangeOwnStatus)
        self.ui.toxTryDeleteFriend.clicked.connect(self.onDeleteFriend)
        self.ui.toxTryCreateGroupchat.clicked.connect(self.onCreateGroupchat)
        self.toxThread.incomingFriendRequest.connect(self.onIncomingFriendRequest)
        self.toxThread.incomingFriendMessage.connect(self.onIncomingFriendMessage)
        self.toxThread.incomingGroupInvite.connect(self.onIncomingGroupInvite)
        self.toxThread.incomingGroupMessage.connect(self.onIncomingGroupMessage)
        self.toxThread.incomingNameChange.connect(self.onIncomingNameChange)
        self.toxThread.incomingStatusChange.connect(self.onIncomingStatusChange)
        self.toxThread.incomingStatusMessageChange.connect(self.onIncomingStatusMessageChange)
        self.toxThread.incomingGroupNameChange.connect(self.onClickToxUser)
        self.toxThread.connectToDHT.connect(self.onConnectToDHT)
        self.toxThread.disconnectToDHT.connect(self.onDisconnectToDHT)
        
    def onCreateGroupchat(self):
      self.tryToxic.add_groupchat()
      groupNr = -1
      for gnr in self.tryToxic.get_chatlist():
          if gnr not in self.tryToxic.groupNrs:
            groupNr = gnr
      if groupNr != -1:
        peersNr = self.tryToxic.group_number_peers(groupNr)
        self.tryToxic.toxGroupUser.append(toxGroupUser(groupNr,"Group #"+str(groupNr),self.tryToxic.get_client_id(groupNr),0,str(peersNr)+" peoples are online in this groupchat"))
        self.updateToxUsersGuiList(self.tryToxic.toxUserList+self.tryToxic.toxGroupUser)
              
        
    def onDeleteFriend(self):
      if self.tryToxic.currentToxUser is not None:
        self.msgBox.setWindowTitle(tr("REALLY DELETE A USER? AWAY IS AWAY!"))
        self.msgBox.setText(tr("Do you really want to delete ")+self.tryToxic.currentToxUser.name+"?")
        select = self.msgBox.exec()
        if select == QtGui.QMessageBox.Yes:
          if self.tryToxic.currentToxUser.isGroup:
            self.tryToxic.toxGroupUser.remove(self.tryToxic.currentToxUser)
            self.tryToxic.del_groupchat(self.tryToxic.currentToxUser.friendId)
            self.ui.toxTryNotifications.append(tr("Delete groupchat ")+self.tryToxic.currentToxUser.name)
          else:
            self.toxMessagesHandler.deleteUserMessages(self.tryToxic.currentToxUser.friendId)
            self.tryToxic.del_friend(self.tryToxic.currentToxUser.friendId)
            self.tryToxic.updateToxUserObjects()
            self.ui.toxTryNotifications.append(tr("Delete user ")+self.tryToxic.currentToxUser.name)
            self.tryToxic.saveLocalData()
          self.tryToxic.currentToxUser = None
          self.updateToxUsersGuiList(self.tryToxic.toxUserList+self.tryToxic.toxGroupUser)
        
    def onConnectToDHT(self):
      self.ui.toxTryNotifications.append(tr('Connected to DHT.'))
      self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
    
    def onDisconnectToDHT(self): 
      self.ui.toxTryNotifications.append(tr('Disonnected to DHT.'))
      self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
    
    def onIncomingNameChange(self,friendId,name):
      self.ui.toxTryNotifications.append(tr("Name changed to ")+name)
      self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
      tu = self.tryToxic.getToxUserByFriendId(friendId)
      if tu is not None:       tu.name=name
      self.updateToxUsersGuiList(self.tryToxic.toxUserList+self.tryToxic.toxGroupUser)
      
    def onIncomingStatusMessageChange(self,friendId,statusMsg):
      tu = self.tryToxic.getToxUserByFriendId(friendId)
      if tu is not None:       tu.statusMessage=statusMsg
      self.updateToxUsersGuiList(self.tryToxic.toxUserList+self.tryToxic.toxGroupUser)
    def onIncomingStatusChange(self,friendId,status):
      tu = self.tryToxic.getToxUserByFriendId(friendId)
      if tu is not None:         tu.status=status
      self.updateToxUsersGuiList(self.tryToxic.toxUserList+self.tryToxic.toxGroupUser)
      
    def onIncomingGroupMessage(self,timeDateString,groupname,username,message):
      self.app.alert(self,4000)
      #logger.info("Username vs messagename: "+username +" vs "+self.lastMessageName)
      if username == self.lastMessageName:
        self.ui.toxTryChat.append('<div style="background-color:'+self.colorchanger(self.lastMessageColor)+'">['+timeDateString+']               '+message+'</div>')
      else:
        self.lastMessageColor += 1
        if self.lastMessageColor >= 9:
          self.lastMessageColor = 1
        self.ui.toxTryChat.append(" <h3>["+timeDateString+"] "+groupname+"->"+username+":</h3>"+"<div style='background-color:"+self.colorchanger(self.lastMessageColor)+";float: right;'>"+message+"</div>")
        self.lastMessageName = username
        
      self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
      self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
      logger.debug(tr("Recive Groupmessage [")+timeDateString+"] "+groupname+"->"+username+": "+message)
    def onIncomingGroupInvite(self,friendId,groupPk):
        self.app.alert(self,4000)
        fr = self.tryToxic.getToxUserByFriendId(friendId)
        foundExistGroupPk=False
        for gtu in self.tryToxic.toxGroupUser:
          if gtu.pubKey == groupPk:
            foundExistGroupPk=True
        if not foundExistGroupPk:
          self.ui.toxTryNotifications.append(tr("Becoming group invite from ")+fr.name)
          self.tryToxic.join_groupchat(friendId,groupPk)
          groupNr = -1
          for gnr in self.tryToxic.get_chatlist():
              if gnr not in self.tryToxic.groupNrs:
                groupNr = gnr
          try:
            if groupNr != -1:
              peersNr = self.tryToxic.group_number_peers(groupNr)
              self.tryToxic.toxGroupUser.append(toxGroupUser(groupNr,"Group #"+str(groupNr),groupPk,0,str(peersNr)+" peoples are online in this groupchat"))
            self.updateToxUsersGuiList(self.tryToxic.toxUserList+self.tryToxic.toxGroupUser)
          except Exception as e:
            logger.error(tr("Group joining failed: ")+e.args[0])
        else:
          self.ui.toxTryNotifications.append(tr("Becoming group invite from ")+fr.name+tr(", but group is already added"))
          
          
    def onIncomingFriendMessage(self,friendId,message):
        self.app.alert(self,4000)
        ts = strftime('%c', gmtime())
        tu = self.tryToxic.getToxUserByFriendId(friendId)
        self.toxMessagesHandler.addMessage(toxMessage(tu.friendId,ts,message,"False",individualName=tu.name))
        if tu.name is self.lastMessageName:
          self.ui.toxTryChat.append('<div style="background-color:'+self.colorchanger(friendId)+'">['+ts+']               '+message+'</div>')
        else:
          self.ui.toxTryChat.append(" <h3>["+ts+"] "+tu.name+':</h3> '+'<div style="background-color:'+self.colorchanger(friendId)+';float: right;">'+message+'</div>')
          self.lastMessageName = tu.name
        self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
    def onIncomingFriendRequest(self,pk,message):
        self.app.alert(self,4000)
        self.msgBox.setWindowTitle(tr("Recived friendrequest"))
        self.msgBox.setText(tr("Do you want to add ")+pk+tr("? He wrote you: ")+message)
        select = self.msgBox.exec()
        if select == QtGui.QMessageBox.Yes:
          self.tryToxic.add_friend_norequest(pk)
          self.tryToxic.saveLocalData()
          self.tryToxic.updateToxUserObjects()
          self.ui.toxTryNotifications.append(tr('Accept friend request from:')+pk)
          logger.info(tr('Accept friend request from:')+pk)
          self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
        else:
          logger.info(tr('Accept friend request from:')+pk)
    def onChangeOwnStatus(self):
      cT = self.ui.toxTryStatus.currentText()
      if cT == "Online":
        self.tryToxic.set_user_status(self.tryToxic.USERSTATUS_NONE)
      elif cT == "Away":
        self.tryToxic.set_user_status(self.tryToxic.USERSTATUS_AWAY)
      elif cT == "Busy":
        self.tryToxic.set_user_status(self.tryToxic.USERSTATUS_BUSY)
      else:
        self.tryToxic.set_user_status(self.tryToxic.USERSTATUS_INVALID)
          
    def onNewFriendRequest(self):
      pk = QtGui.QInputDialog()
      pubKey = pk.getText(QtGui.QWidget(),tr("Add new friend"),tr("Please enter your friends tox-id"))
      msg = QtGui.QInputDialog()
      message = msg.getText(QtGui.QWidget(),tr("Add a message"),tr("Send your friend a first message too."),text=tr("I would like to add u to my list"))
      try:
          self.tryToxic.add_friend(str(pubKey[0]),str(message[0]))
      except Exception as e:
        
        if e.args[0] == "the friend was already there but the nospam was different":
          self.msgBox.warning(self,tr("User is already exist"), tr("The User you want to add exists already!"))
          pass
        self.msgBox.critical(self,tr("Send friendrequest failed"), tr("Problem on sending friendrequest: ")+e.args[0])
      self.tryToxic.saveLocalData()
      self.tryToxic.updateToxUserObjects()
      self.updateToxUsersGuiList(self.tryToxic.toxUserList+self.tryToxic.toxGroupUser)
      self.ui.toxTryNotifications.append(tr('Your friendrequest is sendet '))
    def onSaveToxUsername(self):
      self.tryToxic.set_name(self.ui.toxTryUsername.text())
      self.tryToxic.saveLocalData()
      self.ui.toxTryNotifications.append(tr('Your username is changed to ')+self.ui.toxTryUsername.text())
      self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
        
    def onChangeStatusMessage(self):
      self.tryToxic.set_status_message(self.ui.toxTryStatusMessage.text())
      self.tryToxic.saveLocalData()
      self.statusMessage = self.ui.toxTryStatusMessage.text()
      self.ui.toxTryNotifications.append(tr('Your status changed to ')+self.ui.toxTryStatusMessage.text())
      self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
        
    def onSendToxMessage(self):
      message = self.ui.toxTrySendText.text()
      try:
        if self.tryToxic.currentToxUser is not None:
          ts = strftime('%c', gmtime())
          friendId = 777
          
          if self.tryToxic.currentToxUser.isGroup:
            self.tryToxic.group_message_send(self.tryToxic.currentToxUser.friendId,message)
          else:
            
            self.tryToxic.send_message(self.tryToxic.currentToxUser.friendId, message)
            sendetToxMessage = toxMessage(self.tryToxic.currentToxUser.friendId,ts,message,"True")
            self.toxMessagesHandler.addMessage(sendetToxMessage)
            if self.lastMessageName == self.tryToxic.name:
              self.ui.toxTryChat.append('<div style="background-color:'+self.colorchanger(friendId)+';  padding-left:5em">['+ts+']       '+message+'</div>')
            else:
              self.lastMessageName = self.tryToxic.name
              self.ui.toxTryChat.append(" <h3>["+ts+"] "+self.tryToxic.name+':</h3> <div style="background-color:'+self.colorchanger(friendId)+';float: right;">'+message+'</div>')
          self.ui.toxTrySendText.clear()
          self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
        else:
          self.ui.toxTryChat.append("["+ts+"] curentuser is none, message sending failed")

      except Exception as e:
        self.msgBox.critical(self,tr("Send Message failed"), tr("Send Message failed: ")+e.args[0])
    
    
    def colorchanger(self,id):
      if id > 2:
        r = (id * 45) % 255
        g = (id * 60) % 255
        b = (id * 210) % 255
      elif id > 4:
        r = (id * 120) % 255
        g = (id * 140) % 255
        b = (id * 45) % 255
      elif id >8:
        r = (id * 180) % 255
        g = (id * 60) % 255
        b = (id * 120) % 255
      elif id >16:
        r = (id * 180) % 255
        g = (id * 180) % 255
        b = (id * 180) % 255
      else:
        r = (id * 180) % 255
        g = (id * 210) % 255
        b = (id * 120) % 255
      
      return "rgb("+str(r)+","+str(g)+","+str(b)+")"
    def onClickToxUser(self,item):
      item=self.ui.toxTryFriends.currentItem()
      txt = item.text()
      self.lastMessageName=""
      mergedList = self.tryToxic.toxUserList + self.tryToxic.toxGroupUser
      for tu in mergedList:
        if tu.name == txt or tu.pubKey == txt:
          self.tryToxic.currentToxUser = tu
          #First userinfos...
          self.ui.toxTryFriendInfos.clear()
          self.ui.toxTryFriendInfos.append(tr("Name: ")+tu.name)
          self.ui.toxTryFriendInfos.append(tr("Public key: ")+tu.pubKey)
          self.ui.toxTryFriendInfos.append(tr("Status: ")+self.tryToxic.statusResolver(tu.status))
          self.ui.toxTryFriendInfos.append(tr("Status message: ")+tu.statusMessage)
          #...then messages
          self.ui.toxTryChat.clear() 
          
          #This part is groupchat
          if tu.isGroup:
            for gcName in self.tryToxic.group_get_names(tu.friendId):
              self.ui.toxTryFriendInfos.append(tr("In group: ")+gcName)
            tmpBeginnString = "<div style='background-color: "+self.colorchanger(tu.friendId)+";float: right;'>"

            for msg in tu.messages:
              if tu.name[0:7] == "Group #" and msg.individualName != "":
                name = msg.individualName
              else:
                name = tu.name
              if self.lastMessageName is not "" and self.lastMessageName == name:
                self.ui.toxTryChat.append(tmpBeginnString+"["+msg.timestamp+"] "+msg.message+"</div>")
              else:
                logger.info(tu.name[0:7])
                if name != "" and name[0:7] != "Group #":
                  self.ui.toxTryChat.append(" <h3>["+msg.timestamp+"] "+name+":</h3> "+tmpBeginnString+msg.message+"</div>")
                  self.lastMessageName = name
                else:
                  self.ui.toxTryChat.append(" <h3>["+msg.timestamp+"] "+str(friendId)+":</h3> "+tmpBeginnString+msg.message+"</div>")
          else:
            #while this is for "usual"chat
            msgList = self.toxMessagesHandler.updateMessages(tu.friendId)
            for msg in msgList:
              #is it me or he?
              #set the name and friendId.. my own is a static (else)
              if "False" == msg.me:
                name=tu.name
                friendId = tu.friendId
              else:
                name=self.tryToxic.name
                friendId = 777
              #is the name from last time setet and the same we have now? when yes, we didn't have to do so much.stay on color and append to chat
              if self.lastMessageName != "" and name == self.lastMessageName:
                tmpBeginnString = "<div style='background-color: "+self.colorchanger(friendId)+"; padding-left:5em'>"
                self.ui.toxTryChat.append(tmpBeginnString+"["+msg.timestamp+"]          "+msg.message+"</div>")
              else:
                if self.lastMessageColor==3:
                  self.lastMessageColor=2
                else:
                  self.lastMessageColor=3
                tmpBeginnString = "<div style='background-color: "+self.colorchanger(friendId)+";float: right;'>"
                self.lastMessageName = name
                self.ui.toxTryChat.append(" <h3>["+msg.timestamp+"] "+name+":</h3>"+tmpBeginnString+msg.message+"</div>")
              
              
    def updateToxUsersGuiList(self, userList):
      self.ui.toxTryFriends.clear()
      ci = self.ui.toxTryFriends.currentItem()
      for tu in userList:
        if tu.name == "":
          item1 = QtGui.QListWidgetItem(tu.pubKey)
        else:
          item1 = QtGui.QListWidgetItem(tu.name)
          
        self.ui.toxTryFriends.addItem(item1)
        item1.setData(3, str(tu.statusMessage))
        if self.tryToxic.get_friend_connection_status(tu.friendId) and self.tryToxic.online:
          item1.setBackgroundColor(QtGui.QColor(51,253,0))
        else:
          item1.setBackgroundColor(QtGui.QColor(253,0,51))
      if ci is not None:          self.ui.toxTryFriends.setItemSelected(ci,True)
       
       
       
    #down here it's just config-stuff   
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
        dbCursor.execute('select * from config;') 
        for row in dbCursor.fetchall():
            self.configlist.append(Config(row[0], row[1], row[2]))
        for config in self.configlist:
            if config.key.lower()== "encrypted" and self.encryptionObject is None:
                logger.debug(tr("Found encryption in config. Init Module with value "+config.value))
                if self.encryptionObject is None:
                    self.encryptionObject = cm(scm.getMod(config.value), "encryptionInit")
            elif config.key == "lang" or config.key == "language":
                if os.path.isfile("lang/"+config.value):
                    self.lang=config.value
                elif os.path.isfile("lang/"+config.value+".qm"):
                    self.lang=config.value+".qm"
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
 