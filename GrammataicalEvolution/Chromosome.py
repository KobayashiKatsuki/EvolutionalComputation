# -*- coding: utf-8 -*-
"""
染色体
可変長バイナリコード
= 遺伝子（コドン）数 x 8bit
"""

from Gene import Gene
from GESetting import GESetting
import copy

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

    def show_chrom_code(self):
        """ 染色体の表示 """
        gtype = []
        for codon in self.g_array:
            if codon is not None:
                gtype.append(codon.g_code)
            else:
                gtype.append(None)
                
        #print(gtype)
        print(self.d_array)
        
#%%
    def append_gene(self, gene):
        """ 末尾に遺伝子を追加する """
        self.g_array.append(gene)
        if gene is not None:
            self.d_array.append(gene.d_code)
        else:
            self.d_array.append(None)
            
        self.n_codon += 1
        
        
    def get_gene(self, locus):
        """ 指定位置の遺伝子を返す """
        if locus < 0 and  locus > self.n_codon-1:
            return None        
        else:
            gene = copy.deepcopy(self.g_array[locus])    
            return gene
    
    def set_gene(self, locus, gene: Gene):
        """ 指定位置に遺伝子をセットする """
        if locus < 0 and  locus > self.n_codon-1:
            return     
        else:
            self.g_array[locus] = gene
            if gene is not None:
                self.d_array[locus] = gene.d_code
            else:
                self.d_array[locus] = None
            
            return

    def compress_none(self):
        """ 遺伝子に含まれるNoneを削除し圧縮する """
        self.g_array = [g for g in self.g_array if g is not None]
        self.d_array = [d for d in self.d_array if d is not None]
        self.n_codon = self.g_array.__len__()
        

#%%
if __name__ == '__main__':
    chrom = Chromosome(n_codon=3)
    chrom.show_chrom_code()
    


