from functionJSON import *
import uuid
import random
import string
from pbkdf2 import crypt

def createVote(user):
    vote = []

    quest = input("Quelle est votre question ? ")
    nbAns = int(input("Nombre de réponse possible ? "))

    vote.append(quest)

    for i in range(0, nbAns):
        msg = "Réponse {} : ".format(i + 1)
        ans = input(msg)
        vote.append(ans)

    # Génération d'un ID de vote
    freeID = getUnusedVoteID()

    #Génération de l'UUID
    uuid = generateUUID()
    addUUID(user, freeID, uuid)

    #Génération du code de vote
    cDv = generateC(uuid)
    addCDV(user, freeID, cDv)

    data = {
        "ID": freeID,
        "Question": vote[0],
        "Response": vote[1:3],
        "Voters": [cDv],
        "Admin": uuid,
        "Authorized": []
    }
    addVote(data)

    msg = 'Le vote {} "{}" est créé !\n'.format(freeID, quest)
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

    # Si on ne trouve pas l'utilisateur, on lui créé un compte
    if not len(userFound):
        user = {
            "lname": lname,
            "fname": fname,
            "mail": email,
            "uuids": [],
            "CodesDeVote": []
        }

        addUser(user)
        print("Compte créé")

    # Rafraichissement
    userFound = getUser(lname, fname, email)

    #Génération de l'UUID pour le vote
    uuid = generateUUID()
    addUUID(userFound, voteID, uuid)

    # Génération du code de vote
    cDv = generateC(uuid)
    addCDV(userFound, voteID, cDv)

    # Rafraichissement
    userFound = getUser(lname, fname, email)

    addVoter(userFound, voteID)

    print("\nCette personne sera-t-elle autorisée à dépouiller ?\n\n"
          "1 - Oui.\n"
          "0 - Non.\n")
    choice = int(input("Votre choix : "))  # AJOUT DES DROITS DEPOUILLEMENT
    if choice:
        addAuthorized(userFound, voteID)

    print("Electeur enregistré ! \n")

def saveVote(voteID):
    cDv = input("Veuillez indiquer votre code de vote : ")
    print("Vote enregistré ! \n")

def checkVote():
    print("Vote vérifié ! \n")

def counting():
    print("Dépouillement fait ! \n")

###---------- CHIFFREMENT / SIGNATURES ----------###
def generateUUID():
    return str(uuid.uuid4())

def generateC(uuid):
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
