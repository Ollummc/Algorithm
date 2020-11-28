from BasicFacility import BasicFacility
from FacilityEnum import FacilityEnum, AreaHours
class OutpatientService(BasicFacility):
     def __init__(self, p_facilityName, p_maxAvailableTrainingPositions):
          self.facilityName = p_facilityName
          self.maxAvailableTrainingPositions = p_maxAvailableTrainingPositions
          self.facility_supply_area = FacilityEnum.AS.value
          self.targetHours = AreaHours.AS.value