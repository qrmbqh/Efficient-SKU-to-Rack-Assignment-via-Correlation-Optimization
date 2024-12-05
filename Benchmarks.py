# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:30:14 2024

@author: DELL
"""
import matlab.engine
import generate_instances as G
import numpy as np
import functions as F

def Turnover(skuNum, shelfCapacity):
    s = 0.139
    u = {}
    for i in range(skuNum):
        u[i] = (pow(1/skuNum*(i+1), s) - pow(1/skuNum*i, s))
    num = int(len(u) / shelfCapacity)
    racks = []
    for i in range(num):
        rack = list(u.keys())[i*shelfCapacity:(i+1)*shelfCapacity]
        racks.append(rack)
    racks.append(list(u.keys())[num*shelfCapacity:])
    new_racks = {}
    index = 0
    for x in racks:
        if len(x) > 0:
            new_racks[index] = x
            index = index + 1
    return new_racks

def IEEESolution(skuNum, shelfCapacity, similarityMatrix):
    similarityMatrix = F.copy(similarityMatrix)
    eng = matlab.engine.start_matlab()
    # similarityMatrix = G.generate_similarity_matrix(skuNum,strength_coefficient)
    data_matlab = matlab.double(np.array(similarityMatrix).tolist())
    data = eng.IEEE_CH(data_matlab, shelfCapacity)
    eng.quit()
    python_list = [[int(value)-1 for value in row[0]] for row in data]
    racks = {}
    for i in range(len(python_list)):
        racks[i] = python_list[i]
    return racks

def IISESolution(skuNum, shelfCapacity, orders):
    orders = F.copy(orders)
    initialRack = F.genInitialRacks(skuNum, shelfCapacity, orders)
    initialRack = matlab.double(np.array(initialRack).tolist())
    
    A = F.genMatricxAbyOrders(orders, skuNum)
    A = matlab.double(np.array(A).tolist())
    
    eng = matlab.engine.start_matlab()
    data = eng.IISE_EC(A, initialRack, shelfCapacity)
    eng.quit()
    racks = [[int(value)-1 for value in row[0]] for row in data]
    res = {}
    for i in range(len(racks)):
        res[i] = racks[i]
    return res
