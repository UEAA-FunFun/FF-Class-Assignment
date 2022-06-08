
from random import shuffle
from utils import *
# how we assign classes. Should come with a function that prints
#metrics
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
        
        aMiss = 0
        pMiss = 0
        bothMiss = 0
        for rid in range(self.rutil.getSize()):
            if not self.rutil.isRegistered(rid,"AM") and not self.rutil.isRegistered(rid,"PM"):
                bothMiss += 1
            elif not self.rutil.isRegistered(rid,"AM"):
                aMiss += 1

            elif not self.rutil.isRegistered(rid,"PM"):
                pMiss += 1

        print("\n--------------------------------Missing Classes--------------------------------")
        print(f"{aMiss} students do not have an AM class")
        print(f"{pMiss} students do not have an PM class")
        print(f"{bothMiss} have neither")





class GreedyRandomStudent(Strategy):
    def __init__(self, cutil, rutil):
        super().__init__(cutil, rutil)

    def eval(self):
        for rid in self.lotto:
            amChoices = self.rutil.getTimeChoices(rid,"AM",self.cutil)
            pmChoices = self.rutil.getTimeChoices(rid,"PM",self.cutil)


            for currClass in amChoices:
                cid = self.cutil.getId(currClass)
                if Utils.addToClass(cid,rid,self.cutil,self.rutil):
                    break

            for currClass in pmChoices:
                cid = self.cutil.getId(currClass)
                if Utils.addToClass(cid,rid,self.cutil,self.rutil):
                    break

