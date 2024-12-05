

import pandas as pd
from SLAP import slap, fv
from heuristic import heuristic


results = []
columns = ['|S|','C','Θ','instanceNumber','Gurobi-objective','Gurobi-CPUtime','IPM-objective','IPM-CPUtime']

for S in [20,40,60]:
    for C in [4,6,8,10,12]:
        for strength_coefficient in [0.4,0.6,0.8,1]:
            for num in range(5):
                filename = "Small instances\\" + str(S) + '-' + str(C) + '-' + str(strength_coefficient) + '-' + str(num) + '.csv'
                c = pd.read_csv(filename, index_col=0)
                c = pd.DataFrame(c.values)
    
                obj, time1 = slap(C, c, 300)
                
                racks, time_heu = heuristic(c, C)
                obj_heu = fv(racks, c)
                
                result = [S, C, strength_coefficient, num, obj, time1, obj_heu, time_heu]
                results.append(result.copy())
                
df = pd.DataFrame(results, columns=columns)
filename = 'Performance results for small instances.csv'
df.to_csv(filename) 
                
