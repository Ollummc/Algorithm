import json
import io
import os, Controller
from User.Trainee import Trainee
data_set = {
    "TraineeID": "3",
    "HomeFacility": "",
    "Name":"",
    "HoursToWorkSupplyArea": {
        "AC": " noooooooo",
        "LTC": "",
        "AS": "Object",
        "PC": "Object",
        "PSYC": "Object"
    },
    "HoursToWorkMandatoryArea": {
        "ORI": "",
        "SPEC": "",
        "ELE1": "",
        "ELE2": ""
    },
    "AssignedFacilities": {
        "AC": " noooooooo",
        "LTC": "",
        "AS": "Object",
        "PC": "Object",
        "PSYC": "Object"
    },
    "Workdays": [
    ]
}
def addOneDay(p_data):
    addOneDay = {
        "FacilityName":"",
        "FacilitySupplyArea":"",
        "Day":"3"
    }
    return addOneDay
JSON_DeploymentPlanning ="Einsatzplanung.json"
JSON_Employee = "Employee.json"
def write_json(data,filename):
    with open(filename,'w') as json_file:
       json.dump(data, json_file)
      
        #json.dump(data, json_file)


def addNewEmployee():
    with open(JSON_Employee) as json_file:
        data = json.load(json_file)
        #for item in data["Date"]:
            # if(item["TraineeID"] == p_Trainee.TraineeID):
            # item["Workdays"].append(addOneDay(data))
        print(data["Trainee"][0]["TraineeID"])
        testdata= data["Trainee"]
        testdata.append(data_set)
        #write_json(data)

def addNewFacility():
    pass

def addDeploymentPlanning():
    with open(JSON_Employee) as json_file:
        data = json.load(json_file)
        #for item in data["Date"]:
            # if(item["TraineeID"] == p_Trainee.TraineeID):
            # item["Workdays"].append(addOneDay(data))
        print(data["TraineeID"])
        testdata= data["Date"]
        testdata.append(data_set)
        #write_json(data)

addNewEmployee()
# def where_json(file_name):
#     return os.path.exists(file_name)


# if where_json('data.json'):
#     pass

# else:

#     with open('data.json', 'w') as outfile:  
#         json.dump(data_set, outfile)

