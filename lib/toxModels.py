from lib.header import *
from PyQt4.QtCore import pyqtSlot,pyqtSignal
# The next 3 classes are just to organize data. toxmessages is a message, 
# only special is that toxmessages by groupusers dont have dbid (theyr just in ram), but individual name
class toxMessage:
  def __init__(self,friendId,message, timestamp,me,dbId=-1,individualName=""):
      if me == False or me == "False":
        self.me = "False"
      else:
        self.me = "True"
      self.friendId=friendId
      self.message = message
      self.timestamp = timestamp
      self.dbId=dbId
      self.individualName=individualName
#toxUser is a individual, in groupchat or saved, single friend
class toxUser:
  def __init__(self,friendId,name,pubKey,status,statusMessage):
    self.friendId = friendId
    self.name = name
    self.pubKey = pubKey
    self.status = status
    self.statusMessage = statusMessage
    self.isGroup = False
#a special version of toxuser, representing a group, which contains itself a list of toxUser
class toxGroupUser(toxUser):
  def __init__(self,friendId,name,pubKey,status,statusMessage,peerList=[]):
    toxUser.__init__(self,friendId,name,pubKey,status,statusMessage)
    self.peerList = peerList
    self.messages = []
    self.checkedPeerIds = []
    self.isGroup = True
  def getPeerByName(self,name):
    for peer in self.peerList:
      if peer.name == name:
        return peer
      else:
        return None
 
#a handler for saving, manage and giving back the messages.
# @TODO make this class enable/disable-able (?) in settings..
class toxMessageHandler(QtCore.QObject):
  def __init__(self,eo):
    QtCore.QObject.__init__(self)
    self.cachedToxMessages=[]
    self.tmpFriendId = -1
    self.eo = eo
    
  def saveAllMessages(self,eo):
    for msg in self.updateMessages():
        if eo != None:
          if msg.me == "True":
            me = "True"
          else:
            me = "False"
          dbCursor.execute("UPDATE messages SET friendId=?, timestamp=?,message=?,me=?,encrypted=? WHERE id=?",  (eo.encrypt(msg.friendId), eo.encrypt(msg.timestamp), eo.encrypt(msg.message),eo.encrypt(me),eo.name, msg.dbId))
        else:
          dbCursor.execute("UPDATE messages SET friendId=?, timestamp=?,message=?,me=?,encrypted=? WHERE id=?",  (msg.friendId, msg.timestamp, msg.message,me,-1, msg.dbId))
    db.commit()
    
  def addMessage(self,toxMessage):
    if self.eo != None:
        dbCursor.execute("INSERT INTO messages (friendId, timestamp, message,me, encrypted) VALUES (?,?,?,?,?)",  ( self.eo.encrypt(toxMessage.friendId), self.eo.encrypt(toxMessage.timestamp),  self.eo.encrypt(toxMessage.message),self.eo.encrypt(toxMessage.me), self.eo.name))
    else:
        dbCursor.execute("INSERT INTO messages (friendId, timestamp, message,me, encrypted) VALUES (?,?,?,?,?)",  ( toxMessage.friendId, toxMessage.timestamp,  toxMessage.message,toxMessage.me, "-1"))
    db.commit()
  def deleteUserMessages(self,friendId):
    msgList = self.updateMessages(friendId)
    for msg in msgList:
      dbCursor.execute("DELETE FROM messages WHERE id=?",  (msg.dbId, ))
    db.commit()
  def updateMessages(self,friendId=-1):
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
   
    
