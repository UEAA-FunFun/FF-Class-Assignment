import csv
import os
import re
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
    def __init__(self,argmapper,dataName,outputName):
        self.map = Map(argmapper)
        self.dataPath = Utils.setDir(dataName)
        self.outputPath = Utils.setDir(outputName)
        self.loader = Loader(self.dataPath,self.outputPath)

        def listToDict(xs):
            res = dict()
            for i in range(len(xs)):
                res[i] = xs[i]
            return res

        
        self.listToDict = listToDict

    '''
    Takes a  string and returns a abs path to the directory within the root directory
    '''
    @staticmethod
    def setDir(pathStr : str) -> str:
        return os.path.realpath(os.path.join(os.getcwd(), pathStr))

    @staticmethod
    def canAdd(cid,rid,cutil,rutil):
        #classes can only be filled to capacity
        if cutil.getClassAttr(cid,"size") >= cutil.getClassAttr(cid,"capacity"): 
            return False
        
        #studnts can only have one class per time
        if rutil.isRegistered(rid,cutil.getClassAttr(cid,"time")):
            return False 
        
        return True


    #returns true iff add successful
    @staticmethod 
    def addToClass(cid,rid,cutil,rutil):
        if Utils.canAdd(cid,rid,cutil,rutil):
            #set first before adding to roster
            rutil.setResponse(rid,f"{cutil.getClassAttr(cid,'time')} class",cutil.getClassAttr(cid,'name'))
            cutil.setClassAttr(cid,"size",cutil.getClassAttr(cid,"size") + 1)
            cutil.getClassAttr(cid,"roster").append(rutil.getResponse(rid))
            
            return True 
            
        return False
class ClassUtils(Utils):
    '''
    argmapper should have maps to: name, time, max, size, roster
    '''
    def __init__(self, argmapper, dataName, outputName):
        super().__init__(argmapper, dataName, outputName)

        #I want this to be a dictionary
        self.classInfo = self.listToDict(self.map.applyMap(self.loader.getClasses()))
        self.nameToId = dict()
        for i in self.classInfo:
            self.nameToId[self.classInfo[i]["name"]] = i

    def numClasses(self):
        return len(self.classInfo)

    def getClass(self,id):
        return self.classInfo[id]

    def setClassAttr(self,id,attr,val):
        self.getClass(id)[attr] = val 

    def getClassAttr(self,id,attr):
        return self.getClass(id)[attr]
    
    def getId(self,name):
        return self.nameToId[name]

    def getName(self,id):
        return self.getClassAttr(id,"name")

    def getSize(self,id):
        return self.getClassAttr(id,"size")

    def getCapacity(self,id):
        return self.getClassAttr(id,"capacity")

    def getRoster(self,id):
        return self.getClassAttr(id,"roster")

    def getTime(self,id):
        return self.getClassAttr(id,"time")


    def sameTime(self,id1,id2):
        return self.classInfo[id1]["time"] == self.classInfo[id2]["time"]


    '''
    Include an optional condtion function that takes in a cid and self, and adds its size if true
    '''
    def totalSize(self,condFunc=None):
        res = 0
        for cid in range(self.numClasses()):
            if condFunc(cid,self):
                res += self.getCapacity(cid)
        return res

    def publishClasses(self):
        keys = ["First","Last","Gender","YOB", 'Special Considerations', 'Primary Contact', 'Primary Telephone', 'Primary Relationship', 'Secondary Contact', 'Secondary Telephone', 'Secondary Relationship', 'Self Dismissed?', 'Dismiss to', 'Dismiss Relationship', 'Shirt Size', 'first choices', 'second choices', 'third choices', 'AM class', 'PM class']
        for cid in self.classInfo:
            with open(os.path.join(self.outputPath,f'{re.sub(r"[^a-zA-Z0-9]","",self.getName(cid))}.csv'),"w+") as classF:
                classWriter = csv.DictWriter(classF,keys)
                classWriter.writeheader()
                classWriter.writerows(self.getRoster(cid))
    

class ResponseUtils(Utils):
    def __init__(self, argmapper, dataName, outputName):
        super().__init__(argmapper, dataName, outputName)
        self.responseInfo = self.listToDict(self.map.applyMap(self.loader.getResponses()))

    def getResponse(self,id):
        return self.responseInfo[id]

    def getAttr(self,id,attr):
        if attr in self.getResponse(id):
            return self.getResponse(id)[attr]

        return None

    def setResponse(self,id,attr,val):        
        self.getResponse(id)[attr] = val

    def getSize(self):
        return len(self.responseInfo)
    


    def isRegistered(self,id,time):
        return self.getAttr(id,f"{time} class") != None

    
    '''
    requires cutil to query time
    '''
    def getTimeChoices(self,id,time,cutil):
        
        fst = self.getAttr(id,"first choices")
        snd = self.getAttr(id,"second choices")
        trd = self.getAttr(id,"third choices")

        res = [] 

        for rank in [fst,snd,trd]:
            for curr in rank:
                if cutil.getClassAttr(cutil.getId(curr),"time") == time:
                    res.append(curr)
        
        return res

    '''
    This will save and write everything to the output directory
    '''
    def publishOverall(self):
        keys = ["First","Last","Gender","YOB", 'Special Considerations', 'Primary Contact', 'Primary Telephone', 'Primary Relationship', 'Secondary Contact', 'Secondary Telephone', 'Secondary Relationship', 'Self Dismissed?', 'Dismiss to', 'Dismiss Relationship', 'Shirt Size', 'first choices', 'second choices', 'third choices', 'AM class', 'PM class']
        with open(os.path.join(self.outputPath,"MASTER.csv"),"w+") as master:
            masterWriter = csv.DictWriter(master,keys)
            masterWriter.writeheader()
            masterWriter.writerows([self.responseInfo[i] for i in self.responseInfo])