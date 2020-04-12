# -*- coding: utf-8 -*-
"""
個体クラス
・個体：　1つまたは複数の染色体から生成される実体
　　　　　最適化問題の解とは最適な個体として表現される
"""

import chromosome

class indivisual:
    def __init__(self):
        # 遺伝子長　個体（解きたい問題）により異なる
        self.g_len = 5
        # 染色体は1つとする
        self.chrom = chromosome.chromosome(g_len=self.g_len)
        
    def show_chromosome(self):
        """ この個体の染色体を表示する """
        chrom_lst = self.chrom.get_gene_list()
        print(f'g_len: {self.chrom.g_len} {chrom_lst}')
        
        # 突然変異体
        #mutant = self.chrom.get_mutant()
        #print(mutant)
