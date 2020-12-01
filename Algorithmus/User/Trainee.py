from User.User import User

class Trainee (User):
    TraineeID = ""
    StartOfTraining = "Date"
    EndOfTraining = "Date"
    def __init__(self, p_name, p_firstname, p_homefacilityName):
        User.__init__(self, p_name,p_firstname, p_homefacilityName)