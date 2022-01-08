import pbkdf2
import uuid
from functionJSON import *
import string
import random
import hashlib
import struct


# ---------- INITIALISATION ----------#
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

P = random.getrandbits(10) #Doit être différent de 1 !
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
    cDv = generatePublicKey(uuidVote)
    addVoteCode(user, uuidVote, cDv)
    print("Votre code de vote de l'électeur (public): {}".format(cDv))  # Clé publique
    addCredential(user, uuidVote, credential)

    data = {
        "ID": uuidVote,
        "Question": vote[0],
        "Response": vote[1:3],
        "Voters": [cDv],
        "Admin": uuidUser,
        "Authorized": []
    }
    addVote(data)

    msg = 'Le vote "{}" est créé !\n'.format(quest)
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
    addVoteCode(user, uuidVote, cDv)
    print("Votre code de vote de l'électeur (public): {}".format(cDv))  # Clé publique
    addCredential(user, voteID, credential)

    # Rafraichissement
    userFound = getUser(lname, fname, email)
    addVoter(userFound, voteID)

    # print("\nCette personne sera-t-elle autorisée à dépouiller ?\n\n"
    #       "1 - Oui.\n"
    #       "0 - Non.\n")
    # choice = int(input("Votre choix : "))  # AJOUT DES DROITS DEPOUILLEMENT
    # if choice:
    #     addAuthorized(userFound, voteID)

    print("Electeur enregistré ! \n")


def saveVote(voteID):
    # PDDBkK3YBE6APr
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

    # #admin
    # mdp = input("Pour valider votre vote et déposer votre bulletin, renseignez votre mot de passe: ")
    # while not verifyPassword(mdp, voteID):
    #     print("Ce mot de passe n'est pas valide. \n")
    #     mdp = input("Renseignez votre mot de passe [q] pour quitter: ")
    #
    #     if mdp == "q":
    #         return

    print("Vote enregistré ! \n")


def checkVote():
    print("Vote vérifié ! \n")


def counting():
    print("Dépouillement fait ! \n")


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


def generatePublicKey(uuid):
    credential = generateC()
    s = secret(credential, uuid.replace("-", ''))
    return fast_exponentiation(g, s, P)


def generateUUID():
    return str(uuid.uuid4())


def cryptVote(msg, g, p):
    r = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(r), p):
        r = ''.join(random.choice(string.digits) for x in range(3))

    m = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(m), p):
        m = ''.join(random.choice(string.digits) for x in range(3))

    alpha = (g ** int(r)) % p

    beta = (alpha ** int(r) % p) * (g ** int(m) % p)

    gm = (g ** int(m) % p)

    hash = hashlib.sha256()
    hash.update(msg.encode())
    hash.update(str(gm).encode())
    iv = hash.hexdigest()

    hash = hashlib.sha256()
    hash.update(iv.encode())
    hash.update(str(alpha).encode())
    encrypted_msg = hash.hexdigest()

    print(encrypted_msg)

    decrypted_msg = decryptVote(encrypted_msg, alpha, beta)

    print(decrypted_msg)

    return


def decryptVote(encrypt_msg, alpha, beta):
    hash = hashlib.sha256()
    hash.update(encrypt_msg.encode())
    formule = beta/(alpha ** beta)
    hash.update(str(formule).encode())
    iv = hash.hexdigest()

    hash = hashlib.sha256()
    hash.update(iv.encode())
    hash.update(str(alpha).encode())
    decrypted_msg = hash.hexdigest()

    return decrypted_msg

def hash(S, M, A):
    hash = hashlib.sha256()
    hash.update(S.encode())
    hash.update(M.encode())
    hash.update(A.encode())
    return hash.hexdigest()


def generateSignature(g, M, c, p):
    w = ''.join(random.choice(string.digits) for x in range(3))

    while generate(int(w), p):
        w = ''.join(random.choice(string.digits) for x in range(3))

    S = "Votix"
    A = g ** int(w)

    chal = hash(S, M, str(A))

    resp = int(w) - int(c, 36) * int(chal, 16) % p

    print(resp)

    # verifSignature(g, resp, int(chal, 16))

    return chal


def verifSignature(g, resp, chal):
    print(resp, chal)
    v = 3
    A = g ** resp * v ** chal

    print(A)

    return
