#this code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster

from lib.guiController import *
import sys

singleView = False
singleViewId = -1
app = QtGui.QApplication(sys.argv)
translator = QtCore.QTranslator()
#translator.load("./"+mightyController.lang,"./")
app.installTranslator(translator)
gui = Gui()
gui.show()

sys.exit(app.exec_())
