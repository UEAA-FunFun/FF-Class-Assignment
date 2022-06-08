class Mapper2022:
    @staticmethod
    def rProcess(pData):
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

        #there are many dup choices in this data
        fst,snd,trd = [],[],[]
        if "stChoice" in pData and pData["stChoice"] != "None":
            fst.append(pData["stChoice"])
        for j in range(7):
            if f"stChoice{j}" in pData and pData[f"stChoice{j}"] != "None":
                fst.append(pData[f"stChoice{j}"])
        
        if "ndChoice" in pData and pData["ndChoice"] != "None":
            snd.append(pData["ndChoice"])
        for j in range(7):
            if f"ndChoice{j}" in pData and pData[f"ndChoice{j}"] != "None":
                snd.append(pData[f"ndChoice{j}"])

        if "rdChoice" in pData  and pData["rdChoice"] != "None":
            trd.append(pData["rdChoice"])
        for j in range(7):
            if f"rdChoice{j}" in pData and pData[f"rdChoice{j}"] != "None":
                trd.append(pData[f"rdChoice{j}"])
        
        res["first choices"] = fst
        res["second choices"] = snd 
        res["third choices"] = trd

        return res

    @staticmethod
    def cProcess(cData):
        res = dict()
        res["name"] = cData["name"]
        res["capacity"] = int(cData["size"])
        res["size"] = 0 
        res["time"] = cData["time"]
        res["roster"] = []
        return res



