from function import *
import time


def start():
    init()
    # initialisation des variables :
    earthIsRound = 1
    earthIsFlat = 0

    while earthIsRound:
        time.sleep(2)

        print("\nBonjour et bienvenue sur votix ! \n"
              "Veuillez vous connecter \n\n")

        userFound, lname, fname, email = connect()

        while earthIsRound:
            print("\nQue puis-je faire pour vous ?\n\n"
                  "1 - Créer un vote.\n"
                  "2 - Enregistrer un électeur.\n"
                  "3 - Enregistrer un vote.\n"
                  "4 - Vérifier un vote.\n"
                  "5 - Procéder au dépouillement.\n"
                  "6 - Annuler une élection.\n"
                  "7 - Changer de compte\n"
                  "8 - Quitter\n")

            choice = int(input("Votre choix : "))

            # CREATION DU VOTE
            if choice == 1:
                createVote(userFound)
                # Rafraichissement de l'utilisateur connecté
                userFound = getUser(lname, fname, email)

            # AJOUT D'ÉLECTEUR
            elif choice == 2:
                votes = findVotesWhereAdmin(userFound)
                if not len(votes):
                    print("Vous n'êtes admin d'aucun vote.")
                else:
                    while True:
                        print("A quel vote souhaitez-vous ajouter un électeur? \n")
                        i = 1
                        votes = [vote for vote in votes  # On retire les votes cloturés
                                 if not vote["Result"]]
                        for vote in votes:
                            print("{} - {}\n".format(i, vote["Question"]))
                            i += i
                        print("0 - Annuler\n")
                        choice = int(input("Vote choisi (ID): "))

                        if choice == 0:
                            break

                        choosenVote = getVote(votes[choice - 1]["ID"])
                        if not choosenVote:
                            print("Choisissez un vote dans la liste (le numéro ;) )\n")
                        else:
                            saveVoter(choosenVote["ID"])
                            break

            # VOTER
            elif choice == 3:
                votes = findVotesWhereVoter(userFound)
                if votes == []:
                    print("Vous ne pouvez participer à aucun vote.")
                    break
                while True:
                    print("Vous avez été convié à voter lors des élections suivantes : \n")
                    i = 1

                    closed = [vote for vote in votes
                              if not vote["Result"]]

                    for vote in votes:
                        print("{} - {}\n".format(i, vote["Question"]))
                        i += i
                    print("0 - Annuler\n")
                    choice = int(input("Pour quelle élection souhaitez-vous voter (ID)?: "))

                    if choice == 0:
                        break

                    choosenVote = getVote(votes[choice - 1]["ID"])
                    if not choosenVote:
                        print("Choisissez un vote dans la liste (le numéro ;) )\n")
                        continue

                    if choosenVote in closed:
                        print("Ce vote a été cloturé. \n"
                              "Question : {} \n"
                              "Résultat : {} - {} voix\n".format(choosenVote["Question"],
                                                                 choosenVote["Result"]["Response"],
                                                                 choosenVote["Result"]["Count"]))
                    else:
                        saveVote(userFound, choosenVote["ID"])
                        break

            # VERIFIER LES VOTES
            elif choice == 4:
                checkVote()

            # DEPOUILLEMENT
            elif choice == 5:
                votes = findVotesWhereAuthorized(userFound)
                if not len(votes):
                    print("Vous ne pouvez pas dépouiller de vote.")
                else:
                    while True:
                        print("Quel vote souhaitez-vous dépouiller?? \n")
                        i = 1
                        for vote in votes:
                            print("{} - {}\n".format(i, vote["Question"]))
                            i += i
                        print("0 - Annuler\n")
                        choice = int(input("Vote choisi (ID): "))

                        if choice == 0:
                            break

                        choosenVote = getVote(votes[choice - 1]["ID"])
                        if not choosenVote:
                            print("Choisissez un vote dans la liste (le numéro ;) )\n")
                        else:
                            winner, total = counting(choosenVote["ID"])
                            setVoteResult(winner, total, choosenVote["ID"])
                            print("Vote dépouillé et archivé")

            # ANNULATION D'ELECTION
            elif choice == 6:
                votes = getAllVotes()
                while True:
                    print("Quel vote souhaitez-vous annuler?? \n")
                    i = 1
                    for vote in votes:
                        print("{} - {}\n".format(i, vote["Question"]))
                        i += i
                    print("0 - Annuler\n")
                    choice = int(input("Vote choisi (ID): "))

                    if choice == 0:
                        break

                    choosenVote = getVote(votes[choice - 1]["ID"])
                    if not choosenVote:
                        print("Choisissez un vote dans la liste (le numéro ;) )\n")
                    else:
                        deleteVote(choosenVote["ID"])

            # DECONNEXION
            elif choice == 7:
                break

            # FIN DE PROGRAMME
            else:
                earthIsRound = 0

    print("\nMerci d'avoir utilisé Votix !")


start()
