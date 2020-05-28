# -*- coding: utf-8 -*-
"""
遺伝子
・8bitのバイナリコード配列 = 1コドンとする
"""

import numpy as np

class Gene:
    def __init__(self):
        self.g_code = [np.random.randint(2) for i in range(8)]
        self.d_code = self.decode()

    
    def decode(self):
        """ コドンの数値表現 """
        cod_val = 0
        # 先頭要素ほど上位の桁
        for i in range(8):
            cod_val += 2**(7-i) * self.g_code[i]
            
        return cod_val
            