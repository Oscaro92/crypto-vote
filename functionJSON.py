import json
import uuid


def getUser(lname, fname, email):
    with open("./json/users.json") as users:
        dataUser = json.load(users)

        matchUser = next((user for user in dataUser
                          if user["lname"].lower() == lname.lower()
                        and user["fname"].lower() == fname.lower()
                        and user["mail"].lower() == email.lower()))
        if not matchUser:
            return []
        return matchUser

def voteExist(voteID):
    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)
        for i in range(1, len(dataVote)):
            infos = dataVote[i]
            if infos["ID"] == voteID:
                return 1
            else:
                return 0


def getUnusedVoteID():
    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)
        # On considère 10 votes en simultané.
        scheme = range(1, 10)
        UsedID = []
        for i in range(0, len(dataVote)):
            infos = dataVote[i]
            UsedID.append(infos["ID"])

        for id in scheme:
            if not id in UsedID:
                return id


def AddVote(user, data):
    generateUUID(user, data["ID"])

    # On rafraichit l'utilisateur modifié (ajout de l'uuid)
    with open("./json/users.json") as users:
        dataUser = json.load(users)
        # Je retrouve mon 'user'
        matchUser = next((infos for infos in dataUser if infos["lname"].lower() == user["lname"].lower() \
                          and infos["fname"].lower() == user["fname"].lower() \
                          and infos["mail"].lower() == user["mail"].lower()))
        # Je retrouve l'UUID correspondant au vote (fraichement généré)
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
    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)

        matchVote = next((vote for vote in dataVote if vote["ID"] == ID), 0)
        if not matchVote:
            print("Erreur lors de la récupération de vote : le vote {} n'a pas été trouvé.".format(ID))
            return
        return matchVote


def addUser(data):
    with open("./json/users.json") as users:
        dataUser = json.load(users)
        dataUser.append(data)

    with open("./json/users.json", "w") as users:
        json.dump(dataUser, users)


def generateUUID(user, voteID):
    with open("./json/users.json", "r") as users:
        data = json.load(users)

        match = next((person for person in data
                      if person["lname"].lower() == user["lname"].lower()
                      and person["fname"].lower() == user["fname"].lower()
                      and person["mail"].lower() == user["mail"].lower())
                     , 0)

        if not match:
            print("Erreur lors de la génération de l'UUID : l'utilisateur n'a pas de compte.")
            return

        match["uuids"].append({"voteID": voteID, "uuid": str(uuid.uuid4())})

    with open("./json/users.json", "w") as users:
        json.dump(data, users)


def addVoter(user, voteID):
    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)

        # Verification : L'utilisateur doit avoir un UUID pour ce vote
        matchUser = next((pair for pair in user["uuids"] if pair["voteID"] == voteID), 0)
        if not matchUser:
            print("Erreur lors de l'ajout de l'électeur : l'utilisateur n'a pas d'UUID pour ce vote.")
            return
        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        if not matchVote:
            print("Erreur lors de l'ajout de l'électeur : le vote n'a pas été trouvé.")
            return
        matchVote["Voters"].append(matchUser["uuid"])

    with open("./json/vote.json", "w") as votes:
        json.dump(dataVote, votes)


def addAdmin(user, voteID):
    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)

        # Verification : L'utilisateur doit avoir un UUID pour ce vote
        matchUser = next((pair for pair in user["uuids"] if pair["voteID"] == voteID), 0)
        if not matchUser:
            print("Erreur lors de l'ajout de l'administrateur : l'utilisateur n'a pas d'UUID pour ce vote.")
            return
        matchVote = next((vote for vote in dataVote if vote["ID"] == voteID), 0)
        if not matchVote:
            print("Erreur lors de l'ajout de l'administrateur : le vote n'a pas été trouvé.")
            return
        matchVote["Admins"].append(matchUser["uuid"])

    with open("./json/vote.json", "w") as votes:
        json.dump(dataVote, votes)


def addAuthorized(user, voteID):
    with open("./json/vote.json", "r") as votes:
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

    with open("./json/vote.json", "w") as votes:
        json.dump(dataVote, votes)


def findVotesWhereVoter(user):
    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)

        return [vote for vote in dataVote
                for person in user["uuids"]
                for person["uuid"] in vote["Voters"]
                ]


def findVotesWhereAdmin(user):
    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)

        return [vote for vote in dataVote
                for person in user["uuids"]
                for person["uuid"] in vote["Admins"]
                ]


def findVotesWhereAuthorized(user):
    with open("./json/vote.json", "r") as votes:
        dataVote = json.load(votes)

        return [vote for vote in dataVote
                for person in user["uuids"]
                for person["uuid"] in vote["Authorized"]
                ]


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
    with open("./json/vote.json", "w") as votes:
        json.dump(data, votes)
