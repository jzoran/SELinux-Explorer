
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout,  QWidget, QMessageBox
from PyQt5.QtGui import *
from AnalyzerLogic import *
from ui.FileUi import *
from ui.AnalyzeUi import *
from ui.FilterUi import *
from AppSetting import *
from PythonUtilityClasses.FileWriter import *
from PythonUtilityClasses.FileReader import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SELinux-Explorer")
        self.initVariables()
        self.initMainLayout()
        self.configSignals()
        self.loadSetting()

    def initVariables(self):
        self.analyzerLogic = AnalyzerLogic()
        self.appSetting = AppSetting()

    def loadSetting(self):
        if os.path.isfile("app_setting.json"):
            json_str = FileReader().readFile("app_setting.json")
            self.appSetting = AppSetting.from_json(json_str) 
            self.layoutPath.lastOpenedPath = self.appSetting.lastOpenedPath
            self.layoutAnalyzer.keepResult = self.appSetting.keepTheResult
            self.layoutFilter.setClassTypeSelected(self.appSetting.filterClassType)
            self.layoutFilter.setDomainSelected(self.appSetting.filterDomain)
            self.layoutFilter.setFilenameSelected(self.appSetting.filterFilename)
            self.layoutFilter.setPermissionSelected(self.appSetting.filterPermission)
            print("AppSetting loaded!")
        else:
            self.saveSetting()

    def saveSetting(self):
        self.appSetting.lastOpenedPath = self.layoutPath.lastOpenedPath
        self.appSetting.keepTheResult = self.layoutAnalyzer.keepResult
        self.appSetting.filterClassType = self.layoutFilter.isClassTypeSelected()
        self.appSetting.filterDomain = self.layoutFilter.isDomaineSelected()
        self.appSetting.filterFilename = self.layoutFilter.isFilenameSelected()
        self.appSetting.filterPermission = self.layoutFilter.isPermissionSelected()

        FileWriter().writeFile("app_setting.json", self.appSetting.to_json())
        print("AppSetting saved!")

    def initMainLayout(self):
        self.layoutPath = FileUi(self)
        self.layoutAnalyzer = AnalyzeUi(self, self.analyzerLogic)
        self.layoutFilter = FilterUi(self, self.analyzerLogic)
        self.mainLayout = QVBoxLayout()
        self.container = QWidget()

        #mainLayout
        self.mainLayout.addLayout(self.layoutPath)
        self.mainLayout.addLayout(self.layoutAnalyzer)
        self.mainLayout.addLayout(self.layoutFilter)

        self.container.setLayout(self.mainLayout)
        # Set the central widget of the Window.
        self.setCentralWidget(self.container)

        self.setWindowPosition()

    def configSignals(self):
        self.layoutAnalyzer.connectToGetSelectedPaths( self.layoutPath.getSelectedPaths)
        self.layoutAnalyzer.connectToGetAllPaths( self.layoutPath.getAllPaths)

    def setWindowPosition(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self,event):
            result = QMessageBox().question(self,
                        "Confirm Exit...",
                        "Are you sure you want to exit ?",
                        QMessageBox.Yes| QMessageBox.No)
            event.ignore()

            if result == QMessageBox.Yes:
                self.saveSetting()
                event.accept()

