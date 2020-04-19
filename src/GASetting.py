# -*- coding: utf-8 -*-
"""
遺伝的アルゴリズムの問題設定クラス
    
"""
from collections import OrderedDict

class GASetting:
    # 何世代ループするか
    GENERATION_LOOP_NUM = 3        
    # 1世代で生成する個体数
    GROUP_SIZE = 10
    # 選択する個体数
    SELECT_NUM = 3    
    # ランキング選択のテーブル
    ranking_tbl = []
    
    # 収束判定
    converged_dif = 0.1
    
    """ ナップサック問題固有の設定 """
    capacity = 2.5 # ナップサックの容量
    item = OrderedDict()
    """ Ei: アイテム名, (Pi, Ci): (価値, 容量) """
    item['E1'] = (1.0, 0.9)
    item['E2'] = (1.1, 1.2)
    item['E3'] = (0.8, 0.9)
    item['E4'] = (1.4, 1.5)
    item['E5'] = (0.6, 0.5)
    
    def __init__(self):
        pass