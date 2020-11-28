import numpy as np 
import PsychiatricCare, Pediatrics, InpatientAcuteCare, InpatientLongTermCare, OutpatientService
from BasicFacility import BasicFacility 
def main():
    facilitysList = []
    facilitysList.append(InpatientAcuteCare.InpatientAcuteCare("Einrichtung2", 3))
    facilitysList.append(OutpatientService.OutpatientService("Einrichtung2", 3))
    facilitysList.append(InpatientLongTermCare.InpatientLongTermCare("Einrichtung2", 3))
    facilitysList.append(Pediatrics.Pediatrics("Einrichtung2", 3))
    facilitysList.append(PsychiatricCare.PsychatricCare("Einrichtung 1", 3))
    for f in facilitysList:
        print ("Name: {0} Supply_area: {1}, Capazity: {2} TargerHours: {3}" .format (f.facilityName, f.facility_supply_area, f.maxAvailableTrainingPositions, f.targetHours))
main()