# -*- coding: utf-8 -*-
"""
染色体
可変長バイナリコード
= 遺伝子（コドン）数 x 8bit
"""

from Gene import Gene
from GESetting import GESetting

class Chromosome:
        
    def __init__(self, n_codon):
        self.g_array = [] # 遺伝子コードの配列 
        self.d_array = [] # 遺伝子数値の配列
        self.n_codon=n_codon # コドンの総数
        self.ge = GESetting()

        for locus in range(self.n_codon):
            g = Gene()
            self.g_array.append(g)
            self.d_array.append(g.d_code)

    def show_gene(self):
        """ 染色体の表示 """
        for locus in range(self.n_codon):
            print(self.g_array[locus].g_code)
            print(self.d_array[locus])

#%%
if __name__ == '__main__':
    chrom = Chromosome(n_codon=3)
    chrom.show_gene()


