from lib.header import *
from lib.cryptClass import *
class Config:
  """
  Config-data-object
  """
  def __init__(self, id, key, value):
    """
    id --- is the db-id of config
    key --- the reference
    value --- the setted value
    """
    logger.debug("|Models| Init config " + key + "=" + value)
    self.id = id
    self.key = key
    self.value = value

  def save(self, key, value):
    """
    save the config-object
    """
    try:
        dbCursor.execute("UPDATE config SET key=?, value=? WHERE coid=?", (key, value, self.id))
        db.commit()
    except sqlite3.Error as e:
        logger.error("An DB-error occurred: " + e.args[0])("An DB-error occurred: " + e.args[0])

  def delete(self):
    """
    delete the config-object
    """
    try:
        dbCursor.execute("DELETE FROM config WHERE coid=?", (self.id,))
        db.commit()
    except sqlite3.Error as e:
        logger.error("An DB-error occurred: " + e.args[0])("An DB-error occurred: " + e.args[0])

class staticConfigTools:
  """
  A pool for static config-tools in context to config
  """
  @staticmethod
  def updateConfigListData():
    """
    update the list of config-data-objects
    """
    logger.debug("|Models| Update configList")
    configList = []
    dbCursor.execute('select * from config;')
    for row in dbCursor.fetchall():
        configList.append(Config(row[0], row[1], row[2]))
    return configList


  @staticmethod
  def createConfig(key, value):
    """
    create new Config
    """
    try:
        dbCursor.execute("INSERT INTO config (key, value) VALUES (?,?);", (key, value))
        db.commit()
    except sqlite3.Error as e:
        logger.error("An DB-error occurred: " + e.args[0])
        return -1
  @staticmethod
  def getConfigByKey(key):
    """
    get a config by it's key.
    return Config
    """
    dbCursor.execute("SELECT * FROM config WHERE key=?;", (key,))
    for row in dbCursor.fetchall():
      return Config(row[0], row[1], row[2])
    return None

  @staticmethod
  def getLoggerLevel(levelString):
    """
    get the right value for log-levels.
    return int level
    """
    levelString = levelString.lower()
    if levelString == "error":
      return logging.ERROR
    elif levelString == "fatal":
      return logging.FATAL
    elif levelString == "debug":
      return logging.DEBUG
    elif levelString == "info":
      return logging.INFO
    elif levelString == "warning" or levelString == "warn":
      return logging.WARNING
    else:
      return logging.ERROR
