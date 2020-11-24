from ortools.sat.python import cp_model
import numpy as np 


# weeks= 50
# num_days = weeks * 7
# fixed_Azubis_in = [[1,0],[2,0]]
# for a in fixed_Azubis:
#     print (a[1])
soll_SA = 8#(400/8/at) / 0 bis 18. Monat = 0 bis (18*4) --> BSP bis Woche 40 abgeschlossen
soll_SL = 8#(400/8/at)/ --> BSP bis Woche 40 abgeschlossen
soll_AD = 8 #(400/8/at)--> BSP bis Woche 40 abgeschlossen
soll_Paed = 2 #(60/8/at) --> BSP bis Woche 40 abgeschlossen
soll_PSV = 3 #(120/8/at) --> BSP bis Woche 50 abgeschlossen
num_days =52 #40 #75
all_days = range(num_days)

schoolweeks = [1,2,3,4,5,10,11,12,13,14,15,20,21,23,44,45,46,47]
workdays = np.setdiff1d(all_days,schoolweeks)
test = np.setdiff1d(range(0,30),schoolweeks)
testdata = [
        [soll_SA,0,40],#np.setdiff1d(range(0,40),schoolweeks)],
        [soll_SL,0,int(40/2)],
        [soll_AD,0,40],
        [soll_Paed,0,40],
        [soll_PSV,10,50]
    ]

testdata2 = [
    [soll_SA,0,int(num_days)],
    [soll_SL,0,int(num_days)],
    [soll_AD,0,int(num_days)],
    [soll_Paed,0, int(num_days)],
    [soll_PSV,0,int(num_days)]
]

for data in testdata2:
    anz_tage = data[2] - len(schoolweeks)
    data[2] = np.setdiff1d(range(data[1],data[2]),schoolweeks)
   # for d in data:
    print(data[2])    
    print (anz_tage)
work ={}
print ("workdays", workdays)
for data in testdata:
    data[2] = np.setdiff1d(range(data[1],data[2]),schoolweeks)
    #ra = range(testdata)
    
    #print( int(num_days/2))
    # for d in data[2]:
    #     print ("real: ",data[2][1])
# for data in testdata:
#     for d in data[2]:
#         print(d)  
# i = 0        
# for n in all_nurses:
#     for d in workdays:
#         for s in all_shifts:
#             shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))
            

# for data in testdata:
#     print("data", data[1])
#     for d in data[2]:
#         print(d)

# print ("workd",len(test))
# print(test)