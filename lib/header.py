from PyQt4 import QtCore,QtGui
from binascii import b2a_hex
import re
import logging
def tr(name):
    return QtCore.QCoreApplication.translate("@default",  name)
lang = ""
singleView = False
singleViewId = -1
singleViewName = ""
dbDateFormat = "dd.MM.yyyy"

logger = logging.getLogger('jobManagement')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('jobManagement.log')
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

