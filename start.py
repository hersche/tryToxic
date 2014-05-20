# This code is GPL-FORCED so let changes open, pls!!
# License @ http://www.gnu.org/licenses/gpl.txt
# Author: skamster
from PyQt4 import QtCore, QtGui
from lib.controller import mainController
from lib.configControll import staticConfigTools
import sys


app = QtGui.QApplication(sys.argv)
translator = QtCore.QTranslator()
configLang = staticConfigTools.getConfigByKey("lang")
if configLang is None:
  configLang = staticConfigTools.getConfigByKey("language")
if configLang is not None:
  translator.load(configLang.value, "./lang/")
  app.installTranslator(translator)
mc = mainController(app)
mc.show()

sys.exit(app.exec_())
