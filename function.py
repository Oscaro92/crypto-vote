from functionJSON import *
import string
import random

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
    for i in range(1, nbAns + 1):
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

    # Génération de mote de passe
    # mdp = generateMDP()
    mdp = "admin"
    addMDP(userFound, voteID, mdp)
    #Rafraichissement
    userFound = getUser(lname, fname, email)
    addVoter(userFound, voteID)
    print("\nCette personne sera-t-elle Admin ?\n\n"
          "1 - Oui.\n"
          "0 - Non.\n")
    choice = int(input("Votre choix : "))  # AJOUT DES DROITS ADMINS
    if choice:
        addAdmin(userFound, voteID)

    print("\nCette personne sera-t-elle autorisée à dépouiller ?\n\n"
          "1 - Oui.\n"
          "0 - Non.\n")
    choice = int(input("Votre choix : "))  # AJOUT DES DROITS DEPOUILLEMENT
    if choice:
        addAuthorized(userFound, voteID)

    print("Electeur enregistré ! \n")

def saveVote(voteID):
    #PDDBkK3YBE6APr
    cDv = input("Veuillez indiquer votre code de vote : \n")
    while not verifyVoteCode(cDv, voteID):
        print("Code incorrect.\n")
        cDv = input("Veuillez indiquer votre code de vote [q] pour quitter: ")

        if cDv == "q":
            return

    print("Authentification réussie. Procédez au vote. \n")
    vote = getVote(voteID)
    print("{} \n {}".format(vote["Question"], vote["Response"]))

    idResponse = input("Renseignez votre réponse : ")
    while idResponse < 0 and len(vote["Response"]) < idResponse:
        print("Choix impossible.\n")
        idResponse = input("Renseignez votre réponse [q] pour quitter : ")
        if idResponse == "q":
            return

    #admin
    mdp = input("Pour valider votre vote et déposer votre bulletin, renseignez votre mot de passe: ")
    while not verifyPassword(mdp, voteID):
        print("Ce mot de passe n'est pas valide. \n")
        mdp = input("Renseignez votre mot de passe [q] pour quitter: ")

        if mdp == "q":
            return

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


def createS(g):
    s = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(s), g):
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


def generateAlpha(g):
    r = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(r), g):
        r = ''.join(random.choice(string.digits) for x in range(3))

    alpha = g ** int(r)

    return alpha

def generateA(g, M):

    w = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(w), g):
        w = ''.join(random.choice(string.digits) for x in range(3))

    A = g ** w

    #chal = h(A,M,S)

    return A