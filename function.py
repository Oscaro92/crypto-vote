from functionJSON import *
from pbkdf2 import crypt
import uuid
import string
import random

def createVote(user, voteID):
    vote = []

    quest = input("Quelle est votre question ? ")
    nbAns = int(input("Nombre de réponse possible ? "))

    vote.append(quest)

    for i in range(0, nbAns):
        msg = "Réponse {} : ".format(i + 1)
        ans = input(msg)
        vote.append(ans)

    #save vote in json
    data = {
        "ID": voteID,
        "Question": vote[0],
        "Response": vote[1:3],
        "Voters": [],
        "Admins": [],
        "Authorized": []
    }
    AddVote(user, data)

    msg = 'Le vote {} "{}" est créé !\n'.format(voteID, quest)
    print(msg)
    print("Les réponses possibles sont : ")
    for i in range(1, nbAns+1):
        print(vote[i])

def saveVoter(voteID):
    print("Renseignez les informations suivantes :\n")
    lname = input("Nom: ")
    fname = input("Prénom: ")
    email = input("Email: ")

    userFound = getUser(lname, fname, email)

    if not userFound == []:
        generateUUID(userFound, voteID) #GENERATION DE L'UUID UNIQUE AU VOTE
        addVoter(userFound, voteID) # AJOUT DU DROIT DE VOTE
        print("\nCette personne sera-t-elle Admin ?\n\n"
              "1 - Oui.\n"
              "0 - Non.\n")
        choice = int(input("Votre choix : "))
        if choice:
            addAdmin(userFound, voteID) # AJOUT DES DROITS ADMINS

        print("\nCette personne sera-t-elle autorisée à dépouiller ?\n\n"
          "1 - Oui.\n"
          "0 - Non.\n")
        choice = int(input("Votre choix : ")) # AJOUT DES DROITS DEPOUILLEMENT
        if choice:
            addAuthorized(userFound, voteID)

    #Si on ne trouve pas l'utilisateur, on lui créé un compte
    else:
        data = {
            "lname": lname,
            "fname": fname,
            "email": email,
            "uuids": []
        }

        print("\nCette personne sera-t-elle Admin ?\n\n"
              "1 - Oui.\n"
              "0 - Non.\n")
        choice = int(input("Votre choix : ")) # AJOUT DES DROITS ADMINS
        if choice:
              data["voteAdmin"] = [voteID]
        else:
            data["voteAdmin"] = []

        print("\nCette personne sera-t-elle autorisée à dépouiller ?\n\n"
              "1 - Oui.\n"
              "0 - Non.\n")
        choice = int(input("Votre choix : "))  # AJOUT DES DROITS DEPOUILLEMENT
        if choice:
            data["voteAuthorized"] = [voteID]
        else:
            data["voteAuthorized"] = []

        addUser(data)

    print("Electeur enregistré ! \n")

def saveVote():
    print("Vote enregistré ! \n")

def checkVote():
    print("Vote vérifié ! \n")

def counting():
    print("Dépouillement fait ! \n")

def generateC():
    c = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(14))
    return c

def createS():
    s = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(s), 15):
        s = ''.join(random.choice(string.digits) for x in range(3))

    return int(s)

def createPub(s, g):
    pub = 0
    cond = True

    while cond == True:
        pub = g ** s
        if len(str(pub)) > 512 and len(str(pub)) < 1000 :
            cond = False

    return pub

def generate(a, Z):
    for i in range(1, Z):
        b = (a**i)%Z
        if b == 1:
            if i == Z-1:
                return True
            else :
                return False

