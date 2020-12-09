from Facilities.BasicFacility import BasicFacility
from FacilityEnum import FacilityEnum, AreaHours
import Controller
class InpatientAcuteCare(BasicFacility):
     def __init__(self, p_facilityName, p_maxAvailableTrainingPositions):
          self.facilityName = p_facilityName
          self.maxAvailableTrainingPositions = p_maxAvailableTrainingPositions
          self.facility_supply_area = FacilityEnum.AC.value
          self.targetHours = AreaHours.AC.value
          self.startData = 0
          self.endData = Controller.num_weeks 
          self.midData = Controller.half_num_of_days
          #self.number_supply_area = 0