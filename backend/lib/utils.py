def filter_dict(dictObj, callback):
    newDict = dict()
    
    for (key, value) in dictObj.items():
        if callback((key, value)):
            newDict[key] = value
            
    return newDict