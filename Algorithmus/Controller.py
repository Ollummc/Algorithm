import FacilityEnum as FE


#Facility
facilitysList = []
AmbulantCareFacilityList =[]
LongTermCareList = []
InpatientAcuteCareFacilityList = []
PediatricsFacilityList = []
PsychiatricCareFacilityList = []
sorted_facilityList = []
num_weeks = 56#56
half_num_of_days = int(num_weeks /2 + (num_weeks %2 >0))
maxCapDict = {
    FE.FacilityEnum.AC: 0,
    FE.FacilityEnum.AS:0 ,
    FE.FacilityEnum.LTC: 0,
    FE.FacilityEnum.PC:0,
    FE.FacilityEnum.PSYC: 0,
}

#User
traineeList = []

