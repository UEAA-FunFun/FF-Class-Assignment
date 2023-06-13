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
              - argmapper must have complete mapping:
        (rid,pData) |->
                    - rid
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

            see mappers.py for examples
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
        """
        Set the directory to the current working directory, and then append the pathStr.
        @param pathStr - the path to append to the current working directory.
        @returns the path to the directory.
        """
        return os.path.realpath(os.path.join(os.getcwd(), pathStr))

    @staticmethod
    def canAdd(cid,rid,cutil,rutil):
        """
        Check if a class can be added to the class utilization dictionary.
        @param cid - the class id
        @param rid - the response id
        @param cutil - the class utilization dictionary
        @param rutil - the rotation utilization dictionary
        @returns True if the class can be added, False otherwise.
        """
        #classes can only be filled to capacity
        if cutil.getClassAttr(cid,"size") >= cutil.getClassAttr(cid,"capacity"): 
            return False
        
        #studnts can only have one class per time
        if rutil.isRegistered(rid,cutil.getClassAttr(cid,"time")):
            print("ripperino")
            return False 
        
        return True


    """
        Add a response to a class. If the class is full, return false. Otherwise, add the response to the class and return true.
        @param cid - the class id           
        @param rid - the response id           
        @param cutil - the class util           
        @param rutil - the response util           
        @return True if the response was added to the class, false otherwise.           
        """
    @staticmethod   
    def addToClass(cid,rid,cutil,rutil):
        if Utils.canAdd(cid,rid,cutil,rutil):
            #set first before adding to roster
            rutil.setResponse(rid,f"{cutil.getClassAttr(cid,'time')} class",cutil.getClassAttr(cid,'name'))
            cutil.setClassAttr(cid,"size",cutil.getClassAttr(cid,"size") + 1)
            cutil.addToRoster(cid,rutil.getResponse(rid))
            
            return True 
            
        return False
    @staticmethod
    def removeFromClass(cid,rid,cutil,rutil):
        """
        Remove a response from a class.
        @param cid - the class id
        @param rid - the response id
        """
        rutil.removeResponse(rid,f"{cutil.getClassAttr(cid,'time')} class")
        cutil.setClassAttr(cid,"size",cutil.getClassAttr(cid,"size") - 1)
        cutil.removeFromRoster(cid,rid)
        
        return True
class ClassUtils(Utils):
    '''
    argmapper should have maps to: name, time, max, size, roster
    '''
    def __init__(self, argmapper, dataName, outputName):
        super().__init__(argmapper, dataName, outputName)

        #I want this to be a dictionary
        self.classInfo = self.listToDict(self.map.applyMap(enumerate(self.loader.getClasses())))
        self.nameToId = dict()
        for i in self.classInfo:
            self.nameToId[self.classInfo[i]["name"]] = i

    def printClasses(self,filterFunc = lambda x: True):
        """
        Print the classes.
        @param filterFunc - a function that takes in a class and returns true if the class should be printed, false otherwise.
        """


        print("~~~~~~~~~~id: Classes~~~~~~~~~~")
        for i in self.classInfo: #for each class, print the name and size
            if filterFunc(self.classInfo[i]):
                print(str(i) + ": " + self.classInfo[i]["name"] + self.classInfo[i]["time"] + " (" + str(self.classInfo[i]["size"]) + "/" + str(self.classInfo[i]["capacity"]) + ")")
        print("~~~~~~~~~~~~~~~~~~~~~")
    def numClasses(self):
        """
        Return the number of classes in the dataset.
        @return The number of classes in the dataset.
        """
        return len(self.classInfo)

    def getClass(self,id):
        """
        Given an id, return the class name.
        @param id - the id of the class
        @return the class name
        """
        return self.classInfo[id]
    
    def printClassRoster(self,id):
        """
        Print the roster of a class.
        @param id - the id of the class
        """
        currClass = self.getClass(id)
        print("~~~~~~~~~~id: " + currClass["name"] + " roster~~~~~~~~~~")
        for student in currClass["roster"]:
            print(str(student["rid"]) + ": " + student["First"] + " " + student["Last"])
        print("~~~~~~~~~~~~~~~~~~~~~")

    def setClassAttr(self,id,attr,val):
        """
        Set the attribute of a class to a value.
        @param self - the class itself
        @param id - the id of the class
        @param attr - the attribute to set
        @param val - the value to set the attribute to
        """
        self.getClass(id)[attr] = val 

    

    def getClassAttr(self,id,attr):
        """
        Get the attribute of a class.
        @param self - the class itself
        @param id - the id of the class
        @param attr - the attribute of the class
        @returns the attribute of the class
        """
        return self.getClass(id)[attr]
    
    def getId(self,name):
        """
        Given a name, return the id of the class.
        @param name - the name of the camera
        @return the id of the camera
        """
        return self.nameToId[name]

    def removeFromRoster(self,id,rid):
        """
        Remove a response from a class.
        @param idInRoster - the id of the response in the roster
        @param rid - the response id
        """
        currRoster = self.getClassAttr(id,"roster")
        for i in range(len(currRoster)):
            if currRoster[i]["rid"] == rid:
                idInRoster = i
                break
        print("Removing " + currRoster[idInRoster]["First"] + " " + currRoster[idInRoster]["Last"] + " from " + self.getClassAttr(id,"name"))
        currRoster.pop(idInRoster)
        self.setClassAttr(id,"roster",currRoster)
    
    def addToRoster(self,id,studentData):
        """
        Add a response to a class.
        @param id - the id of the class
        @param studentData - the student data to add to the class 
            (this is the data found by calling rutil.getResponse(rid))
        """
        print(self.getClass(id).keys())
        self.getClassAttr(id,"roster").append(studentData)
         
        print("Adding " + studentData["First"] + " " + studentData["Last"] + " to " + self.getClassAttr(id,"name"))


    def getName(self,id):
        """
        Given an id, return the name of the class.
        @param self - the class itself
        @param id - the id of the class
        @return the name of the class
        """
        return self.getClassAttr(id,"name")

    def getSize(self,id):
        """
        Get the size of the object from the object id.
        @param id - the object id
        @return the size of the object
        """
        return self.getClassAttr(id,"size")

    def getCapacity(self,id):
        """
        Get the capacity of the class.
        @param id - the id of the class
        @return the capacity of the class
        """
        return self.getClassAttr(id,"capacity")

    def getRoster(self,id):
        """
        Get the roster for a given class.
        @param id - the class id
        @return the roster
        """
        return self.getClassAttr(id,"roster")

    def getTime(self,id):
        """
        Get the time of the event.
        @param id - the id of the event
        @return the time of the event
        """
        return self.getClassAttr(id,"time")


    def sameTime(self,id1,id2):
        """
        Check if two classes are in the same time slot.
        @param id1 - the first class id
        @param id2 - the second class id
        @returns True if they are in the same time slot, False otherwise
        """
        return self.classInfo[id1]["time"] == self.classInfo[id2]["time"]


    '''
    Include an optional condtion function that takes in a cid and self, and adds its size if true
    '''
    def totalSize(self,condFunc=None):
        """
        Given a condition function, return the total number of items in the warehouse.
        @param condFunc - the condition function
        @return the total number of items in the warehouse
        """
        res = 0
        for cid in range(self.numClasses()):
            if condFunc(cid,self):
                res += self.getCapacity(cid)
        return res

    def publishClasses(self):
        """
        Publish the class roster to a csv file.
        @param self - the class object itself
        """
        keys = ["rid","First","Last","Gender","YOB", 'Special Considerations', 'Primary Contact', 'Primary Telephone', 'Primary Relationship', 'Secondary Contact', 'Secondary Telephone', 'Secondary Relationship', 'Self Dismissed?', 'Dismiss to', 'Dismiss Relationship', 'Shirt Size', 'first choices', 'second choices', 'third choices', 'AM class', 'PM class']
        for cid in self.classInfo:
            with open(os.path.join(self.outputPath,f'{re.sub(r"[^a-zA-Z0-9]","",self.getName(cid))}.csv'),"w+") as classF:
                classWriter = csv.DictWriter(classF,keys)
                classWriter.writeheader()

                classWriter.writerows(self.getRoster(cid))

                
    

class ResponseUtils(Utils):
    def __init__(self, argmapper, dataName, outputName):
        super().__init__(argmapper, dataName, outputName)
        self.responseInfo = self.listToDict(self.map.applyMap(enumerate(self.loader.getResponses())))

    def getResponse(self,id):
        """
        Given an id, return the response for that id.
        @param self - the object itself
        @param id - the id we are looking for
        @return the response for that id
        """
        return self.responseInfo[id]

    def getAttr(self,id,attr):
        if attr in self.getResponse(id):
            return self.getResponse(id)[attr]

        return None

    def setResponse(self,id,attr,val):        
        """
        Set the response of the node with the given id to the given value.
        @param id - the id of the node to set the response of.
        @param attr - the attribute to set.
        @param val - the value to set the attribute to.
        """
        self.getResponse(id)[attr] = val
    
    def removeResponse(self,rid,attr):
        """
        Remove the response of the node with the given id to the given value.
        @param id - the id of the node to set the response of.
        @param attr - the attribute to set.
        """
        if attr not in self.getResponse(rid):
            #raise a value error
            raise ValueError(f"Attribute {attr} not in response {rid}")

        self.setResponse(rid,attr,None)

    def getSize(self):
        """
        Get the size of the response array.
        @return The size of the response array.
        """
        return len(self.responseInfo)
    


    def isRegistered(self,id,time):
        """
        Check if the id is registered at the given time.
        @param id - the id to check against
        @param time - the time to check against
        @returns true if the id is registered at the given time, false otherwise
        """
        return self.getAttr(id,f"{time} class") != None

    
    '''
    requires cutil to query time
    '''
    def getTimeChoices(self,id,time,cutil):
        """
        Given an id, time, and cutil, return the ids of the first, second, and third choices for that time.
        @param id - the id of the current node
        @param time - the time of the current node
        @param cutil - the cutil object
        @returns the ids of the first, second, and third choices for that time.
        """
        
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
        """
        Write the response info to a csv file.
        @param self - the object itself
        """
        keys = ["rid","First","Last","Gender","YOB", 'Special Considerations', 'Primary Contact', 'Primary Telephone', 'Primary Relationship', 'Secondary Contact', 'Secondary Telephone', 'Secondary Relationship', 'Self Dismissed?', 'Dismiss to', 'Dismiss Relationship', 'Shirt Size', 'first choices', 'second choices', 'third choices', 'AM class', 'PM class']
        with open(os.path.join(self.outputPath,"MASTER.csv"),"w+") as master:
            masterWriter = csv.DictWriter(master,keys)
            masterWriter.writeheader()
            masterWriter.writerows([self.responseInfo[i] for i in self.responseInfo])