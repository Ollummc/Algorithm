from User.User import User
class Trainee (User):
    TraineeID = ""
    StartOfTraining = "Date"
    EndOfTraining = "Date"
    Fac_AcutCare = ""
    Fac_Long_Term_Care= "" 
    Fac_AmbulantService = ""
    Fac_Pediatrics_Care =""
    Fac_Psychiatric_Care =""
    testomest = []
    dividedFacilitys = {}

    def __init__(self, p_name, p_firstname, p_homefacilityName):
        User.__init__(self, p_name,p_firstname, p_homefacilityName)
        self.dividedFacilitys= {
        "Acut-Care": None,#6#400
        "Long-Term_Care":None,#6#400
        "Ambulant_Service" : None,#6#400
        "Pediatrics_Care" : None,#2#120
        "Psychiatric_Care": None #2#120
        }
# for key,value in divided_facilitys.items():
#     print(value)
# print(divided_facilitys["AC"])