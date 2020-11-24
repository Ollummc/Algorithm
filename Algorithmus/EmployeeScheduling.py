from ortools.sat.python import cp_model
import numpy as np 


class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_nurses,num_days, num_workdays, num_schooldays, num_shifts, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_workdays = num_workdays
        self._num_shifts = num_shifts
        self._num_schooldays = num_schooldays
        self._solutions = set(sols)
        self._solution_count = 0
        
    def on_solution_callback(self):
        
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in (self._num_workdays):
                print('Woche %i' % d)
                for n in range(self._num_nurses):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print('  Azubi %i arbeitet in Versorgungsbereich %i' % (n, s))      
                    if not is_working:
                        print('  Nurse {} does not work'.format(n))

                print()
            for n in range (self._num_nurses):
                counter = 0
                for s in range(self._num_shifts):
                    counter = 0
                    for d in (self._num_workdays):
                       if self.Value(self._shifts[(n, d, s)]):
                           counter +=1
                    print('  Azubi %i arbeitet in Versorgungsbereich %i insgesamt %i Wochen' % (n, s,counter))
            self._solution_count += 1

    def solution_count(self):
        return self._solution_count




def main():
    # Data.
    at = 5 #Arbeitstage
    num_nurses = 10#10#100
    num_shifts = 5
    num_days =60
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    maxkap = [10,20,30,30,10]#[1,2,3,3,1]#[20,20,30,30,25]

    soll_SA = 8#(400/8/at) / 0 bis 18. Monat = 0 bis (18*4) --> BSP bis Woche 40 abgeschlossen
    soll_SL = 8#(400/8/at)/ --> BSP bis Woche 40 abgeschlossen
    soll_AD = 8 #(400/8/at)--> BSP bis Woche 40 abgeschlossen
    soll_Paed = 2 #(60/8/at) --> BSP bis Woche 40 abgeschlossen
    soll_PSV = 2 #(120/8/at) --> BSP bis Woche 50 abgeschlossen
    
    sollstd = [soll_SA,soll_SL,soll_AD,soll_Paed,soll_PSV]
    # Creates the model.
    model = cp_model.CpModel()
    schoolweeks = [1,2,3,4,5,10,11,12,13,14,15,20,21,23,44,45,46,47]
    #schoolweeks = [1]

    workdays = np.setdiff1d(all_days,schoolweeks)
 
    testdata = [
        [soll_SA,int(num_days/2),num_days],
        [soll_SL,int(num_days/2),int(num_days)],
        [soll_AD,int(num_days/2),int(num_days)],
        [soll_Paed,int(num_days/2),int(num_days)],
        [soll_PSV,int(num_days/2),int(num_days)]
    ]
    testdata2 = [
        [soll_SA,0,int(num_days/2)],
        [soll_SL,0,int(num_days/2)],
        [soll_AD,0,int(num_days/2)],
        [soll_Paed,0, int(num_days/2)],
        [soll_PSV,int(num_days/2),int(num_days)]
    ]
    for data in testdata2:
        data[2] = np.setdiff1d(range(data[1],data[2]),schoolweeks)
    # Creates shift variables.
    for data in testdata:
        data[2] = np.setdiff1d(range(data[1],data[2]),schoolweeks)
    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for d in workdays:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # #(2)In einer Shift s/ Versorgungsbereich v müssen alle Nurses n über den Zeitraum d gewisse Stunden arbeiten        
    for s in all_shifts: 
        for n in all_nurses:
            #Im realen Szenario können die Stunden nicht einfach haltbiert werden. Die Aufgaben mussen bis zum 18.Monat fertig
            # sein. Das heißt 18* 4 nach 144 Wochen / 2 =  78 Wochen
            # 3 Jahre haben 156 Wochen/ 2 = 78 Wochen
            if(testdata[s][0]== soll_PSV):
                model.Add(sum(shifts[(n, g, s)] for g in testdata[s][2] ) >= (int(sollstd[s])))
            else:
                model.Add(sum(shifts[(n, g, s)] for g in testdata2[s][2] ) >= (int(sollstd[s]/2)))          
                model.Add(sum(shifts[(n, g, s)] for g in testdata[s][2] ) >= (int(sollstd[s]/2)))
    # (1) Ein Versorgungsbereich v/Shift s hat eine Maximalkapazität 
    for d in workdays:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) <= maxkap[s])


#(2)In einer Shift s/ Versorgungsbereich v müssen alle Nurses n über den Zeitraum d gewisse Stunden arbeiten 
    # for n in all_nurses:
    #     for s in all_shifts:
    #         model.Add(sum(shifts[(n, d, s)] for d in workdays) >= sollstd[s])
    # #         #print(sum(shifts[(n, d, s)] for d in all_days) >= sollstd[s])



    # (3) Jede nurse kann nur in einer Shift s an einem Tag d arbeiten 
    for n in all_nurses:
        for d in workdays:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) == 1)
            #print(sum(shifts[(n, d, s)] for s in all_shifts) == 1)
    
#(d_(a,v,w) )+(d_(a,v,w+1) )≥ 2 ∀a ∈A,∀v ∈V,∀w ∈W 
# #(4) Ein Auszubildender a sollte mindestens 2 Wochen w am Stück in einem Versorgungsbereich v eingeteilt sein
#     for n in all_nurses:
#         for d in all_days:
#             #for s in all_shifts:
#             if(d+1 <len(all_days)):
#                 nextday= d+1
#                 print ("day", d, "   d+1", nextday)
#                 day_before = d-1
#             #print ("day", d, "   d+1", nextday)
#                 model.Add(sum(shifts[(n, d, s)] +shifts[(n, nextday, s)] +shifts[(n, nextday +1, s)]for s in all_shifts)  >= 3)
#                 print((shifts[(n, d, s)] +shifts[(n, nextday, s)])  >= 2)
#             #print (, [d-1])


    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first five solutions.
    a_few_solutions = range(1)
    solution_printer = NursesPartialSolutionPrinter(shifts, num_nurses,num_days,
                                                   workdays, schoolweeks, num_shifts,
                                                   a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)

    #Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()