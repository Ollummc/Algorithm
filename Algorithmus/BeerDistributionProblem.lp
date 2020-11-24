\* Mein_Problem *\
Maximize
Sum_of_Transporting_Costs: 3 Route_PSV_1 + Route_PSV_2 + 3 Route_PSV_3
 + 2 Route_PSV_4 + 3 Route_PSV_5 + 3 Route_PV_1 + Route_PV_2 + 3 Route_PV_3
 + 2 Route_PV_4 + 3 Route_PV_5 + 2 Route_SLP_1 + 4 Route_SLP_2 + 5 Route_SLP_3
 + 2 Route_SLP_4 + Route_SLP_5
Subject To
Summe_der_erbrachten_SollstundenPSV: 10 Route_PSV_1 + 10 Route_PSV_2
 + 10 Route_PSV_3 + 10 Route_PSV_4 + 10 Route_PSV_5 <= 400
Summe_der_erbrachten_SollstundenPV: 10 Route_PV_1 + 10 Route_PV_2
 + 10 Route_PV_3 + 10 Route_PV_4 + 10 Route_PV_5 <= 400
Summe_der_erbrachten_SollstundenSLP: 10 Route_SLP_1 + 10 Route_SLP_2
 + 10 Route_SLP_3 + 10 Route_SLP_4 + 10 Route_SLP_5 <= 460
Bounds
0 <= Route_PSV_1
0 <= Route_PSV_2
0 <= Route_PSV_3
0 <= Route_PSV_4
0 <= Route_PSV_5
0 <= Route_PV_1
0 <= Route_PV_2
0 <= Route_PV_3
0 <= Route_PV_4
0 <= Route_PV_5
0 <= Route_SLP_1
0 <= Route_SLP_2
0 <= Route_SLP_3
0 <= Route_SLP_4
0 <= Route_SLP_5
Generals
Route_PSV_1
Route_PSV_2
Route_PSV_3
Route_PSV_4
Route_PSV_5
Route_PV_1
Route_PV_2
Route_PV_3
Route_PV_4
Route_PV_5
Route_SLP_1
Route_SLP_2
Route_SLP_3
Route_SLP_4
Route_SLP_5
End
