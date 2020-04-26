# -*- coding: utf-8 -*-
"""
染色体クラス
・染色体：　遺伝子の並びで定義される個体情報
　‐遺伝子長(g_len)：　染色体（配列）の長さn <-パラメータ
　‐遺伝子座(locus)：　染色体上における各遺伝子の位置
　‐遺伝子型（GType）：　染色体を表す記号列、内部表現
　‐表現型（PType）：　染色体から個体として発現する外部表現
 
  どの遺伝子を用いるかは問題設定次第 
 
"""

import gene
import numpy as np
from GASetting import GASetting as GA

class Chromosome:
        
    def __init__(self, g_len):
        self.chrom = []
        self.g_len = g_len # 遺伝子長
        
        if GA.PROBLEM_TYPE == 'KNAPSACK':            
            for i in range(self.g_len):
                g = gene.GeneBin() # 遺伝子(バイナリ)
                self.chrom.append(g)
                
        elif GA.PROBLEM_TYPE == 'TSP':
            # ランダムなalleleの順序で遺伝子配列を生成する
            allele_perm = np.array(list(GA.item.keys()))
            np.random.shuffle(allele_perm)
            for city_code in list(allele_perm):
                g = gene.GenePerm(city_code)
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
        """ 対立遺伝子をひとつ取り出す """
        if locus >= 0 and locus < self.g_len:
            g = self.chrom[locus]
            allele = gene.GeneBin(g.g_code) # 同じコードの遺伝子を生成し…
            allele.invert_g_code() # その遺伝子コードを反転させる
            return allele
        
        else:
            return None