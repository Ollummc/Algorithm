
import numpy as np
days = 50
all_days= range(50)
schoolweeks = [1,2,3,4,5,10,11,12,13,14,15,20,21,23,24,25,30,31]
workdays = np.setdiff1d(all_days,schoolweeks)
#for day in all_days:
# for day in all_days:
#     if(schoolday = day for schoolday in schoolweeks):
#         workdays.append(day)
for w in range(workdays):
    print (w)