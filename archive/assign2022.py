import csv
import re
from utils import *
import json
import random


#Utils
#takes the original pData and removes irrelevant fields
#ship of theseus
#Last	First	Year	Age	Gender	Class	Class Location	Special Considerations	Primary Contact	Primary #	Relationship	Secondary Contact	Secondary #	Relationship	Self Dismisal?	Leave with Relative/Sibling	Shirt Size
def process(pData):
    res = dict()
    
    res["Last"] = pData["lastName"]
    res["First"] = pData["firstName"]
    if "gender" in pData:
        res["Gender"] = pData["gender"]
    else:
        res["Gender"] = "Not Specified"
    res["YOB"] = pData["yearOfBirth"]

    #lmao
    if "specialConcernsDietaryRestrictionsDueToReligiousOrOtherReasonsFoodAllergiesPhysicalConditionMedicationEtcPleaseSpecifyIfAny" in pData:
        res["Special Considerations"] = pData["specialConcernsDietaryRestrictionsDueToReligiousOrOtherReasonsFoodAllergiesPhysicalConditionMedicationEtcPleaseSpecifyIfAny"]
    else:
        res["Special Considerations"] = "None"

    res["Primary Contact"] = pData["primaryContact"]
    res["Primary Telephone"] = pData["telephone"]
    if "relationship" in pData:
        res["Primary Relationship"] = pData["relationship"]
    else:
        res["Primary Relationship"] = "NA"

    if "secondaryContact" in pData:
        res["Secondary Contact"] = pData["secondaryContact"]
    else:
        res["Secondary Contact"] = "None"
    if "telephone2" in pData:
        res["Secondary Telephone"] = pData["telephone2"]
    else:
        res["Secondary Telephone"] = "None"
    if "relationship2" in pData:
        res["Secondary Relationship"] = pData["relationship2"]
    else:
        res["Secondary Relationship"] = "None"
    
    res["Self Dismissed?"] = pData["ifParticipantIsAge12OrAboveAllowSelfdismissal"]

    if "allowDismissalWith" in pData:
        res["Dismiss to"] = pData["allowDismissalWith"]
    else:
        res["Dismiss to"] = "NA"

    if "relationshipWithStudent" in pData:
        res["Dismiss Relationship"] = pData["relationshipWithStudent"]
    else:
        res["Dismiss Relationship"] = "NA"

    res["Shirt Size"] = pData["tshirtSize"]


    return res


util = Utils(process,"data","output")

__location__ = util.dataPath

__sheet_location__ = util.outputPath




for i in cInfo:
    print(cInfo[i])

with open(os.path.join(__location__,"responses.json")) as jFile:
    data = json.load(jFile)

#transform
idData = dict()
for i,row in enumerate(data):
    #because fun data, look for all instances of stdata<num> and add new entry "first" to consolidate
    fst,snd,trd = [],[],[]
    if "stChoice" in row and row["stChoice"] != "None":
        fst.append(row["stChoice"])
    for j in range(7):
        if f"stChoice{j}" in row and row[f"stChoice{j}"] != "None":
            fst.append(row[f"stChoice{j}"])
    
    if "ndChoice" in row and row["ndChoice"] != "None":
        snd.append(row["ndChoice"])
    for j in range(7):
        if f"ndChoice{j}" in row and row[f"ndChoice{j}"] != "None":
            snd.append(row[f"ndChoice{j}"])

    if "rdChoice" in row  and row["rdChoice"] != "None":
        trd.append(row["rdChoice"])
    for j in range(7):
        if f"rdChoice{j}" in row and row[f"rdChoice{j}"] != "None":
            trd.append(row[f"rdChoice{j}"])

    idData[i] = {"row" : row, 1 : fst, 2 : snd, 3 : trd}

#util

#shuffle
enum = list(range(len(idData)))
random.shuffle(enum)


#



#args: pData - idData[i]
#      info - class info dict
#returns: chosen classes added and reformats old pData (not in place). Will also update cInfo with new size and roster addition
def getPicks(pData, info):
    res = []
    
    for i in [1,2,3]:
        for curr in pData[i]:
            if len(res) == 2:
                return res 
            if info[nameToId[curr]]["size"] < info[nameToId[curr]]["max"]:

                #check not 2 classess at same time period
                if len(res) == 1 and info[nameToId[curr]]["time"] == info[nameToId[res[0]]]["time"]:
                    print(f"{res[0]} and {curr} are at the same time!")
                else:
                    res.append(curr)
                    info[nameToId[curr]]["size"] += 1

                    ppData = process(pData["row"])
                    info[nameToId[curr]]["roster"].append(ppData)
    return res

            
            

for i in enum:
    idData[i]["assigned"] = getPicks(idData[i],cInfo)
    print(idData[i][1],idData[i][2],idData[i][3])
    print(idData[i]["assigned"])
    
    #now that classes are assigned for this participant assigned, add both classes and process fields
    idData[i]["row"] = process(idData[i]["row"])
    
    idData[i]["row"]["class1"] = ""
    idData[i]["row"]["class2"] = ""
    if len(idData[i]["assigned"]) >= 1:
        idData[i]["row"]["class1"] = idData[i]["assigned"][0]
    if len(idData[i]["assigned"]) == 2:
        idData[i]["row"]["class2"] = idData[i]["assigned"][1] 

for i in cInfo:
    entry = cInfo[i]
    print(entry["name"],entry["size"],entry["max"])

numUnass = 0
for i in enum:
    if len(idData[i]["assigned"]) == 0:
        numUnass += 1

numLess = 0
for i in enum:
    if len(idData[i]["assigned"]) < len(idData[i][1]):
        numLess += 1
        print(idData[i]["row"]["First"],idData[i]["assigned"],idData[i][1])
print(f"there are {numUnass} students without any classes")
print(f"there are {numLess} students with one class when they wanted two")


# with open(os.path.join(__sheet_location__,"assigned.json"),"w+") as new:
#     json.dump(cInfo,new)

#Now since spreadsheets are important, lets turn this json into a bunch of csvs L
#Also an overall one
overall = dict()
okeys = idData[i]["row"].keys()
keys = cInfo["1"]["roster"][0].keys()
with open(os.path.join(__sheet_location__,"overall.csv"),"w+") as o:
    oWrite = csv.DictWriter(o, okeys)
    oWrite.writeheader()
    
    for i in cInfo:
        entry = cInfo[i]
        name = entry["name"]



        with open(os.path.join(__sheet_location__,f'{re.sub(r"[^a-zA-Z0-9]","",name)}.csv'),"w+") as c:
            w = csv.DictWriter(c, keys)
            w.writeheader()
            w.writerows(entry["roster"])
        
    
    oWrite.writerows([idData[i]["row"] for i in idData])

#NOTE: CVS is a stupid broken format for most use cases
# #Open responses
# with open(os.path.join(__location__, 'responses.csv'),"r+") as responses:
#     rList = responses.readlines()

# #Get Header
# header = rList[0].split(",")



# print(header)
# #filter all responses that do not correspond to ranked choices. Class names should be translated to some class id
# #dict of id -> {first: ..., second: ..., third: ...}

# #regex match 1st choice, 2nd choice, 3rd choice to get those indices
# def matchedInd(pattern : str,listCols : list[str]) -> list[int]:
#     res = []
#     for i,col in enumerate(listCols):
#         if re.match(pattern,col):
#             res.append(i)
#     return res

# choice1 = matchedInd("1st Choice", header) 
# choice2 = matchedInd("2nd Choice", header)
# choice3 = matchedInd("3rd Choice", header)

# for i in choice1:
#     print(header[i])
# cIndList = [choice1,choice2,choice3]

# for row in rList:
#     print(len(row.split(",")))

# #enum responses in a dict as their ids
# #store {row : original string, 1 : first choice, 2 : second choice, 3 : choice 3}
# rDict = dict()

# for i,row in enumerate(rList[1:]):
#     print("new row!")
#     subDict = dict()
#     subDict["row"] = row

#     parsedRow = row.split(",")
#     print(row)
#     print(parsedRow)

#     for choiceInd in range(3):
#         print(f"{choiceInd + 1} choice")
#         #AM and PM
#         chosenClasses = []
#         for j in cIndList[choiceInd]:
#             classPicked = parsedRow[j]
#             if classPicked != "":
#                 print(classPicked)
#                 chosenClasses.append(classPicked)

#         subDict[f"choice{choiceInd}"] = chosenClasses


#     rDict[i] = subDict