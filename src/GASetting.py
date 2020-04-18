# -*- coding: utf-8 -*-
"""
遺伝的アルゴリズムの問題設定クラス
    
"""
from collections import OrderedDict

class GASetting:
    # 何世代ループするか
    GENERATION_LOOP_NUM = 1    
    
    """
     ナップサック問題の設定    
    """
    capacity = 2.5 # ナップサックの容量
    item = OrderedDict()
    
    def __init__(self):
        """ Ei: アイテム名, (Pi, Ci): (価値, 容量) """
        GASetting.item['E1'] = (1.0, 0.9)
        GASetting.item['E2'] = (1.1, 1.2)
        GASetting.item['E3'] = (0.8, 0.9)
        GASetting.item['E4'] = (1.4, 1.5)
        GASetting.item['E5'] = (0.6, 0.5)
    