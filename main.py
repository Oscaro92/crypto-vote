def start():

    earthIsRound = 1
    earthIsFlat = 0

    while earthIsRound == 1:
        print("Bonjour, que puis-je faire pour vous ?\n\n"
              "1 - Créer un vote.\n"
              "2 - Enregistrer un électeur.\n"
              "3 - Enregistrer un vote.\n"
              "4 - Vérifier un vote.\n"
              "5 - Procéder au dépouillement.")

        choice = int(input())

        if choice == 1:
            addVote()
        elif choice == 2:
            saveVoter()
        elif choice == 3:
            saveVote()
        elif choice == 4:
            checkVote()
        elif choice == 5:
            counting()
        else:
            print("Sais-tu lire et compter ?")


def addVote():
    print("Vote ajouté !")

def saveVoter():
    print("Electeur enregistré !")

def saveVote():
    print("Vote enregistré !")

def checkVote():
    print("Vote vérifié !")

def counting():
    print("Dépouillement fait !1")

start()