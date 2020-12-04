from ortools.sat.python import cp_model
import Controller
import FacilityFactory, UserFactory
import numpy as np 
from Facilities.BasicFacility import BasicFacility 
from FacilityEnum import FacilityEnum as FE, AreaHours as AH, InternalAssignments as IA
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
        
    def on_solution_callback(self):
        
        if self._solution_count <= self._solutions:
            print('Solution %i' % self._solution_count)
            for d in (self._num_weeks_for_work):
                print('Woche %i' % d)
                for n in self._homeFacility:
                #for n in range(self._num_employees):
                    is_working = False
                    #for s in range(self._num_areas):
                    for s in self._facility_supply_area_dict:
                        if self.Value(self._shifts[(n[0], d, s[1], s[0])]):# or self.Value(self._pflicht[(n[0], d, s[1], s[0])]):
                                is_working = True
                                print('  Employee %i works in Facility %i with supply area %i. His HomeFacility is %i ' % (n[0], s[1], s[0], n[1]))
                        # if self.Value(self._pflicht[(n[0], d, s[1], p)]):
                        #      is_working = True
                        #     print('  Employee %i works in the Plfichteinsatz  %i' % (n[0]))          
                    if not is_working:
                        print('  Employee {} does not work'.format(n))
            self._solution_count += 1
        
            print()
            for n in range (self._num_employees):
                counter = 0
                for e in self._facility_supply_area_dict:
                    counter = 0
                    for d in (self._num_weeks_for_work):
                       if self.Value(self._shifts[(n, d,e[1], e[0])]):
                           counter +=1
                    print('  Employee %i works in Facility %i with the supply area %i a total of %i weeks' % (n, e[1], e[0], counter))
            
    def solution_count(self):
        return self._solution_count

def main():
    num_employees =  len(Controller.traineeList)#10#5#40
    num_areas = len(FE)
    print("numareas: ",num_areas)
    num_Pflichteinsaetzen = len(IA)
    all_employees = range(num_employees)
    all_days = range(Controller.num_weeks)
    all_Pflichteinsaetze = range( num_Pflichteinsaetzen)
    all_areas = range(num_areas)
    #capazity for the 5 areas
    maxkap = []
    for cap in Controller.maxCapDict.values():
        maxkap.append(cap)
    print("maxkap: ", maxkap)

    #time that the Employee needs in the diffenrent facilities
    sollstd = [AH.AC.value,AH.LTC.value,AH.AS.value,AH.PC.value,AH.PSYC.value]
    sollstd_stamm = [1,2,2,1]#[8,2,2,10]
    # Creates the model.
    model = cp_model.CpModel()
    schoolweeks = [1,2,3,4,5,10,11,12,13,14,15,20,21,23,44,45,46,47]
    #schoolweeks = [1]
    #Get the current days a employee can work in one of the 5 areas
    weeks_for_work = np.setdiff1d(all_days,schoolweeks)


    starts = []
    ends = []
   #Get the days a employee can work in a facility_area
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
# Should be 1 if Trainee got his Home-Facility in Facility E
    home_facility = {}
    for n, trainee in enumerate(Controller.traineeList):
        for e, fac in enumerate(Controller.facilitysList):
            if(trainee.homeFacilityName == fac.facilityName):
                home_facility[(n, e)] = model.NewBoolVar('home_facility_n%ie%i' % (n, e))
                print ("homefac: ")
                print ( home_facility[(n, e)])
                model.Add(home_facility[(n,e)] == 1)
    
    
# Should be 1 if Facility e got supply_area s
    facility_supply_area_dict= {}
    testarr = []
    all_facilities= [FE.AC.value,FE.LTC.value,FE.AS.value,FE.PC.value,FE.PSYC.value]

    for s in all_areas:
            for e, fac in enumerate(Controller.facilitysList):
                if(fac.facility_supply_area == all_facilities[s]):
                    facility_supply_area_dict[(s, e)] = model.NewBoolVar('Schwerpunkt_s%ie%i' % (s, e))
                    print("Facility_area: ", facility_supply_area_dict[(s,e)])
                    model.Add(facility_supply_area_dict[(s,e)] == 1)
                    fac.number_supply_area = s
                    fac.facilityID = e
                    testarr.append([[s,e],fac])
    for fac in Controller.facilitysList:
        print("supplynumber: ", fac.number_supply_area)
        print("ID: ", fac.facilityID)
# Should be 1 if employee n works on week d in area s
    shifts = {}
    for n in all_employees:
        for d in weeks_for_work:
            for item in Controller.facilitysList:
                shifts[(n, d, item.facilityID, item.number_supply_area)] = model.NewBoolVar('shift_n%id%ie%iv%i' % (n, d,item.facilityID, item.number_supply_area))


    pfl = {}
    for n in all_employees:
        for d in weeks_for_work:
            for item in Controller.facilitysList:
                for p in all_Pflichteinsaetze:
                    pfl[(n, d, item.facilityID,  p)] = model.NewBoolVar('pfl_n%id%ie%ip%i' % (n, d, item.facilityID, p))


    # for n in all_employees:
    #     for d in weeks_for_work:
    #         for item in Controller.facilitysList:
    #             for p in all_Pflichteinsaetze: 
    #                 model.Add((shifts[(n,d,item.facilityID, item.number_supply_area)]+ pfl[(n,d,item.facilityID,p)])<=1)

    # (1) Each employee can only work in one supply_area s on one day d
    for n in all_employees:
        for d in weeks_for_work:
            #for p in all_Pflichteinsaetze:
            # model.Add(sum(shifts[(n, d, s[1],s[0])] for s in all_areas) <= 1)
                #model.Add(sum((shifts[(n, d, item.facilityID,item.number_supply_area)] + pfl[(n, d, item.facilityID, p)]) for item in Controller.facilitysList) <= 1)
            model.Add(sum(shifts[(n, d, item.facilityID,item.number_supply_area)] for item in Controller.facilitysList) <= 1)
    

#(2)
    # for item in Controller.facilitysList:
    #     for n, stamm in enumerate(home_facility):
    #         for p in all_Pflichteinsaetze:
    #             #Einteilung der Azubis in Stammeinrichtung
    #             if(stamm[1] == item.facilityID):
    #                 model.Add(sum(pfl[(n, g, item.facilityID, p)] for g in startsIA[p] ) >= (int(sollstd_stamm[p])))#.OnlyEnforceIf(home_facility[(stamm[0],stamm[1])])

    # #(2)In a shift s / in the care area v, all nurses n have to be over the period d   
    #Employee should work the supply area from the home_facility in their home facility
    for item in Controller.facilitysList:
        for n, stamm in enumerate(home_facility):
            #Einteilung der Azubis in Stammeinrichtung
            if(stamm[1] == item.facilityID):
                
                model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for g in starts[item.number_supply_area] ) >= (int(sollstd[item.number_supply_area]/2))).OnlyEnforceIf(home_facility[(stamm[0],stamm[1])])
                model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for g in ends[item.number_supply_area] ) >= (int(sollstd[item.number_supply_area]/2))).OnlyEnforceIf(home_facility[(stamm[0],stamm[1])])

#(3) Azubis sollen nur in eine Einrichtung mit einem Versorgungsbereich geplant werden, damit diese nicht ständig neue Arbeitskollegen bekommen.
    for s, lists in enumerate(Controller.sorted_facilityList):
        for n in all_employees:
                model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in starts[s] )  >= (int(sollstd[s]/2)))
                model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in ends[s] )  >= (int(sollstd[s]/2)))

    # (4) A supply area v / shift s has a maximum capacity
    for d in weeks_for_work:
        for item in Controller.facilitysList:
            model.Add(sum(shifts[(n, d, item.facilityID, item.number_supply_area)] for n in all_employees) <= item.maxAvailableTrainingPositions)

# #(5) An employee a should be assigned to a supply area v for at least 2 weeks w at a time
    #(d_(a,v,w) )+(d_(a,v,w+1) )≥ 2 ∀a ∈A,∀v ∈V,∀w ∈W
    latest_Workday = weeks_for_work[-1]
    for n in all_employees:
        for item in Controller.facilitysList:
        #for s in facility_supply_area_dict:
            first_value = [weeks_for_work[0]]
            for i,d in enumerate(weeks_for_work):
                if(d== first_value and weeks_for_work[i] < latest_Workday):
                    model.Add((shifts [n, weeks_for_work[i+2], item.facilityID, item.number_supply_area] + shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)] + shifts [n, weeks_for_work[i+1], item.facilityID, item.number_supply_area]) >=2).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
                    model.Add((shifts [n, weeks_for_work[i+2], item.facilityID, item.number_supply_area] + (shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)] + shifts [n, weeks_for_work[i+1], item.facilityID, item.number_supply_area])) <=6).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
                elif(d < latest_Workday):
                    model.Add((shifts [n, weeks_for_work[i-1], item.facilityID, item.number_supply_area] + shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)]+ shifts [n, weeks_for_work[i+1],  item.facilityID, item.number_supply_area]) >=2).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
                    model.Add((shifts [n, weeks_for_work[i-1], item.facilityID, item.number_supply_area] + shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)]+ shifts [n, weeks_for_work[i+1],  item.facilityID, item.number_supply_area]) <=6).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
    # # Creates the solver and solve.
    solver = cp_model.CpSolver()
    #Multithreading
    
    #solver.parameters.num_search_of_workers= 3
    solver.parameters.linearization_level = 0

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

    # Display the first five solutions.
    a_few_solutions = range(2)
    solution_printer = NursesPartialSolutionPrinter(shifts, num_employees,
                                                   weeks_for_work, schoolweeks, num_areas,
                                                   a_few_solutions,pfl,facility_supply_area_dict, home_facility, all_Pflichteinsaetze)
    status = solver.SearchForAllSolutions(model, solution_printer)

    print()
    print ("Status: ", solver.StatusName(status))
    #Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    FacilityFactory.CreateFacilities()
    UserFactory.CreateUser()
    main()