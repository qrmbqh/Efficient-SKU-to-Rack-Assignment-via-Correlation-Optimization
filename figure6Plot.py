# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:36:02 2024

@author: 74110
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

data = pd.read_excel(r"C.xlsx")
plt.figure(figsize=(10, 6),dpi=600)
times_new_roman = FontProperties(family='Times New Roman', size=12)
# plt.figure(figsize=(18,10))
plt.plot(data.iloc[:,0], data.iloc[:,1], 'x--')
plt.xticks(ticks=[0,5,10,15,20,25,30,35,40,45,50], labels=[0,5,10,15,20,25,30,35,40,45,50])
# plt.yticks(fontsize=18)
plt.xlabel('$C$', fontproperties=times_new_roman, fontsize=14)
plt.ylabel('$N$', fontproperties=times_new_roman, fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()