import os
from Loader import *
from hof import *
'''
Utilities for handling and transforming class data
'''

class Utils:

    '''
    Initialize a Utils object, which is like a multitool for manipulating the data.
    Takes in a function which translates fields from the original json to the following required fields.

    REQUIRES: - a data folder containing class data. class data should be a complete csv with id,class name, class size, and time columns ("AM"/"PM"). No header
              - argmapper must have complete mappings to 
                    - Last
                    - First
                    - Gender
                    - YOB
                    - Special Considerations
                    - Primary Contact
                    - Primary Telephone
                    - Primary Relationship
                    - Secondary Contact
                    - Secondary Telephone
                    - Secondary Relationship
                    - Self Dismissed?
                    - Dismiss to
                    - Dismissal Relationshipp
                    - Shirt Size

            see archive/assign2022.py for examples
    '''
    def __init__(self,argmapper,dataName,outputName) -> None:
        self.map = Map(argmapper)
        self.dataPath = Utils.setDir(dataName)
        self.outputPath = Utils.setDir(outputName)
        self.loader = Loader(self.dataPath,self.outputPath)

    '''
    Takes a  string and returns a abs path to the directory within the root directory
    '''
    @staticmethod
    def setDir(pathStr : str) -> str:
        return os.path.realpath(os.path.join(os.getcwd(), pathStr))

class ClassUtils(Utils):
    '''
    argmapper should have maps to: name, time, max, size, roster
    '''
    def __init__(self, argmapper, dataName, outputName) -> None:
        super().__init__(argmapper, dataName, outputName)
        self.classInfo = self.map.applyMap(self.loader.getClasses())
        self.nameToId = self.loader.nameToId()

    def getId(self,name):
        return self.nameToId[name]

    def getName(self,id):
        return self.getClassAttr(id,"name")

    def getClass(self,id):
        return self.classInfo[id]

    def setClassAttr(self,id,attr,val):
        self.classInfo[id][attr] = val 

    def getClassAttr(self,id,attr):
        return self.classInfo[id][attr]
    
    '''
    incriment and add to roster. User is responsible for adding the appropriate data entry
    TODO: Include type annotations for implicit check
    '''
    def addToClass(self,cid,entry):
        self.setClassAttr(id,"size",self.getClassAttr(id,"size") + 1)
        self.getClassAttr(cid,"roster").append(entry)

    

class ResponseUtils(Utils):
    def __init__(self, argmapper, dataName, outputName) -> None:
        super().__init__(argmapper, dataName, outputName)
        self.responseInfo = self.map.applyMap(self.loader.getResponses())

    def getResponse(self,id):
        return self.responseInfo[id]
