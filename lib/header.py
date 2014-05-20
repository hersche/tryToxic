from PyQt4 import QtCore

import logging
import os.path,sqlite3

def tr(name):
  """
  The translationmethod
  """
  return QtCore.QCoreApplication.translate("@default",  name)
lang = ""
dbDateFormat = "dd.MM.yyyy"
logger = logging.getLogger('tryToxics')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('tryToxics.log')
fh.setLevel(logging.ERROR)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
fileExist = True
if os.path.isfile('toxMessages.db') == False:
    fileExist = False
db = sqlite3.connect('toxMessages.db')
dbCursor = db.cursor()
if fileExist == False:
    dbCursor.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, friendId text, timestamp text, message text, me text, encrypted text)")
    dbCursor.execute("CREATE TABLE config (coid INTEGER PRIMARY KEY,  key TEXT UNIQUE,  value TEXT, encrypted text)")

