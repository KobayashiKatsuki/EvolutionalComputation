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
import copy
from GPSetting import GPSetting as GP

class Chromosome:
    
    def __init__(self, is_mutant=False):
        self.chrom_dict = {} # 遺伝子IDをキー、遺伝子オブジェクトをバリューとした辞書
        # ルートノード
        g_rn = Gene(g_id=0, node_type=Gene.NODE_ARITHMETIC)
        self.g_len = 1
        self.chrom_dict[g_rn.g_id] = g_rn        
        # 枝葉を再帰的に追加していく
        self.append_gene(g_parent=g_rn, depth=1, is_mutant=is_mutant)
        # Gtypeは遺伝子ID,遺伝子コードのリスト
        self.gtype = self.get_GType()
        
    def reset_chrom_info(self):
        """ 染色体情報をリセット """
        self.g_len = self.chrom_dict.__len__()
        self.gtype = self.get_GType()
        
        
    def append_gene(self, g_parent:Gene, depth, is_mutant=False):
        """ 指定した遺伝子に再帰的に遺伝子を追加していく """
        """ g_anc: 追加対象に指定した遺伝子, d: 追加する階層の深さ """
        
        # 左側引数
        self.g_len += 1           
        if depth < GP.MIN_DEPTH:
            # 最小深さ未満なら演算子
            g_child1 = Gene(g_id=self.g_len-1, node_type=Gene.NODE_ARITHMETIC)        
        elif depth < GP.MAX_DEPTH if is_mutant is True else GP.MAX_MUTANT_DEPTH: 
            # 最大深さ未満ならランダムで演算子かオペランド
            g_child1 = Gene(g_id=self.g_len-1)
        else:
            # 最大深度に到達していればオペランド
            g_child1 = Gene(g_id=self.g_len-1, node_type=Gene.NODE_OPERAND)

        g_parent.arg1_id = g_child1.g_id
        self.chrom_dict[g_child1.g_id] = g_child1                       
        
        if g_child1.node_type == Gene.NODE_ARITHMETIC:
            # 演算子ノードなら再帰的にオペランドを追加する
            self.append_gene(g_parent=g_child1, depth=depth+1, is_mutant=is_mutant)

                        
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
            self.append_gene(g_parent=g_child2, depth=depth+1, is_mutant=is_mutant)
            
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
        try:
            # サブツリーの先頭（ルート）もid0とする
            cur_id = st_id
            subtree[cur_id] = copy.deepcopy(self.chrom_dict[g_id])
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
        
        except:
            return None
        
        
    def get_allele(self, locus):
        """ 対立遺伝子をひとつ取り出す """
        return None
    
    def set_gene(self, locus, g: Gene):
        """ 染色体に遺伝子をセットする """
        if locus >= 0 and locus < self.g_len:
            self.chrom[locus] = g
            
            
    def delete_subtree(self, g_id):
        """ 指定した遺伝子idより先のサブツリーを削除する """
        try:
            if self.chrom_dict[g_id].node_type == Gene.NODE_ARITHMETIC:                
                arg1_id = self.chrom_dict[g_id].arg1_id
                arg2_id = self.chrom_dict[g_id].arg2_id                
                self.delete_subtree(g_id=arg1_id)                
                self.delete_subtree(g_id=arg2_id)

            # deleteする
            del self.chrom_dict[g_id]
            
        except:
            return None
                    
        
    def set_gene_subtree(self, g_id, subtree: dict, st_id=0):
        """ 遺伝子idより先の遺伝子をセットする """
        try:
            st_gene = subtree[st_id]
            if st_id > 0:
                # 接続する位置のidはg_lenで降り直し
                g_id = st_id + self.g_len              
            self.chrom_dict[g_id] = st_gene
            
            if self.chrom_dict[g_id].node_type == Gene.NODE_ARITHMETIC:
                sub_arg1_id = st_gene.arg1_id + self.g_len
                self.set_gene_subtree(g_id=sub_arg1_id, subtree=subtree, st_id=st_gene.arg1_id)
                self.chrom_dict[g_id].arg1_id = sub_arg1_id 
                
                sub_arg2_id = st_gene.arg2_id + self.g_len
                self.set_gene_subtree(g_id=sub_arg2_id, subtree=subtree, st_id=st_gene.arg2_id)
                self.chrom_dict[g_id].arg2_id = sub_arg2_id            

        except:
            return None
    
    def copy_gene_tree(self, g_id, src_tree: dict, s_id=0):
        """ 遺伝子ツリーを染色体にコピーしていく """
        cur_id = g_id
        self.chrom_dict[cur_id] = copy.deepcopy(src_tree[s_id])
        self.chrom_dict[cur_id].g_id = g_id
        
        if self.chrom_dict[cur_id].node_type == Gene.NODE_ARITHMETIC:            
            g_arg1_id = g_id+1
            g_id = self.copy_gene_tree(g_id=g_arg1_id, src_tree=src_tree, s_id=src_tree[s_id].arg1_id)
            self.chrom_dict[cur_id].arg1_id = g_arg1_id
            
            g_arg2_id = g_id+1
            g_id = self.copy_gene_tree(g_id=g_arg2_id, src_tree=src_tree, s_id=src_tree[s_id].arg2_id)
            self.chrom_dict[cur_id].arg2_id = g_arg2_id
                
        return g_id

#%% 
if __name__ == '__main__':
    dbg_chrom = Chromosome()
    subtree={}
    dbg_chrom.get_gene_subtree(0, subtree)        
            