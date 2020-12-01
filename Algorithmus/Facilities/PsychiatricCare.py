from Facilities.BasicFacility import BasicFacility
from FacilityEnum import FacilityEnum, AreaHours
import Controller
class PsychatricCare(BasicFacility):
     def __init__(self, p_facilityName, p_maxAvailableTrainingPositions):
          self.facilityName = p_facilityName
          self.maxAvailableTrainingPositions = p_maxAvailableTrainingPositions
          self.facility_supply_area = FacilityEnum.PSYC.value
          self.targetHours = AreaHours.PSYC.value
    
          self.endData = Controller.num_weeks
          self.startData = Controller.half_num_of_days
          self.midData = Controller.half_num_of_days
     def derold(self):
         print("Ausgabe",self.facility_supply_area, "+", self.targetHours)
     
     