#This code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster

from lib.controller import *
from lib.toxModels import Config
import sys


app = QtGui.QApplication(sys.argv)
translator = QtCore.QTranslator()
configLang = Config.getConfigByKey("lang")
if configLang is None:
  configLang = Config.getConfigByKey("language")
if configLang is not None:
  translator.load(configLang.value,"./lang/")
  app.installTranslator(translator)
mc = mainController()
mc.show()

sys.exit(app.exec_())
