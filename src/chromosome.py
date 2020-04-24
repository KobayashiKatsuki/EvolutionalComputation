# -*- coding: utf-8 -*-
"""
染色体クラス
・染色体：　遺伝子の並びで定義される個体情報
　‐遺伝子長(g_len)：　染色体（配列）の長さn <-パラメータ
　‐遺伝子座(locus)：　染色体上における各遺伝子の位置
　‐遺伝子型（GType）：　染色体を表す記号列、内部表現
　‐表現型（PType）：　染色体から個体として発現する外部表現
"""

import gene
import numpy as np

class Chromosome:
    def __init__(self, g_len):
        self.chrom = []
        self.g_len = g_len # 遺伝子長
        
        # コンストラクタではランダムに染色体を生成する
        for i in range(self.g_len):
            g = gene.GeneBin(np.random.randint(2))
            self.chrom.append(g)
    
    def get_GType(self):
        """ 染色体（遺伝子配列,GType）を数値リストで返す """
        gtype = []
        for locus in range(self.g_len):
            g = self.chrom[locus]
            gtype.append(g.g_code)
        
        return gtype
    
    def get_gene(self, locus):
        """ 遺伝子をひとつ取り出す """
        if locus >= 0 and locus < self.g_len:
            return self.chrom[locus]
        else:
            return None
    
    def set_gene(self, locus, g: gene.GeneBin):
        """ 染色体に遺伝子をセットする """
        if locus >= 0 and locus < self.g_len:
            self.chrom[locus] = g
    
    def get_allele(self, locus):
        """ 突然変異遺伝子を取り出す """
        if locus >= 0 and locus < self.g_len:
            g = self.chrom[locus]
            allele_code = g.get_allele_code()
            allele = gene.GeneBin(allele_code)
            return allele
        else:
            return None