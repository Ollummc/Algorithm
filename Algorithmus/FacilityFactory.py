import Controller
import FacilityEnum as FE
from Facilities import PsychiatricCare, Pediatrics, InpatientAcuteCare, InpatientLongTermCare,AmbuCare

def CreateFacilities():
    #Einrichtungsname, Verfügbare Kapazität
    Controller.facilitysList.append(InpatientAcuteCare.InpatientAcuteCare("Einrichtung1", 3))
    Controller.facilitysList.append(AmbuCare.AmbulantCare("Einrichtung2", 3))
    Controller.facilitysList.append(InpatientLongTermCare.InpatientLongTermCare("Einrichtung3", 3))
    Controller.facilitysList.append(Pediatrics.Pediatrics("Einrichtung4", 3))
    Controller.facilitysList.append(PsychiatricCare.PsychatricCare("Einrichtung5", 2))
    Controller.facilitysList.append(PsychiatricCare.PsychatricCare("Einrichtung6", 2))
    Controller.facilitysList.append(PsychiatricCare.PsychatricCare("Einrichtung7", 2))
    for f in Controller.facilitysList:
        print ("Name: {0} Supply_area: {1}, Capazity: {2} TargerHours: {3}" .format (f.facilityName, f.facility_supply_area, f.maxAvailableTrainingPositions, f.targetHours))
    #CreateFacilities()
    for facility in Controller.facilitysList:
        if(facility.facility_supply_area == FE.FacilityEnum.AC.value):
            Controller.InpatientAcuteCareFacilityList.append(facility)
            Controller.maxCapDict[FE.FacilityEnum.AC] += facility.maxAvailableTrainingPositions
        
        elif(facility.facility_supply_area == FE.FacilityEnum.AS.value):
            Controller.AmbulantCareFacilityList.append(facility)
            Controller.maxCapDict[FE.FacilityEnum.AS] += facility.maxAvailableTrainingPositions
        
        elif(facility.facility_supply_area == FE.FacilityEnum.LTC.value):
            Controller.LongTermCareList.append(facility)
            Controller.maxCapDict[FE.FacilityEnum.LTC] += facility.maxAvailableTrainingPositions
        
        elif(facility.facility_supply_area == FE.FacilityEnum.PC.value):
            Controller.PediatricsFacilityList.append(facility)
            Controller.maxCapDict[FE.FacilityEnum.PC] += facility.maxAvailableTrainingPositions
        
        elif(facility.facility_supply_area == FE.FacilityEnum.PSYC.value):
            Controller.PsychiatricCareFacilityList.append(facility)
            Controller.maxCapDict[FE.FacilityEnum.PSYC] += facility.maxAvailableTrainingPositions
    
    Controller.sorted_facilityList.append(Controller.InpatientAcuteCareFacilityList)
    Controller.sorted_facilityList.append(Controller.AmbulantCareFacilityList)
    Controller.sorted_facilityList.append(Controller.LongTermCareList)
    Controller.sorted_facilityList.append(Controller.PediatricsFacilityList)
    Controller.sorted_facilityList.append(Controller.PsychiatricCareFacilityList)
#CreateFacilities()    
    print("rangeall: ", range(len(Controller.sorted_facilityList)))
    for b in range(len(Controller.sorted_facilityList)):
        print("lange vong diese: ", b)
    for lists in Controller.sorted_facilityList:
        listlenght= (len(lists))
        print("range: ", range(listlenght))
        for e in range(listlenght):
            print(e)
#     for e in len(lists):
#         print("E: ",e)
#print(len(Controller.sorted_facilityList))