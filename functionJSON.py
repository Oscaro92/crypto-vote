import json
import uuid
import random
import string
from pbkdf2 import crypt


###---------- FONCTIONS JSON----------###

##---- VOTES.JSON ----##
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

def getUnusedVoteID():
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)
        # On considère 10 votes en simultané.
        scheme = range(1, 10)
        UsedID = [vote["ID"] for vote in dataVote]
        return next(id for id in scheme if id not in UsedID)

def addVoter(user, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        # Verification : L'utilisateur doit avoir un code de vote pour ce vote
        cDv = getcDv(user, voteID)
        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        matchVote["Voters"].append(cDv)

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
        matchUser = next((pair for pair in user["uuids"] if pair["voteID"] == voteID), 0)
        if not matchUser:
            print("Erreur lors de l'ajout de l'autorisée : l'utilisateur n'a pas d'UUID pour ce vote.")
            return
        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        if not matchVote:
            print("Erreur lors de l'ajout de l'autorisée : le vote n'a pas été trouvé.")
            return
        matchVote["Authorized"].append(matchUser["uuid"])

    with open("json/votes.json", "w") as votes:
        json.dump(dataVote, votes)

def findVotesWhereVoter(user):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        return [vote for vote in dataVote
                for person in user["uuids"]
                for person["uuid"] in vote["Voters"]
                ]

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
                for person["uuid"] in vote["Authorized"]
                ]

##---- USERS.JSON ----##
def getUser(lname, fname, email):
    with open("./json/users.json") as users:
        dataUser = json.load(users)

        return next((user for user in dataUser
                          if user["lname"].lower() == lname.lower()
                          and user["fname"].lower() == fname.lower()
                          and user["mail"].lower() == email.lower()), 0)

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
                         ,0)
        if not matchUser:
            print("Erreur lors de la récupération de l'UUID : l'utilisateur n'a pas accès au vote {}.".format(voteID))
            return

        return matchVote["uuid"]

def addCDV(user, voteID, cDv):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        match = next((person for person in data
                      if person["lname"].lower() == user["lname"].lower()
                      and person["fname"].lower() == user["fname"].lower()
                      and person["mail"].lower() == user["mail"].lower())
                     , 0)

        if not match:
            print("Erreur lors de la génération du code de vote : l'utilisateur n'a pas de compte.")
            return

        #Génération du code de vote à partir de l'UUID
        match["CodesDeVote"].append({"voteID": voteID, "cDv": cDv})

    with open("./json/users.json", "w") as users:
        json.dump(data, users)

def getcDv(user, voteID):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        matchUser = next((person for person in data
                      if person["lname"].lower() == user["lname"].lower()
                      and person["fname"].lower() == user["fname"].lower()
                      and person["mail"].lower() == user["mail"].lower())
                     , 0)

        if not matchUser:
            print("Erreur lors de la récupération du code de vote : l'utilisateur n'a pas de compte.")
            return

        matchVote = next((cDv for cDv in matchUser["CodesDeVote"]
                          if cDv["voteID"] == voteID)
                         ,0)
        if not matchUser:
            print("Erreur lors de la récupération du code de vote : l'utilisateur n'a pas accès au vote {}.".format(voteID))
            return

        return matchVote["cDv"]