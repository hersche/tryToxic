
from tox import Tox

from lib.toxModels import toxMessage, toxUser,toxGroupUser
from time import sleep,gmtime, strftime
from lib.header import *
import os.path,  sqlite3
from os.path import exists
SERVER = ["144.76.60.215", 33445, "04119E835DF3E78BACF0F84235B300546AF8B936F035185E2A8E9E0A67C8924F"]

class ToxTry(Tox):
  def __init__(self,ui,tmh,passPhrase,thread):
      self.toxMessagesHandler = tmh
      self.passPhrase = passPhrase
      self.toxGroupUser = []
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
      self.userColor = {}
      self.updateToxUserObjects()
      self.thread.updateUiUserList.emit(self.toxUserList+self.toxGroupUser)
      self.saveLocalData()
      self.bootstrap_from_address(SERVER[0], 1, SERVER[1], SERVER[2])
  def getToxGroupUserByFriendId(self,groupFriendId):
    for gtu in self.toxGroupUser:
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
      return tr("Online")
    elif inti == 1:
      return tr("Busy")
    elif inti == 2:
      return tr("Away")
    else:
      return tr("Invalid")
  def loop(self):
    checked = False
    try:
      while True:
          status = self.isconnected()
          if not checked and status:
              self.thread.connectToDHT.emit(1)
              checked = True
              self.online = True
          if checked and not status:
              logger.error(tr("Disconnected from DHT"))
              checked = False
          self.do()
          sleep(0.02)
    except Exception as e:
      logger.error(tr("Disconnected from DHT : ")+e.args[0])
      pass
  def on_friend_request(self, pk, message):
    self.thread.incomingFriendRequest.emit(pk,message)

    
  def on_friend_message(self, friendId, message):
    logger.debug(tr("Friendmessage changed"))
    self.thread.incomingFriendMessage.emit(friendId,message)
    
  def on_file_send_request(self,friendId, fileId, fileSize, filename):
    logger.info("Get request to become a file:"+filename)
    self.f = open('/tmp/output/'+filename, 'rb')
    self.roundsControl = 0
    self.roundsData=0
    self.file_send_control(friendId, 0, fileId, self.FILECONTROL_ACCEPT)
  def on_file_data(self,friend_number, file_number, data):
    logger.info("Would recive file now! "+str(type(data)+" Round +"+str(self.roundsData)))
    self.roundsData+=1
    self.f.writelines(bytes(data, 'ascii'))
  def on_file_control(self,friend_number, receive_send, file_number, control_type, data):
    logger.info("Do a filecontrol now, round :"+str(self.roundsControl))
    self.roundsControl+=1
    if receive_send == 1:
      if control_type == self.FILECONTROL_FINISHED:
        logger.info("file recived")
        self.f.close()
      elif control_type == self.FILECONTROL_PAUSE:
        pass
      elif control_type == self.FILECONTROL_RESUME_BROKEN:
        logger.info("get from broken again")
        self.f.write(data)
      else:
        pass

      
  def on_name_change(self,friendId,name):
    logger.debug(tr("Name changed"))
    self.thread.incomingNameChange.emit(friendId,name)
  def on_user_status(self, friendId,status):  
    self.thread.incomingStatusChange.emit(friendId,status)
  def on_connection_status(self,friendId, status):
    self.thread.incomingOnlineStatus.emit(friendId,status)
  
  def on_group_namelist_change(self,group_number, peer_number, change):
    gtu = self.getToxGroupUserByFriendId(group_number)
    self.thread.incomingGroupNameChange.emit()
      
  def on_status_message(self,friendId, statusMessage):
    self.thread.incomingStatusMessageChange.emit(friendId,statusMessage)
       
  def on_group_invite(self,friendId,groupPk):
    self.thread.incomingGroupInvite.emit(friendId, groupPk)
    
  def on_group_message(self,group_number, friend_group_number, message):
    self.thread.incomingGroupMessage.emit(group_number, friend_group_number, message)
