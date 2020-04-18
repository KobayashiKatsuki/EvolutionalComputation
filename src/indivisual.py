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
import GASetting as GA

#%%
class indivisual:    
    # 問題設定
    ga_setting = GA.GASetting()
    # 遺伝的アルゴリズムの個体共通のパラメータ
    g_len = ga_setting.item.__len__()
    locus2elem = []
    for k in ga_setting.item.keys():
        locus2elem.append(k)

    def __init__(self):
        # この個体が持つ染色体
        self.chrom = chromosome.chromosome(indivisual.g_len)
        # 遺伝子型(genotype)　遺伝子長は個体（解きたい問題）により異なる
        self.gtype = self.chrom.get_gtype()         
        # 表現型（phenotype）
        self.ptype = self.decoder()
        
    def show_indivisual_info(self):
        """ 個体情報を表示する """        
        # 染色体情報
        print(f'g_len: {indivisual.g_len} {self.gtype} {self.ptype}')
        # 適応度
        f, c = self.fitness()
        print(f'fitness: {f:.1f}, capacity: {c:.1f}')
    
    def get_PType(self):
        """ 個体のPtype（表出している特徴、見た目、つまり解候補）を取得する """
        return self.ptype
    
    def fitness(self):
        """ 個体の適応度 """
        f_val = 0
        c_val = 0
        for locus in range(self.g_len):
            if self.gtype[locus]==1:
                elem = indivisual.locus2elem[locus]
                f_val += indivisual.ga_setting.item[elem][0]
                c_val += indivisual.ga_setting.item[elem][1]
                
        return f_val, c_val
    
#%% エンコーダ・デコーダ　実際に最適化問題を設計するときはここの実装を頑張る
    def decoder(self):
        """
        デコーダ　Gtype -> Ptpye の変換
        """
        ptype_array = []        
        for locus in range(self.g_len):
            if self.gtype[locus] == 1:
                ptype_array.append(indivisual.locus2elem[locus])
                
        return ptype_array


    def encoder(self):
        """
        エンコーダー Ptype -> Gtypeの変換
        実質使わない？（外側から遺伝子操作することは無い？）
        """
        pass