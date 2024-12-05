# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:22:53 2024

@author: zhangjiajia
"""
from two_partitioning import two_partitioning
from time import time
from AP import AP
import networkx
import generate_instances as G

def ObjValues(racks, c):
    '''
    计算货架对应的相似度目标值

    Parameters
    ----------
    racks : list
        货架组成的列表。示例：racks=[[1,2],[0,4]]
    c : pandas DataFrame
        SKU相似度矩阵

    Returns
    -------
    values : int
        目标值

    '''
    values = 0
    for i in racks:
        values = values + c.loc[list(i),list(i)].sum().sum() / 2
    return values

def get_inSol(c, midu):
    '''
    生成初始上架方案

    Parameters
    ----------
    c : pandas DataFrame
        SKU相似度矩阵
    midu : int
        货架容量，每个货架里最多存放 midu 个SKU

    Returns
    -------
    sol : list
        货架组成的列表

    '''
    series = c.sum().sort_values(ascending=False)
    skus = list(series.index)
    assigned_sku = set()
    sol = []
    while len(skus) != 0:
        sku = skus[0]
        rack = set([sku])
        assigned_sku.add(sku)
        series2 = c.loc[sku, list(set(skus) - assigned_sku)].sort_values(ascending=False)
        for i in series2.index:
            rack.add(i)
            assigned_sku.add(i)
            if len(rack) == midu:
                break
        sol.append(rack)
        skus = list(c.loc[list(set(skus) - assigned_sku), list(set(skus) - assigned_sku)].sum().sort_values(ascending=False).index)
    return sol
    
def heuristic(c, skuNum, midu):
    '''

    Parameters
    ----------
    c : pandas DataFrame
        SKU相似度矩阵
    midu : int
        货架容量，每个货架里最多存放 midu 个SKU

    Returns
    -------
    racks : dict
        产生的SKU到货架分配方案.

    '''
    # c = G.generate_similarity_matrix(skuNum)
    start = time()
    racks = get_inSol(c, midu)
    best_sol = racks.copy()
    best_value = ObjValues(racks, c)
    current = racks.copy()
    tabus = {x:[] for x in range(len(current))}
    while True:
        values = {}
        nodes = []
        for i in range(len(current)):
            tabu = tabus[i].copy()
            for j in range(i+1, len(current)):
                if j not in tabu:
                    rack1 = current[i]
                    rack2 = current[j]
                    temp = list(rack1 | rack2)
                    temp_c = c.loc[temp,temp]
                    new_two_racks = two_partitioning(temp_c, midu)
                    cut1, cut2 = new_two_racks
                    value = 0.5 * (c.loc[list(cut1), list(cut1)].sum().sum() + c.loc[list(cut2), list(cut2)].sum().sum() - c.loc[list(rack1), list(rack1)].sum().sum() - c.loc[list(rack2), list(rack2)].sum().sum())
                    if value > 0:
                        values[(i,j)] = (value, cut1, cut2)
                        nodes.extend([i,j])
                    else:
                        tabu.append(j)
            tabus[i] = tabu.copy()
        for i in range(len(current)):
            if i in nodes:
                tabus[i] = []
            else:
                tabu = list(set(tabus[i]) - set(nodes))
                tabus[i] = tabu.copy()
                
        if len(set(nodes)) == len(nodes):
            combs = list(values.keys())
        else:
            combs = AP(values)
        
        neighbor = current.copy()
        for i in combs:
            cut1, cut2 = values[tuple(i)][1], values[tuple(i)][2]
            neighbor[i[0]] = set(cut1)
            neighbor[i[1]] = set(cut2)
        neighbor_value = ObjValues(neighbor, c)
        if neighbor_value == best_value:
            break
        else:
            best_sol = neighbor.copy()
            racks1 = []
            for i in best_sol:
                if len(i) != 0:
                    racks1.append(i)
            best_sol = racks1.copy()
            current = best_sol.copy()
            best_value = ObjValues(best_sol, c)
            # print(best_value)
    end = time()
    runtime = end - start
    
    racks = {}
    for i in range(len(current)):
        racks[i] = list(current[i])
    
    return racks