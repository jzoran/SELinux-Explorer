from analyzer.FileAnalyzer import  *
from drawer.RelationDrawer import *
from drawer.DrawerHelper import *
from AppSetting import *
from model.PolicyEntities import *

class AnalyzerLogic:
    def __init__(self):
        super().__init__()
        self.initVariables()
        self.initAnalyzer()


    def initVariables(self):
        self.keepResult = False
        self.listOfPolicyFiles = list()
        self.listOfDiagrams = list()
        self.refPolicyFile = PolicyFiles()
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
        self.refPolicyFile = self.makeRefPolicyFile(self.listOfPolicyFiles)

    def onAnalyzeSelectedPaths(self, paths):
        if self.keepResult :
            self.listOfPolicyFiles.extend(self.analyzer.analyze(paths))
        else:
            self.listOfPolicyFiles = self.analyzer.analyze(paths)

        self.onAnalyzeFinished(None)
        self.updateAnalyzerDataResult(self.listOfPolicyFiles)

    def makeRefPolicyFile(self, policyFile):
        if  self.listOfPolicyFiles == None or len(self.listOfPolicyFiles) == 0:
            return None

        refPolicyFile = PolicyFiles()
        for policyFile in self.listOfPolicyFiles:
            refPolicyFile.typeDef.extend(policyFile.typeDef)
            refPolicyFile.attribute.extend(policyFile.attribute)
            refPolicyFile.contexts.extend(policyFile.contexts)
            refPolicyFile.seApps.extend(policyFile.seApps)
            refPolicyFile.rules.extend(policyFile.rules)
            refPolicyFile.macros.extend(policyFile.macros)
            refPolicyFile.macroCalls.extend(policyFile.macroCalls)

        for macoCall in refPolicyFile.macroCalls:
            #print("macroCall.name: ", macoCall.name)
            for macro in refPolicyFile.macros:
                #print("macro.name: ", macro.name)
                if macro.name == macoCall.name:
                    rules = macro.rules
                    for rule in rules:
                        #Need to replace $number in source, target or classType with parameter from macro call with
                        #the same number
                        for i in range(0, len(macoCall.parameters)):
                            rule.source = rule.source.replace("$"+str(i+1), macoCall.parameters[i])
                            rule.target = rule.target.replace("$"+str(i+1), macoCall.parameters[i])
                            rule.classType = rule.classType.replace("$"+str(i), macoCall.parameters[i])
                        #print("rule: ", rule)
                        refPolicyFile.rules.append(rule)
                        refPolicyFile.macroCalls.clear()
        return refPolicyFile

    def clearOutput(self):
        files = SystemUtility().getListOfFiles(os.getcwd() + "/" +OUT_DIR,"*")
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
        self.listOfDiagrams = SystemUtility().getListOfFiles(os.getcwd() + "/" + OUT_DIR,"*"+DIAGEAM_FILE_EXTENSION)
        self.updateResult()
        