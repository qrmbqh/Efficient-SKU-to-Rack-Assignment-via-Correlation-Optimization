# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:27:55 2024

@author: zhangjiajia
"""
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd


def slap(midu, matric, timelimit):
    '''
    0-1整数规划模型

    Parameters
    ----------
    midu : int
        货架容量，每个货架里最多存放 midu 个SKU
    matric : pandas DataFrame
        SKU相似度矩阵
    timelimit : int
        最大计算时间

    Returns
    -------
    obj : int
        计算结果目标值
    time1 : int
        计算时间

    '''
    allsku = list(matric.columns)
    I = len(allsku)
        
    model = gp.Model('l_r3')
    #model.setParam('OutputFlag', 0)
    #model.Params.method = 0
    model.Params.timelimit = timelimit
    index = []
    for i in range(I-1):
        for j in range(i+1,I):
            index.append((i,j))
    z = model.addVars(index, vtype=GRB.BINARY, name='z')
    
    expr = []
    for i in range(I-1):
        for j in range(i+1, I):
            expr.append(matric.iloc[i,j] * z[i,j])
    model.setObjective(gp.quicksum(expr), GRB.MAXIMIZE)
    
    for i in range(I):
        expr = []
        for j in range(i):
            expr.append(z[j,i])
        for j in range(i+1, I):
            expr.append(z[i,j])
        model.addConstr(gp.quicksum(expr) <= (midu - 1))
        
    for i in range(I-2):
        for j in range(i+1, I-1):
            for l in range(j+1, I):
                model.addConstr(z[i,j] + z[j,l] - z[i,l] <= 1)
    
    for i in range(I-2):
        for j in range(i+1, I-1):
            for l in range(j+1, I):
                model.addConstr(z[i,j] - z[j,l] + z[i,l] <= 1)
    
    for i in range(I-2):
        for j in range(i+1, I-1):
            for l in range(j+1, I):
                model.addConstr(-z[i,j] + z[j,l] + z[i,l] <= 1)
    
    model.optimize()
    #print('obj: %g' % model.objVal)
    obj = model.objVal
    time1 = model.runtime
    
    return obj, time1

def slap_lr(midu, matric):
    '''
    线性松弛模型

    Parameters
    ----------
    midu : int
        货架容量，每个货架里最多存放 midu 个SKU
    matric : pandas DataFrame
        SKU相似度矩阵

    Returns
    -------
    obj : int
        计算结果目标值
    time1 : int
        计算时间

    '''
    allsku = list(matric.columns)
    I = len(allsku)
        
    model = gp.Model('slap_lr')
    model.setParam('OutputFlag', 0)
    #model.Params.method = 1
    #model.Params.timelimit = 200
    #model.Params.Presolve = 2
    index = []
    for i in range(I-1):
        for j in range(i+1,I):
            index.append((i,j))
    z = model.addVars(index, lb=0,ub=1, vtype=GRB.CONTINUOUS, name='z')
    
    expr = []
    for i in range(I-1):
        for j in range(i+1, I):
            expr.append(matric.iloc[i,j] * z[i,j])
    model.setObjective(gp.quicksum(expr), GRB.MAXIMIZE)
    
    for i in range(I):
        expr = []
        for j in range(i):
            expr.append(z[j,i])
        for j in range(i+1, I):
            expr.append(z[i,j])
        model.addConstr(gp.quicksum(expr) <= (midu - 1))
        
    for i in range(I-2):
        for j in range(i+1, I-1):
            for l in range(j+1, I):
                model.addConstr(z[i,j] + z[j,l] - z[i,l] <= 1)
    
    for i in range(I-2):
        for j in range(i+1, I-1):
            for l in range(j+1, I):
                model.addConstr(z[i,j] - z[j,l] + z[i,l] <= 1)
    
    for i in range(I-2):
        for j in range(i+1, I-1):
            for l in range(j+1, I):
                model.addConstr(-z[i,j] + z[j,l] + z[i,l] <= 1)
                
    model.optimize()
    #print('obj: %g' % model.objVal)
    obj = model.objVal
    time1 = model.runtime
    
    return obj, time1
