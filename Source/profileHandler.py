import json

def getProfiles():
    profiles = []
    # empty = ''
    # profile = {
    #     "Profile": values['ProfileName'],
    #     "Game": values['GameName'],
    #     "ChatLoc": self.chatLocation
    # }
    try:
        jsonFile = open('gameProfiles.json',"r")
        profiles = json.load(jsonFile)
        jsonFile.close()
    except:
        profiles =[]

    return profiles

def saveProfiles(profiles):
    # f = open('gameProfiles.json',"w")
    # f.write(json.dumps(profiles))
    # f.close()
    with open('gameProfiles.json', 'w') as f:
        json.dump(profiles, f)

def getProfile(profileId,profiles):
    return [profile for profile in profiles if profile['Profile'] == profileId][0]