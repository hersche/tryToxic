from tox import Tox
from lib.toxModels import toxMessage, toxUser,toxGroupUserList
from time import sleep,gmtime, strftime
from lib.header import *
import os.path,  sqlite3
from os.path import exists
SERVER = ["144.76.60.215", 33445, "04119E835DF3E78BACF0F84235B300546AF8B936F035185E2A8E9E0A67C8924F"]

class ToxTry(Tox):
  #friendListClicked = QtCore.pyqtSignal(QtGui.QListWidgetItem)
  #sendButtonClicked = QtCore.pyqtSignal()
  
  def __init__(self,ui,tmh,passPhrase,thread):
      self.toxMessagesHandler = tmh
      self.passPhrase = passPhrase
      self.toxGroupUserList = []
      self.currentToxUser = None
      self.groupNrs = []
      self.thread = thread
      if exists('./toxData'):
        if passPhrase == "":
          self.load_from_file('./toxData')
        else:
         self.load_from_file('./toxData',self.passPhrase) 
      else:
        self.set_name("tryToxics")
      self.name = self.get_self_name()
      self.pubKey = self.get_address()
      self.statusMessage = self.get_self_status_message()
      self.online = False
      

      self.updateToxUserObjects()
      #self.updateToxUsersGuiList()
      self.thread.updateUiUserList.emit(self.toxUserList+self.toxGroupUserList)
      self.saveLocalData()
      self.bootstrap_from_address(SERVER[0], 1, SERVER[1], SERVER[2])
  def getToxGroupUserByFriendId(self,groupFriendId):
    for gtu in self.toxGroupUserList:
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

  def updateToxUserObjects(self):
    self.toxUserList = []
    for friendId in self.get_friendlist():
      fid = friendId
      self.toxUserList.append(toxUser(fid,self.get_name(fid),self.get_client_id(fid),self.get_user_status(fid),self.get_status_message(fid)))
  def statusResolver(self,inti):
    if inti == 0:
      return "Online"
    elif inti == 1:
      return "Busy"
    elif inti == 2:
      return "Away"
    else:
      return "Invalid"
  def loop(self):
    checked = False
    #try:
    while True:
        status = self.isconnected()
        if not checked and status:
            self.thread.connectToDHT.emit(1)
            checked = True
            self.online = True
        if checked and not status:
            logger.error("Disconnected from DHT")
            checked = False
        #print("some output")
        self.do()
        sleep(0.02)
    #except Exception as e:
        #logger.error("Disconnected from DHT : "+e.args[0])
        #self.saveLocalData()
        #self.kill()
  def on_friend_request(self, pk, message):
    self.thread.incomingFriendRequest.emit(pk,message)

    
  def on_friend_message(self, friendId, message):
    self.thread.incomingFriendMessage.emit(friendId,message)

      
  def on_name_change(self,friendId,name):
    self.thread.incomingNameChange.emit(friendId,name)
  def on_user_status(self, friendId,status):  
    self.thread.incomingStatusChange.emit(friendId,status)
      
  def on_status_message(self,friendId, statusMessage):
    self.thread.incomingStatusMessageChange.emit(friendId,statusMessage)
       
  def on_group_invite(self,friendId,groupPk):
    self.thread.incomingGroupInvite.emit(friendId, groupPk)
    
  def on_group_message(self,group_number, friend_group_number, message):
    self.thread.incomingGroupMessage.emit(group_number,friend_group_number,message)