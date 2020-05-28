# -*- coding: utf-8 -*-
"""
Grammatical Evolution

"""

from Indivisual import Indivisual
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as anm
from matplotlib.animation import PillowWriter
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']






#%%
# Grammatical Evolution　メイン処理
#
if __name__ == '__main__':    
    idv = Indivisual()
    idv.show_g_code()
