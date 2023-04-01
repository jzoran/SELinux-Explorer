from analyzer.FileAnalyzer import  *
from drawer.RelationDrawer import *
from drawer.DrawerHelper import *


class AnalyzerLogic:
    def __init__(self):
        super().__init__()
        self.initVariables()
        self.initAnalyzer()


    def initVariables(self):
        self.keepResult = False
        self.listOfPolicyFiles = list()
        self.listOfDiagrams = list()
        self.drawer = RelationDrawer()

    def initAnalyzer(self):
        self.analyzer = FileAnalyzer()

    def analyzeAll(self, paths):
        if self.keepResult :
            self.listOfPolicyFiles.extend(self.analyzer.analyze(paths))
        else:
            self.listOfPolicyFiles =  self.analyzer.analyze(paths)

        self.onAnalyzeFinished(None)
        self.updateAnalyzerDataResult(self.listOfPolicyFiles)

    def onAnalyzeSelectedPaths(self, paths):
        if self.keepResult :
            self.listOfPolicyFiles.extend(self.analyzer.analyze(paths))
        else:
            self.listOfPolicyFiles = self.analyzer.analyze(paths)

        self.onAnalyzeFinished(None)
        self.updateAnalyzerDataResult(self.listOfPolicyFiles)

    def clearOutput(self):
        files = SystemUtility().getListOfFiles(os.getcwd() + "/out/","*")
        for file in files :
            if os.path.isfile(file):
                SystemUtility().deleteFiles(file)
        self.onAnalyzeFinished(None)
        self.updateAnalyzerDataResult(None)

    def clearFileFromAnalyzer(self, filePath):
        self.analyzer.clear()     
        SystemUtility().deleteFiles(generateDiagramFileName(filePath))
        SystemUtility().deleteFiles(generatePumlFileName(filePath))
        self.onAnalyzeFinished(None)

    def removeFile(self, filePath):
        SystemUtility().deleteFiles( os.path.splitext(filePath)[0]+DIAGEAM_FILE_EXTENSION)
        SystemUtility().deleteFiles( os.path.splitext(filePath)[0]+".puml")

    def clear(self):
        self.listOfPolicyFiles = list()

    def getImagePath(self, filePath):
        return generateDiagramFileName(filePath)
    
    def setKeepResult(self, state):
        self.keepResult = state
        print("self.keepResult:", self.keepResult)


    def setUiUpdateSignal(self, updateResult):
        self.updateResult = updateResult

    def setUiUpdateAnalyzerDataSignal(self, updateResult):
        self.updateAnalyzerDataResult = updateResult

    def onAnalyzeFinished(self, filteredPolicyFile):
        self.listOfDiagrams = SystemUtility().getListOfFiles(os.getcwd() + "/out/","*"+DIAGEAM_FILE_EXTENSION)
        self.updateResult()
        