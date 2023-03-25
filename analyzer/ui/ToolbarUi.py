
from PyQt5.QtWidgets import QAction, QToolBar, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from AnalyzerLogic import *
from PyQt5.QtCore import Qt
from ui.UiUtility import *
import sys
from PythonUtilityClasses.SystemUtility import *



class ToolbarUi(QToolBar):
    def __init__(self, mainWindow, analyzerLogic, appSetting):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.appSetting = appSetting
        self.initVariables()
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        self.keepResult = False

    def initWidgets(self):
        iconPath = './ui/icons/'
        self.actAddFile = QAction(QIcon(iconPath + 'add-file.png'),"Add a file to the list", self.mainWindow)
        self.actAddPath = QAction(QIcon(iconPath + 'add-folder.png'),"Add a Path to the list", self.mainWindow)
        self.actRemoveOutput = QAction(QIcon(iconPath + 'remove.png'),"Remove Outputs", self.mainWindow)
        self.actClearAnalyze = QAction(QIcon(iconPath + 'reset.png'),"Clear Analyze", self.mainWindow)
        self.actWipeAll = QAction(QIcon(iconPath + 'broom.png'),"Wipe all(output, analyze, etc.)", self.mainWindow)
        self.actMakeReference = QAction(QIcon(iconPath + 'reference.png'),"Make reference from the analyzed data", self.mainWindow)
        self.actAnalyzeAll = QAction(QIcon(iconPath + 'data-integration.png'),"Analyze all the files/paths", self.mainWindow)
        self.actKeepResult = QAction(QIcon(iconPath + 'hosting.png'),"Don't erase the current result before Analyzing", self.mainWindow)

        self.actKeepResult.setCheckable(True)

    def configSignals(self):
        self.addAction(self.actAddFile)
        self.addAction(self.actAddPath)
        self.addSeparator()
        self.addAction(self.actAnalyzeAll)
        self.addSeparator()
        self.addAction(self.actMakeReference)
        self.addSeparator()
        self.addAction(self.actRemoveOutput)
        self.addAction(self.actClearAnalyze)
        self.addAction(self.actWipeAll)
        self.addSeparator()
        self.addAction(self.actKeepResult)

    def configLayout(self):
        self.actAddFile.triggered.connect(self.onAddFile)
        self.actAddPath.triggered.connect(self.onAddPath)
        self.actAnalyzeAll.triggered.connect(self.onAnalyzeAll)
        self.actClearAnalyze.triggered.connect(self.onClearAnalyze)
        self.actRemoveOutput.triggered.connect(self.onClearOutput)
        self.actWipeAll.triggered.connect(self.onWipeAll)
        self.actKeepResult.triggered.connect(self.onClickedKeepResult)

        self.setOrientation(Qt.Vertical)


    def connectOnAddFileFolder(self, onAddFileFolder):
        self.addFileFolder = onAddFileFolder

    def connectToGetSelectedPaths(self, getSelectedPath):
        self.getSelectedPaths = getSelectedPath

    def connectToGetAllPaths(self, getAllPaths):
        self.getAllPaths = getAllPaths        

    def onAddFile(self):
        dlg = QFileDialog(directory = self.appSetting.lastOpenedPath)
        if dlg.exec_():
            self.addPathToList(dlg.selectedFiles()[0])

    def onAddPath(self):
        self.addPathToList( QFileDialog(directory = self.appSetting.lastOpenedPath).getExistingDirectory(self.mainWindow, 'Hey! Select a Folder', options=QFileDialog.ShowDirsOnly))

    def addPathToList(self, path):
        self.appSetting.lastOpenedPath = path
        self.addFileFolder(path)

    def onAnalyzeSelectedPaths(self):
        paths = self.getSelectedPaths()
        self.analyzerLogic.analyzeAll(paths)
        showMessage("Analyzer", "The selected files are analyzed!")

    def onAnalyzeAll(self):
        paths = self.getAllPaths()
        self.analyzerLogic.analyzeAll(paths)
        showMessage("Analyzer", "All the files are analyzed!")

    def onClearAnalyze(self):
        self.analyzerLogic.clear()     

    def onClearOutput(self):
        self.analyzerLogic.clearOutput()
            
    def onDeleteAllFile(self):
        self.analyzerLogic.clearOutput()

    def onWipeAll(self):
        self.onClearOutput()
        self.onClearAnalyze()

    def onResultAdded(self, filePath):
        item = QListWidgetItem(filePath)
        self.lstResults.addItem(item)

    def onAnalyzeFinished(self):
        self.lstResults.clear()
        for file in self.analyzerLogic.listOfDiagrams:
            self.lstResults.addItem(QListWidgetItem(file))

    def onSelectedResult(self):
        listItems=self.lstResults.selectedItems()
        if len(listItems) > 0:
            self.diagram = DiagramWindow(listItems[0].text())
            self.diagram.show()

    def onClickedKeepResult(self):
        self.keepResult = self.sender().isChecked()
        self.analyzerLogic.setKeepResult( self.sender().isChecked())