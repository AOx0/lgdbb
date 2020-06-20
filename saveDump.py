import pickle
import json

data = {
    "users": {
        "NSH~Alejandro": {
            "userID" : "326169547902287874",
            "uMention" : "NSH~Alejandro#9853",
            "activado" : True,
            "acid": 0,
            "admin": True,
            "superAdmin": True,
            "presNo" : 0,
            "pres" : 0
        },
        "Legendary Bank": {
            "userID" : "721303081379168347",
            "uMention" : "Legendary Bank#5251",
            "activado" : True,
            "acid": 0,
            "admin": True,
            "superAdmin": True,
            "presNo" : 0,
            "pres" : 0
        }
    },
    "log": {
        "logs": 0,
        "log" : {

        }
    },
    "date": "2020-06-14",
    "cuota": 0.001,
    "debug": False
}
# Saving the objects:

with open('objs.txt', 'w') as f:  # Python 3: open(..., 'wb')
    json.dump(data, f)


"""# Getting back the objects:
with open('objs.txt','r') as f:  # Python 3: open(..., 'rb')
    data = json.load(f)
"""