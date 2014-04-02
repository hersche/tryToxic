#This code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster
from PyQt4 import QtCore,QtGui
from lib.controller import mainController
from lib.configControll import Config
import sys


app = QtGui.QApplication(sys.argv)
translator = QtCore.QTranslator()
configLang = Config.getConfigByKey("lang")
if configLang is None:
  configLang = Config.getConfigByKey("language")
if configLang is not None:
  translator.load(configLang.value,"./lang/")
  app.installTranslator(translator)
mc = mainController(app)
mc.show()

sys.exit(app.exec_())
