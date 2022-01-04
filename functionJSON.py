import json

def writeJSON(data, path):
    with open(path, 'w') as mon_fichier:
        json.dump(data, mon_fichier)

def readJSON(path):
    with open(path) as mon_fichier:
        data = json.load(mon_fichier)

    return data

def userExist(lname, fname, email):
    with open("./json/users.json") as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["lname"] == lname and infos["fname"] == fname and infos["email"] == email:
            return 1

    return 0

def voteExist(voteID):
    with open("./json/vote.json") as mon_fichier:
        data = json.load(mon_fichier)
    for i in range(0, len(data)):
        infos = data[i]
        if infos["ID"] == voteID:
            return 1
        else:
            return 0

def getVote(ID):
    with open("./json/vote.json") as mon_fichier:
        data = json.load(mon_fichier)
    for i in range(0, len(data)):
        infos = data[i]
        if infos["ID"] == ID:
            return infos
        else:
            return 0

def addUser(data, path):
    with open(path) as mon_fichier:
        dataFinal = json.load(mon_fichier)

    print(dataFinal)
    dataFinal.append(data)
    print(dataFinal)

    with open(path, 'w') as mon_fichier:
        json.dump(dataFinal, mon_fichier)

def addVoteAccess(user, voteID):
    with open("./json/users.json") as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["lname"] == user["lname"] and infos["fname"] == user["fname"] and infos["email"] == user["email"]:
            infos["voteAccess"].append(voteID)

    with open("./json/users.json", 'w') as mon_fichier:
        json.dump(data, mon_fichier)

def addVoteAdmin(user, voteID):
    with open("./json/users.json") as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["lname"] == user["lname"] and infos["fname"] == user["fname"] and infos["email"] == user["email"]:
            infos["voteAdmin"].append(voteID)

    with open("./json/users.json", 'w') as mon_fichier:
        json.dump(data, mon_fichier)

def addVoteAuthorized(user, voteID):
    with open("./json/users.json") as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["lname"] == user["lname"] and infos["fname"] == user["fname"] and infos["email"] == user["email"]:
            infos["voteAuthorized"].append(voteID)

    with open("./json/users.json", 'w') as mon_fichier:
        json.dump(data, mon_fichier)

def findVoteWhereAccess(user):
    with open("./json/users.json") as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["lname"] == user["lname"] and infos["fname"] == user["fname"] and infos["email"] == user["email"]:
            return infos["voteAccess"]

    return 0

def findVoteWhereAdmin(user):
    with open("./json/users.json") as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["lname"] == user["lname"] and infos["fname"] == user["fname"] and infos["email"] == user["email"]:
            return infos["voteAdmin"]

    return 0

def findVoteWhereAuthorized(user):
    with open("./json/users.json") as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["lname"] == user["lname"] and infos["fname"] == user["fname"] and infos["email"] == user["email"]:
            return infos["voteAuthorized"]

    return 0

def voterExist(lname, fname, email, path):
    with open(path) as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["lname"] == lname and infos["fname"] == fname and infos["email"] == email:
            return 1

    return 0

def deleteAllVoter():
    data = []

    with open("./json/voter.json", 'w') as mon_fichier:
        json.dump(data, mon_fichier)