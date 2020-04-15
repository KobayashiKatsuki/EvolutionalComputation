# -*- coding: utf-8 -*-
"""
個体クラス
解きたい問題に応じて実装する

・個体：　1つまたは複数の染色体から生成される実体
　　　　　最適化問題の解とは最適な個体として表現される

　個体は遺伝子型（G-type）と表現型（P-type）をもつ
　G-typeは各種演算（交叉・淘汰・突然変異）の対象であり、
　P-typeは解そのものを表す
"""

import chromosome

#%%
class indivisual:    
    """ ナップサック問題の個体 """
    capacity = 10
    
    item = {'E1': (0.9, 1.0), 'E2': (1.1, 1.3)}
    
    def __init__(self, g_len=1):
        # 遺伝子型(genotype)　遺伝子長は個体（解きたい問題）により異なる
        self.gtype = chromosome.chromosome(g_len=g_len)
        # 表現型（phenotype）
        self.ptype = self.decoder()
        
    def show_chromosome(self):
        """ この個体の染色体を表示する """
        chrom_lst = self.chrom.get_gene_list()
        print(f'g_len: {self.chrom.g_len} {chrom_lst}')

#%% エンコーダ・デコーダ　実際に最適化問題を設計するときはここの実装を頑張る

    def encoder(self):
        """
        エンコーダー Ptype -> Gtypeの変換
        実質使わない？（外側から遺伝子操作することは無い？）
        """
        pass
    
    def decoder(self):
        """
        デコーダ　Gtype -> Ptpye の変換
        
        """
        
        
        
        
        
        
        
        
        pass
    
