import json
import uuid


def writeJSON(data, path):
    with open(path, 'w') as mon_fichier:
        json.dump(data, mon_fichier)


def readJSON(path):
    with open(path) as mon_fichier:
        data = json.load(mon_fichier)

    return data


def getUser(lname, fname, email):
    data = readJSON("./json/users.json")

    for i in range(1, len(data)):
        infos = data[i]
        if infos["lname"].lower() == lname.lower() \
                and infos["fname"].lower() == fname.lower() \
                and infos["mail"].lower() == email.lower():
            return infos
    return []


def voteExist(voteID):
    data = readJSON("./json/vote.json")
    for i in range(1, len(data)):
        infos = data[i]
        if infos["ID"] == voteID:
            return 1
        else:
            return 0


def getUnusedVoteID():
    data = readJSON("./json/vote.json")
    scheme = range(1, 10)
    UsedID = []
    for i in range(0, len(data)):
        infos = data[i]
        UsedID.append(infos["ID"])

    for id in scheme:
        if not id in UsedID:
            return id


def AddVote(user, data):
    generateUUID(user, data["ID"])

    #On rafraichit l'utilisateur modifié (ajout de l'uuid)
    with open("./json/users.json") as users:
        dataUser = json.load(users)
        #Je retrouve mon 'user'
        matchUser = next((infos for infos in dataUser if infos["lname"].lower() == user["lname"].lower() \
                    and infos["fname"].lower() == user["fname"].lower() \
                    and infos["mail"].lower() == user["mail"].lower()))
        #Je retrouve l'UUID correspondant au vote (fraichement généré)
        match = next((pair for pair in matchUser["uuids"] if pair["voteID"] == data["ID"]), 0)
        if match:
            data["Admins"].append(match["uuid"])
        else:
            print("Erreur lors de la création du vote : l'utilisateur n'a pas d'UUID pour ce vote.")
            return

    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)
        dataVote.append(data)
    with open("./json/vote.json", "w") as votes:
        json.dump(dataVote, votes)


def getVote(ID):
    if voteExist(ID):
        data = readJSON("./json/vote.json")
        for i in range(1, len(data)):
            infos = data[i]
            if infos["ID"] == ID:
                return infos
    else:
        return []


def addUser(data):
    dataFinal = readJSON("./json/users.json")

    print(dataFinal)
    dataFinal.append(data)
    print(dataFinal)

    writeJSON(dataFinal, "./json/users.json")


def generateUUID(user, voteID):
    with open("./json/users.json") as mon_fichier:
        data = json.load(mon_fichier)

        for i in range(1, len(data)):
            infos = data[i]
            if infos["lname"].lower() == user["lname"].lower() \
                    and infos["fname"].lower() == user["fname"].lower() \
                    and infos["mail"].lower() == user["mail"].lower():
                infos["uuids"].append({"voteID": voteID, "uuid": str(uuid.uuid4())})
                writeJSON(data, "./json/users.json")
                return

    print("Erreur lors de la génération de l'UUID : l'utilisateur n'a pas de compte.")
    return


def addVoter(user, voteID):
    data = readJSON("./json/vote.json")

    for i in range(1, len(data)):
        infos = data[i]
        # Verification : L'utilisateur doit avoir un UUID pour ce vote
        match = next((pair for pair in user["uuids"] if pair["voteID"] == voteID), 0)
        if match:
            infos["Voters"].append(match["uuid"])
        else:
            print("Erreur lors de l'ajout de l'électeur : l'utilisateur n'a pas d'UUID pour ce vote.")
            return

    writeJSON(data, "./json/vote.json")


def addAdmin(user, voteID):
    data = readJSON("./json/vote.json")

    for i in range(1, len(data)):
        infos = data[i]
        match = next((pair for pair in user["uuids"] if pair["voteID"] == voteID), 0)
        if match:
            infos["Admins"].append(user["uuid"])
        else:
            print("Erreur lors de l'ajout de l'administrateur : l'utilisateur n'a pas d'UUID pour ce vote.")
            return

    writeJSON(data, "./json/vote.json")


def addAuthorized(user, voteID):
    data = readJSON("./json/vote.json")

    for i in range(1, len(data)):
        infos = data[i]
        match = next((pair for pair in user["uuids"] if pair["voteID"] == voteID), 0)
        if match:
            infos["Authorized"].append(user["uuid"])
        else:
            print("Erreur lors de l'ajout de l'autorisée : l'utilisateur n'a pas d'UUID pour ce vote.")
            return

    writeJSON(data, "./json/vote.json")


def findVotesWhereVoter(user):
    data = readJSON("./json/vote.json")

    result = []
    for i in range(1, len(data)):
        infos = data[i]
        # On vient parcourir tous les UUID de l'utilisateur (unique à 1 seul vote)
        if any(pair["uuid"] in infos["Voters"] for pair in user["uuids"]):
            result.append(infos)
        return result


def findVotesWhereAdmin(user):
    data = readJSON("./json/vote.json")

    result = []
    for i in range(1, len(data)):
        infos = data[i]
        # On vient parcourir tous les UUID de l'utilisateur (unique à 1 seul vote)
        if any(pair["uuid"] in infos["Admins"] for pair in user["uuids"]):
            result.append(infos)
    return result


def findVotesWhereAuthorized(user):
    data = readJSON("./json/vote.json")

    result = []
    for i in range(1, len(data)):
        infos = data[i]
        # On vient parcourir tous les UUID de l'utilisateur (unique à 1 seul vote)
        if any(pair["uuid"] in infos["Authorized"] for pair in user["uuids"]):
            result.append(infos)
    return result


def deleteAllVote():
    data = [
        {
            "ID": 0,
            "Question": "BASE",
            "Response": [
                "A",
                "B"
            ],
            "Voters": [],
            "Admins": [],
            "Authorized": []
        },
    ]
    writeJSON(data, "./json/vote.json")
