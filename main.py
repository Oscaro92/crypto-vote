from function import *
import time


def start():
    # initialisation des variables :
    earthIsRound = 1
    earthIsFlat = 0

    while earthIsRound == 1:
        time.sleep(2)

        print("\nBonjour et bienvenue sur votix ! \n"
              "Etes-vous admin ou électeur ? \n\n"
              "1 - Admin\n"
              "2 - Electeur\n"
              "3 - Quitter\n")

        choice = int(input("Votre choix : "))

        if choice == 1:
            id = input("ID : ")
            mdp = input('Mot de passe : ')

            if id == "admin" and mdp == "admin":
                while earthIsRound == 1:
                    print("\nQue puis-je faire pour vous ?\n\n"
                          "1 - Créer un vote.\n"
                          "2 - Enregistrer un électeur.\n"
                          "3 - Procéder au dépouillement.\n"
                          "4 - Retour\n")

                    choice = int(input("Votre choix : "))

                    if choice == 1:
                        addVote()
                    elif choice == 2:
                        saveVoter()
                    elif choice == 3:
                        counting()
                    elif choice == 4:
                        break
                    else:
                        print("Sais-tu lire et compter ? \n")
            else:
                print("ID et/ou Mot de passe Incorrect")
                break

        elif choice == 2:
            lname = input("Nom : ")
            fname = input("Prénom : ")
            email = input("Mail : ")

            auth = voterExist(lname, fname, email, "./json/voter.json")

            if auth == 1:
                idSession = generateUUID()

                print("Votre ID de session : ", idSession)


                while earthIsRound == 1:

                    print("\nQue puis-je faire pour vous ?\n\n"
                          "1 - Enregistrer un vote.\n"
                          "2 - Vérifier un vote.\n"
                          "3 - Retour\n")

                    choice = int(input("Votre choix : "))

                    if choice == 1:
                        saveVote()
                    elif choice == 2:
                        checkVote()
                    elif choice == 3:
                        break
                    else:
                        print("Sais-tu lire et compter ? \n")
            else:
                print("Mail et/ou UUID incorrect")


        elif choice == 3:
            break
        else:
            print("Sais-tu lire et compter ? \n")

    print("\nMerci d'avoir utilisé Votix !")

start()