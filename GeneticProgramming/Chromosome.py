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
        self.chrom = {}
        self.g_id_list= [0]
        
        # ルートノードは四則演算のいずれか
        g_rn = Gene(g_id=0)
        self.g_len = 1
        self.chrom[g_rn.g_id] = g_rn
        
        # 枝葉を再帰的に追加していく
        self.append_gene(g_parent=g_rn, depth=1)
        # 末端のノードをランダムで変数に置き換える
        
        
        self.gtype = self.get_GType()
        
    def append_gene(self, g_parent:Gene, depth):
        """ 指定した遺伝子に再帰的に遺伝子を追加していく """
        """ g_anc: 追加対象に指定した遺伝子, d: 追加する階層の深さ """
        
        # 右側引数
        self.g_len += 1   
        if depth < GP.MAX_DEPTH: 
            # 最大深さ未満なら乱数か演算子かランダム
            g_child1 = Gene(g_id=self.g_len-1)
        else:
            # 最大深度に到達していれば乱数ノード
            g_child1 = Gene(g_id=self.g_len-1, is_operand=True)

        g_parent.arg1_id = g_child1.g_id
        self.chrom[g_child1.g_id] = g_child1                       
        
        if g_child1.node_type == Gene.NODE_ARITHMETIC:
            # 演算子ノードなら再帰的にオペランドを追加する
            self.append_gene(g_parent=g_child1, depth=depth+1)

                        
        # 左側引数 右とやること同じ
        self.g_len += 1   
        if depth < GP.MAX_DEPTH: 
            g_child2 = Gene(g_id=self.g_len-1)
        else:
            g_child2 = Gene(g_id=self.g_len-1, is_operand=True)            

        g_parent.arg2_id = g_child2.g_id
        self.chrom[g_child2.g_id] = g_child2               
        
        if g_child2.node_type == Gene.NODE_ARITHMETIC:
            self.append_gene(g_parent=g_child2, depth=depth+1)
            
        return
    
    def calc_gene_tree(self, g_id):
        """ 遺伝子ツリーを巡回して計算する """
        g:Gene = self.chrom[g_id]
        ans = 0
        
        if g.node_type == Gene.NODE_ARITHMETIC:
            # 演算子　左右の引数オペランドを取得
            arg1 = self.calc_gene_tree(g_id=g.arg1_id)
            arg2 = self.calc_gene_tree(g_id=g.arg2_id)
            
            if g.g_code == 'add':
                ans = arg1 + arg2
            elif g.g_code == 'sub':
                ans = arg1 - arg2
            elif g.g_code == 'mul':
                ans = arg1 * arg2
            elif g.g_code == 'div':
                if arg2 != 0:
                    ans = arg1 / arg2
                else:
                    ans = 1            
            
        elif g.node_type == Gene.NODE_OPERAND:
            # 実数ノード
            ans = g.g_code
        
        return ans
    
    
    def get_GType(self):
        """ 染色体（遺伝子配列,GType）を数値リストで返す """
        gtype = []
        for g_id, g in self.chrom.items():
            gtype.append((g_id, g.g_code))
        
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