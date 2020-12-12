from ortools.sat.python import cp_model
import Controller
import FacilityFactory, UserFactory
import numpy as np 
from Facilities.BasicFacility import BasicFacility 
from random import randint
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
        testooarr = []
        not_working_counter= 0
        if self._solution_count <= self._solutions:
            print('Solution %i' % self._solution_count)
            for d in self._num_weeks_for_work:
                print('Woche %i' % d)
                for n in self._homeFacility:
                    not_working_counter= 0
                #for n in range(self._num_employees):
                    is_working = False
                    #for s in range(self._num_areas):
                    for s in self._facility_supply_area_dict:
                        if self.Value(self._shifts[(n[0], d, s[1], s[0])]):# or self.Value(self._pflicht[(n[0], d, s[1], s[0])]):
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
                    print(' works in Facility %i with the supply area %i a total of %i weeks (%i in Supply, %i in Pflicht)' % (e.facilityID, e.number_supply_area, counter + counterpflicht, counter,counterpflicht))
            for element in testooarr:
                print(testooarr)
        else:
            return
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
    sollstd_stamm = [2,2,2,2]#[5,5,2,1]#[8,2,2,10]
    # Creates the model.
    model = cp_model.CpModel()
    schoolweeks = [1,2,3,4,5,10,11,12,13,14,15,20,21,23,44,45,46,47] # 18 Stück 56 - 18 = 38 Tage zur Planung 14 std. Stamm und 12 std in soll
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
                model.Add(home_facility[(n,e)] == 1)
                trainee.TraineeID = n
    
    
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
    #         for liste in Controller.sorted_facilityList:
    #             model.Add(sum((shifts[(n, d, item.facilityID, item.number_supply_area)]) for item in liste) <= 1)
    #             print(sum((shifts[(n, d, item.facilityID, item.number_supply_area)]) for item in liste) <= 1)
    # for n in all_employees:
    #     for d in weeks_for_work:
    #             model.Add(sum((shifts[(n, d, item.facilityID, item.number_supply_area)]) for item in Controller.facilitysList) <= 1)
    #             print(sum((shifts[(n, d, item.facilityID, item.number_supply_area)]) for item in Controller.facilitysList) <= 1)
    for n, trainee in enumerate(Controller.traineeList):
        for d in weeks_for_work:
            test = []
            rest= []
            for e in Controller.facilitysList:
                if(trainee.homeFacilityName == e.facilityName):
                    rest.append(shifts[(n, d, e.facilityID,e.number_supply_area)])
                    for p in all_Pflichteinsaetze:            
                        #if(trainee.homeFacilityName == e.facilityName):     
                        test.append(pfl[(n,d,e.facilityID, p)])
                elif(trainee.homeFacility.facility_supply_area != e.facility_supply_area):
                    rest.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
                #rest.append(shifts[(n, d, e.facilityID,e.number_supply_area)])
                #model.AddBoolXOr([test, rest])
            model.Add((sum(t for t in test) + sum(g for g in rest))==1)
            #print((sum(t for t in test) + sum(g for g in rest))==1)
           
   
    # for d in weeks_for_work:
    #     b =[]
    #     for n, trainee in enumerate(Controller.traineeList):
    #         testomesto= []
    #         for lists in Controller.sorted_facilityList:
    #             for e in lists:
    #                 if(trainee.homeFacilityName == e.facilityName):
    #                     testomesto.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
    #                     break
    #                 elif(trainee.homeFacility.facility_supply_area != e.facility_supply_area):
    #                     testomesto.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
        
    #         model.Add(sum(t for t in testomesto) <=1)
    #         print(sum(t for t in testomesto) <=1)
                
    # for n, trainee in enumerate(Controller.traineeList):
    #     #print("trainee {} in HomeFacility {}".format(trainee.TraineeID, trainee.homeFacilityName))
    #     for d in weeks_for_work:
    #         testomesto= []
    #         for lists in Controller.sorted_facilityList:
    #             for e in lists:
    #                 if(trainee.homeFacilityName == e.facilityName):
    #                     for p in all_Pflichteinsaetze:            
    #                         #if(trainee.homeFacilityName == e.facilityName):     
    #                         testomesto.append(pfl[(n,d,e.facilityID, p)])
    #                     break
                      
    #         model.Add(sum(t for t in testomesto) <=1)
    #         print(sum(t for t in testomesto) <=1)

    # for n, trainee in enumerate(Controller.traineeList):
    #     print("trainee {} in HomeFacility {}".format(trainee.TraineeID, trainee.homeFacilityName))
    #     for d in weeks_for_work:
    #         for i in range(longestList):
    #             hotaf= []
    #             for liste in Controller.sorted_facilityList:
    #                 # for e in liste:
    #                 #     if(trainee.homeFacilityName == e.facilityName):
    #                 #         testomesto.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
    #                 #         break
    #                 #     elif(trainee.homeFacility.facility_supply_area != e.facility_supply_area):
    #                 #         testomesto.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
    #                 if len(liste) == 1:
    #                     hotaf.append(shifts[(n,d,liste[0].facilityID, liste[0].number_supply_area)])
    #                 if len(liste) == longestList:
    #                     hotaf.append(shifts[(n,d,liste[i].facilityID, liste[i].number_supply_area)])
    #                 elif len(liste) > i and len(liste) !=1:
    #                     test= len(liste)-1
    #                     hotaf.append(shifts[(n,d,liste[test].facilityID, liste[test].number_supply_area)])

    #             print(sum(t for t in hotaf) ==1)
    #             #model.Add(sum(t for t in hotaf) ==1)







            #         for bebe in hotaf:
            #             #print("laenge", len(hotaf))
            #             if(bebe.facility_supply_area != e.facility_supply_area or bebe.facilityName == e.facilityName):
            #                 counter +=1
            #             if (counter == (len(hotaf))):
            #                 te.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
            #             # else:
            #             #     print("Versorgungsbereich von {} existiert in Liste schon:".format(bebe.facilityName))
            # model.Add(sum(t for t in te)<=1)
            # print(sum(t for t in te)<=1)
            




                #if (trainee.homeFacility.facility_supply_area == item.facility_supply_area  ):
        # for lists in Controller.sorted_facilityList:
    #(shift_n15d55e0v0) + shift_n15d55e1v2) + shift_n15d55e2v1) + shift_n15d55e3v3) + shift_n15d55e4v3) +
    #  shift_n15d55e5v4) + shift_n15d55e6v4) + shift_n15d55e7v4) 
        #     for e in lists:
        #         beste = []
                #randi = randint(0, len(lists)-1)
                #print ("e: ",e)
                #hotaf.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
            #te.append(hotaf)
            #randi = randint(0, len(lists)-1)
            #e= lists[randi]
        #abogullo.append(shifts[(n,d,e.facilityID, e.number_supply_area)])
        #model.Add(sum(abo for abo in abogullo) <=1)
        #print(sum(abo for abo in abogullo) ==1)
        #print(sum( h for h in hotaf) ==1)
# # #(2)Verteilt die definierten Soll-Stunden der Azbis n an Tag d nur, wenn Die aktuelle Einrichtung identisch mti der im Einrichtungsobjekt ist
    puffer =0
    for n, trainee in enumerate(Controller.traineeList):
        for item in Controller.facilitysList: 
            for p in all_Pflichteinsaetze:
                #Einteilung der Azubis in Stammeinrichtung
                if(trainee.homeFacility.facilityID == item.facilityID):
                    model.Add(sum(pfl[(n, g, item.facilityID, p)] for g in startsIA[p] ) == sollstd_stamm[p])
                    #model.Add(sum(pfl[(n, g, item.facilityID, p)] for g in startsIA[p] ) <= (int(sollstd_stamm[p] + 1)))
                    #print("Stammeinrichtung: ", n, stamm[1], p )
                    
    # #(2)In a shift s / in the care area v, all nurses n have to be over the period d   
    #Employee should work the supply area from the home_facility in their home facility
    #for s, lists in enumerate(Controller.sorted_facilityList):
    # for item in Controller.facilitysList:
    #     for n, stamm in enumerate(home_facility):
    #         #Einteilung der Azubis in Stammeinrichtung
    #         if(stamm[1] == item.facilityID):
                
    #             model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for g in starts[item.number_supply_area] ) >= (int(sollstd[item.number_supply_area]/2+puffer))).OnlyEnforceIf(home_facility[(stamm[0],stamm[1])])
    #             model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for g in ends[item.number_supply_area] ) >= (int(sollstd[item.number_supply_area]/2+puffer))).OnlyEnforceIf(home_facility[(stamm[0],stamm[1])])
    #         else:
    #         #(3) Azubis sollen nur in eine Einrichtung mit einem Versorgungsbereich geplant werden, damit diese nicht ständig neue Arbeitskollegen bekommen.
    #             for s, lists in enumerate(Controller.sorted_facilityList):
    #                 model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in starts[s] )  >= (int(sollstd[s]/2+puffer))) #noch nicht ausprobiert####.OnlyEnforceIf(home_facility[(stamm[0],stamm[1])])
    #                 model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in ends[s] )  >= (int(sollstd[s]/2+puffer)))
    for n, trainee in enumerate(Controller.traineeList):
        for s, lists in enumerate(Controller.sorted_facilityList):
            for itemo in lists:
            # for n, stamm in enumerate(home_facility):
                #Einteilung der Azubis in Stammeinrichtung
                if(trainee.homeFacility.facilityID == itemo.facilityID):
                    if(itemo.facility_supply_area == FE.PSYC.value):
                        model.Add(sum(shifts[(n, g, itemo.facilityID, itemo.number_supply_area)] for g in ends[itemo.number_supply_area] ) >=itemo.targetHours)#.OnlyEnforceIf(home_facility[(n,itemo.facilityID)])
                    else:
                        model.Add(sum(shifts[(n, g, itemo.facilityID, itemo.number_supply_area)] for g in starts[itemo.number_supply_area] ) >=int(itemo.targetHours/2)) # (int(sollstd[item.number_supply_area]/2+puffer)))#.OnlyEnforceIf(home_facility[(stamm[0],stamm[1])])
                        model.Add(sum(shifts[(n, g, itemo.facilityID, itemo.number_supply_area)] for g in ends[itemo.number_supply_area] ) >=int(itemo.targetHours/2))# (int(sollstd[item.number_supply_area]/2+puffer)))#.OnlyEnforceIf(home_facility[(stamm[0],stamm[1])])
                else:
                #(3) Azubis sollen nur in eine Einrichtung mit einem Versorgungsbereich geplant werden, damit diese nicht ständig neue Arbeitskollegen bekommen.
                
                    if(itemo.facility_supply_area == FE.PSYC.value):
                        model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in ends[itemo.number_supply_area]  ) >=itemo.targetHours)#.OnlyEnforceIf(shifts[(n, d, itemo.facilityID, itemo.number_supply_area)])
                        #model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in ends[itemo.number_supply_area]  ) <=itemo.targetHours+1)#
                    else:
                        model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in starts[itemo.number_supply_area] )  >= (int(itemo.targetHours/2)))#.OnlyEnforceIf(shifts[(n, d, itemo.facilityID, itemo.number_supply_area)])
                        #model.Add(sum(shifts[(n, g, item.facilityID, item.number_supply_area)] for item in lists for g in ends[itemo.number_supply_area] )  >= (int(itemo.targetHours/2+puffer)))


    # (4) A supply area v / shift s has a maximum capacity
    for d in weeks_for_work:
        for item in Controller.facilitysList:
            #for p in all_Pflichteinsaetze:
                #model.Add((sum(t for t in test) + sum(g for g in rest))==1)
            model.Add((sum(shifts[(n, d, item.facilityID, item.number_supply_area)] for n in all_employees) + sum(pfl[(n, d, item.facilityID, p)] for n in all_employees for p in all_Pflichteinsaetze)) <= item.maxAvailableTrainingPositions)
            #print((sum(shifts[(n, d, item.facilityID, item.number_supply_area)] for n in all_employees) + sum(pfl[(n, d, item.facilityID, p)] for n in all_employees for p in all_Pflichteinsaetze)) <= item.maxAvailableTrainingPositions)
    # for d in weeks_for_work:
    #         for item in Controller.facilitysList:
    #             for p in all_Pflichteinsaetze:
    #                 model.Add(sum(pfl[(n, d, item.facilityID, p)] for n in all_employees) <= item.maxAvailableTrainingPositions)

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
                    #model.Add((shifts [n, weeks_for_work[i+2], item.facilityID, item.number_supply_area] + (shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)] + shifts [n, weeks_for_work[i+1], item.facilityID, item.number_supply_area])) <=6).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
                elif(d < latest_Workday):
                    model.Add((shifts [n, weeks_for_work[i-1], item.facilityID, item.number_supply_area] + shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)]+ shifts [n, weeks_for_work[i+1],  item.facilityID, item.number_supply_area]) >=2).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
                    #model.Add((shifts [n, weeks_for_work[i-1], item.facilityID, item.number_supply_area] + shifts[(n, weeks_for_work[i], item.facilityID, item.number_supply_area)]+ shifts [n, weeks_for_work[i+1],  item.facilityID, item.number_supply_area]) <=6).OnlyEnforceIf(shifts[(n,d,item.facilityID,item.number_supply_area)])
# # #     # # Creates the solver and solve.
    solver = cp_model.CpSolver()
#     #Multithreading

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