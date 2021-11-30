import uuid
import json


def start():
    # initialisation des variables :
    earthIsRound = 1
    earthIsFlat = 0
    # Serveurs
    A = []
    E = []
    S = []

    while earthIsRound == 1:
        print("\nBonjour, que puis-je faire pour vous ?\n\n"
              "1 - Créer un vote.\n"
              "2 - Enregistrer un électeur.\n"
              "3 - Enregistrer un vote.\n"
              "4 - Vérifier un vote.\n"
              "5 - Procéder au dépouillement.\n")

        choice = int(input("Votre choix : "))
        print("")

        if choice == 1:
            addVote()
        elif choice == 2:
            saveVoter(A, E, S)
        elif choice == 3:
            saveVote()
        elif choice == 4:
            checkVote()
        elif choice == 5:
            counting()
        else:
            print("Sais-tu lire et compter ? \n")


def addVote():
    lname = input("Nom du candidat : ")
    fname = input("Prénom du candidat : ")

    print(lname, fname)

    #Idée de stocker les candidats dans un json
    #
    #with open('candidat.json') as mon_fichier:
    #    candidat = json.load(mon_fichier)
    #
    # with open('config.json', 'w') as mon_fichier:
    #    json.dump(api, mon_fichier)

    print("Vote ajouté ! \n")


def saveVoter(A, E, S):
    lname = input("Nom : ")
    fname = input("Prénom : ")
    email = input("Mail : ")
    idUser = str(uuid.uuid4())

    user = (lname, fname, email, idUser)
    A.append(user)

    E.append(len(A) - 1)

    # envoyer les
    createSecretKey()

    print("Electeur enregistré ! \n")


def saveVote():
    print("Vote enregistré ! \n")


def checkVote():
    print("Vote vérifié ! \n")


def counting():
    print("Dépouillement fait ! \n")


def createSecretKey():
    print("Clé secrète généré ! \n")


start()
