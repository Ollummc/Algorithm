import User as user
from pulp import *

class Einrichtung:
    def __init__(self, p_name, p_cap, p_ver):
        self.name = p_name
        self.cap = p_cap
        self.ver = p_ver
       # print (name, cap, ver)

    def returnEinrichtung(self):
        return  self.name, self.ver, self.cap

NAMES = ["EINRICHTUNG 1", "EINRICHTUNG 2", "EINRICHTUNG 3", "EINRICHTUNG 4", "EINRICHTUNG 5" ]
CAPAZITY = [5,6,8,5,4]
VERSORGUNGSBEREICH  = ["SLP", "PSV", "PV","V4", "V5"]
days = 365;
for x in range (5):
    er = Einrichtung(NAMES[x], CAPAZITY[x], VERSORGUNGSBEREICH[x])
    print (er.returnEinrichtung())

#prob = LpProblem("Mein Problem",LpMaximize)
#prob += lpSum([vars[w][b]*costs[w][b] for (w,b) in Routes]), "Sum_of_Transporting_Costs"