# -*- coding: utf-8 -*-
"""
個体クラス
個体の遺伝子表現は木構造である

"""

import numpy as np
import pandas as pd
from Gene import Gene
from Chromosome import Chromosome
from GPSetting import GPSetting as GP
from graphviz import Digraph

#%%
class Indivisual:    
    
    def __init__(self, init_chrom=None):
        # この個体が持つ染色体
        if init_chrom == None:
            #染色体の遺伝子数の初期値は個体ごとにランダムとする
            #self.g_len = np.random.randint(GP.INIT_NODE_NUM, GP.INIT_NODE_NUM+10)            
            self.chrom = Chromosome()
            self.g_len = self.chrom.g_len # GAと異なり、染色体側でlenを決める
        else:
            self.chrom = init_chrom

        # 遺伝子型(genotype)　遺伝子長は個体（解きたい問題）により異なる
        self.gtype = self.chrom.get_GType()         
        # 表現型（phenotype）
        self.ptype = self.decoder()
        # 適応度
        self.fitness = self.calc_fitness()
            
        
    def show_indivisual_info(self):
        """ 個体情報を表示する """        
        # 染色体情報
        print(f'{self.gtype} {self.ptype}')
        # 適応度
        print(f'fitness: {self.fitness:.3f}')
        
    def visualize_indivisual(self):
        """ グラフを描画する """
        g_tree = Digraph(format='png')        
        for g_id, gene in self.chrom.chrom_dict.items():
            g_tree.node(f'({g_id}) {gene.g_code}')
            if gene.node_type == Gene.NODE_ARITHMETIC:
                # 演算子ノードの場合
                arg1_code = self.chrom.chrom_dict[gene.arg1_id].g_code
                arg2_code = self.chrom.chrom_dict[gene.arg2_id].g_code         
                g_tree.edge(f'({g_id}) {gene.g_code}', f'({gene.arg1_id}) {arg1_code}')
                g_tree.edge(f'({g_id}) {gene.g_code}', f'({gene.arg2_id}) {arg2_code}')
        
        g_tree.view()        
        return
        
    def show_GType(self):
        """ G typeだけ表示する """
        print(f'{self.gtype}')
    
    def calc_fitness(self):
        """ 適応度計算 """        
        # ツリーで各テストデータの計算を行い、結果の平均誤差を評価値とする
        f_val = 0
        for tc in GP.testcase.values():
            print(tc)
            calc_result = self.chrom.calc_gene_tree(g_id=0, **tc)        
            print(calc_result)
            break

        return f_val
            
    
#%% エンコーダ・デコーダ　実際に最適化問題を設計するときはここの実装を頑張る
    def decoder(self):
        """
        デコーダ　Gtype -> Ptpye の変換
        木構造。。。。
        """
        ptype_array = []        
        """
        for locus in range(self.g_len):
            city = self.gtype[locus]
            ptype_array.append(GA.item[city])
        """
        
        return ptype_array

#%%
    def crossover(self, partner_chrom: Chromosome):
        """ 
         交叉 他の個体のG-typeとランダムで遺伝子を交換する        
        """        
        child1_chrom = Chromosome(Indivisual.g_len)
        child2_chrom = Chromosome(Indivisual.g_len)
        
        # 一様交叉
        for locus in range(Indivisual.g_len):
            p1_g = self.chrom.get_gene(locus)
            p2_g = partner_chrom.get_gene(locus)                
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
        mutant_chrom = Chromosome(Indivisual.g_len)

        # まずはコピー
        for locus in range(self.g_len):
            p_g = self.chrom.get_gene(locus)
            mutant_chrom.set_gene(locus, p_g)
            
        # ランダムで選んだ2か所の遺伝子座を入れ替える                            
        swap_locus = np.random.choice(np.array(range(self.g_len)), size=2, replace=False)
        m1_g = self.chrom.get_gene(swap_locus[0])
        m2_g = self.chrom.get_gene(swap_locus[1])
        mutant_chrom.set_gene(swap_locus[0], m2_g)
        mutant_chrom.set_gene(swap_locus[1], m1_g)
        
        mutant = Indivisual(mutant_chrom)
        
        return mutant
