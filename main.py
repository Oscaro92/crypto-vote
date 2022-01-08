from function import *
import time


def start():
    # initialisation des variables :
    earthIsRound = 1
    earthIsFlat = 0

    while earthIsRound:
        time.sleep(2)

        print("\nBonjour et bienvenue sur votix ! \n"
              "Veuillez vous connecter \n\n")

        lname = input('Nom: ')
        fname = input('Prénom: ')
        email = input('Adresse email: ')

        userFound = getUser(lname, fname, email)
        if not userFound == []:
            while earthIsRound:
                print("\nQue puis-je faire pour vous ?\n\n"
                      "1 - Créer un vote.\n"
                      "2 - Enregistrer un électeur.\n"
                      "3 - Enregistrer un vote.\n"
                      "4 - Vérifier un vote.\n"
                      "5 - Procéder au dépouillement.\n"
                      "6 - Annuler un vote.\n"
                      "7 - Changer de compte\n"
                      "8 - Quitter\n")

                choice = int(input("Votre choix : "))

                # CREATION DU VOTE
                if choice == 1:
                    createVote(userFound)

                # AJOUT D'ÉLECTEUR
                elif choice == 2:
                    votes = findVotesWhereAdmin(userFound)
                    if not len(votes):
                        print("Vous n'êtes admin d'aucun vote.")
                    else:
                        while True:
                            print("A quel vote souhaitez-vous ajouter un électeur? \n")
                            i = 1
                            for vote in votes:
                                print("{} - {}\n".format(i, vote["Question"]))
                                i += i
                            print("0 - Annuler\n")
                            choice = int(input("Vote choisi (ID): "))

                            if choice == 0:
                                break

                            if not getVote(votes[choice]["uuid"]):
                                print("Choisissez un vote dans la liste (le numéro ;) )\n")
                            else:
                                saveVoter(choice)
                                break
    #TODO :
                # VOTER
                elif choice == 3:
                    votes = findVotesWhereVoter(userFound)
                    if votes == []:
                        print("Vous ne pouvez participer à aucun vote.")
                        break
                    while True:
                        print("Vous avez été convié à voter lors des élections suivantes : \n")
                        for vote in votes:
                            print("{} - {}\n".format(vote["ID"], vote["Question"]))
                        print("0 - Annuler\n")
                        choice = int(input("Pour quelle élection souhaitez-vous voter?: "))

                        if choice == 0:
                            break

                        if not getVote(choice):
                            print("Choisissez un vote dans la liste (le numéro ;) )\n")
                        else:
                            saveVote(choice)
                            break

                elif choice == 4:
                    checkVote()
                elif choice == 5:
                    counting()
                elif choice == 6:
                    deleteAllVote()
                elif choice == 7:
                    break
                else:
                    earthIsRound = 0
        else:
            print("ID et/ou Mot de passe Incorrect")

    print("\nMerci d'avoir utilisé Votix !")

start()