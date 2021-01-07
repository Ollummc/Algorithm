from User.Trainee import Trainee
import Controller
import FacilityFactory
def CreateUser():
    t= 0
    for liste in Controller.sorted_facilityList:
        for item in liste:
            for i in range (item.numberInternEmployee):
                Trainee1 = Trainee("Azubi" + str(t), "Vorname", item.facilityName)
                Controller.traineeList.append(Trainee1)
                t+=1

    for trainee in Controller.traineeList:
        for e in Controller.facilitysList:
            if(trainee.homeFacilityName == e.facilityName and trainee.homeFacility is object):
                trainee.homeFacility = e
