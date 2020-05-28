# -*- coding: utf-8 -*-
"""
個体
Gtypeのバイナリコードと
Ptypeのコドンを持つ

"""

from GESetting import GESetting
from Chromosome import Chromosome
import numpy as np
import copy

class Indivisual:
    
    def __init__(self):
        self.chrom = Chromosome(n_codon=np.random.randint(10, 20))
        self.ge = GESetting()
        self.ptype = self.Ptype_mapping()
        self.isvalid = True
        self.fitness = self.calc_fitness()
    
    def Ptype_mapping(self):
        """ プロダクションルールに則り表現型を得る """
        ptype_arr = [] # 終端記号を格納していく
        
        gramm_list = copy.deepcopy(self.ge.start_grammer)
        wrapping_num = 0       
        locus = 0
        while len(gramm_list) > 0:
            if wrapping_num > self.ge.max_wrapping: # ラッピングが一定数超えたら終了
                self.isvalid = False # 無効個体
                break 
            
            # 現在のgrammリストの先頭からgrammをポップ
            gramm = gramm_list.pop(0)
            if gramm in self.ge.terminal: 
                # 終端記号なら
                ptype_arr.append(gramm)
                
            else:
                codon = self.chrom.d_array[locus]                        
                prod = self.ge.prod_rule[gramm]
                rule = codon % len(prod)
                new_gramm = copy.deepcopy(prod[rule])
                if isinstance(new_gramm, str):
                    gramm_list.insert(0, new_gramm)
                    
                else:
                    new_gramm.extend(gramm_list)
                    gramm_list = new_gramm
            
                # コドンの遺伝子座更新
                locus += 1
                if locus > self.chrom.n_codon-1:
                    locus = 0
                    wrapping_num += 1
                    
                    # ラッピング発生時はルールを変更して収束させる
                    if wrapping_num == self.ge.rule_change_wrapping:
                        prod = self.ge.prod_rule['<expr>']
                        self.ge.prod_rule['<expr>'] = prod[2]

        return ptype_arr
    
    
    def calc_fitness(self):
        """ 適応度計算 """
        # 無効個体は出来損ない
        
        ptype_str = ''.join(self.ptype)
        return ptype_str
    
    def calc_grammer(self, x):
        """ この個体の式を計算する """
        ptype_str = ''.join(self.ptype)
        ans = eval(ptype_str)
        return ans
        
    
                        
    def show_g_code(self):
        """ 個の表現 """
        self.chrom.show_gene()
        
        
#%%
if __name__ == '__main__':
    idv = Indivisual()
    print(idv.ptype)
    print(idv.fitness)
    a = idv.calc_grammer(x=1)
    print(f'ans={a}')
    
    print('fin')
    
        