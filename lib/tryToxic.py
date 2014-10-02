
from pytox import Tox
from lib.toxModels import *
from time import sleep
from lib.header import *
import os

class ToxTry(Tox):
  """
  The tox-handler-class
  """
  def __init__(self, passPhrase, thread):
    """
    ui --- ui is from mainController
    passPhrase --- or key, password
    thread --- to connect to it's signals
    """
    SERVER = ["144.76.60.215", 33445, "04119E835DF3E78BACF0F84235B300546AF8B936F035185E2A8E9E0A67C8924F"]
    self.passPhrase = passPhrase
    self.toxGroupUser = []
    self.thread = thread
    if os.path.exists('./toxData'):
      if passPhrase == "":
        self.load_from_file('./toxData')
      else:
        self.load_from_file('./toxData', self.passPhrase)
    else:
      self.set_name("tryToxics")
    self.name = self.get_self_name()
    self.pubKey = self.get_address()
    self.statusMessage = self.get_self_status_message()
    self.online = False
    self.userColor = {}
    self.updateToxUserObjects()
    self.thread.updateUiUserList.emit(self.toxUserList)
    self.saveLocalData()
    self.bootstrap_from_address(SERVER[0], SERVER[1], SERVER[2])
  def getToxGroupUserByFriendId(self, groupFriendId):
    """
    Get a toxGroup by friendId
    return toxGroupUser
    """
    for gtu in self.toxGroupUser:
      if gtu.friendId == groupFriendId:
        return gtu

  def getToxUserByFriendId(self, friendId):
    """
    Get a toxUser by friendId
    return toxUser
    """
    for tu in self.toxUserList:
      if tu.friendId == friendId:
        return tu
  def saveLocalData(self):
    if self.passPhrase == "":
      self.save_to_file('toxData')
    else:
      self.save_to_file('toxData', self.passPhrase)

  def updateToxUserObjects(self):
    """
    update toxUser-data-objects.
    """
    self.toxUserList = []
    for friendId in self.get_friendlist():
      fid = friendId
      self.toxUserList.append(toxUser(fid, self.get_name(fid), str(self.get_client_id(fid)), self.get_user_status(fid), self.get_status_message(fid)))

  def statusResolver(self, inti):
    """
    Status-resolving of online-statuses.
    Give int,
    return str
    """
    if inti == 0:
      return tr("Online")
    elif inti == 1:
      return tr("Busy")
    elif inti == 2:
      return tr("Away")
    else:
      return tr("Invalid")
  def loop(self):
    """
    mainloop of tox!
    """
    checked = False
    while True:
      try:
        status = self.isconnected()
        if not checked and status:
            self.thread.connectToDHT.emit(1)
            checked = True
            self.online = True
        if checked and not status:
            logger.error(tr("Disconnected from DHT"))
            checked = False
            raise
        self.do()
        sleep(0.02)
      except Exception as e:
        logger.error(tr("Catch exception in toxLoop: ") + str(e))
        continue
  def on_friend_request(self, pk, message):
    self.thread.incomingFriendRequest.emit(pk, message)


  def on_friend_message(self, friendId, message):
    logger.debug(tr("Friendmessage changed"))
    self.thread.incomingFriendMessage.emit(friendId, message)

  def on_file_send_request(self, friendId, fileId, fileSize, filename):
    self.thread.incomingFriendFile.emit(friendId, fileId, fileSize, filename)

  def on_file_data(self, friend_number, file_number, data):
    logger.info("Recive data now")
    tu = self.getToxUserByFriendId(friend_number)
    tf = tu.getFileById(file_number)
    tf.fileObject.write(data)
  def on_file_control(self, friend_number, receive_send, file_number, control_type, data):
    """ Callback for everykind of file-changes. Big method!
    receive_send : 0 = rec, 1 = send
    """
    logger.info("Do a filecontrol now, r/s " + str(receive_send) + " controll type " + str(control_type))
    if receive_send == 0:
      if control_type == self.FILECONTROL_FINISHED:
        tu = self.getToxUserByFriendId(friend_number)
        tf = tf = tu.getFileById(file_number)
        if data is not None:
          # tf.fileobject.write(data)
          logger.info("receive restdata of file: " + str(data))
        logger.info("fileobject recived")
        tf.fileObject.close()
      elif control_type == self.FILECONTROL_PAUSE:
        pass
      elif control_type == self.FILECONTROL_RESUME_BROKEN:
        logger.info("get from broken again")
        self.f.write(data)
      else:
        pass
    elif receive_send == 1:
      if control_type == self.FILECONTROL_ACCEPT:
        logger.info("user accept filerequest, sending")
        tu = self.getToxUserByFriendId(friend_number)
        toxFile = tu.getFileById(file_number)
        if toxFile.fileObject is not None:
          completed = False
          sended = 0
          fileSize = toxFile.size
          data = toxFile.fileObject.read()
          count = 0
          while not completed:
            if sended == fileSize:
              logger.info("complete")
              self.file_send_control(friend_number, 1, file_number, self.FILECONTROL_FINISHED)
              completed = True
            else:
              next = sended + toxFile.splitSize
              if next > fileSize:
                next = fileSize
              logger.info(str(next) + " / " + str(toxFile.splitSize))
              try:
                subData = data[sended:next]
                # logger.info(str(friend_number)+" "+str(file_number)+" DATA: "+subData)
                self.file_send_data(friend_number, file_number, subData)
              except Exception as e:
                logger.error("file-send-data interrupted: " + str(e.args))
              sended = next

  def on_name_change(self, friendId, name):
    logger.debug(tr("Name changed"))
    self.thread.incomingNameChange.emit(friendId, name)
  def on_user_status(self, friendId, status):
    self.thread.incomingStatusChange.emit(friendId, status)
  def on_connection_status(self, friendId, status):
    self.thread.incomingOnlineStatus.emit(friendId, status)

  def on_group_namelist_change(self, group_number, peer_number, change):
    gtu = self.getToxGroupUserByFriendId(group_number)
    self.thread.incomingGroupNameChange.emit()

  def on_status_message(self, friendId, statusMessage):
    self.thread.incomingStatusMessageChange.emit(friendId, statusMessage)

  def on_group_invite(self, friendId, groupPk):
    self.thread.incomingGroupInvite.emit(friendId, groupPk)

  def on_group_message(self, group_number, friend_group_number, message):
    self.thread.incomingGroupMessage.emit(group_number, friend_group_number, message)
