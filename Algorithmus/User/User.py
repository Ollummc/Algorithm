class User:
    name = "string"
    firstName = ""
    id = int
    age = int
    dateOfBirth = "format Date"
    homeAdress = ""
    homeFacilityName = ""
    homeFacility = object
    email = ""
    phoneNumer =""
    
    def __init__(self, p_name, p_firstname, p_homefacilityName):
        self.name = p_name
        self.firstName = p_firstname
        self.homeFacilityName = p_homefacilityName
        