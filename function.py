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
    emptyVoteVoteCodes()
    for user in users:
        votes = findVotesWhereVoter(user)
        for vote in votes:
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
        b = (a ** i) % Z
        if b == 1:
            if i == Z - 1:
                return True
            else:
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

    # Génération de l'UUID de l'administrateur
    uuidUser = generateUUID()
    addUUID(user, uuidVote, uuidUser)

    # Génération du code de vote
    credential = generateC()
    print("Identifiant secret de l'admin (privé): {}".format(credential))  # Clé privée

    cDv = generatePublicKey(credential, uuidVote)
    print("Code de vote de l'admin (public): {}".format(cDv))  # Clé publique
    addCredentials(user, uuidVote, credential, cDv)

    authorized = [uuidUser]
    voters = [uuidUser]
    votersCodes = [cDv]

    print("\nCombien de personnes seront autorisées à dépouiller ?\n\n")
    choice = int(input("Votre choix : "))
    for i in range(choice):
        print("Renseignez les informations suivantes :\n")
        while True:
            lname = input('Nom: ')
            fname = input('Prénom: ')
            email = input('Adresse email: ')

            if len(lname) == 0 or len(fname) == 0 or len(email) == 0:
                print("Il manque une information (Nom, Prénom, Mail)\n")
                continue
            break

        userFound = getUser(lname, fname, email)

        # Si on ne trouve pas l'utilisateur, on lui créé un compte
        if not len(userFound):
            newUUID = generateUUID()
            newCredential = generateC()
            newCode = generatePublicKey(newCredential, uuidVote)
            user = {
                "lname": lname,
                "fname": fname,
                "mail": email,
                "uuids": [
                    {
                        "voteID": uuidVote,
                        "uuid": newUUID
                    }
                ],
                "Credentials": [
                    {
                        "voteID": uuidVote,
                        "credential": newCredential,
                        "voteCode": newCode
                    }
                ]
            }
            voters.append(newUUID)
            votersCodes.append(newCode)
            authorized.append(newUUID)
            addUser(user)
            userFound = getUser(lname, fname, email)
            print("Compte créé")

        elif getUUID(userFound, uuidVote) == "":
            newUUID = generateUUID()
            newCredential = generateC()
            newCode = generatePublicKey(newCredential, uuidVote)
            addUUID(userFound, uuidVote, newUUID)
            addCredentials(userFound, uuidVote, newCredential, newCode)

            userFound = getUser(lname, fname, email)

        if not getUUID(userFound, uuidVote) in voters:
            voters.append(getUUID(userFound, uuidVote))
        if not getVoteCode(userFound, uuidVote) in votersCodes:
            votersCodes.append(getVoteCode(userFound, uuidVote))
        if not getUUID(userFound, uuidVote) in authorized:
            authorized.append(getUUID(userFound, uuidVote))


        print("Autorisé ajouté\n")

    # Key generation
    a = random.choice(range(1, P))
    while not pgcd(a, P) == 1:
        a = random.choice(range(1, P))

    ga = fast_exponentiation(g, a, P)

    data = {
        "ID": uuidVote,
        "Keys": {
            "public": ga,
            "private": a
        },
        "Question": vote[0],
        "Response": vote[1:3],
        "Voters": voters,
        "VoteCodes": votersCodes,
        "Admin": uuidUser,
        "Authorized": authorized,
        "Ballots": [],
        "Result": {}
    }
    addVote(data)

    msg = 'Le vote "{}" est créé !\n'.format(quest)
    print(msg)
    print("Les réponses possibles sont : ")
    for i in range(1, nbAns + 1):
        print(vote[i])


def createBallot(voteID, userUUID, cipherVote, gk, signature, h):
    data = {
        "voterUUID": userUUID,
        "choice": {
            "vote": cipherVote,
            "decryptKey": gk
        },
        "signature": [signature, h]
    }
    addBallot(data, voteID)


def saveVoter(voteID, voter):
    # Génération de l'UUID pour le vote
    uuid = generateUUID()
    addUUID(voter, voteID, uuid)

    # Génération du code de vote
    credential = generateC()
    print("Identifiant secret de l'électeur (privé): {}".format(credential))  # Clé privée
    cDv = generatePublicKey(credential, voteID)
    print("Votre code de vote de l'électeur (public): {}".format(cDv))  # Clé publique
    addCredentials(voter, voteID, credential, cDv)

    # Rafraichissement
    userFound = getUser(voter["lname"], voter["fname"], voter["mail"])
    addVoter(userFound, voteID)

    print("Electeur enregistré ! \n")


def hasAlreadyVote(uuidUser, voteID):
    for ballot in getAllBallots(voteID):
        if uuidUser == ballot["voterUUID"]:
            return ballot
    return []


def saveVote(user, voteID):
    credential = input("Veuillez indiquer votre identifiant secret (cn) : ")
    while not verifyCredential(credential, voteID):
        print("Code incorrect.\n")
        credential = input("Veuillez indiquer votre code de vote [q] pour quitter: ")

        if credential == "q":
            return

    print("Authentification réussie...\n")
    vote = getVote(voteID)
    if hasAlreadyVote(getUUID(user, voteID), voteID):
        print("Vous avez déjà voté\n")
        return

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

    ga = getVotePubKeys(voteID)
    cipherVote, gk = cryptVote(vote["Response"][idResponse - 1], ga)

    signature, h = generateSignature(g, P, str(vote["Response"][idResponse - 1]).encode("utf-8"), credential)
    createBallot(voteID, getUUID(user, voteID), cipherVote, gk, signature, h)

    print("Vote enregistré ! \n")


def checkVote(voteID):
    ballots = getAllBallots(voteID)

    for ballot in ballots:
        if not verifySignature(ballot["choice"]["vote"], ballot["signature"][1],
                               ballot["signature"][0], ballot["choice"]["decryptKey"], getVotePrivateKey(voteID)):
            user = getUserFromUUID(ballot["voterUUID"])
            print("Le bulletin de {} - {} n'est pas authentique. Il a été retiré".format(user["fname"], user["lname"]))
            deleteBallot(ballot, voteID)

    print("Vote vérifié ! \n")


def counting(voteID):
    ballots = getAllBallots(voteID)
    result = []
    for ballot in ballots:
        gk = ballot["choice"]["decryptKey"]
        decryptedBallotVote = decryptVote(ballot["choice"]["vote"], gk, getVotePrivateKey(voteID))
        result.append(decryptedBallotVote)

    grouped = collections.Counter(result).items()  # Grouping votes to auto count them
    print(dict(grouped))
    winner = []
    nbVote = 0
    for dic in dict(grouped):
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


def cryptVote(msg, ga):
    en_msg = []
    print("Vote:", msg)
    encrypted_msg = [None] * len(msg)

    k = random.choice(range(1, P))
    while not pgcd(k, P) == 1:
        k = random.choice(range(1, P))

    gk = fast_exponentiation(g, k, P)%P
    s = fast_exponentiation(ga, k, P)%P

    for i in range(0, len(msg)):
        en_msg.append(msg[i])

    for i in range(0, len(en_msg)):
        encrypted_msg[i] = s * ord(msg[i])

    print("Crypted:", encrypted_msg)
    return encrypted_msg, gk

def decryptVote(encrypt_msg, gk, a):
    print("Crypted:", encrypt_msg)
    decrypted_msg = []
    s = fast_exponentiation(gk, a, P)%P

    print("gk : {} | a : {}".format(gk, a))

    for i in range(0, len(encrypt_msg)):
        decrypted_msg.append(chr(int(encrypt_msg[i] * euclide_inverse_modulaire(s, P))))

    decrypted_msg = ''.join(decrypted_msg)
    print("Decrypted:", decrypted_msg)
    return decrypted_msg


# -----------------Partie signature-----------------#
def generateSignature(g, p, msg, credential):  # ElGamal
    x = BigEndianToInteger(StringToBigEndian(credential))
    h = fast_exponentiation(g, x, p)

    hM = int(hashlib.sha256(msg).hexdigest(), 16)

    y = random.choice(range(1, p - 2))
    while not pgcd(y, p - 1) == 1:
        y = random.choice(range(1, p - 2))

    s1 = g ** y
    invY = euclide_inverse_modulaire(y, p - 1)

    s2 = invY * (hM - x * s1) % (p - 1)

    signature = (s1, s2)
    return signature, h


def verifySignature(encrypted_msg, h, signature, q ,a):
    # P, g variables globales fixes
    msg = decryptVote(encrypted_msg, q, a)

    hM = int(hashlib.sha256(msg).hexdigest(), 16)
    (s1, s2) = signature
    val1 = (h ** s1) * (s1 ** s2) % P
    val2 = fast_exponentiation(g, hM, P)

    if not (val1 == val2):
        return False
    return True


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
