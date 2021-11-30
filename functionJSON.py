import json

def writeJSON(data, path):
    with open(path, 'w') as mon_fichier:
        json.dump(data, mon_fichier)

def readJSON(path):
    with open(path) as mon_fichier:
        data = json.load(mon_fichier)

    return data

def addVoter(data, path):
    with open(path) as mon_fichier:
        dataFinal = json.load(mon_fichier)

    print(dataFinal)
    dataFinal.append(data)
    print(dataFinal)

    with open(path, 'w') as mon_fichier:
        json.dump(dataFinal, mon_fichier)

def voterExist(uuid, email, path):
    with open(path) as mon_fichier:
        data = json.load(mon_fichier)

    for i in range(0, len(data)):
        infos = data[i]
        if infos["uuid"] == uuid and infos["email"] == email:
            return 1

    return 0