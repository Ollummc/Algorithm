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
    num_nurses = 5#40
    num_shifts = 5
    #Im realen Szenario können die Stunden nicht einfach haltbiert werden. Die Aufgaben mussen bis zum 18.Monat fertig
    # sein. Das heißt 18* 4 nach 144 Wochen / 2 =  78 Wochen
    # 3 Jahre haben 156 Wochen/ 2 = 78 Wochen
    num_days = 10#56
    einrichtungen_arr = []

    num_einrichtungen = 10
    all_einrichtungen = (range (num_einrichtungen))
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    maxkap = [15,20,30,30,10]#[1,2,3,3,1]#[20,20,30,30,25]
    
    soll_SA = 2#8#(400/8/at) / 0 bis 18. Monat = 0 bis (18*4) --> BSP bis Woche 40 abgeschlossen
    soll_SL = 2#8#(400/8/at)/ --> BSP bis Woche 40 abgeschlossen
    soll_AD = 2#8 #(400/8/at)--> BSP bis Woche 40 abgeschlossen
    soll_Paed = 1#2 #(60/8/at) --> BSP bis Woche 40 abgeschlossen
    soll_PSV = 1#2 #(120/8/at) --> BSP bis Woche 50 abgeschlossen
    
    sollstd = [soll_SA,soll_SL,soll_AD,soll_Paed,soll_PSV]
    # Creates the model.
    model = cp_model.CpModel()
    #testModel = model.NewIntVar(0,maxkap, 'testModel')
    #schoolweeks = [1,2,3,4,5,10,11,12,13,14,15,20,21,23,44,45,46,47]
    schoolweeks = [1]

    workdays = np.setdiff1d(all_days,schoolweeks)
    half_num_of_days = num_days /2 + (num_days %2 >0)
    testdata = [
        [soll_SA,int(half_num_of_days),num_days],
        [soll_SL,int(half_num_of_days),int(num_days)],
        [soll_AD,int(half_num_of_days),int(num_days)],
        [soll_Paed,int(half_num_of_days),int(num_days)],
        [soll_PSV,int(half_num_of_days),int(num_days)]
    ]
    testdata2 = [
        [soll_SA,0,int(half_num_of_days)],
        [soll_SL,0,int(half_num_of_days)],
        [soll_AD,0,int(half_num_of_days)],
        [soll_Paed,0, int(half_num_of_days)],
        [soll_PSV,int(half_num_of_days),int(num_days)]
    ]
    soll_Orientierung = 12 #460
    soll_Vertiefung = 13# 500
    soll_wahl1 = 2 #80
    soll_wahl2 = 2 #80
    pflichteinsaetze = [
        [soll_Orientierung,0,int(half_num_of_days)],
        [soll_Vertiefung,int(half_num_of_days), num_days],
        [soll_wahl1,int(half_num_of_days)],num_days,
        [soll_wahl2, int(half_num_of_days), num_days]
    ]

    for data in testdata2:
        data[2] = np.setdiff1d(range(data[1],data[2]),schoolweeks)
    # Creates shift variables.
    for data in testdata:
        data[2] = np.setdiff1d(range(data[1],data[2]),schoolweeks)
    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    # stammeinrichtung = {}
    # for n in all_nurses:
    #     for e in all_einrichtungen:
    #         stammeinrichtung[(n, e)] = model.NewBoolVar('einrichtung_e%in%i' % (e, n))


    shifts = {}
    for n in all_nurses:
        for d in workdays:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # #(2)In einer Shift s/ Versorgungsbereich v müssen alle Nurses n über den Zeitraum d gewisse Stunden arbeiten        
    for s in all_shifts: 
        for n in all_nurses:

            #if(n.Stammeinrichtung.id == s )
                # model.Add(sum(shifts[(n, g, s)] for g in testdata[s][2] ) >= (int(sollstd[s])))
            if(testdata[s][0]== soll_PSV):
                model.Add(sum(shifts[(n, g, s)] for g in testdata[s][2] ) >= (int(sollstd[s])))
            else:
                model.Add(sum(shifts[(n, g, s)] for g in testdata2[s][2] ) >= (int(sollstd[s]/2)))          
                model.Add(sum(shifts[(n, g, s)] for g in testdata[s][2] ) >= (int(sollstd[s]/2)))
    # (1) Ein Versorgungsbereich v/Shift s hat eine Maximalkapazität 
    for d in workdays:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) <= maxkap[s])

    # (3) Jede nurse kann nur in einer Shift s an einem Tag d arbeiten 
    for n in all_nurses:
        for d in workdays:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) == 1)

#(d_(a,v,w) )+(d_(a,v,w+1) )≥ 2 ∀a ∈A,∀v ∈V,∀w ∈W 

    # obj_var = model.NewIntVar(0,10, 'makespan')
    # model.AddMaxEquality(obj_var, [
    #     all_shifts[job_id, len(job) - 1].end
    #     for job_id, job in enumerate(jobs_data)
    # ])
    # model.Maximize(obj_var)
    #model.Maximize(testModel)
# #(4) Ein Auszubildender a sollte mindestens 2 Wochen w am Stück in einem Versorgungsbereich v eingeteilt sein
    
    #(d_(a,v,w) )+(d_(a,v,w+1) )≥ 2 ∀a ∈A,∀v ∈V,∀w ∈W 
    latest_Workday = workdays[-1]
    print(workdays)
    for n in all_nurses:
        for s in all_shifts:
            i = 0 
            first_value = [workdays[0]]
            safe_d= 0
          #  for d in workdays [::2]:
            t= 0
            #t == first_value and
            if( workdays[i] < latest_Workday):
                #model.Add((shifts [n, workdays[i-1], s] + (shifts[(n, workdays[d], s)] + shifts [n, workdays[i+1], s])>=1))
                #model.Add(sum((shifts[(n, workdays[d], s)] + shifts [n, workdays[i+1], s]) for d in workdays[::2]) >=2)
                #model.Add(sum((shifts[(n, workdays[d], s)] + shifts [n, workdays[i+1], s]) for d in workdays[::2]) >=2)
                #model.Add((shifts[(n, d, s)]+ shifts [n, workdays[i-1], s] + shifts [n, workdays[i+1], s])<= 6)
                print(sum((shifts[(n, workdays[d], s)] + shifts [n, workdays[i+1], s]) for d in workdays[::2])>=1)
            #elif(d < latest_Workday):
                    #print(d)
                    #print("workdays: ", workdays[i])
                    #print("else",shifts [n, workdays[safe_d +1], s] + (shifts[(n, workdays[d], s)] + shifts [n, workdays[safe_d+3], s])>=1)
                i+=1
                t=1
                safe_d = d
      #  min_Wochenlaenge = 2
   # for a in all_traineess:
    #    numb_test = 0
     #   for w in all_weeks:
      #      for v in all_Versorgungsbereiche:
       #         numb_test += trainees_in_versorgung[(a,w,v)]
       # model.Add(min_Wochenlaenge <= numb_test)
       # model.Add(numb_test <= 10)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first five solutions.
    a_few_solutions = range(1)
    solution_printer = NursesPartialSolutionPrinter(shifts, num_nurses,num_days,
                                                   workdays, schoolweeks, num_shifts,
                                                   a_few_solutions)
    status = solver.SearchForAllSolutions(model, solution_printer)
    print ("Status: ", solver.StatusName(status))
    #Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()