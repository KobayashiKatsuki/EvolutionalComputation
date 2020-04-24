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

import numpy as np
import chromosome
from GASetting import GASetting as GA

#%%
class Indivisual:    
    # 遺伝的アルゴリズムの個体共通のパラメータ
    g_len = GA.item.__len__()
    locus2elem = []
    for k in GA.item.keys():
        locus2elem.append(k)
    
    def __init__(self, init_chrom=None):
        # この個体が持つ染色体
        if init_chrom == None:
            self.chrom = chromosome.Chromosome(Indivisual.g_len)
        else:
            self.chrom = init_chrom

        # 遺伝子型(genotype)　遺伝子長は個体（解きたい問題）により異なる
        self.gtype = self.chrom.get_GType()         
        # 表現型（phenotype）
        self.ptype = self.decoder()
        # 適応度、容量
        self.fitness, self.capacity = self.fitness_and_capacity()
        
    def show_indivisual_info(self):
        """ 個体情報を表示する """        
        # 染色体情報
        print(f'g_len: {Indivisual.g_len} {self.gtype} {self.ptype}')
        # 適応度
        print(f'fitness: {self.fitness:.1f}, capacity: {self.capacity:.1f}')
    
    def fitness_and_capacity(self):
        """ 個体の適応度, キャパ計算 """
        f_val = 0
        c_val = 0
        for locus in range(Indivisual.g_len):
            if self.gtype[locus]==1:
                elem = Indivisual.locus2elem[locus]
                f_val += GA.item[elem][0]
                c_val += GA.item[elem][1]
                
        return f_val, c_val
    
#%% エンコーダ・デコーダ　実際に最適化問題を設計するときはここの実装を頑張る
    def decoder(self):
        """
        デコーダ　Gtype -> Ptpye の変換
        """
        ptype_array = []        
        for locus in range(Indivisual.g_len):
            if self.gtype[locus] == 1:
                ptype_array.append(Indivisual.locus2elem[locus])
                
        return ptype_array


    def encoder(self, ptype = []):
        """
        エンコーダー Ptype -> Gtypeの変換
        """
        pass

#%%
    def crossover(self, partner_chrom: chromosome.Chromosome):
        """ 
         交叉 他の個体のG-typeとランダムで遺伝子を交換する        
        """        
        child1_chrom = chromosome.Chromosome(Indivisual.g_len)
        child2_chrom = chromosome.Chromosome(Indivisual.g_len)

        for locus in range(Indivisual.g_len):
            p1_g = self.chrom.get_gene(locus)
            p2_g = partner_chrom.get_gene(locus)
            
            # 一様交叉　
            is_cross = np.random.randint(2)
            if is_cross == 1:
                child1_chrom.set_gene(locus, p2_g)
                child2_chrom.set_gene(locus, p1_g)
            else:
                child1_chrom.set_gene(locus, p1_g)
                child2_chrom.set_gene(locus, p2_g)
        
        child1 = Indivisual(child1_chrom)
        child2 = Indivisual(child2_chrom)        
        
        return child1, child2

#%%
    def mutation(self):
        """ 突然変異体を生成する """
        mutant_chrom = chromosome.Chromosome(Indivisual.g_len)
        
        # 少なくともひとつの遺伝子座を一定確率で対立遺伝子にする
        mutant_flg = False
        while mutant_flg is False:
        
            for locus in range(Indivisual.g_len):
                p_g = self.chrom.get_gene(locus)
                p_a = self.chrom.get_allele(locus)
                
                is_mutation = np.random.randint(GA.MUTATION_RATE)
                if is_mutation == 0:
                    mutant_chrom.set_gene(locus, p_a)
                    mutant_flg = True
                else:
                    mutant_chrom.set_gene(locus, p_g) 
            
        mutant = Indivisual(mutant_chrom)
        
        return mutant
