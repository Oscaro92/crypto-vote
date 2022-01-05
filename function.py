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

    # save vote in json
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
    for i in range(1, nbAns + 1):
        print(vote[i])


def saveVoter(voteID):
    print("Renseignez les informations suivantes :\n")
    lname = input("Nom: ")
    fname = input("Prénom: ")
    email = input("Email: ")

    userFound = getUser(lname, fname, email)

    # Si on ne trouve pas l'utilisateur, on lui créé un compte
    if not len(userFound):
        user = {
            "lname": lname,
            "fname": fname,
            "mail": email,
            "uuids": []
        }

        addUser(user)
        print("Compte créé")

    # Génération de l'UUID pour le vote
    generateUUID(userFound, voteID)

    # Rafraichissement
    userFound = getUser(lname, fname, email)
    addVoter(userFound, voteID)
    print("\nCette personne sera-t-elle Admin ?\n\n"
          "1 - Oui.\n"
          "0 - Non.\n")
    choice = int(input("Votre choix : "))  # AJOUT DES DROITS ADMINS
    if choice:
        addAdmin(userFound, voteID)

    print("\nCette personne sera-t-elle autorisée à dépouiller ?\n\n"
          "1 - Oui.\n"
          "0 - Non.\n")
    choice = int(input("Votre choix : "))  # AJOUT DES DROITS DEPOUILLEMENT
    if choice:
        addAuthorized(userFound, voteID)

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


def createS(g):
    s = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(s), g):
        s = ''.join(random.choice(string.digits) for x in range(3))

    return int(s)


def createPub(s, g):
    pub = 0
    cond = True

    while cond == True:
        pub = g ** s
        if len(str(pub)) > 512 and len(str(pub)) < 1000:
            cond = False

    return pub


def generate(a, Z):
    for i in range(1, Z):
        b = (a ** i) % Z
        if b == 1:
            if i == Z - 1:
                return True
            else:
                return False


def generateAlpha(g):
    r = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(r), g):
        r = ''.join(random.choice(string.digits) for x in range(3))

    alpha = g ** int(r)

    return alpha

def generateA(g):

    w = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(w), g):
        w = ''.join(random.choice(string.digits) for x in range(3))

    A = g ** w

    return A