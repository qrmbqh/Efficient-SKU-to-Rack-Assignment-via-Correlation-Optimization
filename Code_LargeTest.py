
import numpy as np
import pandas as pd
from TRE_SA import SA
from time import time
from SLAP import slap, fv, slap_lr, slap_with_warmStart
from IEEE_CH import CH
from heuristic import heuristic,heuristic3
from generate_instances import generate_instances, generate_instances2


results = []
columns = ['|S|','C','Θ','instanceNumber','Gurobi-objective','Gurobi-CPUtime','upper bound','IPM-objective','IPM-CPUtime']

                
for S in [200,250]: 
    for midu in [8,12,16,20,24,30]:
        for strength_coefficient in [0.4,0.6,0.8,1]:
            for num in range(5):
                filename = "Large instances\\" + str(S) + '-' + str(midu) + '-' + str(strength_coefficient) + '-' + str(num) + '.csv'
                c = pd.read_csv(filename, index_col=0)
                c = pd.DataFrame(c.values)
    
                obj, time1 = slap(midu, c, 300)
                
                obj_lr = slap_lr(midu, c)
                
                racks, time_heu = heuristic(c, midu)
                obj_heu = fv(racks, c)
                
                result = [S, midu, strength_coefficient, num, obj, time1, obj_lr, obj_heu, time_heu]
                results.append(result.copy())
                
df = pd.DataFrame(results, columns=columns)
filename = 'Performance results for large instances.csv'
df.to_csv(filename) 



