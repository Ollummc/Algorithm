
from ortools.sat.python import cp_model


def main():
    # This program tries to find an optimal assignment of nurses to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each nurse can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled shift requests.
    num_trainees = 6
    num_Versorgungsbereiche = 5
    max_cap =[4, 3, 4,5,6]
    num_week  = 10
    all_traineess = range(num_trainees)
    all_Versorgungsbereiche = range(num_Versorgungsbereiche)
    all_weeks = range(num_week)
    soll_Stunden = [[]]
    # Creates the model.
    model = cp_model.CpModel()
    #Entscheidungsvariable d(a,v,w) ist 1, wenn Azubi a in Versorgungsbereich v in Woche w arbeitet. Ansonsten 0
    trainees_in_versorgung = {}
    for a in all_traineess:
        for v in all_Versorgungsbereiche :
            for w in all_weeks:
                trainees_in_versorgung [(a,v,w)]= model.NewBoolVar('shift_a%iv%iw%i' % (a, v, w))
# (1) Ein Versorgungsbereich v hat eine Maximalkapazität 
    for w in all_weeks:
        for v in all_Versorgungsbereiche:
            model.Add(sum(trainees_in_versorgung[(a, v, w)] for a in all_traineess) <= max_cap[v])              
# (2) Ein Auszubildender a kann pro Woche w nur in einem Versorgungsbereich V eingeteilt sein
    for a in all_traineess:
        for w in all_weeks:
            model.Add(sum(trainees_in_versorgung[(a, v, w)] for v in all_Versorgungsbereiche) <= 1)

# (3) Ein Auszubildender a darf seine Monatsarbeitsstunden nicht überschreiten
    # for v in all_Versorgungsbereiche:
    #     for w in all_weeks:
    #         model.Add(sum(trainees_in_versorgung[(a, v, w)] * 8 *5 for a in all_traineess) <= 160)

    # min_shifts_per_nurse = (num_Versorgungsbereiche * num_week) // num_trainees
    # print (min_shifts_per_nurse)
    # for n in all_traineess:
    #     num_shifts_worked = 0
    #     for d in all_weeks:
    #         for s in all_Versorgungsbereiche:
    #             num_shifts_worked += trainees_in_versorgung[(a, v, w)]
    #     model.Add(min_shifts_per_nurse <= num_shifts_worked)
    #     model.Add(num_shifts_worked <= 6)

  #  min_Wochenlaenge = 2
   # for a in all_traineess:
    #    numb_test = 0
     #   for w in all_weeks:
      #      for v in all_Versorgungsbereiche:
       #         numb_test += trainees_in_versorgung[(a,w,v)]
       # model.Add(min_Wochenlaenge <= numb_test)
       # model.Add(numb_test <= 10)


    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first five solutions.
    a_few_solutions = range(5)
    solution_printer = NursesPartialSolutionPrinter(trainees_in_versorgung, num_trainees,
                                                    num_week, num_Versorgungsbereiche,
                                                    a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)

    # Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())

class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_trainees, num_weeks, num_versorgungs, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_trainees = num_trainees
        self._num_weeks = num_weeks
        self._num_Versorgungsbereiche = num_versorgungs
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in range(self._num_days):
                print('Day %i' % d)
                for n in range(self._num_nurses):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print('  Azubi %i works Versorgungsbereich %i' % (n, s))
                    if not is_working:
                        print('  Nurse {} does not work'.format(n))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count

if __name__ == '__main__':
    main()