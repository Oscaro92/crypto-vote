from function import *
import time


def start():
    # initialisation des variables :
    earthIsRound = 1
    earthIsFlat = 0

    vote_counter = 0

    while earthIsRound:
        time.sleep(2)

        print("\nBonjour et bienvenue sur votix ! \n"
              "Veuillez vous connecter \n\n")

        lname = input('Nom: ')
        fname = input('Prénom: ')
        email = input('Adresse email: ')

        userFound = userExist(lname, fname, email)
        if userFound:
            while earthIsRound:
                print("\nQue puis-je faire pour vous ?\n\n"
                      "1 - Créer un vote.\n"
                      "2 - Enregistrer un électeur.\n"
                      "3 - Enregistrer un vote.\n"
                      "4 - Vérifier un vote.\n"
                      "5 - Procéder au dépouillement.\n"
                      "6 - Changer de compte\n")

                choice = int(input("Votre choix : "))

                # CREATION DU VOTE
                if choice == 1:
                    vote_counter += 1
                    createVote(vote_counter)
                    addVoteAdmin(userFound, vote_counter)

                # AJOUT D'ÉLECTEUR
                elif choice == 2:
                    voteAdmin = findVoteWhereAdmin(userFound)
                    if voteAdmin == []:
                        print("Vous n'êtes admin d'aucun vote.")
                        break
                    else:
                        while earthIsRound:
                            if choice == 0:
                                break
                            print("A quel vote souhaitez-vous ajouter un électeur? \n")
                            for voteID in voteAdmin:
                                voteQuestion = getVote(voteID)["Question"]
                                print("{} - {}\n".format(voteID, voteQuestion))
                            choice = int(input("Vote choisi (ID): "))
                            if not voteExist(choice):
                                print("Cet ID n'est pas bon. Réessayez ('0' pour stopper)")
                            saveVoter(choice)
    #TODO :
                elif choice == 3:
                    counting()
                elif choice == 4:
                    break
                elif choice == 5:
                    break
                else:
                    break
        else:
            print("ID et/ou Mot de passe Incorrect")
            break

    print("\nMerci d'avoir utilisé Votix !")

start()