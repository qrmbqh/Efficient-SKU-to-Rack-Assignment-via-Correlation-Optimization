# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:58:38 2024

@author: zhangjiajia
"""
import numpy as np
import pandas as pd
import math 

def find_next_nodes(c2, paths):
    new_paths = []
    for path in paths:
        remain = list(set(c2.index) - set(path))
        remain.sort()
        for node in remain:
            if node > path[-1]:
                if np.count_nonzero(c2.loc[node, path].values) == len(path):
                    new_path = path.copy()
                    new_path.append(node)
                    new_paths.append(new_path)
    return new_paths
        
def find_all_circles(c,size_ub):
    skus = list(set(np.nonzero(c.values)[0]))
    skus.sort()
    c2 = c.loc[skus, skus]
    paths = []
    for i in c2.index:
        paths.append([i])
    all_paths = {1:paths}
    for i in range(size_ub-1):
        paths = all_paths[i+1]
        new_paths = find_next_nodes(c2, paths)
        all_paths[i+2] = new_paths
    del all_paths[1]
    keys = list(all_paths.keys())
    for i in keys:
        if len(all_paths[i]) == 0:
            del all_paths[i]
    
    return all_paths

def update_circles(all_circles, c):
    new_all_circles = {}
    for i in all_circles.keys():
        paths = all_circles[i]
        circles = []
        for path in paths:
            order = list(set(path))
            temp = c.loc[order, order]
            if len(temp.values[temp.values == 0]) == temp.shape[0]:
                circles.append(path)
        if len(circles) > 0:
            new_all_circles[i] = circles
    return new_all_circles

def generate_similarity_matrix(S, strength_coefficient):
    '''
    生成相似度矩阵。

    Parameters
    ----------
    S : int
        SKU数量
    strength_coefficient: float
                          相关性强度系数，取值范围 0 < strength_coefficient <= 1

    Returns
    -------
    c : pandas DataFrame
        SKU相似度矩阵

    '''
    s = 0.139
    D = 30*S
    turnover = {}
    for i in range(S):
        turnover[i] = round(D * (pow(1/S*(i+1), s) - pow(1/S*i, s)))
        
    c = pd.DataFrame(np.zeros((S,S)))
    
    lists = list(turnover.values())
    
    for i in range(S):
        for j in range(i+1,S):
            up_list = [0]
            for k in range(i):
                up_list.append(c.iloc[k,i] + c.iloc[k,j] - lists[k])
            lb = max(up_list)
            ub = math.ceil(strength_coefficient * min([lists[i], lists[j]]))
            if lb <= ub:
                value = np.random.randint(lb, ub+1)
            else:
                value = 0
            c.iloc[i,j] = value
            c.iloc[j,i] = value
            if value > 0:
                temp = sum([c.iloc[k,i] for k in range(i)])
                if temp >= value:
                    value2 = np.random.randint(0,value+1)
                else:
                    value2 = value - temp
                lists[i] = max([0,lists[i] - value2])
                temp = sum([c.iloc[k,j] for k in range(j)])
                if temp >= value:
                    value2 = np.random.randint(0,value+1)
                else:
                    value2 = value - temp
                lists[j] = max([0,lists[j] - value2])
    #np.count_nonzero(c.values)
    remain_turnover = pd.Series(lists)
    remain_turnover = remain_turnover.replace(0,np.nan).dropna()
    return c, remain_turnover

def generate_orders(similarity_matrix, remain_turnover,S, size_ub):
    '''
    第二种从相似度矩阵中生成订单的方式：
       与第一种的区别：第一种方式从矩阵中选择订单后，（1）从选出来的订单计算出的相关性矩阵与原始生成的相关性矩阵c可能不相等，会影响仿真结果。
                    第二种方式从生成的订单计算出的相关性矩阵与原始矩阵c相同，但生成的订单数量不可控，可能会比较多。

    Parameters
    ----------
    similarity_matrix : pandas DataFrame
        SKU相似度矩阵
    S : int
        SKU数量
    n : int
        订单数量
    remain_turnover：pandas Series
                    生成相关性矩阵后，每种SKU剩余的数量，用于生成size为1的订单
    size_ub: int
            生成的订单在最大允许的size

    Returns
    -------
    orders : dict
        产生的订单.

    '''
    c = similarity_matrix.copy()
    
    orders = []
    while c.sum().sum() != 0:
        all_circles = find_all_circles(c,size_ub)
        while len(all_circles) != 0:
            order_size = np.random.choice(list(all_circles.keys()))
            circles = all_circles[order_size]
            order = list(set(circles[np.random.choice(range(len(circles)))]))
            orders.append(order)
            for i in range(len(order)):
                for j in range(i+1,len(order)):
                    sku1,sku2 = order[i], order[j]
                    c.loc[sku1,sku2] = c.loc[sku1,sku2] - 1
                    c.loc[sku2,sku1] = c.loc[sku1,sku2] 
            all_circles = update_circles(all_circles, c)
        
    new_orders = {x:orders[x] for x in range(len(orders))}
    for i in remain_turnover.index:
        for j in range(int(remain_turnover.loc[i])):
            new_orders[len(new_orders)] = [i]
    
    return new_orders

def main(S, size_ub, strength_coefficient):
    similarity_matrix, remain_turnover = generate_similarity_matrix(S, strength_coefficient)
    orders = generate_orders(similarity_matrix, remain_turnover, S, size_ub)
    return orders
    


















