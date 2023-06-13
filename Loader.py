import os
import json

class Loader:
    '''
    Loader is responsible for loading class and response information. Will open the files needed 
    and parse to dictionaries (or functions, I have not completely decided yet).
    '''
    def __init__(self,dataPath,outputPath) -> None:
        self.dataPath = dataPath
        self.outputPath = outputPath
        
        #sets attr cInfo and nameId
        self.loadClasses()
        self.loadResponses()

    def jsonLoad(self,obj,path):
        with open(os.path.join(path,obj),"r+") as opened:
            res = json.load(opened)
        return res

    def csvLoad(self,obj,path):
        res = []
        with open(os.path.join(path,obj),"r+") as opened:
            for line in opened.readlines():
                res.append(line)
        return res 

    def loadClasses(self):
        self.classes = self.jsonLoad("classes.json",self.dataPath)

        
    

    def loadResponses(self):
        self.responses = self.jsonLoad("responses.json",self.dataPath)

    '''
    returns classes dictionary
    '''
    def getClasses(self):
        return self.classes

    '''
    returns response info dictionary list
    '''
    def getResponses(self):
        return self.responses

    