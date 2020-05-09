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
        self.chrom_dict = {} # 遺伝子IDをキー、遺伝子オブジェクトをバリューとした辞書
        # ルートノード
        g_rn = Gene(g_id=0, node_type=Gene.NODE_ARITHMETIC)
        self.g_len = 1
        self.chrom_dict[g_rn.g_id] = g_rn        
        # 枝葉を再帰的に追加していく
        self.append_gene(g_parent=g_rn, depth=1)
        # Gtypeは遺伝子ID,遺伝子コードのリスト
        self.gtype = self.get_GType()
        
        
    def append_gene(self, g_parent:Gene, depth):
        """ 指定した遺伝子に再帰的に遺伝子を追加していく """
        """ g_anc: 追加対象に指定した遺伝子, d: 追加する階層の深さ """
        
        # 左側引数
        self.g_len += 1           
        if depth < GP.MIN_DEPTH:
            # 最小深さ未満なら演算子
            g_child1 = Gene(g_id=self.g_len-1, node_type=Gene.NODE_ARITHMETIC)        
        elif depth < GP.MAX_DEPTH: 
            # 最大深さ未満ならランダムで演算子かオペランド
            g_child1 = Gene(g_id=self.g_len-1)
        else:
            # 最大深度に到達していればオペランド
            g_child1 = Gene(g_id=self.g_len-1, node_type=Gene.NODE_OPERAND)

        g_parent.arg1_id = g_child1.g_id
        self.chrom_dict[g_child1.g_id] = g_child1                       
        
        if g_child1.node_type == Gene.NODE_ARITHMETIC:
            # 演算子ノードなら再帰的にオペランドを追加する
            self.append_gene(g_parent=g_child1, depth=depth+1)

                        
        # 右側引数 左とやること同じ
        self.g_len += 1   
        if depth < GP.MIN_DEPTH:
            # 最小深さ未満なら演算子
            g_child2 = Gene(g_id=self.g_len-1, node_type=Gene.NODE_ARITHMETIC)        
        elif depth < GP.MAX_DEPTH: 
            g_child2 = Gene(g_id=self.g_len-1)
        else:
            g_child2 = Gene(g_id=self.g_len-1, node_type=Gene.NODE_OPERAND)            

        g_parent.arg2_id = g_child2.g_id
        self.chrom_dict[g_child2.g_id] = g_child2               
        
        if g_child2.node_type == Gene.NODE_ARITHMETIC:
            self.append_gene(g_parent=g_child2, depth=depth+1)
            
        return
    
    def calc_gene_tree(self, g_id, **testcase: dict):
        """ 遺伝子ツリーを巡回して計算する """
        g:Gene = self.chrom_dict[g_id]
        ans = 0
        
        if g.node_type == Gene.NODE_ARITHMETIC:
            # 演算子　左右の引数オペランドを取得
            arg1 = self.calc_gene_tree(g_id=g.arg1_id, **testcase)
            arg2 = self.calc_gene_tree(g_id=g.arg2_id, **testcase)
            
            if g.g_code == 'add':
                ans = arg1 + arg2
            elif g.g_code == 'sub':
                ans = arg1 - arg2
            elif g.g_code == 'mul':
                ans = arg1 * arg2
            elif g.g_code == 'div':
                eps = 1.0e-7 # 0除算は0とする
                ans = arg1 / arg2 if np.abs(arg2) > eps else 0
                
        elif g.node_type == Gene.NODE_OPERAND:
            # オペランドノード
            if g.g_code in testcase.keys():
                ans = testcase[g.g_code]
            else:            
                ans = g.g_code
        
        return ans
    
    
    def get_GType(self):
        """ 染色体（遺伝子ID,遺伝子コードのリスト）を数値リストで返す """
        gtype = []
        for g_id, g in self.chrom_dict.items():
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
    
    def get_gene_subtree(self, g_id, subtree: dict, st_id=0):
        """ 指定した遺伝子IDより先のサブツリーを取得する """
        
        # まず先頭 サブツリーも先頭（ルート）はid0とする
        cur_id = st_id
        subtree[cur_id] = self.chrom_dict[g_id]
        subtree[cur_id].g_id = st_id

        if subtree[cur_id].node_type == Gene.NODE_ARITHMETIC:
            # 演算子ノードなら左右オペランドで再帰的に抽出
            st_arg1_id = st_id+1
            st_id = self.get_gene_subtree(g_id=subtree[cur_id].arg1_id, subtree=subtree, st_id=st_arg1_id)
            subtree[cur_id].arg1_id = st_arg1_id
            
            st_arg2_id = st_id+1
            st_id = self.get_gene_subtree(g_id=subtree[cur_id].arg2_id, subtree=subtree, st_id=st_arg2_id)
            subtree[cur_id].arg2_id = st_arg2_id

        return st_id
            
    def get_allele(self, locus):
        """ 対立遺伝子をひとつ取り出す """
        return None
    
    def set_gene(self, locus, g: Gene):
        """ 染色体に遺伝子をセットする """
        if locus >= 0 and locus < self.g_len:
            self.chrom[locus] = g
            
    def delete_subtree(self, g_id):
        """ 指定した遺伝子idより先のサブツリーを削除する """
        if self.chrom_dict[g_id].node_type == Gene.NODE_ARITHMETIC:
            self.delete_subtree(self.chrom_dict[g_id].arg1_id)
            self.delete_subtree(self.chrom_dict[g_id].arg2_id)

        del self.chrom_dict[g_id]
        self.g_len = self.chrom_dict.__len__()         
        self.gtype = self.get_GType()
                    
    def set_gene_subtree(self, g_id, subtree: dict, st_id=0):
        """ 遺伝子idより先の遺伝子をセットする """
        st_gene = subtree[st_id]
        self.chrom_dict[g_id] = st_gene
        if st_gene.node_type == Gene.NODE_ARITHMETIC:
            pass
            
