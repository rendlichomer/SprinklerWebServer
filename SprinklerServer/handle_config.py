import json

# Recives config path and returns a dict of the parsed json
def readFile(filename):
    with open(filename, 'r') as config:
        data = json.loads(config.read())
    return data

# Recieves config path and returns the raw json text
def getConfig(filename):
    with open(filename, 'r') as config:
        return config.read()

# Recieves config path and data to overwrite with and overwrites the existing configuration
def writeFile(filename, data):
    with open(filename, "w") as config:
        config.write(json.dumps(data))