# -*- coding: utf-8 -*-
"""
個体
Gtypeのバイナリコードと
Ptypeのコドンを持つ

"""

from GESetting import GESetting
from Gene import Gene
from Chromosome import Chromosome
import numpy as np
import copy

class Indivisual:
    
    def __init__(self, init_chrom=None):
        self.ge = GESetting()
        
        if init_chrom is None:
            self.chrom = Chromosome(n_codon=np.random.randint(self.ge.MIN_CODON_LEN, self.ge.MAX_CODON_LEN))
        else:
            self.chrom = copy.deepcopy(init_chrom)
            
        self.gtype = self.Gtype_array()
        self.ptype = self.Ptype_mapping()
        self.isvalid = True
        self.fitness = self.calc_fitness()
        self.formula = ''.join(self.ptype)

#%%
    def Gtype_array(self):
        """ 8ビットコドン（バイナリコード）をひとつの配列に展開 """
        gtype_arr = []
        for codon in self.chrom.g_array:
            gtype_arr.extend(codon.g_code)

        return gtype_arr
   
    
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
        if self.isvalid == False:
            # 無効個体は負数
            return -1

        else:        
            total_err = 0
            for tc_idx, tc in self.ge.testcase.items():
                # 個体のBNFによる計算結果
                idv_ans = self.calc_grammatical_formula(x=tc['x'])  
                # 正解データ
                train_ans = self.ge.testcase_answer[tc_idx]
                
                # 絶対誤差の平均を加算
                mean_err = np.abs(train_ans - idv_ans) / self.ge.testcase.__len__()
                total_err += mean_err
                # 誤差が一定値超えたら頭打ち
                if total_err > 1.0e7:
                    break
            
            # 誤差平均の逆数 誤差10000分の1以下は正解として打ち切り
            eps = 0.0001 # 1.0e-7
            f_val = 1 / total_err if total_err > eps else 10000

            return f_val

        
    def calc_grammatical_formula(self, x):
        """ この個体の式を計算する """
        ptype_str = ''.join(self.ptype)
        ans = eval(ptype_str)
        return ans
        
                        
    def show_chrom_info(self):
        """ 個体の染色体情報 """
        self.chrom.show_chrom_code()
        
        
#%%
    def crossover(self, partner_chrom: Chromosome):
        """ 
         交叉 他の個体のG-typeとランダムで遺伝子を交換する        
        """        
        child1_chrom = copy.deepcopy(self.chrom)        
        child2_chrom = copy.deepcopy(partner_chrom)

        # 一様交叉
        """
        イメージ (a～hはコドン)        
        ch1 = [a, b, c,  ,  ]
        ch2 = [d, e, f, g, h]
        ↓
        ch1 = [a, e, c, g,  ]
        ch2 = [d, b, f,  , h]       
        """        
        if child1_chrom.n_codon > child2_chrom.n_codon:
            for i in range(child1_chrom.n_codon - child2_chrom.n_codon):
                child2_chrom.append_gene(None)
        elif child2_chrom.n_codon > child1_chrom.n_codon:
            for i in range(child2_chrom.n_codon - child1_chrom.n_codon):
                child1_chrom.append_gene(None)
        
        # コドンを交叉で入れ替える　長さが違う場合はNoneと入れ替える（無を取得）
        for locus in range(child1_chrom.n_codon):
            p1_g = child1_chrom.get_gene(locus)
            p2_g = child2_chrom.get_gene(locus)             
            is_cross = np.random.randint(2)
            if is_cross == 1:
                child1_chrom.set_gene(locus, p2_g)
                child2_chrom.set_gene(locus, p1_g)
            else:
                child1_chrom.set_gene(locus, p1_g)
                child2_chrom.set_gene(locus, p2_g)
 
        child1_chrom.compress_none()
        child2_chrom.compress_none()
        
        child1 = Indivisual(child1_chrom)
        child2 = Indivisual(child2_chrom)        
        
        return child1, child2
    

#%%
    def mutation(self):
        """ 突然変異体を生成する """
        
        # 少なくともひとつの遺伝子座の遺伝子を一定確率でランダムに置き換える
        mutant_flg = False
        while mutant_flg is False:            
            mutant_chrom = Chromosome(self.chrom.n_codon)            
            for locus in range(self.chrom.n_codon):
                orig_g = self.chrom.get_gene(locus)
            
                is_mutation = np.random.randint(self.ge.MUTATION_RATE)                
                if is_mutation == 0:
                    mutant_flg = True
                else:
                    mutant_chrom.set_gene(locus, orig_g)

        mutant = Indivisual(mutant_chrom)        
        return mutant
        
        
#%%
if __name__ == '__main__':
    ch = Chromosome(n_codon=4)
    idv = Indivisual(ch)
    idv.show_chrom_info()

    """
    ch2 = Chromosome(n_codon=8)
    idv2 = Indivisual(ch2)
    idv2.show_chrom_info()
    """
    
    print('-----')
    
    """
    print(idv.ptype)
    print(idv.fitness)
    #a = idv.calc_grammatical_formula(x=1)
    #print(f'ans={a}')
    """
    
    #idv.crossover(idv2.chrom)
    mutant = idv.mutation()
    mutant.show_chrom_info()
    
    print('fin')
    
        