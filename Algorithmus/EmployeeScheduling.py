from ortools.sat.python import cp_model
import numpy as np 


class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_employees,num_weeks, num_weeks_for_work, num_schooldays, num_areas, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_employees = num_employees
        self._num_weeks = num_weeks
        self._num_weeks_for_work = num_weeks_for_work
        self._num_areas = num_areas
        self._num_schooldays = num_schooldays
        self._solutions = set(sols)
        self._solution_count = 0
        
    def on_solution_callback(self):
        
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in (self._num_weeks_for_work):
                print('Woche %i' % d)
                for n in range(self._num_employees):
                    is_working = False
                    for s in range(self._num_areas):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print('  Employee %i works in the supply area %i' % (n, s))      
                    if not is_working:
                        print('  Nurse {} does not work'.format(n))

                print()
            for n in range (self._num_employees):
                counter = 0
                for s in range(self._num_areas):
                    counter = 0
                    for d in (self._num_weeks_for_work):
                       if self.Value(self._shifts[(n, d, s)]):
                           counter +=1
                    print('  Employee %i works in the supply area %i a total of %i weeks' % (n, s,counter))
            self._solution_count += 1

    def solution_count(self):
        return self._solution_count

def main():
    # Data.
    num_employees = 5#40
    num_areas = 5
    num_weeks = 12#56

    all_employees = range(num_employees)
    all_areas = range(num_areas)
    all_days = range(num_weeks)

    #capazity for the 5 areas
    maxkap = [15,20,30,30,10]#[1,2,3,3,1]#[20,20,30,30,25]

    #time that the Employee needs in the diffenrent facilities
    hours_acut_care = 4#400h/one_work_day/5
    hours_longterm_care = 2 #(400/8/5)
    hours_ambulant_service = 2 #(400/8/5)
    hours_pediatrics = 2 #(60/8/5) 
    hours_psychiatric_care = 1 #(120/8/5)
    sollstd = [hours_acut_care,hours_longterm_care,hours_ambulant_service,hours_pediatrics,hours_psychiatric_care]
    # Creates the model.
    model = cp_model.CpModel()
    #schoolweeks = [1,2,3,4,5,10,11,12,13,14,15,20,21,23,44,45,46,47]
    schoolweeks = [1]
    #Get the current days a employee can work in one of the 5 areas
    weeks_for_work = np.setdiff1d(all_days,schoolweeks)
    #If the half number of days isnt integer
    half_num_of_days = num_weeks /2 + (num_weeks %2 >0)
    start_end_data = [
        ["acut_care",0,int(half_num_of_days),int(num_weeks)],
        ["long-term_care", 0,int(half_num_of_days),int(num_weeks)],
        ["ambulant_service", 0,int(half_num_of_days),int(num_weeks)],
        ["pediatrics", 0,int(half_num_of_days),int(num_weeks)],
        ["psychiatric_care", int(half_num_of_days),int(half_num_of_days),int(num_weeks)]
    ]
    starts = []
    ends = []
    #Get the days a employee can work in a facility
    for data in start_end_data:
        if(data[0]== "psychiatric_care"):
            starts.append(np.setdiff1d(range(data[1],data[3]),schoolweeks))
        else:
            starts.append(np.setdiff1d(range(data[1],data[2]),schoolweeks))
        ends.append(np.setdiff1d(range(data[2],data[3]),schoolweeks))
    #Decision-Variable. Should be 1 if employee n works on week d in area s
    shifts = {}
    for n in all_employees:
        for d in weeks_for_work:
            for s in all_areas:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # #(1)In a shift s / in the care area v, all nurses n have to be over the period d    
    for s in all_areas: 
        for n in all_employees:
            if(start_end_data[s][0]== "psychiatric_care"):
                model.Add(sum(shifts[(n, g, s)] for g in starts[s] ) >= (int(sollstd[s])))
            else:
                model.Add(sum(shifts[(n, g, s)] for g in starts[s] ) >= (int(sollstd[s]/2)))
                model.Add(sum(shifts[(n, g, s)] for g in ends[s] ) >= (int(sollstd[s]/2)))
    # (2) A supply area v / shift s has a maximum capacity
    for d in weeks_for_work:
        for s in all_areas:
            model.Add(sum(shifts[(n, d, s)] for n in all_employees) <= maxkap[s])

    # (3) Each employee can only work in one shift s on one day d
    for n in all_employees:
        for d in weeks_for_work:
            model.Add(sum(shifts[(n, d, s)] for s in all_areas) == 1)

# #(4) An employee a should be assigned to a supply area v for at least 3 weeks w at a time
    #(d_(a,v,w) )+(d_(a,v,w+1) )≥ 2 ∀a ∈A,∀v ∈V,∀w ∈W  --> that was the mathematical idea for the constraint

    # latest_Workday = weeks_for_work[-1]
    print(len(weeks_for_work))
    # for n in all_employees:
    #     for s in all_areas:
    #         i = 0 
    #         first_value = [weeks_for_work[0]]
    #         safe_d= 0
    #         for d in weeks_for_work [::2]:
                # if(d== first_value and weeks_for_work[i] < latest_Workday):
                #     #model.Add((shifts [n, weeks_for_work[i-1], s] + (shifts[(n, weeks_for_work[d], s)] + shifts [n, weeks_for_work[i+1], s])>=1))
                #     #model.Add((shifts[(n, weeks_for_work[d], s)] + shifts [n, weeks_for_work[i+1], s])>=1)
                #     model.AddLinearConstraint((shifts[(n, weeks_for_work[d], 1)] + shifts [n, weeks_for_work[i+1], 1]),2,5)
                #     #model.Add((shifts[(n, d, s)]+ shifts [n, weeks_for_work[i-1], s] + shifts [n, weeks_for_work[i+1], s])<= 6)
                #     print((shifts[(n, weeks_for_work[d], 1)] + shifts [n, weeks_for_work[i+1], 1])>=1)
                # elif(d < latest_Workday):
                #         #print(d)
                #         #print("weeks_for_work: ", weeks_for_work[i])
                #     print("else",shifts [n, weeks_for_work[safe_d +1], s] + (shifts[(n, weeks_for_work[d], s)] + shifts [n, weeks_for_work[safe_d+3], s])>=1)
                # i+=1
                # safe_d = d
    # var = 5
    # for n in all_employees:
    #     for k in range((len(weeks_for_work)-var)):
    #         t= k
    #         model.Add(sum(shifts[n, t, 1] for s in all_areas for t in range(k + var)) <= var)
    #         print("k: ", k)
    #         print((sum(shifts[n, t, s] for s in all_areas for t in range(k + 2)) >= 2))



    
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first five solutions.
    a_few_solutions = range(1)
    solution_printer = NursesPartialSolutionPrinter(shifts, num_employees,num_weeks,
                                                   weeks_for_work, schoolweeks, num_areas,
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