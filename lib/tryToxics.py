from tox import Tox
from lib.toxModels import toxMessage, toxUser,toxGroupUser
from time import sleep,gmtime, strftime
from lib.header import *
import os.path,  sqlite3
from os.path import exists
SERVER = ["54.199.139.199", 33445, "56A1ADE4B65B86BCD51CC73E2CD4E542179F47959FE3E0E21B4B0ACDADE5185520B3E6FC5D64"]

class ToxTry(Tox):
  def __init__(self,ui,tmh,passPhrase):
      self.ui=ui
      self.toxMessagesHandler = tmh
      self.passPhrase = passPhrase
      self.groupToxUsers = []
      self.currentToxUser = None
      self.groupNrs = []
      self.online = False
      if exists('./toxData'):
        if passPhrase == "":
          self.load_from_file('./toxData')
        else:
         self.load_from_file('./toxData',self.passPhrase) 
      else:
        self.set_name("ToxTry")
      self.name = self.get_self_name()
      self.pubKey = self.get_address()
      self.statusMessage = self.get_self_status_message()
      self.ui.toxTryChat.append("<h3>Welcome 2 toxTry</h3> <br /> <p>This is 'just a little by the way'-project, but it's phun to code, so i will continue. Add friends, chat, have phun! <hr />(and dont forget to click one for your friends to get a rid of booring welcomescreen)</p>")
      self.ui.toxTryUsername.setText(self.name)
      self.ui.toxTryStatusMessage.setText(self.statusMessage)
      self.ui.toxTryId.setText(self.pubKey)
      self.updateToxUserObjects()
      self.updateToxUsersGuiList()
      self.saveLocalData()
      self.ui.toxTryFriends.itemClicked.connect(self.onClickToxUser)
      self.ui.toxTrySendButton.clicked.connect(self.onSendToxMessage)
      self.ui.toxTrySendText.returnPressed.connect(self.onSendToxMessage)
      self.ui.toxTryStatusMessage.returnPressed.connect(self.onChangeStatusMessage)
      self.ui.toxTryUsername.returnPressed.connect(self.onSaveToxUsername)
      self.ui.toxTryNewFriendRequest.clicked.connect(self.onNewFriendRequest)
      self.ui.toxTryStatus.currentIndexChanged.connect(self.onChangeOwnStatus)
      self.bootstrap_from_address(SERVER[0], 1, SERVER[1], SERVER[2])
  def getToxGroupUserByFriendId(self,groupFriendId):
    for gtu in self.groupToxUsers:
      if gtu.friendId == groupFriendId:
        return gtu
  def getToxUserByFriendId(self,friendId):
    for tu in self.toxUserList:
      if tu.friendId == friendId:
        return tu
  def saveLocalData(self):
    if self.passPhrase == "":
      self.save_to_file('toxData')
    else:
      self.save_to_file('toxData',self.passPhrase)
    
  
  def onChangeOwnStatus(self):
    cT = self.ui.toxTryStatus.currentText()
    if cT == "Online":
      self.set_user_status(self.USERSTATUS_NONE)
    elif cT == "Away":
      self.set_user_status(self.USERSTATUS_AWAY)
    elif cT == "Busy":
      self.set_user_status(self.USERSTATUS_BUSY)
    else:
      self.set_user_status(self.USERSTATUS_INVALID)
  def onChangeStatusMessage(self):
    self.set_status_message(self.ui.toxTryStatusMessage.text())
    self.saveLocalData()
    self.statusMessage = self.ui.toxTryStatusMessage.text()
    self.ui.toxTryNotifications.append('Your status changed to '+self.ui.toxTryStatusMessage.text())
    self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
  def onNewFriendRequest(self):
    pk = QtGui.QInputDialog()
    pubKey = pk.getText(QtGui.QWidget(),"Add new friend","Please enter your friends tox-id")
    msg = QtGui.QInputDialog()
    message = msg.getText(QtGui.QWidget(),"Add a message","Send your friend a first message too.",text="I would like to add u to my list")
    try:
        self.add_friend(str(pubKey[0]),str(message[0]))
    except Exception as e:
      if e.args[0] == "the friend was already there but the nospam was different":
        logger.error("put a alertbox here. user is already exist")
        pass
      logger.error("Problem on sending friendrequest: "+e.args[0])
    self.saveLocalData()
    self.updateToxUserObjects()
    self.updateToxUsersGuiList()
    self.ui.toxTryNotifications.append('Your friendrequest is sendet ')
  def updateToxUserObjects(self):
    self.toxUserList = []
    for friendId in self.get_friendlist():
      fid = friendId
      self.toxUserList.append(toxUser(fid,self.get_name(fid),self.get_client_id(fid),self.get_user_status(fid),self.get_status_message(fid)))
      
  def updateToxUsersGuiList(self):
    self.ui.toxTryFriends.clear()
    ci = self.ui.toxTryFriends.currentItem()
    mergedList = self.toxUserList + self.groupToxUsers
    for tu in mergedList:
      if tu.name == "":
        item1 = QtGui.QListWidgetItem(tu.pubKey)
        self.ui.toxTryFriends.addItem(item1)
        item1.setData(3, str(tu.statusMessage))
        if tu.status < 2 and self.online:
          item1.setBackgroundColor(QtGui.QColor(51,253,0))
        else:
          item1.setBackgroundColor(QtGui.QColor(253,0,51))
      else:
        item1 = QtGui.QListWidgetItem(tu.name)
        self.ui.toxTryFriends.addItem(item1)
        item1.setData(3, str(tu.statusMessage))
        if tu.status < 2 and self.online:
          item1.setBackgroundColor(QtGui.QColor(51,253,0))
        else:
          item1.setBackgroundColor(QtGui.QColor(253,0,51))
    if ci is not None:          self.ui.toxTryFriends.setItemSelected(ci,True)
    sleep(.1)
        
  def statusResolver(self,inti):
    if inti == 0:
      return "Online"
    elif inti == 1:
      return "Busy"
    elif inti == 2:
      return "Away"
    else:
      return "Invalid"
    
    
  def onSaveToxUsername(self):
    self.set_name(self.ui.toxTryUsername.text())
    self.saveLocalData()
    self.ui.toxTryNotifications.append('Your username is changed to '+self.ui.toxTryUsername.text())
    self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
  def onSendToxMessage(self):
    message = self.ui.toxTrySendText.text()
    try:
      if self.currentToxUser is not None:
        ts = strftime('%Y-%m-%d %H:%M:%S', gmtime())
        if self.currentToxUser.isGroup:
          self.group_message_send(self.currentToxUser.friendId,message)
        else:
          self.send_message(self.currentToxUser.friendId, message)
          self.toxMessagesHandler.addMessage(toxMessage(self.currentToxUser.friendId,ts,message,"True"))
          self.ui.toxTryChat.append("["+ts+"] "+self.name+": "+message)
        self.ui.toxTrySendText.clear()
        self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
    except Exception as e:
      logger.error("Send Message failed: "+e.args[0])
  def onClickToxUser(self,item):
    txt = item.text()
    mergedList = self.toxUserList + self.groupToxUsers
    
    for tu in mergedList:
      if tu.name == txt or tu.pubKey == txt:
        self.currentToxUser = tu
        self.ui.toxTryFriendInfos.clear()
        self.ui.toxTryFriendInfos.append("Name: "+tu.name)
        self.ui.toxTryFriendInfos.append("Public key: "+tu.pubKey)
        self.ui.toxTryFriendInfos.append("Status message: "+self.statusResolver(tu.status))
        self.ui.toxTryFriendInfos.append("Status message: "+tu.statusMessage)
        self.ui.toxTryChat.clear()
        self.toxMessagesHandler.kickUpdate(tu.friendId)
        sleep(0.1)
        if tu.isGroup:
          for msg in tu.messages:
            self.ui.toxTryChat.append("["+msg.timestamp+"] "+tu.name+": "+msg.message)
        else:
          for msg in self.toxMessagesHandler.messages:
            if "False" == msg.me:
              name=tu.name
            else:
              name=self.name
            self.ui.toxTryChat.append("["+msg.timestamp+"] "+name+": "+msg.message)

  def loop(self):
    checked = False
    try:
        while True:
            status = self.isconnected()
            if not checked and status:
                self.ui.toxTryNotifications.append('Connected to DHT.')
                self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
                checked = True
                self.online = True
            if checked and not status:
                self.ui.toxTryNotifications.append('Disconnected from DHT.')
                self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
                #self.connect()
                checked = False

            self.do()
            sleep(0.02)
    except Exception as e:
        logger.error(e.args[0])
        self.saveLocalData()
        self.kill()
  def on_friend_request(self, pk, message):
      self.ui.toxTryNotifications.append('Friend request from %s: %s' % (pk, message))
      self.add_friend_norequest(pk)
      self.saveLocalData()
      self.updateToxUserObjects()
      self.updateToxUsersGuiList()
      self.ui.toxTryNotifications.append('Accepted friend request')
      self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)

    
  def on_friend_message(self, friendId, message):
      ts = strftime('%Y-%m-%d %H:%M:%S', gmtime())
      tu = self.getToxUserByFriendId(friendId)
      self.toxMessagesHandler.addMessage(toxMessage(tu.friendId,ts,message,"False"))
      self.ui.toxTryChat.append("["+ts+"] "+tu.name+": "+message)
      self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
      
  def on_name_change(self,friendId,name):
      self.ui.toxTryNotifications.append("Name changed to "+name)
      self.ui.toxTryNotifications.moveCursor(QtGui.QTextCursor.End)
      tu = self.getToxUserByFriendId(friendId)
      if tu is not None:       tu.name=name
      self.updateToxUsersGuiList()
  def on_user_status(self, friendId,status):  
      tu = self.getToxUserByFriendId(friendId)
      if tu is not None:         tu.status=status
      self.updateToxUsersGuiList()
      
  def on_status_message(self,friendId, statusMessage):
      tu = self.getToxUserByFriendId(friendId)
      if tu is not None:       tu.statusMessage=statusMessage
      self.updateToxUsersGuiList()  
  def on_group_invite(self,friendId,groupPk):
    fr = self.getToxUserByFriendId(friendId)
    self.ui.toxTryNotifications.append("Becoming group invite from "+fr.name)
    self.join_groupchat(friendId,groupPk)
    groupNr = -1
    for gnr in self.get_chatlist():
        if gnr not in self.groupNrs:
          groupNr = gnr
    try:
      if groupNr != -1:
        peersNr = self.group_number_peers(groupNr)
        self.groupToxUsers.append(toxGroupUser(groupNr,"Group #"+str(groupNr),groupPk,0,str(peersNr)+" peoples are online in this groupchat"))
      self.updateToxUsersGuiList()
    except Exception as e:
      logger.error("Group joining failed: "+e.args[0])
    
  def on_group_message(self,group_number, friend_group_number, message):
    gtu = self.getToxGroupUserByFriendId(group_number)
    ts = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    gtu.messages.append(toxMessage(gtu.friendId,message,ts,"False"))
    sendingPeerUser = None
    try:
      if len(gtu.peerList)>0:
        for peerUser in gtu.peerList:
            if peerUser.friendId == friend_group_number and peerUser.name is not "":
              sendingPeerUser = peerUser
            elif peerUser.friendId == friend_group_number and peerUser.name == "":
              peerUser.name = self.group_peername(group_number,friend_group_number)
              sendingPeerUser = peerUser
            elif friend_group_number not in gtu.checkedPeerIds:
              name = self.group_peername(group_number,friend_group_number)
              sendingPeerUser = toxUser(friend_group_number,name,"",0,"")
              gtu.peerList.append(sendingPeerUser)
              gtu.checkedPeerIds.append(friend_group_number)
      else:
        name = self.group_peername(group_number,friend_group_number)
        sendingPeerUser = toxUser(friend_group_number,name,"",0,"")
        gtu.checkedPeerIds.append(friend_group_number)
        gtu.peerList.append(sendingPeerUser)
    except Exception as e:
        logger.error("workFail on resolving name" + str(e.args[0]))
        logger.error("Fail to get name" + str(e.args[0]))
        pass
    if sendingPeerUser is not None and sendingPeerUser.name is not "":
      name = sendingPeerUser.name
    else:
      name = str(friend_group_number)
    self.ui.toxTryChat.append("["+ts+"] "+gtu.name+"->"+name+": "+message)
    self.ui.toxTryChat.moveCursor(QtGui.QTextCursor.End)
    logger.error("Recive Groupmessage ["+str(friend_group_number)+"]  Name: "+str(name)+" |  message"+message)