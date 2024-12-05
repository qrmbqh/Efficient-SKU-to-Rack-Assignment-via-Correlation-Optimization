# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:29:10 2024

@author: 74110
"""

import Benchmarks as B
import generateInstance as G
import heuristic as H
from tqdm import tqdm
from datetime import datetime
import csv
import simulation_shelf as SM
skuNum = 150
orderCount = 1000
# order_size_maxs = [2,5,8,10,15,20]

# shelfCapacitys = [2,3,5,6,10,15,30,50]
# strength_coefficients = [0,0.2,0.4,0.6,0.8,1]
stationCapacitys = [2,5,8,12,15,20,25]
count = 10
current_date = datetime.now().date()
date = current_date.strftime("%Y-%m-%d")

fileName = './Data/'+date+'figure4.csv'#末尾数字表示算例生成方案
f = open(fileName,'a',newline='')
writer = csv.writer(f)
writer.writerow(['sku','orderCount','shelfCapacity','strength_coefficient','stationCapacity','order_size_max','ours','trnvr','imp_to','ieee','imp_ieee','iise','imp_iise'])
f.close()

# for order_size_max in order_size_maxs:
# for shelfCapacity in shelfCapacitys:
for stationCapacity in stationCapacitys:
    order_size_max = 10
    shelfCapacity = 10
    strength_coefficient = 0.5
    # stationCapacity = 5
    for _ in tqdm(range(count),ncols=100):
        similarity_matrix, orders = G.generateInstanceByDiffWays(skuNum, strength_coefficient, order_size_max, way=2, orderCount=orderCount)#way=1 or 2
        
        racks_ours = H.heuristic(similarity_matrix, skuNum, shelfCapacity)
        racks_trnv = B.Turnover(skuNum, shelfCapacity)
        racks_ieee = B.IEEESolution(skuNum, shelfCapacity, similarity_matrix)
        racks_iise = B.IISESolution(skuNum, shelfCapacity, orders)
        
        count_ours = SM.simulation(orders, racks_ours, stationCapacity)
        count_trnv = SM.simulation(orders, racks_trnv, stationCapacity)
        count_ieee = SM.simulation(orders, racks_ieee, stationCapacity)
        count_iise = SM.simulation(orders, racks_iise, stationCapacity)
        imp_to = (count_trnv-count_ours)/count_ours
        imp_ieee = (count_ieee-count_ours)/count_ours
        imp_iise = (count_iise-count_ours)/count_ours
        wdata = [skuNum,orderCount,shelfCapacity,strength_coefficient,stationCapacity,order_size_max,count_ours,count_trnv,imp_to,count_ieee,imp_ieee,count_iise,imp_iise]
        f = open(fileName,'a',newline='')
        writer = csv.writer(f)
        writer.writerow(wdata)
        f.close()