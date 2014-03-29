import os.path,sqlite3
from lib.header import *
from PyQt4.QtCore import pyqtSlot,pyqtSignal
fileExist = True
if os.path.isfile('toxMessages.db') == False:
    #..und ggf umgestellt..
    fileExist = False
#..denn sqlite3.connect erstellt immer ein file!
db2 = sqlite3.connect('toxMessages.db')
#aber wir brauchen ja den cursor, um die db initialisieren zu können.
c2 = db2.cursor()
if fileExist == False:
    c2.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, friendId text, timestamp text, message text, me text, encrypted text)")
    c2.execute("CREATE TABLE config (coid INTEGER PRIMARY KEY,  key TEXT UNIQUE,  value TEXT, encrypted text)")
class toxMessageHandler(QtCore.QObject):
  toxMessageArrived = pyqtSignal(object)
  toxMessageDbUpdate = pyqtSignal(object)
  def __init__(self,eo):
    QtCore.QObject.__init__(self)
    self.cachedToxMessages=[]
    self.tmpFriendId = -1
    self.eo = eo
    self.toxMessageArrived.connect(self.flushMessage)
    self.toxMessageDbUpdate.connect(self.updateMessages)
  def saveAllMessages(self,eo):
    for msg in self.messages:
        if eo != None:
          if msg.me == "True":
            me = "True"
          else:
            me = "False"
          c2.execute("UPDATE messages SET friendId=?, timestamp=?,message=?,me=?,encrypted=? WHERE id=?",  (self.eo.encrypt(msg.friendId), self.eo.encrypt(msg.timestamp), self.eo.encrypt(msg.message),self.eo.encrypt(me),eo.name, msg.dbId))
        else:
          c2.execute("UPDATE messages SET friendId=?, timestamp=?,message=?,me=?,encrypted=? WHERE id=?",  (msg.friendId, msg.timestamp, msg.message,me,-1, msg.dbId))
    db2.commit()
          
      
        
    
  def addMessage(self,toxMessage):
    self.cachedToxMessages.append(toxMessage)
    self.toxMessageArrived.emit(toxMessage)
    
  def kickUpdate(self,friendId):
      self.tmpFriendId = friendId
      #logger.error("update kicket")
      self.toxMessageDbUpdate.emit(friendId)
  def updateMessages(self,friendId=-1):
    self.messages = []
    self.tmpDecryptData = []
    if friendId != -1:
      if self.eo is not None and self.eo.name is not "None":
        c2.execute('select id,friendId from messages;')
        for tmp in c2.fetchall():
          #logger.error("get Ids first "+str(friendId)+" vs "+str(self.eo.decrypt(tmp[1])))
          if str(friendId) == str(self.eo.decrypt(tmp[1])):
            #logger.error("append "+str(tmp[0]))
            self.tmpDecryptData.append(tmp[0])
            c2.execute('select * from messages;')
      else:
        c2.execute('select * from messages where friendId='+str(self.tmpFriendId)+';')
    else:
        c2.execute('select * from messages;')
    #logger.error("decrypt started or so..?!?")
    for msg in c2.fetchall():
      #logger.error("Secondround")
      if friendId != -1:
        if self.eo != None:
          #logger.error("get second,real connect "+str(msg[0])+" vs "+str(self.tmpDecryptData))
          if msg[0] in self.tmpDecryptData:
            self.messages.append(toxMessage(self.eo.decrypt(msg[1]),self.eo.decrypt(msg[2]),self.eo.decrypt(msg[3]),self.eo.decrypt(msg[4]),msg[0]))
        else:
          self.messages.append(toxMessage(msg[1],msg[2],msg[3],msg[4],msg[0]))
      else:
        if self.eo != None:
            self.messages.append(toxMessage(self.eo.decrypt(msg[1]),self.eo.decrypt(msg[2]),self.eo.decrypt(msg[3]),self.eo.decrypt(msg[4]),msg[0]))
        else:
            self.messages.append(toxMessage(msg[1],msg[2],msg[3],msg[4],msg[0]))
  def flushMessage(self):
    try:
      #logger.error("signal catched, write now!")
      for toxMessage in self.cachedToxMessages:
        if toxMessage.me:       tmpBoolMe = "True"
        else:   tmpBoolMe = "False"
        if self.eo != None:
            c2.execute("INSERT INTO messages (friendId, timestamp, message,me, encrypted) VALUES (?,?,?,?,?)",  ( self.eo.encrypt(toxMessage.friendId), self.eo.encrypt(toxMessage.timestamp),  self.eo.encrypt(toxMessage.message),self.eo.encrypt(tmpBoolMe), self.eo.name))
        else:
            c2.execute("INSERT INTO messages (friendId, timestamp, message,me, encrypted) VALUES (?,?,?,?,?)",  ( toxMessage.friendId, toxMessage.timestamp,  toxMessage.message,tmpBoolMe, "-1"))
      db2.commit()
      self.cachedToxMessages=[]
    except sqlite3.Error as e:
      logger.error("An DB-error occurred: "+e.args[0])
      
class Config:
    #"CREATE TABLE config (coid INTEGER PRIMARY KEY,  key TEXT,  value TEXT)
    def __init__(self,  id,  key,  value):
        logger.debug("|Models| Init config "+key+"="+value)
        self.id = id
        self.key = key
        self.value = value
    @staticmethod
    def createConfig(key, value):
        try:
            c2.execute("INSERT INTO config (key, value) VALUES (?,?);",  (key, value))
            db2.commit()
            #self.updateConfigList()
        except sqlite3.Error as e:
            logger.error("An DB-error occurred: "+e.args[0])
            return -1
    @staticmethod
    def getConfigByKey(key):
      c2.execute("SELECT * FROM config WHERE key=?;",(key, ))
      for row in c2.fetchall():
        return Config(row[0],row[1],row[2])
      return None
    def save(self, key,  value):
        try:
            c2.execute("UPDATE config SET key=?, value=? WHERE coid=?",  (key, value,  self.id))
            db2.commit()
        except sqlite3.Error as e:
            logger.error("An DB-error occurred: "+e.args[0])("An DB-error occurred: "+e.args[0])
    def delete(self):
        try:
            c2.execute("DELETE FROM config WHERE coid=?",  (self.id, ))
            db2.commit()
        except sqlite3.Error as e:
            logger.error("An DB-error occurred: "+e.args[0])("An DB-error occurred: "+e.args[0])
   
    
class toxMessage:
  def __init__(self,friendId,message, timestamp,me,dbId=-1):
      if me == 0:
        self.me = False
      else:
        self.me = True
      #logger.error("message created, timestamp "+timestamp)
      self.friendId=friendId
      self.message = message
      self.timestamp = timestamp
      self.dbId=dbId

class toxUser:
  def __init__(self,friendId,name,pubKey,status,statusMessage):
    self.friendId = friendId
    self.name = name
    self.pubKey = pubKey
    self.status = status
    self.statusMessage = statusMessage
    self.isGroup = False
    
class toxGroupUser(toxUser):
  def __init__(self,friendId,name,pubKey,status,statusMessage,peerList=[]):
    toxUser.__init__(self,friendId,name,pubKey,status,statusMessage)
    self.peerList = peerList
    self.messages = []
    self.checkedPeerIds = []
    
    self.isGroup = True
 