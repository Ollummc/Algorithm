from User.Trainee import Trainee
import Controller
import FacilityFactory
def CreateUser():
    # Azubi (Name,Nachname, Stammeinrichtung, )
    #Controller.facilitysList.append(InpatientAcuteCare.InpatientAcuteCare("Einrichtung1", 3))
    for i in range (2):
        Trainee1 = Trainee("Azubi" + str(i), "Vorname", "Einrichtung1")
        Controller.traineeList.append(Trainee1)
    for i in range (3):
        Trainee1 = Trainee("Azubi" + str(i), "Vorname", "Einrichtung2")
        Controller.traineeList.append(Trainee1)
    for i in range (2):
        Trainee1 = Trainee("Azubi" + str(i), "Vorname", "Einrichtung3")
        Controller.traineeList.append(Trainee1)
    for i in range (2):
        Trainee1 = Trainee("Azubi" + str(i), "Vorname", "Einrichtung4")
        Controller.traineeList.append(Trainee1)
    for i in range (2):
        Trainee1 = Trainee("Azubi" + str(i), "Vorname", "Einrichtung5")
        Controller.traineeList.append(Trainee1)
    for i in range (2):
        Trainee1 = Trainee("Azubi" + str(i), "Vorname", "Einrichtung6")
        Controller.traineeList.append(Trainee1)
    for i in range (2):
        Trainee1 = Trainee("Azubi" + str(i), "Vorname", "Einrichtung7")
        Controller.traineeList.append(Trainee1)
    
    
    

    
    for trainee in Controller.traineeList:
        for e in Controller.facilitysList:
            if(trainee.homeFacilityName == e.facilityName and trainee.homeFacility is object):
                trainee.homeFacility = e
                print (trainee.name, trainee.homeFacility.facility_supply_area)

# FacilityFactory.CreateFacilities()
# CreateUser()
# for e, lists in enumerate(Controller.sorted_facilityList):
#     print(e)
#     print(lists[e])