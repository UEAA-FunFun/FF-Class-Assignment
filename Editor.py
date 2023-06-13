import os 
import json 
from Loader import Loader
from utils import *

class Editor(Loader):
    '''
    Editor is responsible for making changes to the output changes. In particular,
    if a change is made to a specific student in a specific class, it should be consistent
    across the master csv and the class csv.
    '''
    def __init__(self,cutil,rutil,dataPath,outputPath) -> None:
        super().__init__(dataPath,outputPath)
        self.cutil = cutil
        self.rutil = rutil
    


    def loop(self):
        curr = input("0: View classes\n1: View class rosters\n2: Remove a student\n3: Move Student\ninput:")
        if curr == "0":
            self.cutil.printClasses()
            input("Press enter to continue...")

        elif curr == "1":
            self.cutil.printClasses()
            chooseClass = input("Enter class id: ")
            self.cutil.printClassRoster(int(chooseClass))
            input("Press enter to continue...")
        
        elif curr == "2":
            self.cutil.printClasses()
            chosenClass = input("Enter class id: ")
            print("Here is the current roster")
            self.cutil.printClassRoster(int(chosenClass))
            chosenStudent = input("Enter student id to remove: ")
            
            Utils.removeFromClass(int(chosenClass),int(chosenStudent),self.cutil,self.rutil)

            print("Here is the new roster")
            self.cutil.printClassRoster(int(chosenClass))
            input("Press enter to continue...")

        elif curr == "3":
            self.cutil.printClasses()
            chosenClass = input("Enter class id: ")
            print("Here is the current roster")
            self.cutil.printClassRoster(int(chosenClass))
            chosenStudent = input("Enter student id to move: ")
            print("Here are classes that you can move them to")

            self.cutil.printClasses(lambda x: x["cid"] != int(chosenClass) and x["size"] < x["capacity"] and x["time"] == self.cutil.getTime(int(chosenClass)))
            chosenClass2 = input("Enter class id to move to: ")
            Utils.removeFromClass(int(chosenClass),int(chosenStudent),self.cutil,self.rutil)
            Utils.addToClass(int(chosenClass2),int(chosenStudent),self.cutil,self.rutil)
            print("Here is the new roster of class" + self.cutil.getName(int(chosenClass)))
            self.cutil.printClassRoster(int(chosenClass))
            self.cutil.printClassRoster(int(chosenClass2))
