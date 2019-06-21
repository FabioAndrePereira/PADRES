import json



def rulesJSON(data):
    dataRet = []
    for i in data:
        ruleOBJ = {}

        ruleOBJ['rID'] = i[0]
        ruleOBJ['rDefinition'] = i[1]

        dataRet.append(ruleOBJ)
    return json.dumps(dataRet)

def principlesJSON(data):
    dataRet = []
    for i in data:
        pOBJ = {}

        pOBJ['pID'] = i[0]
        pOBJ['pDefinition'] = i[1]

        dataRet.append(pOBJ)
    return json.dumps(dataRet)

def countryJSON(data):
    dataRet = []
    for i in data:
        cOBJ = {}

        cOBJ['cID'] = i[0]
        cOBJ['cName'] = i[1]
        cOBJ['cAcronym'] = i[2]

        dataRet.append(cOBJ)
    return json.dumps(dataRet)

def phJSON(data):
    dataRet = []
    for i in data:
        phOBJ = {}

        phOBJ['phID'] = i[0]
        phOBJ['phDesc'] = i[1]

        dataRet.append(phOBJ)
    return json.dumps(dataRet)


def swJSON(data):
    dataRet = []
    for i in data:
        swOBJ = {}

        swOBJ['id'] = i[0]
        swOBJ['description'] = i[1]

        dataRet.append(swOBJ)
    return json.dumps(dataRet)

