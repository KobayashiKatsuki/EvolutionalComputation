# -*- coding: utf-8 -*-
"""
遺伝子クラス（バイナリエンコード）
・遺伝子(gene)：　個体を形成する最小構成要素
　‐対立遺伝子(allele)：　遺伝子がとりうる値(g_code)
 　（バイナリエンコーディングなら0, 1の2値）
"""
class GeneBin:
    allele = {0: 0, 1: 1} #対立遺伝子セット（バイナリ）

    def __init__(self, code=0):
        # コードをキーに遺伝子を生成する
        if code == 0 or code == 1:
            self.g_code = self.allele[code]
        else:
            self.g_code = self.allele[0]
    
    def get_allele(self):
        """ 対立遺伝子を1つ返す """
        return self.allele[0] if self.g_code == 1 else self.allele[1]
        