# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 22:12:23 2024

@author: 74110
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import PercentFormatter

def plotLine(file_path, x, xlabel, model = 0):
    # 设置字体为 Times New Roman
    plt.figure(figsize=(10, 6),dpi=600)
    times_new_roman = FontProperties(family='Times New Roman', size=12)
    
    # 读取 Excel 文件
    # file_path = '../2024-11-10拣选站容量分析_2.xlsx'
    df = pd.read_excel(file_path)
    
    if model == 0:
        # 根据 order_size_max 分组计算 ours, trnvr, ieee, iise 的平均值
        grouped = df.groupby(x)[['ours', 'trnvr', 'ieee', 'iise']].mean()
        
        # 绘制折线图
        
        plt.plot(grouped.index, grouped['trnvr'], label='FT', marker='o')
        plt.plot(grouped.index, grouped['ieee'], label='CH', marker='s')
        plt.plot(grouped.index, grouped['iise'], label='EC', marker='^')
        plt.plot(grouped.index, grouped['ours'], label='IPM', marker='*')
        
        # 设置标题和轴标签字体
        # plt.title('Metrics vs Order Size Max', fontproperties=times_new_roman, fontsize=16)
        plt.xlabel(xlabel, fontproperties=times_new_roman, fontsize=14)
        plt.ylabel('$N$', fontproperties=times_new_roman, fontsize=14)
    if model == 1:
        # 根据 order_size_max 分组计算 ours, trnvr, ieee, iise 的平均值
        grouped = df.groupby(x)[['imp_to', 'imp_ieee', 'imp_iise']].mean()

        # 绘制折线图
        plt.figure(figsize=(10, 6),dpi=600)
        plt.plot(grouped.index, grouped['imp_to'] * 100, label='FT', marker='o')  # 转换为百分比
        plt.plot(grouped.index, grouped['imp_ieee'] * 100, label='CH', marker='s')    # 转换为百分比
        plt.plot(grouped.index, grouped['imp_iise'] * 100, label='EC', marker='^')    # 转换为百分比

        # 设置标题和轴标签字体
        # plt.title('Metrics vs Order Size Max', fontproperties=times_new_roman, fontsize=16)
        plt.xlabel(xlabel, fontproperties=times_new_roman, fontsize=14)
        plt.ylabel('$IR$ (%)', fontproperties=times_new_roman, fontsize=14)

        # 设置纵坐标为百分比格式
        plt.gca().yaxis.set_major_formatter(PercentFormatter())
    # 设置图例字体
    plt.legend(fontsize=12, prop=times_new_roman)
    
    # 添加网格
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # 显示图形
    plt.show()

if __name__=='__main__':
    file_path = './Results/2024-11-25新货架容量C_2.xlsx'
    x = 'shelfCapacity'
    xlabel = '$C$'
    
    # file_path = './Results/2024-11-25新关联强度theta_2.xlsx'
    # x = 'strength_coefficient'
    # xlabel = '$\\theta$'
    
    # file_path = './Results/2024-11-25新订单sizeL_2.xlsx'
    # x = 'order_size_max'
    # xlabel = '$L$'
        
    # file_path = './Results/2024-11-25新拣选站容量Q_2.xlsx'
    # x = 'stationCapacity'
    # xlabel = '$Q$'
    plotLine(file_path, x, xlabel, model = 1)