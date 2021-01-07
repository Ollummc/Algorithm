import Controller
import FacilityEnum as FE
from Facilities import PsychiatricCare, Pediatrics, InpatientAcuteCare, InpatientLongTermCare,AmbuCare

def CreateFacilities():
    t= 0 
    acuteCare = [[18,9]] # [39]
    ambulantCare = [[20,20]]##[[2,0],[1,0],[5,0],[2,0],[3,0],[5,0]]# 
    longTermCare = [[20,20]] #[[3,2],[4,3],[7,2],[4,3],[5,3]]
    pediatricCare =  [[15,15],[20,15]]#[[1,0],[1,0],[5,0],[6,6],[5,3]]
    psychiatricCare =[[20,5],[5,5],[5,5]] #[[2,0],[1,0],[5,0],[2,0],[1,0],[2,0],[2,0],[2,0]]
    #Einrichtungsname, Verfügbare Kapazität, eingeteilte Auszubildende
    for i in range (len(acuteCare)):
         Controller.facilitysList.append(InpatientAcuteCare.InpatientAcuteCare("Einrichtung" + str(t),acuteCare[i][0],acuteCare[i][1]) )
         t+=1
    for i in range(len(ambulantCare)):
        Controller.facilitysList.append(AmbuCare.AmbulantCare("Einrichtung"  + str(t), ambulantCare[i][0], ambulantCare[i][1])) #3 Azubis in Stamm
        t+=1
    for i in range(len(longTermCare)):
        Controller.facilitysList.append(InpatientLongTermCare.InpatientLongTermCare("Einrichtung"  + str(t), longTermCare[i][0], longTermCare[i][1])) #3 Azubis in Stamm
        t+=1
    for i in range((len(pediatricCare))):
        Controller.facilitysList.append(Pediatrics.Pediatrics("Einrichtung"  + str(t), pediatricCare[i][0], pediatricCare[i][1]))
        t+=1 
    for i in range(len(psychiatricCare)):
        Controller.facilitysList.append(PsychiatricCare.PsychatricCare("Einrichtung"  + str(t), psychiatricCare[i][0], psychiatricCare[i][1]) )
        t+=1 
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