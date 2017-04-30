'''
tribGui.py

Antony Hallam
2017-04-25
'''


from PyQt5 import QtGui, QtWidgets

from tribgui import tribDesign,tribDialogAbout

from tufpy.stats import distr
from scipy import stats

#Global Parameters
distrTypes = {'Normal' : 'norm',
              'Log-Normal' : 'lognorm'}


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
      self.comboBoxDist.addItems(list(distrTypes.keys()))
      self.activeDistr = self.comboBoxDist.currentText()
      
      #Populate Fixed Distr Tab Table
      
      self._getFixedDistrValues()
      self._calcFixedDistr()
      
      print(self.fixedDistrMu,self.fixedDistrStd)
      
      self.tableWidgetDistrValues.setColumnCount(2)
      self.basicOutputs = {
                           'Variable':['90','50','10','mean','std'],\
                           'Value':['0','0','0','0','0']}
      self._setTableWidgetDistrValuesData(self.basicOutputs)
      self._calcFixedDistrTable()

      
   def _onActionAbout(self):
      self.aboutDialog.show()	
      
   #functions for Fixed Distribution Tab
   
   def _getFixedDistrValues(self):
      self.fixedDistr={}
      self.fixedDistr[self.lineEditProb1.text()]=self.lineEditValue1.text()
      self.fixedDistr[self.lineEditProb2.text()]=self.lineEditValue2.text()
      
   def _calcFixedDistr(self):
      p = []; f = []
      for key in self.fixedDistr.keys():
         p.append(1-float(key))
         f.append(float(self.fixedDistr[key]))
      self.fixedDistrMu, self.fixedDistrStd = \
         distr.invNormPpf(f[0],p[0]/100,f[1],p[1]/100)
         
   def _calcFixedDistrTable(self):
      kstats = ['mean', 'std', 'median']
      rows=self.tableWidgetDistrValues.rowCount()-1
      val=''
      for row in range(0,rows+1):
         var = self.tableWidgetDistrValues.itemAt(row,0).text()
         print(row,var)
         if var in kstats:
            if var == 'mean':
               val = self.fixedDistrMu
            if var == 'std':
               val = self.fixedDistrStd
            if var == 'median':
               val = stats.norm.median(loc=self.fixedDistrMu, scale=self.fixedDistrStd)
         self.tableWidgetDistrValues.itemAt(row,0).setText(var)      
         self.tableWidgetDistrValues.itemAt(row,1).setText(str(val))
            
   
#   def _getTableWidgetDistrValuesData(self):
#      horHeaders = self.tableWidgetDistrValues.takeHorizontalHeaderItem(1)
#      print(horHeaders)
      
   def _setTableWidgetDistrValuesData(self,data):
      horHeaders = []
      self.tableWidgetDistrValues.setRowCount(len(data['Variable'])+1)
      for n, key in enumerate(data.keys()):
         horHeaders.append(key)
         for m, item in enumerate(data[key]):
            print(m,item)
            newitem = QtWidgets.QTableWidgetItem(item)
            self.tableWidgetDistrValues.setItem(m, n, newitem)
      self.tableWidgetDistrValues.setHorizontalHeaderLabels(horHeaders)