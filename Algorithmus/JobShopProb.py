from __future__ import print_function

import collections

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model

def MinimalJobshopSat():
    """Minimal jobshop problem."""
    # Create the model.
    model = cp_model.CpModel()

    jobs_data = [  # task = (Versorgungsbereich_id, processing_time).
        [(0, 10), (1, 13), (2, 20)],  # Job0/ Azubi 0
        [(0, 11), (1, 14), (2, 20)],  # Job1 / Azubi1
        [(0, 12), (1, 15), (2, 20)]  # Job2/ Azubi 2
    ]

    machines_count = 5 #1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)

    # Computes horizon dynamically as the sum of all durations.
   #horizon = sum(task[1] for job in jobs_data for task in job)
    horizon = 500

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)
    max_task =[2, 2,1]
    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            
            all_tasks[job_id, task_id] = task_type(
                start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[machine].append(interval_var)
    #print (machine_to_intervals)

    # Create and add disjunctive constraints.
    max_kapa = model.NewIntVar(0, max_task[1], 'max Kapazizät')
    #for machine in all_machines:
        #print("machine",machine_to_intervals[machine])
        #model.Add(machine_to_intervals[machine]<= max_kapa)
        #model.AddNoOverlap(machine_to_intervals[machine])
        # (1) Ein Versorgungsbereich v hat eine Maximalkapazität 
    #for w in all_weeks:
     #   for machine in all_machines:
      #      model.Add(sum(machine_to_intervals[( v, w)] for a in all_traineess) <= max_cap[v])          
    #Eine Maschine soll maximal max Tasks haben
    # for machine in all_machines:
    #     max_kapa = model.NewIntVar(0, max_task[1], 'max Kapazizät')
    #     model.Add(assigned_jobs[machine] <= max_kapa[1])
    # Precedences inside a job. p
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(
                        start=solver.Value(all_tasks[job_id, task_id].start),
                        job=job_id,
                        index=task_id,
                        duration=task[1]))
        # for jobs in enumerate(assigned_jobs):
        #     #model.Add(sum(jobs[0] <= max_kapa[1]))              
        #     print("Job nr", jobs)
        #     x= 0
        #     #for jo in jobs:
        #         #x += 1
        #     model.Add(sum(jo for jo in jobs) <= 5) 
        #     #print ("job in jobs", jo, x)
        # print("assinged", assigned_jobs)
        # print("assinged Jobs", assigned_jobs[0])
        # print("assinged Jobs", assigned_jobs[0][0])
        # print("assinged Jobs", assigned_jobs[0][0][1])
        
        # Create per machine output lines.
        output = ''
        for machine in all_machines:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line_tasks = 'Ver ' + str(machine) + ': '
            sol_line = '           '

            for assigned_task in assigned_jobs[machine]:
                name = 'Az_%i_%i' % (assigned_task.job, assigned_task.index)
                # Add spaces to output to align columns.
                sol_line_tasks += '%-10s' % name

                start = assigned_task.start
                duration = assigned_task.duration
                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Add spaces to output to align columns.
                sol_line += '%-10s' % sol_tmp

            sol_line += '\n'
            sol_line_tasks += '\n'
            output += sol_line_tasks
            output += sol_line

        # Finally print the solution found.
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        print(output)


MinimalJobshopSat()