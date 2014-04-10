from lib.header import *
from PyQt4.QtCore import pyqtSlot,pyqtSignal
# The next 4 classes are just to organize data. toxmessages is a message, 
# only special is that toxmessages by groupusers dont have dbid (theyr just in ram), but individual name
class toxMessage:
  """
  A data-message-class handled by tox.
  """
  def __init__(self,friendId,message, timestamp,me,dbId=-1,individualName=""):
    """
    dbId is only setted when it's reloaded min. once from db (only toxuser, but not groupuser has db)
    individualName is only setted when user is a group. It's done to make other names possible than GroupBot #?
    """
    if me == False or me == "False":
      self.me = "False"
    else:
      self.me = "True"
    self.friendId=friendId
    self.message = message
    self.timestamp = timestamp
    self.dbId=dbId
    self.individualName=individualName
      
class toxFile:
  """
  A data-file-class handled by tox.
  """
  def __init__(self,id,filename,folder,size,fileObject,sr):
    """
    id -- fileId or file_number
    fileObject -- any io-object created on accept request or send in controller
    sr -- send recive. 0 = send, 1 = recive
    """
    self.id = id
    self.filename = filename
    self.folder = folder
    self.size = size
    self.sr = sr
    self.splitSize=-1
    self.fileObject = fileObject

class toxUser:
  """    
  toxUser is a individual in binary/dual/non-group-chat. It's a data-object too.
  """
  def __init__(self,friendId,name,pubKey,status,statusMessage):
    self.friendId = friendId
    self.name = name
    self.pubKey = pubKey
    self.status = status
    self.statusMessage = statusMessage
    self.isGroup = False
    self.isOnline = False
    self.files = []
    
  def getFileById(self,id):
    """
    Get a toxFile-Object by it's fileId
    return toxFile or None
    """
    tf = None
    for toxFile in self.files:
      if toxFile.id == id:
        return toxFile
#a special version of toxuser, representing a group, which contains itself a list of toxUser
class toxGroupUser(toxUser):
  """
  A groupUser inherits from toxUser, because they are to big parts similiar.
  You could make a diffrent by static variable isGroup.
  """
  def __init__(self,friendId,name,pubKey,status,statusMessage,peerList=[]):
    toxUser.__init__(self,friendId,name,pubKey,status,statusMessage)
    self.peerList = peerList
    # This is a list of toxUser's
    self.messages = []
    self.checkedPeerIds = []
    self.isGroup = True
  def getPeerByName(self,name):
    """
    Get a temporary toxUser from groupchat.
    return toxUser or None
    """
    for peer in self.peerList:
      if peer.name == name:
        return peer
      else:
        return None
 

class toxMessageHandler(QtCore.QObject):
  """
  a handler for saving, manage and giving back the messages.
  @TODO make this class enable/disable-able (?) in settings.
  """
  def __init__(self,eo):
    """
    eo -- encryptionObject - give it also when it's None!!
    """
    QtCore.QObject.__init__(self)
    self.cachedToxMessages=[]
    self.tmpFriendId = -1
    self.eo = eo
  
  def saveAllMessages(self,eo):
    """
    reSave all messages. Mainly used by scm's method migrateEncryptedData
    eo -- is the NEW encryptionObject
    """
    for msg in self.updateMessages():
      if msg.me == "True":
        me = "True"
      else:
        me = "False"
      if eo != None:
        dbCursor.execute("UPDATE messages SET friendId=?, timestamp=?,message=?,me=?,encrypted=? WHERE id=?",  (eo.encrypt(msg.friendId), eo.encrypt(msg.timestamp), eo.encrypt(msg.message),eo.encrypt(me),eo.name, msg.dbId))
      else:
        dbCursor.execute("UPDATE messages SET friendId=?, timestamp=?,message=?,me=?,encrypted=? WHERE id=?",  (msg.friendId, msg.timestamp, msg.message,me,-1, msg.dbId))
    db.commit()
    
  def addMessage(self,toxMessage):
    """
    add toxMessage to the database
    """
    if self.eo != None:
        dbCursor.execute("INSERT INTO messages (friendId, timestamp, message,me, encrypted) VALUES (?,?,?,?,?)",  ( self.eo.encrypt(toxMessage.friendId), self.eo.encrypt(toxMessage.timestamp),  self.eo.encrypt(toxMessage.message),self.eo.encrypt(toxMessage.me), self.eo.name))
    else:
        dbCursor.execute("INSERT INTO messages (friendId, timestamp, message,me, encrypted) VALUES (?,?,?,?,?)",  ( toxMessage.friendId, toxMessage.timestamp,  toxMessage.message,toxMessage.me, "-1"))
    db.commit()
    
  def deleteUserMessages(self,friendId):
    """
    Delete a user's history/messages from database
    """
    msgList = self.updateMessages(friendId)
    for msg in msgList:
      dbCursor.execute("DELETE FROM messages WHERE id=?",  (msg.dbId, ))
    db.commit()
  def updateMessages(self,friendId=-1):
    """
    updateMessages get messages from database to RAM.
    friendId -- if setted -1 / you dont set it, it will load the messages of ALL users.
    It's recommended to use a friendId!
    """
    messages = []
    self.tmpDecryptData = []
    if friendId != -1:
      if self.eo is not None and self.eo.name is not "None":
        dbCursor.execute('select id,friendId from messages;')
        for tmp in dbCursor.fetchall():
          if str(friendId) == str(self.eo.decrypt(tmp[1])):
            self.tmpDecryptData.append(tmp[0])
            dbCursor.execute('select * from messages;')
      else:
        dbCursor.execute('select * from messages where friendId=?;',(str(friendId), ))
    else:
        dbCursor.execute('select * from messages;')
    for msg in dbCursor.fetchall():
      if friendId != -1:
        if self.eo != None:
          if msg[0] in self.tmpDecryptData:
            messages.append(toxMessage(self.eo.decrypt(msg[1]),self.eo.decrypt(msg[2]),self.eo.decrypt(msg[3]),self.eo.decrypt(msg[4]),msg[0]))
        else:
          messages.append(toxMessage(msg[1],msg[2],msg[3],msg[4],msg[0]))
      else:
        if self.eo != None:
            messages.append(toxMessage(self.eo.decrypt(msg[1]),self.eo.decrypt(msg[2]),self.eo.decrypt(msg[3]),self.eo.decrypt(msg[4]),msg[0]))
        else:
            messages.append(toxMessage(msg[1],msg[2],msg[3],msg[4],msg[0]))
    return messages
   
    
