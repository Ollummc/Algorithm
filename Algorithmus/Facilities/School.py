from Facilities.BasicFacility import BasicFacility
from FacilityEnum import FacilityEnum
class School (BasicFacility):
    def __init__(self, p_facilityName, p_maxAvailableTrainingPositions):
        self.facilityName = p_facilityName
        self.maxAvailableTrainingPositions = p_maxAvailableTrainingPositions
        # self.facility_supply_area = FacilityEnum.AC.value
        # self.targetHours = AreaHours.PSYC.value
      