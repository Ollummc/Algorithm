from BasicFacility import BasicFacility
from FacilityEnum import FacilityEnum, AreaHours
class InpatientLongTermCare(BasicFacility):
     def __init__(self, p_facilityName, p_maxAvailableTrainingPositions):
          self.facilityName = p_facilityName
          self.maxAvailableTrainingPositions = p_maxAvailableTrainingPositions
          self.facility_supply_area = FacilityEnum.LTC.value
          self.targetHours = AreaHours.LTC.value