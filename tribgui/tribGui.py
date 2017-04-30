'''
tribGui.py

Antony Hallam
2017-04-25
'''


from PyQt5 import QtGui, QtWidgets

from tribgui import tribDesign,tribDialogAbout

from tufpy import stats

#Global Parameters
distrTypes = {'norm' : 'Normal',
              'lognorm' : 'Log-Normal'}


'''
Class to capture the setup of the About Dialog.
'''
class tribAboutDialog(QtWidgets.QDialog, tribDialogAbout.Ui_dialogAbout):
   def __init__(self, parent=None):
      super(tribAboutDialog, self).__init__(parent)
      self.setupUi(self)

'''
Class to caputre the setup of the main window.
'''
class tribApp(QtWidgets.QMainWindow, tribDesign.Ui_MainWindow):
   def __init__(self, parent=None):
      super(tribApp, self).__init__(parent)
      self.setupUi(self)
		
		
      #Connect Menu Actions to Other Windows
      self.actionAbout.triggered.connect(self._onActionAbout)
      self.aboutDialog = tribAboutDialog(self)

      #Populate Distribution Combobox
      self.comboBoxDist.clear()
      self.comboBoxDist.addItems(list(distrTypes.values()))
      self.activeDistr = self.comboBoxDist.currentText()
		
   def _onActionAbout(self):
      self.aboutDialog.show()	