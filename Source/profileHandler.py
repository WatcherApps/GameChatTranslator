import json
from pathlib import Path

def getProfiles():
    profiles = []
    # empty = ''
    # profile = {
    #     "Profile": values['ProfileName'],
    #     "Game": values['GameName'],
    #     "ChatLoc": self.chatLocation
    # }
    try:
        home = str(Path.home())
        Path(home+'\GameChatTranslator').mkdir(parents=True, exist_ok=True)
        jsonFile = open(home+'\GameChatTranslator\gameProfiles.json',"r")
        profiles = json.load(jsonFile)
        jsonFile.close()
    except:
        profiles =[]

    return profiles

def saveProfiles(profiles):
    # f = open('gameProfiles.json',"w")
    # f.write(json.dumps(profiles))
    # f.close()
    home = str(Path.home())
    Path(home+'\GameChatTranslator').mkdir(parents=True, exist_ok=True)
    with open(home+'\GameChatTranslator\gameProfiles.json', 'w') as f:
        json.dump(profiles, f)

def getProfile(profileId,profiles):
    return [profile for profile in profiles if profile['Profile'] == profileId][0]


