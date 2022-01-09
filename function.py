from functionJSON import *
import pbkdf2
import uuid
import string
import random
import hashlib
import struct
import collections


# ---------- INITIALISATION ----------#

# Nécessaire car la clé publique change en fonction de l'instance du programme.
def init():
    users = getAllUsers()
    for user in users:
        votes = findVotesWhereVoter(user)
        for vote in votes:
            emptyVoteVoteCodes(vote["ID"])
            credential = getCredential(user, vote["ID"])
            newVoteCode = generatePublicKey(credential, vote["ID"])
            setUserVoteCode(user, vote["ID"], newVoteCode)
            addVoteVoteCode(vote["ID"], newVoteCode)


def connect():
    while True:
        lname = input('Nom: ')
        fname = input('Prénom: ')
        email = input('Adresse email: ')

        if len(lname) == 0 or len(fname) == 0 or len(email) == 0:
            print("Il manque une information (Nom, Prénom, Mail)\n")
            continue

        userFound = getUser(lname, fname, email)
        if userFound == []:
            print("Identifiants incorrects \n")
            continue

        return userFound, lname, fname, email


def miller_rabin(n, k):
    if n == 1:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate(a, Z):
    for i in range(1, Z):
        b = (a**i)%Z
        if b == 1:
            if i == Z-1:
                return True
            else :
                return False

def fast_exponentiation(a, e, modulo):
    result = 1
    while e > 0:
        if (e % 2) == 1:
            result = (result * a) % modulo
        e = e // 2  # Division entiere
        a = (a * a) % modulo
    return result


def GetPgenerators(P):
    s = set(range(1, P))
    results = []
    for a in s:
        g = set()
        for x in s:
            g.add(fast_exponentiation(a, x, P))
        if g == s:
            results.append(a)
            ###############################
            if len(results) == 2:  # On prend le deuxième générateur par simplicité d'exécution
                return results  # A supprimer pour exécution réelle
            ###############################
    return results


def euclide_inverse_modulaire(a, m):
    modulo = m
    k = 0

    x = 1  # x0
    y = 0  # x1

    u = 0  # y0
    v = 1  # y1

    while m != 0:
        q = a // m  # 0
        r = a % m  # 23
        xx = q * y + x  # 1

        yy = q * v + u  # 0

        a = m  # 13 devient 7
        m = r  # 7 devient 6

        x = y  # x0 prend la valeur x1
        y = xx  # x1 prend la valeur x2 -- ici la nouvelle valeur
        u = v  # y0 prend la valeur y1
        v = yy  # y1 prend la valeur y2 -- ici la nouvelle valeur

        k += 1
    return ((-1) ** k) * x


def pgcd(a, b):
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


# P = random.getrandbits(512) #Récupération d'un entier 512-bits
# while not miller_rabin(P, 25):  #Rabin Miller avec k=25 (erreur 2^-50)
#    P = random.getrandbits(512)  # Récupération d'un entier 512-bits

# la variable P sera notre premier utilisé tout au long du script
# Ici, on prendra P = 10bits car la mémoire ne permet pas de calculer avec P 512bits
# On récupère un générateur aléatoire de P

P = random.getrandbits(10)  # Doit être différent de 1 !
while not miller_rabin(P, 25):
    P = random.getrandbits(10)

allG = GetPgenerators(P)
## g = random.choice(allG) # Pour Exécution réelle
g = allG[1]  # On prend le deuxième générateur par simplicité d'exécution


# ---------- FONCTIONS ----------#
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
    uuidVote = generateUUID()

    # Génération de l'UUID de l'utilisateur
    uuidUser = generateUUID()
    addUUID(user, uuidVote, uuidUser)

    # Génération du code de vote
    credential = generateC()
    print("Identifiant secret de l'électeur (privé): {}".format(credential))  # Clé privée
    cDv = generatePublicKey(credential, uuidVote)
    # addVoteCode(user, uuidVote, cDv)
    print("Code de vote de l'électeur (public): {}".format(cDv))  # Clé publique
    addCredentials(user, uuidVote, credential, cDv)

    data = {
        "ID": uuidVote,
        "Question": vote[0],
        "Response": vote[1:3],
        "Voters": [uuidUser],
        "VoteCodes": [cDv],
        "Admin": uuidUser,
        "Authorized": [],
        "Ballots": [],
        "Result": {}
    }
    addVote(data)

    msg = 'Le vote "{}" est créé !\n'.format(quest)
    print(msg)
    print("Les réponses possibles sont : ")
    for i in range(1, nbAns + 1):
        print(vote[i])


def createBallot(voteID, userUUID, cipherVote, signature):
    data = {
        "voteID": voteID,
        "voterUUID": userUUID,
        "choice": cipherVote,
        "signature": signature
    }


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
            "Credentials": []
        }

        addUser(user)
        print("Compte créé")

    # Rafraichissement
    userFound = getUser(lname, fname, email)

    # Génération de l'UUID pour le vote
    uuid = generateUUID()
    addUUID(userFound, voteID, uuid)

    # Génération du code de vote
    credential = generateC()
    print("Identifiant secret de l'électeur (privé): {}".format(credential))  # Clé privée

    cDv = generatePublicKey(voteID)
    addVoteCode(user, voteID, cDv)

    cDv = generatePublicKey(credential, voteID)
    # addVoteCode(user, voteID, cDv)

    print("Votre code de vote de l'électeur (public): {}".format(cDv))  # Clé publique
    addCredentials(userFound, voteID, credential, cDv)

    # Rafraichissement
    userFound = getUser(lname, fname, email)
    addVoter(userFound, voteID)

    print("\nCette personne sera-t-elle autorisée à dépouiller ?\n\n"
          "1 - Oui.\n"
          "0 - Non.\n")
    choice = int(input("Votre choix : "))  # AJOUT DES DROITS DEPOUILLEMENT
    if choice:
        addAuthorized(userFound, voteID)

    print("Electeur enregistré ! \n")


def saveVote(user, voteID):
    # PDDBkK3YBE6APr
    credential = input("Veuillez indiquer votre identifiant secret (cn) : ")
    while not verifyCredential(credential, voteID):
        print("Code incorrect.\n")
        credential = input("Veuillez indiquer votre code de vote [q] pour quitter: ")

        if credential == "q":
            return

    print("Authentification réussie. Procédez au vote. \n")
    vote = getVote(voteID)
    print("Question: {}".format(vote["Question"]))
    i = 1
    for reponse in vote["Response"]:
        print("{} - {}\n".format(i, reponse))
        i += 1

    idResponse = int(input("Renseignez votre réponse : "))
    while idResponse < 0 and len(vote["Response"]) < idResponse:
        print("Choix impossible.\n")
        idResponse = input("Renseignez votre réponse [q] pour quitter : ")
        if idResponse == "q":
            return

    # TODO : Signature du vote
    cipherVote = "1234"
    signature = "zdadzcv"
    newBallot = createBallot(voteID, getUUID(user, voteID), cipherVote, signature)
    addBallot(newBallot, voteID)

    print("Vote enregistré ! \n")


def checkVote(voteID):
    ballots = getAllBallots(voteID)
    voteCodes = getAllVoteCodes(voteID)

    # TODO : Vérification des ballots

    # for ballot in ballots:
    # checkBallot(ballot)

    print("Vote vérifié ! \n")


def counting(voteID):
    ballots = getAllBallots(voteID)


    # TODO : Déchiffer chaque bulletin

    result = []
    for ballot in ballots:
        decryptedBallotVote = decryptVote(ballot["choice"], 1, 2) #Alpha Beta
        result.append(decryptedBallotVote)


    grouped = collections.Counter(result).items()  # Grouping votes to auto count them

    winner, nbVote = [], 0
    for dic in grouped:
        for key in dic.keys():  # Associated response
            response = key
        for value in dic.values():  # Count
            count = value
        if count > nbVote:
            winner = [response]
            nbvote = count
            continue
        if count == nbvote:
            winner.append(response)

    return winner, nbvote


###---------- CHIFFREMENT / SIGNATURES ----------###
def RSA():
    while not miller_rabin(P, 25):  # Génération d'un autre premier de 10 bits
        Q = random.getrandbits(10)

    n = P * Q
    phi = (P - 1) * (Q - 1)
    e = random.getrandbits(10)
    while not (pgcd(e, P - 1) == 1) and not (pgcd(e, Q - 1) == 1):
        e = random.getrandbits(10)

    d = euclide_inverse_modulaire(e, phi)
    return (n, e), d


def tobase58(car):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return alphabet.index(car)


def frombase58(i):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return alphabet[i]


def checksum(c):
    BigEndian = StringToBigEndian(c)
    checksum = 53 - (BigEndianToInteger(BigEndian) % 53)
    return frombase58(checksum)


def StringToBigEndian(credential):  # 14 char long
    base58 = [tobase58(car) for car in credential]  # Interpretation de c en base 58
    BigEndian = struct.pack('>14B', base58[0], base58[1], base58[2], base58[3], base58[4], base58[5], base58[6],
                            base58[7],
                            base58[8], base58[9], base58[10], base58[11], base58[12], base58[13])
    return BigEndian


def CredentialToBigEndian(credential):  # 15 char long
    base58 = [tobase58(car) for car in credential]  # Interpretation de c en base 58
    BigEndian = struct.pack('>15B', base58[0], base58[1], base58[2], base58[3], base58[4], base58[5], base58[6],
                            base58[7],
                            base58[8], base58[9], base58[10], base58[11], base58[12], base58[13], base58[14])
    return BigEndian


def BigEndianToInteger(BigEndian):
    return int.from_bytes(BigEndian, byteorder='big')


# c = 14 char in 123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz
def generateC():
    set = (string.ascii_letters).translate({
        ord('I'): None,
        ord('O'): None,
        ord('l'): None
    }) + (string.digits).translate({
        ord('0'): None
    })

    Fourteen = ''.join([random.choice(set) for x in range(14)])
    credential = Fourteen + checksum(Fourteen)
    # block = CredentialToBigEndian(credential)
    return credential


def secret(credential, uuid):
    exponent = pbkdf2.crypt(credential, uuid.replace("-", ''), 1000)
    secretExponent = BigEndianToInteger(exponent.encode("UTF-8"))
    return secretExponent % (P - 1)  # valeur q = P-1 (ordre du générateur g de P)


def generatePublicKey(credential, uuidVote):
    s = secret(credential, uuidVote.replace("-", ''))
    return fast_exponentiation(g, s, P)


def generateUUID():
    return str(uuid.uuid4())


def cryptVote(msg, g, p):
    r = int(''.join(random.choice(string.digits) for x in range(3)))

    while generate(r, p):
        r = int(''.join(random.choice(string.digits) for x in range(3)))

    m = int(''.join(random.choice(string.digits) for x in range(3)))

    while generate(r, p):
        m = int(''.join(random.choice(string.digits) for x in range(3)))

    alpha = fast_exponentiation(g, r, p)
    alphaPrim = fast_exponentiation(alpha ,m ,p)
    beta = fast_exponentiation(g, m, p)

    encrypted_msg = []

    for i in range(0, len(msg)):
        encrypted_msg.append(msg[i])

    print("Message à chiffrer : ", msg)
    print(alpha)
    print(beta)
    print(alphaPrim)

    for i in range(0, len(encrypted_msg)):
        encrypted_msg[i] = alphaPrim * ord(encrypted_msg[i])

    decrypted_msg = decryptVote(encrypted_msg, beta, r, p)
    decrypted_msg = ''.join(decrypted_msg)

    print("Message déchiffré : ", decrypted_msg)

    return



def decryptVote(encrypt_msg, beta, r, p):
    decrypted_msg = []

    betaPrim = fast_exponentiation(beta, r, p)

    for i in range(0, len(encrypt_msg)):
        decrypted_msg.append(chr(int(encrypt_msg[i] / betaPrim)))

    return decrypted_msg

#-----------------Partie signature-----------------#

def generateSignature(g, p, c):
    w = int(''.join(random.choice(string.digits) for x in range(3)))


    while generate(w, p):
        w = int(''.join(random.choice(string.digits) for x in range(3)))

    A = fast_exponentiation(g, w, p)

    y = int(''.join(random.choice(string.digits) for x in range(3)))

    while generate(y, p):
        y = int(''.join(random.choice(string.digits) for x in range(3)))

    Y = fast_exponentiation(g, y, p)

    resp = (y + int(c, 36) * w)
    #resp = w + int(c, 36) * A % p

    print(int(c, 36))

    verifSignature(g, p, resp, int(c, 36), A, Y)

    return


def verifSignature(g, p, resp, c, A, Y):
    val1 = pow(g, resp) % p
    val2 = (Y * (A ** c)) % p

    if (val1 == val2):
        print("ok")
    else:
        print("nope")

    return


# ---------- VERIFICATIONS --------- #
def verifyCredential(credential, voteID):
    if not len(credential) == 15:
        return False

    # Verification du checksum
    fourteen = credential[:14]
    if not checksum(fourteen) == credential[14]:
        return False

    # Verification du code de vote
    testKey = generatePublicKey(credential, voteID)
    return verifyVoteCode(testKey, voteID)
