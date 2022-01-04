from functionJSON import *
from poo import *
import uuid
import string
import random
from pbkdf2 import crypt

def addVote():
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
        "Question": vote[0],
        "Response": vote[1:3]
    }
    writeJSON(data, "./json/vote.json")

    msg = 'Le vote "{}" est créé !\n'.format(quest)
    print(msg)
    print("Les réponses possbiles sont : ")
    for i in range(1, nbAns):
        print(vote[i])
    print("")

def saveVoter():
    lname = input("Nom : ")
    fname = input("Prénom : ")
    email = input("Mail : ")

    v = Voter(lname, fname, email)

    data = {
        "lname": v.lname,
        "fname": v.fname,
        "email": v.email
    }

    addVoter(data, "./json/voter.json")

    print("Electeur enregistré ! \n")

def saveVote():
    print("Vote enregistré ! \n")

def checkVote():
    print("Vote vérifié ! \n")

def counting():
    print("Dépouillement fait ! \n")

def generateUUID():
    idSession = str(uuid.uuid4())

    return idSession

def generateC():
    c = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(14))
    return c

def createS(c):
    s = crypt(c)

    return s

def createPub(s):
    pub = s

    return s