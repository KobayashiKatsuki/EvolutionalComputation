# -*- coding: utf-8 -*-
"""
染色体クラス
・染色体：　遺伝子で構成するツリー
　‐遺伝子長(g_len)：　遺伝子の数
　‐遺伝子座(locus)：　染色体上における各遺伝子の位置
　‐遺伝子型（GType）：　染色体を表す記号列、内部表現
　‐表現型（PType）：　染色体から個体として発現する外部表現
 
  どの遺伝子を用いるかは問題設定次第 
 
"""

from Gene import Gene
import numpy as np
from GPSetting import GPSetting as GP

class Chromosome:
    
    def __init__(self):
        self.chrom = []
        self.g_id_list= [0]
        
        # ルートは四則演算のいずれか
        g_root = Gene(0)
        self.g_len = 1
        self.chrom.append(g_root)
        
        # 枝葉を再帰的に追加していく
        self.append_gene(g_parent=g_root, depth=1)
        
        # 末端のノードをランダムで変数に置き換える
        
        
        
    def append_gene(self, g_parent: Gene =g_parent, depth=d):
        """ 指定した遺伝子に再帰的に遺伝子を追加していく """
        """ g_anc: 追加対象に指定した遺伝子, d: 追加する階層の深さ """
        
        if g_parent.node_type == Gene.NODE_ARITHMETIC:
            # 四則演算のときのみ実行        

            # 右側引数
            self.g_len += 1   
            g_child1 = Gene(self.g_len-1)
            g_parent.arg1_id = g_child1.g_id
            self.chrom.append(g_child1)       
            
            if g_child1.node_type == Gene.NODE_ARITHMETIC:
                self.append_gene(g_parent=g_child1, depth=d+1)
                
            # 左側引数
            self.g_len += 1   
            g_child2 = Gene(self.g_len-1)
            g_parent.arg2_id = g_child2.g_id
            self.chrom.append(g_child2)               
            
            
            
            if g_child2.node_type == Gene.NODE_ARITHMETIC:
                self.append_gene(g_parent=g_child2, depth=d+1)

            if d < GP.MAX_DEPTH:
                # 最大深さ未満ならランダム
                                
            else:
                # 乱数ノードのみ
                self.g_len += 1
                g_child = Gene(self.g_len-1, is_operand=True)
                
        return
    
    
    def get_GType(self):
        """ 染色体（遺伝子配列,GType）を数値リストで返す """
        gtype = []
        for locus in range(self.g_len):
            g = self.chrom[locus]
            gtype.append(g.g_code)
        
        return gtype
    
    def get_gene(self, locus):
        """ 遺伝子をひとつ取り出す """
        if locus >= 0 and locus < self.g_len:
            return self.chrom[locus]
        else:
            return None
        
    def get_gene_by_code(self, code):
        """ 遺伝子を遺伝子コードから検索して取り出す """
        """ 重複する対立遺伝子を持たない染色体でのみ有効（順列エンコーディングなど） """
        for g in self.chrom:
            if code == g.g_code:
                return g
        return None
    
    def set_gene(self, locus, g: Gene):
        """ 染色体に遺伝子をセットする """
        if locus >= 0 and locus < self.g_len:
            self.chrom[locus] = g
    
    def get_allele(self, locus):
        """ 対立遺伝子をひとつ取り出す """
        return None