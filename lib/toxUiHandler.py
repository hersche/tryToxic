from PyQt4 import QtCore, QtGui
from lib.header import *
from lib.toxModels import *
import html,io,os,binascii
from time import strftime, gmtime

class toxUiHandler(QtCore.QObject):
  appNotify = saveMessagesChanged = QtCore.pyqtSignal()
  def __init__(self,ui,tryToxic,toxMessagesHandler,toxThread):
    QtCore.QObject.__init__(self)
    self.ui = ui
    self.tryToxic = tryToxic
    self.lastMessageName=""
    self.lastMessageColor = 3
    self.currentToxUser = None
    self.toxMessagesHandler = toxMessagesHandler
    self.toxThread = toxThread
    self.groupNrs = []
    #set and create rightclickmenu for friendlist and grouplist
    self.ui.toxTryFriends.setContextMenuPolicy(2)
    self.ui.toxTryGroups.setContextMenuPolicy(2)
    self.groupMenu = QtGui.QMenu()
    self.addToGroupchat = QtGui.QAction(tr("Add to groupchat"), self.ui.toxTryFriends)
    self.addToGroupchat.setShortcutContext (3)
    self.addToGroupchat.setMenu(self.groupMenu)
    contextDeleteHistory = QtGui.QAction(tr("Delete history"), self.ui.toxTryFriends)
    contextDeleteFriend = QtGui.QAction(tr("Delete"), self.ui.toxTryFriends)
    contextSendFile = QtGui.QAction(tr("Send File"), self.ui.toxTryFriends)
    self.ui.toxTryGroups.addAction(contextDeleteFriend)
    self.ui.toxTryGroups.addAction(contextDeleteHistory)
    self.ui.toxTryFriends.addAction(self.addToGroupchat)
    self.ui.toxTryFriends.addAction(contextDeleteFriend)
    self.ui.toxTryFriends.addAction(contextDeleteHistory)
    self.ui.toxTryFriends.addAction(contextSendFile)
    
    #setup ui
    self.ui.toxTryUsername.setText(self.tryToxic.name)
    self.ui.toxTryStatusMessage.setText(self.tryToxic.statusMessage)
    self.ui.toxTryId.setText(self.tryToxic.pubKey)
    self.generateDnsId(self.tryToxic.pubKey)
    #init toxUsers
    self.tryToxic.updateToxUserObjects()
    self.updateToxUsersGuiList(self.tryToxic.toxUserList)
    
    self.msgBox = QtGui.QMessageBox()
    self.msgBox.addButton(QtGui.QMessageBox.Yes)
    self.msgBox.addButton(QtGui.QMessageBox.No)
    #catching tryToxic-signals

    contextSendFile.triggered.connect(self.onSendFile)
    contextDeleteFriend.triggered.connect(self.onDeleteFriend)
    contextDeleteHistory.triggered.connect(self.onDeleteFriendHistory)
    self.toxThread.updateUiUserList.connect(self.updateToxUsersGuiList)
    self.ui.toxTryDeleteGroup.clicked.connect(self.onDeleteFriend)
    self.ui.toxTryFriends.currentItemChanged.connect(self.onClickToxUser)
    self.ui.toxTryGroups.currentItemChanged.connect(self.onClickToxGroup)
    self.ui.toxTrySendButton.clicked.connect(self.onSendToxMessage)
    self.ui.toxTrySendText.returnPressed.connect(self.onSendToxMessage)
    self.ui.toxTryStatusMessage.returnPressed.connect(self.onChangeStatusMessage)
    self.ui.toxTryUsername.returnPressed.connect(self.onSaveToxUsername)
    self.ui.toxTryNewFriendRequest.clicked.connect(self.onNewFriendRequest)
    self.ui.toxTryStatus.currentIndexChanged.connect(self.onChangeOwnStatus)
    self.ui.toxTryDeleteFriend.clicked.connect(self.onDeleteFriend)
    self.ui.toxTryCreateGroupchat.clicked.connect(self.onCreateGroupchat)
    self.toxThread.incomingFriendFile.connect(self.onIncomingFriendFile)
    self.toxThread.incomingFriendRequest.connect(self.onIncomingFriendRequest)
    self.toxThread.incomingFriendMessage.connect(self.onIncomingFriendMessage)
    self.toxThread.incomingGroupInvite.connect(self.onIncomingGroupInvite)
    self.toxThread.incomingGroupMessage.connect(self.onIncomingGroupMessage)
    self.toxThread.incomingNameChange.connect(self.onIncomingNameChange)
    self.toxThread.incomingStatusChange.connect(self.onIncomingStatusChange)
    self.toxThread.incomingOnlineStatus.connect(self.onIncomingOnlineStatus)
    self.toxThread.incomingStatusMessageChange.connect(self.onIncomingStatusMessageChange)
    self.toxThread.incomingGroupNameChange.connect(self.onClickToxUser)
    self.toxThread.connectToDHT.connect(self.onConnectToDHT)
    self.toxThread.disconnectToDHT.connect(self.onDisconnectToDHT)
    
  def onDeleteFriendHistory(self):
    """
    In contextmenu, when you delete the messages or a history of a friend
    """
    if self.currentToxUser is not None:
      self.msgBox.setWindowTitle(tr("Really want to delete history/log?"))
      self.msgBox.setText(tr("Do you really want to delete ")+self.currentToxUser.name+"'s message-history?")
      select = self.msgBox.exec()
      if select == QtGui.QMessageBox.Yes:
        if self.currentToxUser.isGroup:
          self.currentToxUser.messages = []
          self.onClickToxGroup()
          self.ui.toxTryNotifications.append(tr("Clear group-history out of RAM"))
        else:
          self.toxMessagesHandler.deleteUserMessages(self.currentToxUser.friendId)
          self.tryToxic.updateToxUserObjects()
          self.ui.toxTryNotifications.append(tr("Delete ")+self.currentToxUser.name+"'s history")
          self.tryToxic.saveLocalData()
          self.updateToxUsersGuiList(self.tryToxic.toxUserList)

  def onDeleteFriend(self):
    """
    When you want to delete a friend.
    """
    if self.currentToxUser is not None:
      self.msgBox.setWindowTitle(tr("REALLY DELETE A USER? AWAY IS AWAY!"))
      self.msgBox.setText(tr("Do you really want to delete ")+self.currentToxUser.name+"?")
      select = self.msgBox.exec()
      if select == QtGui.QMessageBox.Yes:
        if self.currentToxUser.isGroup:
          self.tryToxic.toxGroupUser.remove(self.currentToxUser)
          self.tryToxic.del_groupchat(self.currentToxUser.friendId)
          self.ui.toxTryNotifications.append(tr("Delete groupchat ")+self.currentToxUser.name)
          self.updateToxGroupsGuiList(self.tryToxic.toxGroupUser)
        else:
          self.toxMessagesHandler.deleteUserMessages(self.currentToxUser.friendId)
          self.tryToxic.del_friend(self.currentToxUser.friendId)
          self.tryToxic.updateToxUserObjects()
          self.ui.toxTryNotifications.append(tr("Delete user ")+self.currentToxUser.name)
          self.tryToxic.saveLocalData()
          self.updateToxUsersGuiList(self.tryToxic.toxUserList)
        self.currentToxUser = None
        
  def onClickToxGroup(self,item=None):
    """
    When you click a toxGroup. Change gui.
    """
    if item is not None:
      txt = item.text()
    elif self.currentToxUser is not None:
      if self.currentToxUser.isGroup :
        self.currentToxUser.statusMessage = str(self.tryToxic.group_number_peers(self.currentToxUser.friendId))+ " users are online"
      txt = self.currentToxUser.name
    else:
      return
    self.lastMessageName=""
    for tu in self.tryToxic.toxGroupUser:
      if tu.name == txt or tu.pubKey == txt:
        self.currentToxUser = tu
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
              self.ui.toxTryChat.append(" <h3>["+msg.timestamp+"] "+name+":</h3> "+tmpBeginnString+html.escape(msg.message)+"</div>")
              self.lastMessageName = name
            else:
              self.ui.toxTryChat.append(" <h3>["+msg.timestamp+"] "+str(tu.name)+"(worse):</h3> "+tmpBeginnString+html.escape(msg.message)+"</div>")


  def onClickToxUser(self,item=None):
    """
    When you click a toxUser
    """
    if item is not None:
      txt = item.text()
    elif self.currentToxUser is not None:
      txt = self.currentToxUser.name
    else:
      return
    self.lastMessageName=""
    for tu in self.tryToxic.toxUserList:
      if tu.name == txt or tu.pubKey == txt:
        self.currentToxUser = tu
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
            self.ui.toxTryChat.append(tmpBeginnString+"["+msg.timestamp+"]          "+html.escape(msg.message)+"</div>")
          else:
            if self.lastMessageColor==3:
              self.lastMessageColor=2
            else:
              self.lastMessageColor=3
            tmpBeginnString = "<div style='background-color: "+self.colorchanger(friendId)+";float: right;'>"
            self.lastMessageName = name
            self.ui.toxTryChat.append(" <h3>["+msg.timestamp+"] "+name+":</h3>"+tmpBeginnString+html.escape(msg.message)+"</div>")
            
  def onIncomingFriendFile(self,friendId, fileId, fileSize, filename):
    """
    on incoming friend-toxFile-signal.
    This is the request, where user could cancel reciving
    """
    tu = self.tryToxic.getToxUserByFriendId(friendId)
    self.msgBox.setWindowTitle(tr("Filerequest"))
    self.msgBox.setText(tr("Do you want to recive ")+filename+" from "+tu.name+"?")
    select = self.msgBox.exec()
    if select == QtGui.QMessageBox.Yes:
      folder = os.path.expanduser("~/toxFiles/")
      logger.info("Get request to become a file:"+filename+" and try to create folder "+folder)
      if os.path.exists(folder) is not True:
        os.makedirs(folder)
      try:
        f = io.FileIO(folder+filename,"wb+")
      except Exception as e:
        logger.error("Old venom-bug (18.4.14), last sign of recived filename got NUL at end. workarounded.")
        logger.info(folder+filename[:-1])
        f = io.FileIO(folder+filename[:-1],"wb+")
      tu.files.append(toxFile(fileId,filename,folder,fileSize,f,1))
      self.tryToxic.file_send_control(friendId, 1, fileId, self.tryToxic.FILECONTROL_ACCEPT)
    else:
      self.tryToxic.file_send_control(friendId, 1, fileId, self.tryToxic.FILECONTROL_KILL)
      
  def onSendFile(self):
    """
    When you want to send a file to a user
    """
    fullPath = QtGui.QFileDialog.getOpenFileName(None, 'Open file',os.path.expanduser("~/"))
    f=io.FileIO(fullPath,"rb")
    filename=os.path.basename(fullPath)
    folder=os.path.dirname(fullPath)
    friendId = self.currentToxUser.friendId
    if self.currentToxUser.isOnline:
      fileSplitSize = self.tryToxic.file_data_size(friendId)
      fileNr = self.tryToxic.new_file_sender(friendId, fileSplitSize, filename)
      tf = toxFile(fileNr,filename,folder,len(f.read()),f,0)
      tf.splitSize = fileSplitSize
      self.currentToxUser.files.append(tf)
    else:
      logger.info("DEBUG: "+fullPath)
        
  def onContextGroupInviteClick(self, obj):
    """
    This gets active, when you invite a friend to a group-chat.
    """
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
    """
    When you create a groupchat.
    """
    self.tryToxic.add_groupchat()
    groupNr = -1
    for gnr in self.tryToxic.get_chatlist():
      if gnr not in self.groupNrs:
        groupNr = gnr
        self.groupNrs.append(gnr)
    if groupNr != -1:
      peersNr = self.tryToxic.group_number_peers(groupNr)
      self.tryToxic.toxGroupUser.append(toxGroupUser(groupNr,"ownGroup #"+str(groupNr),self.tryToxic.get_client_id(groupNr),0,str(peersNr)+" peoples are online in this groupchat"))
      groupAction = QtGui.QAction("ownGroup #"+str(groupNr), self.ui.toxTryFriends)
      self.groupMenu.addActions([groupAction])
      groupAction.triggered.connect(self.onContextGroupInviteClick)
      self.updateToxGroupsGuiList(self.tryToxic.toxGroupUser)


      
  def onConnectToDHT(self):
    self.ui.toxTryNotifications.append(tr('Connected to DHT'))
    self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
  
  def onDisconnectToDHT(self): 
    self.ui.toxTryNotifications.append(tr('Disonnected to DHT'))
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
    
  def onIncomingOnlineStatus(self,friendId,onlineStatus):
    tu = self.tryToxic.getToxUserByFriendId(friendId)
    if onlineStatus:
      tu.isOnline = True
    else:
      tu.isOnline = False
    logger.info("incomming onlinestatus for user "+tu.name+" Online seems "+str(onlineStatus))
    self.updateToxUsersGuiList(self.tryToxic.toxUserList)
  def onIncomingStatusChange(self,friendId,status):
    tu = self.tryToxic.getToxUserByFriendId(friendId)
    if tu is not None:         tu.status=status
    tu.isOnline = self.tryToxic.get_friend_connection_status(tu.friendId)
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
    self.appNotify.emit()
    #logger.info("Username vs messagename: "+username +" vs "+self.lastMessageName)
    if username == self.lastMessageName:
      self.ui.toxTryChat.append('<div style="background-color:'+self.colorchanger(sendingPeerUser.friendId)+'">['+timeDateString+']               '+html.escape(message)+'</div>')
    else:
      self.ui.toxTryChat.append(" <h3>["+timeDateString+"] "+username+":</h3>"+"<div style='background-color:"+self.colorchanger(sendingPeerUser.friendId)+";float: right;'>"+html.escape(message)+"</div>")
      self.lastMessageName = username
    self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
    logger.debug(tr("Recive Groupmessage [")+timeDateString+"] "+gtu.name+"->"+username+": "+message)
    
  def onIncomingGroupInvite(self,friendId,groupPk):
    self.appNotify.emit()
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
            if gnr not in self.groupNrs:
              groupNr = gnr
              self.groupNrs.append(gnr)
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
    self.appNotify.emit()
    ts = strftime('%c', gmtime())
    tu = self.tryToxic.getToxUserByFriendId(friendId)
    self.toxMessagesHandler.addMessage(toxMessage(tu.friendId,ts,message,"False"))
    if tu.name is self.lastMessageName:
      self.ui.toxTryChat.append('<div style="background-color:'+self.colorchanger(friendId)+'">['+ts+'] '+html.escape(message)+'</div>')
    else:
      self.ui.toxTryChat.append(" <h3>["+ts+"] "+tu.name+':</h3> '+'<div style="background-color:'+self.colorchanger(friendId)+';float: right;">'+html.escape(message)+'</div>')
      self.lastMessageName = tu.name
    self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
      
  def onIncomingFriendRequest(self,pk,message):
    self.appNotify.emit()
    self.msgBox.setWindowTitle(tr("Recived friendrequest"))
    self.msgBox.setText(tr("Do you want to add ")+pk+tr("? He wrote you: ")+message)
    select = self.msgBox.exec()
    if select == QtGui.QMessageBox.Yes:
      self.tryToxic.add_friend_norequest(pk)
      self.tryToxic.saveLocalData()
      self.tryToxic.updateToxUserObjects()
      self.updateToxGroupsGuiList(self.tryToxic.toxGroupUser)
      self.ui.toxTryNotifications.append(tr('Accept friend request from:')+pk)
      logger.info(tr('Accept friend request from:')+pk)
      self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
    else:
      logger.info(tr('Denied friend request from:')+pk)
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
    message = pk.getText(QtGui.QWidget(),tr("Add a message"),tr("Send your friend a first message too."),text=tr("I would like to add u to my list"))
    try:
        if pubKey[0][0:7] == "v=tox2;":
          pin = pk.getText(QtGui.QWidget(),tr("V2 Tox-ID"),tr("Please enter your friends pin to do the full request"))
          self.tryToxic.add_friend(self.generateKey(str(pubKey[0]),str(pin[0])),str(message[0]))
        else:
          self.tryToxic.add_friend(str(pubKey[0]),str(message[0]))
    except Exception as e:
      
      if e.args[0] == "the friend was already there but the nospam was different":
        self.msgBox.warning(self,tr("User is already exist"), tr("The User you want to add exists already!"))
        pass
      self.msgBox.critical(None,tr("Send friendrequest failed"), tr("Problem on sending friendrequest: ")+e.args[0])
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
      if self.currentToxUser is not None:
        ts = strftime('%c', gmtime())
        friendId = 777
        if self.currentToxUser.isGroup:
          self.tryToxic.group_message_send(self.currentToxUser.friendId,message)
        else:
          
          self.tryToxic.send_message(self.currentToxUser.friendId, message)
          sendetToxMessage = toxMessage(self.currentToxUser.friendId,ts,message,"True")
          self.toxMessagesHandler.addMessage(sendetToxMessage)
          if self.lastMessageName == self.tryToxic.name:
            self.ui.toxTryChat.append('<div style="background-color:'+self.colorchanger(friendId)+';  padding-left:5em">['+ts+'] '+html.escape(message)+'</div>')
          else:
            self.lastMessageName = self.tryToxic.name
            self.ui.toxTryChat.append(" <h3>["+ts+"] "+self.tryToxic.name+':</h3> <div style="background-color:'+self.colorchanger(friendId)+';float: right;">'+html.escape(message)+'</div>')
        self.ui.toxTrySendText.clear()
        self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
      else:
        self.ui.toxTryChat.append("["+ts+"] curentuser is none, message sending failed")

    except Exception as e:
      self.msgBox.critical(None,tr("Send Message failed"), tr("Send Message failed: ")+e.args[0])
  
  
  def colorchanger(self,id):
    """
    Try to change color for chats
    return (r,g,b)
    """
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
  def generateKey(self, dns,pin):
    """
    Temporary method to generate lookupkey out of dns and pin
    """
    #dns.trim("'")
    pub = dns[11:75]
    logger.info(pub)
    check = dns[83:87]
    logger.info(check)
    nospam = binascii.a2b_base64(pin+"==")
    nospam =str(binascii.hexlify(nospam))
    nospam = nospam[2:-1]
    nospam = nospam.upper()
    logger.info(nospam)
    logger.info("lookupkey="+pub+nospam+check)
    return pub+nospam+check
  def generateDnsId(self,key):
    """
    Temporary method to generate dns and pin out of lookupkey
    """
    if len(key)==76:
      logger.info("init-lookupkey: "+key)
      pub = key[0:64]
      nospam = key[64:72]
      checksum = key[71:76]
      dns="v=tox2;pub="+pub+";check="+checksum
      logger.info(dns)
      binData = binascii.unhexlify(nospam)
      b64data= binascii.b2a_base64(binData)
      b64data=str(b64data)
      b64data=b64data[2:-5]
      b64dta=b64data.rstrip('=')
      self.ui.toxTryNotifications.append(dns)
      self.ui.toxTryNotifications.append("Your pin is "+b64data)
      #self.generateKey(dns,b64data)
    else:
      logger.info("Wrong key size")

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
        if tu.status == 0:
          item1.setBackgroundColor(QtGui.QColor(51,253,0))
        elif tu.status == 1:
          item1.setBackgroundColor(QtGui.QColor(229, 213, 0))
        else:
          item1.setBackgroundColor(QtGui.QColor(229, 107, 0))
      else:
        item1.setBackgroundColor(QtGui.QColor(255,0,0))
    if ci is not None:          self.ui.toxTryFriends.setItemSelected(ci,True)
    
    
  def updateToxGroupsGuiList(self, groupList):
    """
    update grouplist, but just ui
    """
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
        if tu.status == 0:
          item1.setBackgroundColor(QtGui.QColor(51,253,0))
        elif tu.status == 1:
          item1.setBackgroundColor(QtGui.QColor(229, 213, 0))
        else:
          item1.setBackgroundColor(QtGui.QColor(229, 107, 0))
      else:
        item1.setBackgroundColor(QtGui.QColor(255,0,0))
    if ci is not None:          self.ui.toxTryGroups.setItemSelected(ci,True)
      
               