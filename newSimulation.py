# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:22:06 2024

@author: 74110
"""

import functions as F
import generate_instances as G
# import heuristic as H

import numpy as np
# import Benchmarks as B
class Station:
    def __init__(self, orders:dict, processSequence:list, shelves:dict, n:int):
        self.n = n#工作站同时处理订单的数量
        self.orderList = F.copy(orders)#订单信息
        self.processSequence = F.copy(processSequence)#订单处理顺序
        self.processingOrders = []#正在处理的订单编号
        self.shelfUsing = None#正在使用的货架编号
        self.skusRequired = set()#需要拣选的SKU集合
        self.shelves = F.copy(shelves)#所有货架的信息
        self.shelfCount = len(self.shelves)#货架数量
        self.totalCount = 0 #货架使用个数
        self.ordersDetailProcessing = {}
        return
    
    def getNewOrders(self):
        while len(self.processingOrders) < self.n and self.processSequence:
            orderId = self.processSequence.pop(0)
            self.processingOrders.append(orderId)
            self.ordersDetailProcessing[orderId] = set(F.copy(self.orderList[orderId]))
        if self.ordersDetailProcessing:
            self.skusRequired = set().union(*self.ordersDetailProcessing.values())#找到所有正在被处理的订单还需要的sku的并集
        return 
    
    def getNewShelf(self):
        sf = list(range(self.shelfCount))
        matchDegrees = []
        for s in sf:
            md = len(self.skusRequired.intersection(self.shelves[s]))#计算每个货架的匹配度
            matchDegrees.append(md)
        maxMatchShelf = matchDegrees.index(max(matchDegrees))#找到匹配度最大的货架
        self.shelfUsing = maxMatchShelf
        self.totalCount += 1
        return
    
    def needChangeShelf(self):
        if self.shelfUsing == None:
            return True
        else:
            tag = True
            for _o in self.processingOrders[:]:
                skusPicked = self.ordersDetailProcessing[_o].intersection(self.shelves[self.shelfUsing])#
                if skusPicked:
                    tag = False
                    break
            return tag
        
    def pick(self):
        while not self.canEnd():
            self.getNewOrders()
            if self.needChangeShelf():#是否需要更换货架
                self.getNewShelf()
            for _o in self.processingOrders[:]:#拣选
                skusPicked = self.ordersDetailProcessing[_o].intersection(self.shelves[self.shelfUsing])#对每个订单，计算可以拣选的SKU列表
                self.ordersDetailProcessing[_o] = self.ordersDetailProcessing[_o]-skusPicked#从订单中取出已经拣选的SKU
                if not self.ordersDetailProcessing[_o]:#如果剩下的集合为空集
                    del self.ordersDetailProcessing[_o]#从当前处理的订单中删除
                    self.processingOrders.remove(_o)
        return 
        
    def canEnd(self):
        if len(self.processingOrders)==0 and len(self.processSequence) == 0:#待处理订单和正在处理的订单都为空
            return True
        else:
            return False
        
def simulation(orders, shelves, n, processSequence = None):
    if not processSequence:
        processSequence = list(range(len(orders)))
    station = Station(orders, processSequence, shelves, n)
    station.pick()
    return station.totalCount



if __name__ == '__main__':
    skuNum = 100
    shelfCapacity = 100
    orderCount = 100
    maxSize = 5
    stationCapacity = 3
    order_size_ub = 10
    strength_coefficient = 0.5
    #为了保证生成订单时候的相似度矩阵和ieee方案中使用的相似度矩阵相同，直接在这里生成矩阵在传入两函数。
    # similarity_matrix = G.generate_similarity_matrix(skuNum, strength_coefficient)
    # orders = G.generate_orders(similarity_matrix, skuNum, orderCount, order_size_ub)
    shelves, orders = F.genRandomCase(skuNum, shelfCapacity, orderCount, maxSize)
    count = simulation(orders, shelves, stationCapacity)
    
    # racks_ours = H.heuristic(skuNum, shelfCapacity)
    # racks_turnover = B.Turnover(skuNum, shelfCapacity)
    # racks_ieee = B.IEEESolution(skuNum, shelfCapacity, similarity_matrix)
    # racks_iise = B.IISESolution(skuNum, shelfCapacity, orders)
    
    # count_ours = simulation(orders, racks_ours, stationCapacity)
    # count_turnover = simulation(orders, racks_turnover, stationCapacity)
    # count_ieee = simulation(orders, racks_ieee, stationCapacity)
    # count_iise = simulation(orders, racks_iise, stationCapacity)
