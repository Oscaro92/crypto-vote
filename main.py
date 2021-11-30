from function import *

def start():
    # initialisation des variables :
    earthIsRound = 1
    earthIsFlat = 0
    vote = []
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
            addVote(vote)
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

start()