import json
import struct


###---------- FONCTIONS JSON----------###

##---- VOTES.JSON ----##
def getVotePubKeys(voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        if not matchVote:
            print("Erreur lors de la récupération de vote : le vote {} n'a pas été trouvé.".format(voteID))
            return 0
        return matchVote["Keys"]["public"]


def getVotePrivateKey(voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        if not matchVote:
            print("Erreur lors de la récupération de vote : le vote {} n'a pas été trouvé.".format(voteID))
            return 0
        return matchVote["Keys"]["private"]


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
    with open("json/votes.json", "w") as votes:
        json.dump(data, votes)


def deleteVote(voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        dataVote.remove(matchVote)

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def getAllVotes():
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        return dataVote


def addVote(vote):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)
        dataVote.append(vote)
    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def getVote(voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        if not matchVote:
            print("Erreur lors de la récupération de vote : le vote {} n'a pas été trouvé.".format(voteID))
            return 0
        return matchVote


def addVoter(user, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        # Verification : L'utilisateur doit avoir un code de vote pour ce vote
        uuid = getUUID(user, voteID)
        cDv = getVoteCode(user, voteID)
        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        matchVote["Voters"].append(uuid)
        matchVote["VoteCodes"].append(cDv)

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def addAdmin(user, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        # Verification : L'utilisateur doit avoir un UUID pour ce vote
        uuid = getUUID(user, voteID)
        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        matchVote["Admin"] = uuid

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def getAdmin(voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)
        return next((vote["Admin"] for vote in dataVote if vote["ID"] == voteID), 0)


def addAuthorized(user, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        # Verification : L'utilisateur doit avoir un UUID pour ce vote
        uuidUser = getUUID(user, voteID)
        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        if not matchVote:
            print("Erreur lors de l'ajout de l'autorisée")
            return
        matchVote["Authorized"].append(uuidUser)

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def findVotesWhereVoter(user):
    return [getVote(credential["voteID"]) for credential in user["Credentials"]]


def findVotesWhereAdmin(user):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        return [vote for vote in dataVote
                for item in user["uuids"]
                if vote["Admin"] == item["uuid"]
                ]


def findVotesWhereAuthorized(user):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        return [vote for vote in dataVote
                for person in user["uuids"]
                if person["uuid"] in vote["Authorized"]
                ]


def emptyVoteVoteCodes():
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        for vote in dataVote:
            vote["VoteCodes"] = []

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def addVoteVoteCode(voteID, cDv):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        matchVote["VoteCodes"].append(cDv)

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def verifyVoteCode(code, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

    matchVote = getVote(voteID)
    if not matchVote:
        return False
    if code in matchVote["VoteCodes"]:
        return True
    return False


def addBallot(ballot, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        matchVote["Ballots"].append(ballot)

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def getAllBallots(voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        return matchVote["Ballots"]


def deleteBallot(ballot, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        matchVote["Ballots"].remove(ballot)

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


def getAllVoteCodes(voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        return matchVote["VoteCodes"]


def setVoteResult(winner, total, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        data = {
            "Response": winner,  # String
            "Count": total  # Int
        }
        matchVote["Result"] = data

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)


##---- USERS.JSON ----##
def getUser(lname, fname, email):
    with open("./json/users.json") as users:
        dataUser = json.load(users)

        return next((user for user in dataUser
                     if user["lname"].lower() == lname.lower()
                     and user["fname"].lower() == fname.lower()
                     and user["mail"].lower() == email.lower()), [])


def getAllUsers():
    with open("./json/users.json") as users:
        dataUser = json.load(users)
        return dataUser


def getUserFromUUID(uuid):
    with open("./json/users.json") as users:
        dataUser = json.load(users)

        return next((user for user in dataUser
                     for item in user["uuids"]
                     if user["uuid"] == uuid), 0)


def addUser(user):
    with open("./json/users.json") as users:
        dataUser = json.load(users)
        dataUser.append(user)

    with open("./json/users.json", "w") as users:
        json.dump(dataUser, users)


def addUUID(user, voteID, uuid):
    with open("./json/users.json", "r") as users:
        data = json.load(users)
        match = next((person for person in data
                      if person["lname"].lower() == user["lname"].lower()
                      and person["fname"].lower() == user["fname"].lower()
                      and person["mail"].lower() == user["mail"].lower())
                     , 0)

        if not match:
            print("Erreur lors de l'ajout de l'UUID : l'utilisateur n'a pas de compte.")
            return

        match["uuids"].append({"voteID": voteID, "uuid": uuid})

    with open("./json/users.json", "w") as users:
        json.dump(data, users)


def getUUID(user, voteID):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        matchUser = next((person for person in data
                          if person["lname"].lower() == user["lname"].lower()
                          and person["fname"].lower() == user["fname"].lower()
                          and person["mail"].lower() == user["mail"].lower())
                         , 0)

        if not matchUser:
            print("Erreur lors de la récupération de l'UUID : l'utilisateur n'a pas de compte.")
            return

        matchVote = next((uuid for uuid in matchUser["uuids"]
                          if uuid["voteID"] == voteID)
                         , "")
        if matchVote == "":
            return matchVote
        return matchVote["uuid"]


def setUserVoteCode(user, voteID, cDv):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        matchUser = next((person for person in data
                          if person["lname"].lower() == user["lname"].lower()
                          and person["fname"].lower() == user["fname"].lower()
                          and person["mail"].lower() == user["mail"].lower())
                         , 0)

        matchingVote = next((infos for infos in matchUser["Credentials"]
                             if infos["voteID"] == voteID), 0)

        matchingVote["voteCode"] = cDv

    with open("./json/users.json", "w") as users:
        json.dump(data, users)


def getVoteCode(user, voteID):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        matchUser = next((person for person in data
                          if person["lname"].lower() == user["lname"].lower()
                          and person["fname"].lower() == user["fname"].lower()
                          and person["mail"].lower() == user["mail"].lower())
                         , 0)

        if not matchUser:
            print("Erreur lors de la récupération du credential : l'utilisateur n'a pas de compte.")
            return

        matchCode = next((credential for credential in matchUser["Credentials"]
                          if credential["voteID"] == voteID)
                         , 0)
        if not matchUser:
            print(
                "Erreur lors de la récupération du credential : l'utilisateur n'a pas accès au vote {}.".format(voteID))
            return

        return matchCode["voteCode"]


def addCredentials(user, voteID, credential, cDv):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        match = next((person for person in data
                      if person["lname"].lower() == user["lname"].lower()
                      and person["fname"].lower() == user["fname"].lower()
                      and person["mail"].lower() == user["mail"].lower())
                     , 0)

        if not match:
            print("Erreur lors de l'ajout du credential' : l'utilisateur n'a pas de compte.")
            return

        match["Credentials"].append({"voteID": voteID, "credential": credential, "voteCode": cDv})

    with open("./json/users.json", "w") as users:
        json.dump(data, users)


def getCredential(user, voteID):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        matchUser = next((person for person in data
                          if person["lname"].lower() == user["lname"].lower()
                          and person["fname"].lower() == user["fname"].lower()
                          and person["mail"].lower() == user["mail"].lower())
                         , 0)

        if not matchUser:
            print("Erreur lors de la récupération du credential : l'utilisateur n'a pas de compte.")
            return

        matchCode = next((credential for credential in matchUser["Credentials"]
                          if credential["voteID"] == voteID)
                         , 0)
        if not matchUser:
            print(
                "Erreur lors de la récupération du credential : l'utilisateur n'a pas accès au vote {}.".format(voteID))
            return

        return matchCode["credential"]
