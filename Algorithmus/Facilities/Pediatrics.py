from Facilities.BasicFacility import BasicFacility
from FacilityEnum import FacilityEnum, AreaHours
import Controller
class Pediatrics(BasicFacility):
     def __init__(self, p_facilityName, p_maxAvailableTrainingPositions, p_numberInternEmployee):
          self.facilityName = p_facilityName
          self.maxAvailableTrainingPositions = p_maxAvailableTrainingPositions
          self.facility_supply_area = FacilityEnum.PC.value
          self.targetHours = AreaHours.PC.value
          self.startData = 0
          self.endData = Controller.num_weeks 
          self.midData = Controller.half_num_of_days
          self.numberInternEmployee = p_numberInternEmployee