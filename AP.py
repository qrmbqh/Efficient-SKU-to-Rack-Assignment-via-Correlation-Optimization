# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 16:58:21 2022

@author: mbbsdbd
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd

def AP(values):
    '''
    一对一指派。

    Parameters
    ----------
    values : dict
        工作i指派给j的收益为value。示例：values={(i,j):value}

    Returns
    -------
    combs : list
        指派结果。示例：combs=[[1,2],[3,4]]，1指派给了2，3指派给了4.

    '''
    nodes = set()
    for i in values.keys():
        nodes = nodes | set(i)
    nodes = list(nodes)
    matric = pd.DataFrame(np.zeros((len(nodes),len(nodes))), index=nodes, columns=nodes)
    for i in values.keys():
        matric.loc[i[0],i[1]] = values[i][0]
        
    model = gp.Model('AP')
    model.setParam('OutputFlag', 0)
    x = model.addVars(matric.shape[0], matric.shape[1], vtype=GRB.BINARY, name='x')
    expr = []
    for i in range(matric.shape[0]):
        for j in range(matric.shape[1]):
            expr.append(matric.iloc[i,j] * x[i,j])
    model.setObjective(gp.quicksum(expr), GRB.MAXIMIZE)
    for i in range(matric.shape[0]):
        model.addConstr(gp.quicksum(x[i,j] for j in range(matric.shape[1])) == 1)
    for j in range(matric.shape[1]):
        model.addConstr(gp.quicksum(x[i,j] for i in range(matric.shape[0])) == 1)
    for i in range(matric.shape[0]):
        for j in range(matric.shape[1]):
            model.addConstr(x[i,j] == x[j,i])
    model.optimize()
    # print('obj: %g' % model.objVal)
    combs = []
    for i in range(matric.shape[0]):
        for j in range(matric.shape[1]):
            if x[i,j].x == 1:
                if matric.iloc[i,j] > 0:
                    combs.append([matric.index[i],matric.index[j]])
                
    return combs