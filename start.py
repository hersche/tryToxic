#This code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster

from lib.guiController import *
from lib.toxModels import Config
import sys

singleView = False
singleViewId = -1
app = QtGui.QApplication(sys.argv)
translator = QtCore.QTranslator()
configLang = Config.getConfigByKey("lang")
if configLang is None:
  configLang = Config.getConfigByKey("language")
if configLang is not None:
  print("whatlang"+configLang.value)
  translator.load(configLang.value,"./lang/")
  app.installTranslator(translator)
gui = Gui()
gui.show()

sys.exit(app.exec_())
