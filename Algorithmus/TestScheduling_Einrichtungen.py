from ortools.sat.python import cp_model
import Controller#, TestingJSON
import FacilityFactory, UserFactory
import numpy as np 
from Facilities.BasicFacility import BasicFacility 
from random import randint
from FacilityEnum import FacilityEnum as FE, AreaHours as AH, InternalAssignments as IA
import itertools
from prettytable import PrettyTable
import pandas as pd
import time
#This Class is covering the output in the console
class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""
   
    def __init__(self, shifts, num_employees, num_weeks_for_work, num_schooldays, num_areas, sols, p_pflicht, p_facility_supply_area_dict, p_homeFacility, p_allPflichteinsaetze):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._pflicht = p_pflicht
        self._num_employees = num_employees
        self._num_weeks = Controller.num_weeks
        self._num_weeks_for_work = num_weeks_for_work
        self._num_areas = num_areas
        self._num_schooldays = num_schooldays
        self._solutions = 0
        self._solution_count = 0
        self._facility_supply_area_dict = p_facility_supply_area_dict
        self._homeFacility = p_homeFacility
        self.header = ""
    
    def OutputAllEmployees (self):
        print('Solution %i' % self._solution_count)
        for d in self._num_weeks_for_work:
            print('Woche %i' % d)
            for n in self._homeFacility:
                not_working_counter= 0
                is_working = False
                for s in self._facility_supply_area_dict:
                    if self.Value(self._shifts[(n[0], d, s[1], s[0])]):
                            is_working = True
                            print('  Employee %i works in Facility %i with supply area %i. His HomeFacility is %i ' % (n[0], s[1], s[0], n[1]))
                    for p in range(4):
                        if self.Value(self._pflicht[(n[0], d, s[1], p)]):
                            is_working = True
                            print('  Employee %i works in Facility %i in the Plfichteinsatz %i am Tag %i.His HomeFacility is %i' % (n[0], s[1],p,d,n[1]))  
                if not is_working:
                    print('  Employee {} does not work'.format(n))
                    not_working_counter +=1
        self._solution_count += 1
   
    def OutputScheduleHours(self):
        print()
        for n in range (self._num_employees):
            print('Employee %i' %(n))
            counter = 0
            for e in Controller.facilitysList:
                counter = 0
                counterpflicht = 0
                for d in (self._num_weeks_for_work):
                    if (self.Value(self._shifts[(n, d,e.facilityID, e.number_supply_area)])):
                            counter +=1
                    for p in range(4):
                        if(self.Value(self._pflicht[(n, d,e.facilityID, p)])):
                            counterpflicht +=1
                print(' works in Facility %i with the supply area %i a total of %i weeks (%i in Supply, %i in Mandatory)' % (e.facilityID, e.number_supply_area, counter + counterpflicht, counter,counterpflicht))
  
    def OutputCoordination_View_asTable(self):
        self.getHeader()
        for n, trainee in enumerate(Controller.traineeList):
            schedule = ''
            for d in (self._num_weeks_for_work):
                counter = 0
                for e in Controller.facilitysList:
                    if self.Value(self._shifts[(n, d,e.facilityID, e.number_supply_area)]):
                        schedule += "{:<4}".format(str(e.facilityID))
                    for p in range(4):
                        if(self.Value(self._pflicht[(n, d,e.facilityID, p)])):
                            schedule += "{:<4}".format("P")
            print ('Employee {:<3}: {}'.format(trainee.TraineeID, schedule))
    
    def OutputFacility_View_asTable(self):
        for e in Controller.facilitysList:
            print("Einrichtung ", e.facilityID, e.facility_supply_area)
            self.getHeader()
            for n, trainee in enumerate(Controller.traineeList):
                schedule = ''
                for d in (self._num_weeks_for_work):
                    if self.Value(self._shifts[(n, d,e.facilityID, e.number_supply_area)]) and trainee.dividedFacilitys[e.facility_supply_area] == e.facilityName:
                        schedule += "{:<4}".format("W")
                    for p in range(4):
                        if(self.Value(self._pflicht[(n, d,e.facilityID, p)])):
                            schedule += "{:<4}".format("P")
                            break
                    if(not(self.Value(self._shifts[(n, d,e.facilityID, e.number_supply_area)])) and not(self.Value(self._pflicht[(n, d,e.facilityID, p)]) )):
                        schedule += "{:<4}".format("0")
                if(trainee.dividedFacilitys[e.facility_supply_area] == e.facilityName):
                    print ('Employee {:<3}: {}'.format(trainee.TraineeID, schedule))
            print()
    def OutputEmployee_View_asTabel(self):
        self.getHeader()
        for n, trainee in enumerate(Controller.traineeList):
            print("Employee ", trainee.TraineeID)
            for e in Controller.facilitysList:
                schedule = ''                
                for d in (self._num_weeks_for_work):
                    if self.Value(self._shifts[(n, d,e.facilityID, e.number_supply_area)]) and trainee.dividedFacilitys[e.facility_supply_area] == e.facilityName:
                        schedule += "{:<4}".format("W")
                    for p in range(4):
                        if(self.Value(self._pflicht[(n, d,e.facilityID, p)])):
                            schedule += "{:<4}".format("P")
                            break
                    if(not(self.Value(self._shifts[(n, d,e.facilityID, e.number_supply_area)])) and not(self.Value(self._pflicht[(n, d,e.facilityID, p)]) )):
                        schedule += "{:<4}".format("0")
                if(trainee.dividedFacilitys[e.facility_supply_area] == e.facilityName):
                    print ('Facility {:<3}: {}'.format(e.facilityID, schedule))

    #Mapping from the divide facilitys to the divideFacilitysList from the trainee
    def DivideEmployeesToFacilities(self):
        for n, trainee in enumerate(Controller.traineeList):
            for e in Controller.facilitysList:
                for d in (self._num_weeks_for_work):   
                    if self.Value(self._shifts[(n, d,e.facilityID, e.number_supply_area)]):
                        trainee.dividedFacilitys[e.facility_supply_area] = e.facilityName
                        break

    #Methodeto create a header for the output
    def Build_header(self):
        self.header = '               '
        for w in (self._num_weeks_for_work):
            self.header += "{:<4}".format(str(w))
        
    def getHeader(self):
        print ("{}".format(self.header))

    def on_solution_callback(self):
        testooarr = []
        not_working_counter= 0
        if self._solution_count <= self._solutions:
            self.Build_header()
            self.OutputAllEmployees()
            self.OutputScheduleHours()

            print("Coordination_View_asTable")
            self.OutputCoordination_View_asTable()
           
            self.DivideEmployeesToFacilities()

            print("Facility_View_asTable")
            self.OutputFacility_View_asTable()

            print("Employee_View_asTabel")
            self.OutputEmployee_View_asTabel()      
        else:
            self.StopSearch()

    def solution_count(self):
        return self._solution_count

def main():
    num_employees =  len(Controller.traineeList)#10#5#40
    num_areas = len(FE)
    print("numareas: ",num_areas) 
    num_Pflichteinsaetzen = len(IA)
    all_employees = range(num_employees)
    all_days = range(Controller.num_weeks)
    all_mandatory_area = range( num_Pflichteinsaetzen)
    all_areas = range(num_areas)
    maxkap = []
    for cap in Controller.maxCapDict.values():
        maxkap.append(cap)
    print("maxkap: ", maxkap)



    #time that the Employee needs in the diffenrent facilities
    sollstd = [AH.AC.value,AH.LTC.value,AH.AS.value,AH.PC.value,AH.PSYC.value]
    sollstd_stamm = [2,2,2,2]#[5,5,2,1]#[8,2,2,10]
    # Creates the model.
    model = cp_model.CpModel()
    schoolweeks = [1,2,3,4,5,10,11,12,13,14,15,20,21,23,44,45,46,47]
    #Testdata for 156 Weeks.
    #, 70,71,72,73,74,75,76,77,78, 79, 80,81,82,83,84, 100,101,102,103,104, 110,111,112,113,114,120,121,122, 140,141,142,143,144,145,146,150,151] 
    # 18 Weeks from 56 are schoolweeks. so we have 38 Weeks for the assignment planning
    #Get the current days a employee can work in one of the 5 areas
    weeks_for_work = np.setdiff1d(all_days,schoolweeks)


    starts = []
    ends = []
   #Get the days a employee can work in a facility_area without the schoolweeks
    for data in FE:
        if(data.value == FE.PSYC.value):
            starts.append(np.setdiff1d(range(Controller.half_num_of_days,Controller.num_weeks),schoolweeks))
        else:
            starts.append(np.setdiff1d(range(Controller.num_weeks-Controller.num_weeks,Controller.half_num_of_days),schoolweeks))
        ends.append(np.setdiff1d(range(Controller.half_num_of_days,Controller.num_weeks),schoolweeks))

    startsIA = []
    endsIA = []

    for data in IA:
        if(data.value == IA.ORI.value):
            startsIA.append(np.setdiff1d(range(0,Controller.half_num_of_days),schoolweeks))
        else:
            startsIA.append(np.setdiff1d(range(Controller.half_num_of_days,Controller.num_weeks),schoolweeks))
        endsIA.append(np.setdiff1d(range(Controller.half_num_of_days,Controller.num_weeks),schoolweeks))

##DECISION-VARIABLES
# Should be 1 if trainee got his Home-Facility in Facility e
    processingTime = []
    start = time.time()
    #Decision-Var1
    home_facility = {}
    for n, trainee in enumerate(Controller.traineeList):
        for e, fac in enumerate(Controller.facilitysList):
            if(trainee.homeFacilityName == fac.facilityName):
                home_facility[(n, e)] = model.NewBoolVar('home_facility_n%ie%i' % (n, e))
                model.Add(home_facility[(n,e)] == 1)
                trainee.TraineeID = n
    ende = time.time()
    processingTime.append('{:5.3f}s for Descision-Var HomeFacility'.format(ende-start))

    facility_supply_area_dict= {}
    all_supply_areas= [FE.AC.value,FE.LTC.value,FE.AS.value,FE.PC.value,FE.PSYC.value]
    #Decision-Var2
    # Should be 1 if Facility e got supply_area s
    for s in all_areas:
            for e, fac in enumerate(Controller.facilitysList):
                if(fac.facility_supply_area == all_supply_areas[s]):
                    facility_supply_area_dict[(s, e)] = model.NewBoolVar('Schwerpunkt_s%ie%i' % (s, e))
                    print("Facility_area: ", facility_supply_area_dict[(s,e)])
                    model.Add(facility_supply_area_dict[(s,e)] == 1)
                    fac.number_supply_area = s
                    fac.facilityID = e
#Decision-Var3
# Should be 1 if employee n works on week d in area s
    start = time.time()
    shifts = {}
    for n in all_employees:
        for d in weeks_for_work:
            for item in Controller.facilitysList:
                shifts[(n, d, item.facilityID, item.number_supply_area)] = model.NewBoolVar('shift_n%id%ie%iv%i' % (n, d,item.facilityID, item.number_supply_area))
    ende = time.time()
    processingTime.append('{:5.3f}s for the Descision-Var shifz'.format(ende-start))
    start = time.time()
#Decision-Var4
    pfl = {}
    for n in all_employees:
        for d in weeks_for_work:
            for item in Controller.facilitysList:
                for p in all_mandatory_area:
                    pfl[(n, d, item.facilityID,  p)] = model.NewBoolVar('pfl_n%id%ie%ip%i' % (n, d, item.facilityID, p))
    ende = time.time()
    processingTime.append('{:5.3f}s for the Descision-Var mandatory'.format(ende-start))

    allTuples = list(itertools.product(*Controller.sorted_facilityList))
    number_cases = range(len(allTuples))
#Decision-Var5
    intermediateVar = {}
    start = time.time()
    for n, trainee in enumerate(Controller.traineeList):
        for b in number_cases:
            intermediateVar[(n, b)] = model.NewBoolVar('test_n%ib%i' % (n, b))
    ende = time.time()
    processingTime.append('{:5.3f}s for the Descision-Var IntermediateVar'.format(ende-start))
    start = time.time()

    #(1)Add the mandatory hours only if the facility i the home_facility
    for n, trainee in enumerate(Controller.traineeList):
        for d in weeks_for_work:
            test = []
            for e in Controller.facilitysList:
                if(trainee.homeFacilityName == e.facilityName):
                    for p in all_mandatory_area:            
                        test.append(pfl[(n,d,e.facilityID, p)])
                test.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
            model.Add((sum(t for t in test))<=1)
    ende = time.time()
    processingTime.append('{:5.3f}s for Constraint pairing mandatory hours to home_facility'.format(ende-start))

    #(2) Tells the model that only one case from the assignments can be true
    start = time.time()
    for n, trainee in enumerate(Controller.traineeList):
        model.Add(sum(intermediateVar[(n,b)] for b in number_cases) ==1 )
    ende = time.time()
    processingTime.append('{:5.3f}s for Constraint with sum of intermediate Vars '.format(ende-start))
# (3) Create all possible Job-opportunity tuples
    start = time.time()
    mega = []
    for n, trainee in enumerate(Controller.traineeList):
        for d in weeks_for_work:
            for b,tupl in enumerate(allTuples):
                job_opportunities = []
                for item in tupl:
                    job_opportunities.append(shifts[(n,d,item.facilityID, item.number_supply_area)])
                for e in Controller.facilitysList:
                    if(trainee.homeFacilityName == e.facilityName):
                        for p in all_mandatory_area:            
                            job_opportunities.append(pfl[(n,d,e.facilityID, p)])
                mega.append(job_opportunities)
                model.Add(sum(job_opportunities)==1).OnlyEnforceIf(intermediateVar[n,b])
    ende = time.time()
    processingTime.append('{:5.3f}s for Constraint with all possible Job-opportunities'.format(ende-start))

# # #(4) Divide the area_hours from trainee n in week d, if the actual facility is the home facility from the trainee
    start = time.time()
    puffer =0
    for n, trainee in enumerate(Controller.traineeList):
        for item in Controller.facilitysList: 
                #Einteilung der Azubis in Stammeinrichtung
            if(trainee.homeFacility.facilityID == item.facilityID):
                for p in all_mandatory_area:
                    model.Add(sum(pfl[(n, g, item.facilityID, p)] for g in startsIA[p] ) == sollstd_stamm[p])
    ende = time.time()
    processingTime.append('{:5.3f}s for Constraint work hours in mandatory areas'.format(ende-start))

    #(5)In a shift s / in the care area v, all nurses n have to be over the period d   
    #Employee should work the supply area from the home_facility in their home facility
    start = time.time()
    for n, trainee in enumerate(Controller.traineeList):
        for s, lists in enumerate(Controller.sorted_facilityList):
            for itemo in lists:
                #Assignment from the trainees in the home_facility
                if(trainee.homeFacility.facilityID == itemo.facilityID):
                    if(itemo.facility_supply_area == FE.PSYC.value):
                        model.Add(sum(shifts[(n, g, itemo.facilityID, itemo.number_supply_area)] for g in ends[itemo.number_supply_area] ) >=itemo.targetHours)
                    else:
                        model.Add(sum(shifts[(n, g, itemo.facilityID, itemo.number_supply_area)] for g in starts[itemo.number_supply_area] ) >=int(itemo.targetHours/2))
                        model.Add(sum(shifts[(n, g, itemo.facilityID, itemo.number_supply_area)] for g in ends[itemo.number_supply_area] ) >=int(itemo.targetHours/2))
                else:
                    #Assignment in the other facilities with a different supply_area   
                    if(itemo.facility_supply_area == FE.PSYC.value):
                        model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in ends[itemo.number_supply_area]  ) >=itemo.targetHours)#.OnlyEnforceIf(shifts[(n, d, itemo.facilityID, itemo.number_supply_area)])
                    else:
                        model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in starts[itemo.number_supply_area] )  >= (int(itemo.targetHours/2)))#.OnlyEnforceIf(shifts[(n, d, itemo.facilityID, itemo.number_supply_area)])
                        model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in ends[itemo.number_supply_area] )  >= (int(itemo.targetHours/2+puffer)))
    ende = time.time()
    processingTime.append('{:5.3f}s for Constraint work hours in supply area'.format(ende-start))

    # (6) A supply area v / shift s has a maximum capacity
    start = time.time()
    for d in weeks_for_work:
        for item in Controller.facilitysList:
            model.Add((sum(shifts[(n, d, item.facilityID, item.number_supply_area)] for n in all_employees)+ sum(pfl[(n, d, item.facilityID, p)] for n in all_employees for p in all_mandatory_area)) <= item.maxAvailableTrainingPositions)
    ende = time.time()
    processingTime.append('{:5.3f}s for Constraint maximum capazity'.format(ende-start))


    #(7) An employee a should be assigned to a supply area v for at least 2 weeks w at a time
    #(d_(a,v,w) )+(d_(a,v,w+1) )≥ 2 ∀a ∈A,∀v ∈V,∀w ∈W
    latest_Workday = weeks_for_work[-1]
    start = time.time()
    for n in all_employees:
        for item in Controller.facilitysList:
            first_value = [weeks_for_work[0]]
            for i,d in enumerate(weeks_for_work):
                if(d== first_value and weeks_for_work[i] < latest_Workday):
                    model.Add((shifts [n, weeks_for_work[i+2], item.facilityID, item.number_supply_area] + shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)] + shifts [n, weeks_for_work[i+1], item.facilityID, item.number_supply_area]) >=2).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
                    model.Add((shifts [n, weeks_for_work[i+2], item.facilityID, item.number_supply_area] + (shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)] + shifts [n, weeks_for_work[i+1], item.facilityID, item.number_supply_area])) <=6).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
                elif(d < latest_Workday):
                    model.Add((shifts [n, weeks_for_work[i-1], item.facilityID, item.number_supply_area] + shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)]+ shifts [n, weeks_for_work[i+1],  item.facilityID, item.number_supply_area]) >=2).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
                    model.Add((shifts [n, weeks_for_work[i-1], item.facilityID, item.number_supply_area] + shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)]+ shifts [n, weeks_for_work[i+1],  item.facilityID, item.number_supply_area]) <=6).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
    ende = time.time()
    processingTime.append('{:5.3f}s for Constraint assigning minimum Weeks'.format(ende-start))

#Creates the solver and solve.
    solver = cp_model.CpSolver()
#Multithreading
    #solver.parameters.num_search_of_workers= 3
    # #Search for all Solutions with an Objective
    # # Get the optimal objective value
    # model.Maximize(objective)
    # solver.Solve(model)
    # # Set the objective to a fixed value
    # # use round() instead of int()
    # model.Add(objective == round(solver.ObjectiveValue()))
    # model.Proto().ClearField('objective')
    # # Search for all solutions
    # solver.SearchForAllSolutions(model, cp_model.VarArraySolutionPrinter([x, y, z]))


    solver.parameters.linearization_level = 0
    # Display the first five solutions.
    a_few_solutions = range(2)
    solution_printer = NursesPartialSolutionPrinter(shifts, num_employees,
                                                   weeks_for_work, schoolweeks, num_areas,
                                                   a_few_solutions,pfl,facility_supply_area_dict, home_facility, all_mandatory_area)
    status = solver.SolveWithSolutionCallback(model, solution_printer)
    print()
    print ("Status: ", solver.StatusName(status))
    #Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    #print('  - solutions found : %i' % solution_printer.solution_count())
    #assert solution_printer.solution_count() == 2
    for g in processingTime:
        print (g)
if __name__ == '__main__':
    FacilityFactory.CreateFacilities()
    UserFactory.CreateUser()

    main()