import json

def writeJSON(data, path):
    with open(path, 'w') as mon_fichier:
        json.dump(data, mon_fichier)

def readJSON(path):
    with open(path) as mon_fichier:
        data = json.load(mon_fichier)

    return data