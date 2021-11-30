from json import *
from poo import *

def addVote(vote):
    quest = input("Quelle est votre question ? ")
    nbAns = int(input("Nombre de réponses possible ? "))

    vote.append(quest)

    for i in range(0, nbAns):
        msg = "Réponse {} : ".format(i + 1)
        ans = input(msg)
        vote.append(ans)

    #save vote in jsons
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

def saveVoter(A, E, S):
    print("Electeur enregistré ! \n")

def saveVote():
    print("Vote enregistré ! \n")

def checkVote():
    print("Vote vérifié ! \n")

def counting():
    print("Dépouillement fait ! \n")

def createSecretKey():
    print("Clé secrète généré ! \n")

def createPublicKey():
    print("Clé publique généré ! \n")