import json

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

def addVoter(user, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        # Verification : L'utilisateur doit avoir un code de vote pour ce vote
        cDv = getCredential(user, voteID)
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

def verifyVoteCode(cDv, voteID):
    with open("json/votes.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote["Admin"] for vote in dataVote if vote["ID"] == voteID), 0)
        if not matchVote:
            return 0
        if cDv in matchVote["Voters"]:
            return 1
        return 0


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

def addVoteCode(user, voteID, cDv):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        match = next((person for person in data
                      if person["lname"].lower() == user["lname"].lower()
                      and person["fname"].lower() == user["fname"].lower()
                      and person["mail"].lower() == user["mail"].lower())
                     , 0)

        if not match:
            print("Erreur lors de l'ajout du code de vote : l'utilisateur n'a pas de compte.")
            return

        match["Credentials"].append({"voteID": voteID, "voteCode": cDv})

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

def addCredential(user, voteID, credential):
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

        match["Credentials"].append({"voteID": voteID, "credential": credential})

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
                         ,0)
        if not matchUser:
            print("Erreur lors de la récupération du credential : l'utilisateur n'a pas accès au vote {}.".format(voteID))
            return

        return matchCode["credential"]

# def addMDP(user, voteID, mdp):
#     with open("./json/users.json", "r") as users:
#         data = json.load(users)
#
#         match = next((person for person in data
#                       if person["lname"].lower() == user["lname"].lower()
#                       and person["fname"].lower() == user["fname"].lower()
#                       and person["mail"].lower() == user["mail"].lower())
#                      , 0)
#
#         if not match:
#             print("Erreur lors de la génération du mot de passe : l'utilisateur n'a pas de compte.")
#             return
#
#
#         match["Passwords"].append({"voteID": voteID, "mdp": mdp})
#
# def verifyPassword(mdp, voteID):
#     with open("json/users.json", "r") as users:
#         dataUser = json.load(users)
#
#         matchUser = next((user for user in dataUser
#                           for pw in user["Passwords"]
#                           if pw["voteID"] == voteID
#                           and pw["mdp"] == mdp), 0)
#         if not matchUser:
#             return 0
#         return 1