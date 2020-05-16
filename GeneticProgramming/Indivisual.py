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
        #染色体の遺伝子数の初期値は個体ごとにランダムとする
        self.chrom = Chromosome()
        
        # 初期値がある場合は一旦ツリーを削除してコピーする
        if init_chrom is not None:
            self.chrom.delete_subtree(0)
            self.chrom.copy_gene_tree(0, init_chrom.chrom_dict)
            self.chrom.reset_chrom_info()
            
        # GAと異なり、染色体側でlenを決める
        self.g_len = self.chrom.g_len         
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
        # ツリーで各テストデータの計算を行い、結果の平均誤差の逆数を適応度とする
        total_err = 0
        for tc_num, tc in GP.testcase.items():
            # ツリーによる計算結果
            calc_result = self.chrom.calc_gene_tree(g_id=0, **tc)   
            # 絶対誤差を加算
            total_err += np.abs(GP.testcase_answer[tc_num] - calc_result)
        
        # 誤差平均の逆数 誤差0（完全に一致）ならそれもう答えなのでめっちゃでかくする
        eps = 1.0e-7
        f_val = GP.testcase.__len__() / total_err if total_err > eps else 1.0e7
        
        return f_val
            
    
#%% 
    def decoder(self):
        """
        デコーダ　Gtype -> Ptpye の変換
        木構造を式の形に変形する？
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
        # ルートノード以外の任意のノード（遺伝子）を一つ選び、交換する
        # 遺伝子idのリスト（0以外）
        g_id_list1 = list(self.chrom.chrom_dict.keys())
        g_id_list1.remove(0)
        crosspoint_id1 = np.random.choice(g_id_list1)                

        g_id_list2 = list(partner_chrom.chrom_dict.keys())
        g_id_list2.remove(0)
        crosspoint_id2 = np.random.choice(g_id_list2)
        
        # crosspointより先の部分木を抽出
        gene_subtree1 = {}
        gene_subtree2 = {}        
        self.chrom.get_gene_subtree(g_id=crosspoint_id1, subtree=gene_subtree1)
        partner_chrom.get_gene_subtree(g_id=crosspoint_id2, subtree=gene_subtree2)
        
        # サブツリーの入れ替え
        self.chrom.delete_subtree(crosspoint_id1)
        self.chrom.set_gene_subtree(g_id=crosspoint_id1, subtree=gene_subtree2)
        child1 = Indivisual(self.chrom)

        partner_chrom.delete_subtree(crosspoint_id2)
        partner_chrom.set_gene_subtree(g_id=crosspoint_id2, subtree=gene_subtree1)
        child2 = Indivisual(partner_chrom)
        
        return child1, child2

#%%
    def mutation(self):
        """ 突然変異体　ツリーの一部を別のツリーに置き換える """
        mutant_chrom = Chromosome(is_mutant=True)
        
        mutation_point = np.random.randint(1, self.g_len)
        #mutation_point = 1
        
        # 突然変異の染色体と交叉する
        self.chrom.delete_subtree(mutation_point)
        self.chrom.set_gene_subtree(g_id=mutation_point, subtree=mutant_chrom.chrom_dict)
        mutant = Indivisual(self.chrom)
        
        return mutant
    
    
#%% DEBUG
if __name__ == '__main__':
    dbg_idv = Indivisual()
    dbg_idv.crossover(dbg_idv.chrom)
   