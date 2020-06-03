from readsettings import ReadSettings
def writeToConfig(name,value):
    data = ReadSettings('settings.json')
    data[name] = value

def readConfig(name):
    data = ReadSettings('settings.json')
    return data[name]

def deleteConfig(name):
    data = ReadSettings('settings.json')
    del data[name]

comment = '''    
writeToConfig('amd_daily_inv',55)
print(readConfig('amd_daily_inv'))
deleteConfig('amd_daily_inv')
'''