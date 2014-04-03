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
 incomingGroupMessage = QtCore.pyqtSignal(int,int,str) 
 incomingGroupInvite = QtCore.pyqtSignal(int,str)
 incomingNameChange = QtCore.pyqtSignal(int,str)
 incomingStatusChange = QtCore.pyqtSignal(int,int)
 incomingStatusMessageChange = QtCore.pyqtSignal(int,str)
 incomingGroupNameChange = QtCore.pyqtSignal()
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
        self.setEnabled(True)
        self.ui.toxTryFriends.setContextMenuPolicy(2)
        self.ui.toxTryGroups.setContextMenuPolicy(2)
        self.subMenu = QtGui.QMenu()
        self.addToGroupchat = QtGui.QAction("Add to groupchat", self.ui.toxTryFriends)
        self.addToGroupchat.setShortcutContext (3)
        
        self.addToGroupchat.setMenu(self.subMenu)
        contextDelete = QtGui.QAction("Delete", self.ui.toxTryFriends)
        self.ui.toxTryGroups.addAction(contextDelete)
        self.ui.toxTryFriends.addAction(self.addToGroupchat)
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
        self.updateToxUsersGuiList(self.tryToxic.toxUserList)
        self.updateConfigListUi(True)
        #config-Actions
        self.ui.createConfig.clicked.connect(self.onCreateConfig)
        self.ui.saveConfig.clicked.connect(self.onSaveConfig)
        self.ui.deleteConfig.clicked.connect(self.onDeleteConfig)
        self.ui.configList.itemClicked.connect(self.onConfigItemClick)
        
        #catching tryToxic-signals
        contextDelete.triggered.connect(self.onDeleteFriend)
        self.toxThread.updateUiUserList.connect(self.updateToxUsersGuiList)
        self.ui.toxTryDeleteGroup.clicked.connect(self.onDeleteFriend)
        self.ui.toxTryFriends.itemClicked.connect(self.onClickToxUser)
        self.ui.toxTryGroups.itemClicked.connect(self.onClickToxGroup)
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
        
        
    def closeEvent(self, event):
      reply = QtGui.QMessageBox.question(self, tr('Really leave tryToxic?'),
          tr("Are you sure to quit?"), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
      if reply == QtGui.QMessageBox.Yes:
        self.tryToxic.kill()
        event.accept()
      else:
          event.ignore()
    def onContextClick(self, obj):
      sender = self.sender()
      text = sender.text()
      userItem = self.ui.toxTryFriends.currentItem()
      userText = userItem.text()
      user = None
      for usr in self.tryToxic.toxUserList:
        if userText == usr.name:
          user = usr
      if user is not None:
        if len(text) == 11 and text[0:10] == "ownGroup #":
          id = text[10:11]
        elif len(text) == 8 and text[0:7] == "Group #":
          logger.info("could we invite users to not-own-groups? i don't know")
          id = text[7:8]
        logger.info(str(id))
        gtu = self.tryToxic.getToxGroupUserByFriendId(int(id))
        self.tryToxic.invite_friend(user.friendId, gtu.friendId)
        logger.info("getting grouppubkey: "+gtu.pubKey)
    def onCreateGroupchat(self):
      self.tryToxic.add_groupchat()
      groupNr = -1
      for gnr in self.tryToxic.get_chatlist():
          if gnr not in self.tryToxic.groupNrs:
            groupNr = gnr
      if groupNr != -1:
        peersNr = self.tryToxic.group_number_peers(groupNr)
        self.tryToxic.toxGroupUser.append(toxGroupUser(groupNr,"ownGroup #"+str(groupNr),self.tryToxic.get_client_id(groupNr),0,str(peersNr)+" peoples are online in this groupchat"))
        groupAction = QtGui.QAction("ownGroup #"+str(groupNr), self.ui.toxTryFriends)
        self.subMenu.addActions([groupAction])
        groupAction.triggered.connect(self.onContextClick)
        self.updateToxGroupsGuiList(self.tryToxic.toxGroupUser)

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
            self.updateToxGroupsGuiList(self.tryToxic.toxGroupUser)
          else:
            self.toxMessagesHandler.deleteUserMessages(self.tryToxic.currentToxUser.friendId)
            self.tryToxic.del_friend(self.tryToxic.currentToxUser.friendId)
            self.tryToxic.updateToxUserObjects()
            self.ui.toxTryNotifications.append(tr("Delete user ")+self.tryToxic.currentToxUser.name)
            self.tryToxic.saveLocalData()
            self.updateToxUsersGuiList(self.tryToxic.toxUserList)
          self.tryToxic.currentToxUser = None
        
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
      self.updateToxUsersGuiList(self.tryToxic.toxUserList)
      
    def onIncomingStatusMessageChange(self,friendId,statusMsg):
      tu = self.tryToxic.getToxUserByFriendId(friendId)
      if tu is not None:       tu.statusMessage=statusMsg
      self.updateToxUsersGuiList(self.tryToxic.toxUserList)
    def onIncomingStatusChange(self,friendId,status):
      tu = self.tryToxic.getToxUserByFriendId(friendId)
      if tu is not None:         tu.status=status
      self.updateToxUsersGuiList(self.tryToxic.toxUserList)

    def onIncomingGroupMessage(self,group_number, friend_group_number, message):
      gtu = self.tryToxic.getToxGroupUserByFriendId(group_number)
      timeDateString = strftime('%c', gmtime())
      sendingPeerUser = None
      try:
        if len(gtu.peerList)>0:
          for peerUser in gtu.peerList:
              if peerUser.friendId == friend_group_number and peerUser.name is not "":
                sendingPeerUser = peerUser
              elif peerUser.friendId == friend_group_number and peerUser.name == "":
                peerUser.name = self.tryToxic.group_peername(group_number,friend_group_number)
                sendingPeerUser = peerUser
              elif friend_group_number not in gtu.checkedPeerIds:
                username = self.tryToxic.group_peername(group_number,friend_group_number)
                sendingPeerUser = toxUser(friend_group_number,username,"",0,"")
                gtu.peerList.append(sendingPeerUser)
                gtu.checkedPeerIds.append(friend_group_number)
        else:
          username = self.tryToxic.group_peername(group_number,friend_group_number)
          sendingPeerUser = toxUser(friend_group_number,username,"",0,"")
          gtu.checkedPeerIds.append(friend_group_number)
          gtu.peerList.append(sendingPeerUser)
      except Exception as e:
          logger.error(tr("Fail to get name") + str(e.args[0]))
          pass
      if sendingPeerUser is not None and sendingPeerUser.name is not "":
        username = sendingPeerUser.name
      else:
        username = str(friend_group_number)
      gtu.messages.append(toxMessage(gtu.friendId,message,timeDateString,"False",individualName=username))
      self.app.alert(self,4000)
      #logger.info("Username vs messagename: "+username +" vs "+self.lastMessageName)
      if username == self.lastMessageName:
        self.ui.toxTryChat.append('<div style="background-color:'+self.colorchanger(sendingPeerUser.friendId)+'">['+timeDateString+']               '+message+'</div>')
      else:
        self.ui.toxTryChat.append(" <h3>["+timeDateString+"] "+username+":</h3>"+"<div style='background-color:"+self.colorchanger(sendingPeerUser.friendId)+";float: right;'>"+message+"</div>")
        self.lastMessageName = username
      self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
      logger.debug(tr("Recive Groupmessage [")+timeDateString+"] "+gtu.name+"->"+username+": "+message)
    def onIncomingGroupInvite(self,friendId,groupPk):
        self.app.alert(self,4000)
        fr = self.tryToxic.getToxUserByFriendId(friendId)
        foundExistGroupPk=False
        for gtu in self.tryToxic.toxGroupUser:
          if gtu.pubKey == groupPk:
            foundExistGroupPk=True
        if not foundExistGroupPk:
          self.ui.toxTryNotifications.append(tr("Becoming group invite from ")+fr.name)
          self.msgBox.setWindowTitle(tr("Invited to groupchat"))
          self.msgBox.setText(tr("Do you want to enter groupchat from ")+fr.name+"?")
          select = self.msgBox.exec()
          if select == QtGui.QMessageBox.Yes:
            self.tryToxic.join_groupchat(friendId,groupPk)
            groupNr = -1
            for gnr in self.tryToxic.get_chatlist():
                if gnr not in self.tryToxic.groupNrs:
                  groupNr = gnr
            try:
              if groupNr != -1:
                groupAction = QtGui.QAction("Group #"+str(groupNr), self.ui.toxTryFriends)
                self.subMenu.addActions([groupAction])
                groupAction.triggered.connect(self.onContextClick)
                peersNr = self.tryToxic.group_number_peers(groupNr)
                self.tryToxic.toxGroupUser.append(toxGroupUser(groupNr,"Group #"+str(groupNr),groupPk,0,str(peersNr)+" peoples are online in this groupchat"))
              self.updateToxGroupsGuiList(self.tryToxic.toxGroupUser)
            except Exception as e:
              logger.error(tr("Group joining failed: ")+e.args[0])
        else:
          self.ui.toxTryNotifications.append(tr("Becoming group invite from ")+fr.name+tr(", but group is already added"))
          
          
    def onIncomingFriendMessage(self,friendId,message):
        self.app.alert(self,4000)
        ts = strftime('%c', gmtime())
        tu = self.tryToxic.getToxUserByFriendId(friendId)
        self.toxMessagesHandler.addMessage(toxMessage(tu.friendId,ts,message,"False"))
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
      self.updateToxUsersGuiList(self.tryToxic.toxUserList)
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
    
    def onClickToxGroup(self,item=None):
      if item is not None:
        txt = item.text()
      elif self.tryToxic.currentToxUser is not None:
        if self.tryToxic.currentToxUser.isGroup :
          self.tryToxic.currentToxUser.statusMessage = str(self.tryToxic.group_number_peers(self.tryToxic.currentToxUser.friendId))+ " users are online"
        txt = self.tryToxic.currentToxUser.name
      else:
        return
      self.lastMessageName=""
      for tu in self.tryToxic.toxGroupUser:
        if tu.name == txt or tu.pubKey == txt:
          self.tryToxic.currentToxUser = tu
          #First userinfos...
          self.ui.toxTryFriendInfos.clear()
          self.ui.toxTryFriendInfos.append(tr("Group: ")+tu.name)
          self.ui.toxTryFriendInfos.append(tr("Public key: ")+tu.pubKey)
          self.ui.toxTryFriendInfos.append(tr("Status: ")+self.tryToxic.statusResolver(tu.status))
          self.ui.toxTryFriendInfos.append(tr("Status message: ")+tu.statusMessage)
          #...then messages
          self.ui.toxTryChat.clear() 
          
          #This part is groupchat
          self.ui.toxTryFriendInfos.append(tr("Userlist: "))
          for gcName in self.tryToxic.group_get_names(tu.friendId):
            self.ui.toxTryFriendInfos.append(gcName)
            
          
          for msg in tu.messages:
            
            if msg.individualName != "":
              name = msg.individualName
            else:
              name = tu.name
            usr = tu.getPeerByName(name)

            if self.lastMessageName == name:
              tmpBeginnString = "<div style='background-color: "+self.colorchanger(self.lastMessageColor)+";float: right;'>"
              self.ui.toxTryChat.append(tmpBeginnString+"["+msg.timestamp+"] "+msg.message+"</div>")
            else:
              if usr is not None:
                self.lastMessageColor = usr.friendId
              else:
                self.lastMessageColor+=1
                if self.lastMessageColor > 13:
                  self.lastMessageColor = 1
              tmpBeginnString = "<div style='background-color: "+self.colorchanger(self.lastMessageColor)+";float: right;'>"
              if name != "":
                self.ui.toxTryChat.append(" <h3>["+msg.timestamp+"] "+name+":</h3> "+tmpBeginnString+msg.message+"</div>")
                self.lastMessageName = name
              else:
                self.ui.toxTryChat.append(" <h3>["+msg.timestamp+"] "+str(tu.name)+"(worse):</h3> "+tmpBeginnString+msg.message+"</div>")

  
    def onClickToxUser(self,item=None):
      if item is not None:
        txt = item.text()
      elif self.tryToxic.currentToxUser is not None:
        txt = self.tryToxic.currentToxUser.name
      else:
        return
      self.lastMessageName=""
      for tu in self.tryToxic.toxUserList:
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
      
      
    def updateToxGroupsGuiList(self, groupList):
      self.ui.toxTryGroups.clear()
      ci = self.ui.toxTryGroups.currentItem()
      for tu in groupList:
        if tu.name == "":
          item1 = QtGui.QListWidgetItem(tu.pubKey)
        else:
          item1 = QtGui.QListWidgetItem(tu.name)
          
        self.ui.toxTryGroups.addItem(item1)
        item1.setData(3, str(tu.statusMessage))
        if self.tryToxic.get_friend_connection_status(tu.friendId) and self.tryToxic.online:
          item1.setBackgroundColor(QtGui.QColor(51,253,0))
        else:
          item1.setBackgroundColor(QtGui.QColor(253,0,51))
      if ci is not None:          self.ui.toxTryGroups.setItemSelected(ci,True)
       
       
       
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
 