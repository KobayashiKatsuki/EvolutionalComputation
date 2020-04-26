# -*- coding: utf-8 -*-
"""
遺伝子クラス
・遺伝子(gene)：　個体を形成する最小構成要素
　‐対立遺伝子(allele)：　遺伝子がとりうる値(g_code)
 　バイナリエンコーディングなら0, 1の2値
  順列エンコーディングなら順列を構成する集合の要素
"""
import numpy as np
from GASetting import GASetting as GA

class Gene:
    """ 遺伝子基底クラス """
    allele = {} # 対立遺伝子セット問題に応じて設定する
    def __init__(self):
        pass

class GeneBin(Gene):
    """ バイナリエンコーディング """
    allele = {0: 0, 1: 1} #バイナリエンコーディング

    def __init__(self, code=None):
        # 初期コードが無い場合はランダムに生成する
        if code is None:
            code = np.random.randint(2)
        self.g_code = self.allele[code]
    
    def invert_g_code(self):
        """ 突然変異を起こす（自身の遺伝子コードを反転する） """
        self.g_code = self.allele[0] if self.g_code == 1 else self.allele[1]
    
#class GenePerm(Gene):
#    """ 順列エンコーディング """
#    allele = {}