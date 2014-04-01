from lib.header import *
from lib.cryptClass import *
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
            dbCursor.execute("INSERT INTO config (key, value) VALUES (?,?);",  (key, value))
            db.commit()
        except sqlite3.Error as e:
            logger.error("An DB-error occurred: "+e.args[0])
            return -1
    @staticmethod
    def getConfigByKey(key):
      dbCursor.execute("SELECT * FROM config WHERE key=?;",(key, ))
      for row in dbCursor.fetchall():
        return Config(row[0],row[1],row[2])
      return None
    def save(self, key,  value):
        try:
            dbCursor.execute("UPDATE config SET key=?, value=? WHERE coid=?",  (key, value,  self.id))
            db.commit()
        except sqlite3.Error as e:
            logger.error("An DB-error occurred: "+e.args[0])("An DB-error occurred: "+e.args[0])
    def delete(self):
        try:
            dbCursor.execute("DELETE FROM config WHERE coid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            logger.error("An DB-error occurred: "+e.args[0])("An DB-error occurred: "+e.args[0])
            
class staticConfigTools:
  
  def getLoggerLevel(levelString):
    levelString = levelString.lower()
    if levelString=="error":
      return logging.ERROR
    elif levelString=="fatal":
      return logging.FATAL
    elif levelString=="debug":
      return logging.DEBUG
    elif levelString=="info":
      return logging.INFO
    elif levelString=="warning" or levelString=="warn":
      return logging.WARNING
    else:
      return logging.ERROR