# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:30:13 2024

@author: 74110
"""

import pandas as pd
import random
import pickle
from collections import Counter

def copy(originObj): 
    """
    对象深拷贝
    
    参数:
    originObj:被拷贝对象
    返回:
    l: 拷贝对象
    """
    l = pickle.loads(pickle.dumps(originObj))
    assert type(l)== type(originObj)
    return l

def genRandomCase(skuNum,shelfCapacity, orderCount, maxSize):
    '''
    产生随机算例。
    Parameters
    ----------
    skuNum : int
        SKU数量.
    shelfCapacity : int
        货架容量.
    orderCount : int
        订单数量.
    maxSize : int
        订单size最大值.

    Returns
    -------
    shelves : dict
        随机产生的SKU到货架分配方案.
    orders : dict
        随机产生的订单.

    '''
    skus = list(range(skuNum))  # SKU 列表，例如 [1, 2, 3, ..., n]

    # 将 SKU 列表随机打乱
    random.shuffle(skus)
    
    # 将 SKU 分配到货架上，每个货架最多存放 k 种 SKU
    shelves = {}
    index = 0
    for i in range(0, len(skus), shelfCapacity):
        shelves[index] = skus[i:i + shelfCapacity]
        index += 1
        
    # SKU 列表
    all_skus = list(range(skuNum))
    
    # 生成订单字典
    orders = {}
    for i in range(orderCount):
        # 随机生成订单的 SKU 数量（订单大小）
        order_size = random.randint(1, maxSize)
        # 从所有 SKU 中随机选择 order_size 个 SKU
        orders[i] = random.sample(all_skus, order_size)
    
    return shelves, orders

def transform_rack_to_sku_matrix(rack):
    """
    将货架-SKU存储数据转换为SKU-货架矩阵形式。

    输入的二维列表 rack 中，每个子列表代表一个货架上存储的 SKU 列表。函数返回一个 SKU-货架矩阵，其中行表示 SKU，列表示货架。矩阵中的值为 1 表示 SKU 存储在该货架上，0 表示未存储。

    参数:
    rack (list of lists): 一个二维列表，其中每个子列表代表一个货架上存储的 SKU 列表。
                         例如：[[22, 35, 43], [1, 7, 25, 33], [6, 42, 46]]
    
    返回:
    list of lists: 返回一个 SKU-货架矩阵（二维列表），行表示 SKU，列表示货架。
                   如果 SKU 存储在某个货架上，则交点位置为 1，否则为 0。
    
    """
    # 获取所有SKU的集合以确定行数，并找到货架的数量确定列数
    all_skus = {sku for shelf in rack for sku in shelf}
    max_sku = max(all_skus)  # 假设SKU编号为整数
    num_shelves = len(rack)

    # 初始化一个SKU x 货架的矩阵
    sku_matrix = [[0] * num_shelves for _ in range(max_sku + 1)]

    # 填充矩阵：若SKU存储在某货架上，设为1
    for shelf_index, shelf in enumerate(rack):
        for sku in shelf:
            sku_matrix[sku][shelf_index] = 1

    # 移除空行（即没有在任何货架上的 SKU）
    sku_matrix = [row for row in sku_matrix if any(row)]

    return sku_matrix

def genMatricxAbyOrders(orders, skuNum):
    A = []
    for order in orders:
        temp = []
        for sku in range(skuNum):
            if sku in orders[order]:
                temp.append(1)
            else:
                temp.append(0)
        A.append(temp)
    return A

def genInitialRacks(skuNum, shelfCapacity, orders):
    sorted_orders = [order for _, order in sorted(orders.items(), key=lambda x: len(x[1]))]
    racks = []
    skuAssigned = [0]*skuNum
    rack = []
    for order in sorted_orders:
        for sku in order:
            if skuAssigned[sku] == 0 and len(rack) < shelfCapacity:
                rack.append(sku)
                skuAssigned[sku] = 1
                if len(rack) == shelfCapacity:
                    racks.append(rack)
                    rack = []
                    
    for sku in range(skuNum):
        if skuAssigned[sku] == 0 and len(rack) < shelfCapacity:
            rack.append(sku)
            skuAssigned[sku] = 1
            if len(rack) == shelfCapacity:
                racks.append(rack)
                rack = []
    racks = transform_rack_to_sku_matrix(racks)
    return racks