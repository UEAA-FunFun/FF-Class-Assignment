
from random import shuffle
from utils import *
class Strategy:
    def __init__(self,cutil,rutil):
        self.cutil = cutil 
        self.rutil = rutil
        self.lotto = [i for i in range(rutil.getSize())]
        shuffle(self.lotto)

    def shuffle(self):
        shuffle(self.lotto)
        return self.lotto

    def metrics(self):
        # print classes out and their capacity
        print("--------------------------------SOME STATS--------------------------------")

        print(f"There are a total of {self.rutil.getSize()} students signed up")

        f = lambda time : lambda cid,cutil : time == cutil.getTime(cid)
        print(f"There are {self.cutil.totalSize(f ('AM'))} seats in AM and {self.cutil.totalSize( f ('PM'))} seats in the PM.\n")


        print("--------------------------------CLASS SIZES--------------------------------")
        for cid in range(self.cutil.numClasses()):
            cname = self.cutil.getName(cid)
            csize = self.cutil.getSize(cid)
            ccap = self.cutil.getCapacity(cid)

            print(f"{cname}: {csize} out of {ccap}")
        
        #keep a log of the students who do not have a class
        aMiss,aLog = 0, []
        pMiss,pLog = 0, []
        bothMiss,bLog = 0, []

        for rid in range(self.rutil.getSize()):
            #check that the student is neither registered for AM nor PM, and that their list of choices is not empty
            if not self.rutil.isRegistered(rid,"AM") and not self.rutil.isRegistered(rid,"PM") and self.rutil.getTimeChoices(rid,"AM",self.cutil) != [] and self.rutil.getTimeChoices(rid,"PM",self.cutil) != []:
                bothMiss += 1
                bLog.append(rid)
            elif not self.rutil.isRegistered(rid,"AM") and self.rutil.getTimeChoices(rid,"AM",self.cutil) != []:
                aMiss += 1
                aLog.append(rid)

            elif not self.rutil.isRegistered(rid,"PM") and self.rutil.getTimeChoices(rid,"PM",self.cutil) != []:
                pMiss += 1
                pLog.append(rid)

        print("\n--------------------------------Missing Classes--------------------------------")
        print(f"{aMiss} students do not have an AM class")
        #if a student without an AM class exists, print their class choices
        if aMiss > 0:
            print("Their choices are:")
            for rid in aLog:
                print(f"Student {rid}: {self.rutil.getTimeChoices(rid,'AM',self.cutil)}")
        print(f"{pMiss} students do not have an PM class")
        #if a student without an PM class exists, print their class choices
        if pMiss > 0:
            print("Their choices are:")
            for rid in pLog:
                print(f"Student {rid}: {self.rutil.getTimeChoices(rid,'PM',self.cutil)}")
        print(f"{bothMiss} have neither\n")
        if bothMiss > 0:
            print("Their choices are:")
            for rid in bLog:
                print(f"Student {rid}: {self.rutil.getTimeChoices(rid,'AM',self.cutil)} and {self.rutil.getTimeChoices(rid,'PM',self.cutil)}")

        self.bLog = bLog
        self.aLog = aLog
        self.pLog = pLog
    
    





class GreedyRandomStudent(Strategy):
    def __init__(self, cutil, rutil):
        super().__init__(cutil, rutil)

    def eval(self):
        for rid in self.lotto:
            amChoices = self.rutil.getTimeChoices(rid,"AM",self.cutil)
            #pmChoices = self.rutil.getTimeChoices(rid,"PM",self.cutil)


            for currClass in amChoices:
                cid = self.cutil.getId(currClass)
                if Utils.addToClass(cid,rid,self.cutil,self.rutil):
                    break

        self.lotto = self.shuffle()
        for rid in self.lotto:
            pmChoices = self.rutil.getTimeChoices(rid,"PM",self.cutil)
            for currClass in pmChoices:
                cid = self.cutil.getId(currClass)
                if Utils.addToClass(cid,rid,self.cutil,self.rutil):
                    break 
