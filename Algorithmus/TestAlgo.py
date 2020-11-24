"""
The Beer Distribution Problem for the PuLP Modeller

Authors: Antony Phillips, Dr Stuart Mitchell  2007
"""

# Import PuLP modeler functions
from pulp import *
# Creates a list of all the supply nodes
Versorgungsbereich =  ["SLP", "PSV", "PV"]

# Creates a dictionary for the number of units of supply for each supply node
capazity = {
    "SLP": 10,
    "PSV": 7,
    "PV": 9
    }

# Creates a list of all demand nodes
Einrichtung = ["1", "2", "3", "4", "5"]

# Creates a dictionary for the number of units of demand for each demand node
demand = {"SLP":460,
          "PSV":400,
          "PV":400,
          "4":400,
          "5":120}

# Creates a list of costs of each transportation path
costs = [   #Bars
         #1 2 3 4 5
         [2,4,5,2,1],#A   Warehouses
         [3,1,3,2,3],
         [3,1,3,2,3] #B
         ]
maxcap = 26
# The cost data is made into a dictionary
#Einrichtungsart mit Versorgungsbereich und freien Plätzen
einrichtungsart = makeDict([Versorgungsbereich,Einrichtung],costs,0)
#print (einrichtungsart)

# Creates the 'prob' variable to contain the problem data
prob = LpProblem("Mein Problem",LpMaximize)

# Creates a list of tuples containing all the possible routes for transport

Routes = [(v,e) for v in Versorgungsbereich for e in Einrichtung]
#print (Routes)
# A dictionary called 'Vars' is created to contain the referenced variables(the routes)
vars = LpVariable.dicts("Route",(Versorgungsbereich,Einrichtung),0,None,LpInteger)
print (vars)
# The objective function is added to 'prob' first
prob += lpSum([vars[w][b]*einrichtungsart[w][b] for (w,b) in Routes]), "Sum_of_Transporting_Costs"
#Test 
#prob += lpSum([vars[x] for (n) in range(maxcap)]), "Sum_of_possible Trainees"
# The supply maximum constraints are added to prob for each supply node (warehouse)
#for w in Versorgungsbereich:
    #prob += lpSum([vars[w][b] for b in Einrichtung])<=capazity[w], "Sum_of_Products_out_of_Warehouse_%s"%w
weeks = [1, 2, 3,4,5,6,7,8,9,10]
number_of_trainees = 10
for v in Versorgungsbereich:
    #for trainee in range (number_of_trainees):
    prob += lpSum([vars[v] for week in weeks])<=demand[v], "Summe der erbrachten Sollstunden%s"%v
    print ("demand an Stelle v: ",demand[v])
testBinary(number_of_trainees,weeks) >=0

# The demand minimum constraints are added to prob for each demand node (bar)
#for b in Einrichtung:
 #   prob += lpSum([vars[w][b] for w in Versorgungsbereich])>=demand[b], "Sum_of_Products_into_Bar%s"%b









# The problem data is written to an .lp file
prob.writeLP("BeerDistributionProblem.lp")

# The problem is solved using PuLP's choice of Solver
#prob.solve()

# The status of the solution is printed to the screen
#print ("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
#for v in prob.variables():
#    print (v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen    
#print ("Total Cost of Transportation = ", value(prob.objective))
