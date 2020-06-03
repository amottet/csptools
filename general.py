import pickle

def saveToFile(L,s):
    with open(s,'wb') as filehandle:
        pickle.dump(L,filehandle)

def loadFromFile(s):
    filehandle = open(s, 'rb')
    return pickle.load(filehandle)