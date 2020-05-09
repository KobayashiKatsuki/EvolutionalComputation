# -*- coding: utf-8 -*-
"""
遺伝子クラス
"""
import numpy as np
from GPSetting import GPSetting as GP
import random

class Gene:
    """
    木構造エンコーディング
    遺伝子は木構造におけるノードと引数に当たるエッジ    
    数値データは実数値エンコーディング

    Gene:
        g_id #遺伝子ID ルートは0
        node_type # ノードの種別
        g_code # 遺伝子の値（エンコード）
        arg1_id, arg2_id # ノードが演算子の場合、引数の遺伝子id
    """        
    
    # ノード（遺伝子）の種別
    NODE_OPERAND = 'operand'
    NODE_ARITHMETIC ='arithmetic'
    #NODE_BOOLEAN = 'boolean'
    
    # 対立遺伝子
    allele = {
            NODE_OPERAND: GP.var_list,
            NODE_ARITHMETIC: ['add', 'sub', 'mul', 'div'],
            #NODE_BOOLEAN: ['and', 'or', 'not', 'gt', 'lt', 'eq', 'neq']
            }
    
    def __init__(self, g_id, node_type=None):
        self.g_id = g_id

        if node_type == None:
            # デフォルトならランダムに生成
            select_type = np.random.randint(2)                
            if select_type == 0:
                self.create_operand_node()
            elif select_type == 1:
                self.create_arithmetic_node()
            
        else:
            if node_type == Gene.NODE_OPERAND:
                # オペランド指定ならオペランドノード
                self.create_operand_node()
                
            elif node_type == Gene.NODE_ARITHMETIC:
                # 演算子指定なら演算子ノード
                self.create_arithmetic_node()
    
    def create_operand_node(self):
        """ オペランドノードを作る """        
        self.node_type = Gene.NODE_OPERAND
        is_var = np.random.randint(2) # 実数か変数かは確率1/2
        if is_var == 0:
            self.g_code = np.random.randint(1, 10) # 1～9の整数
        else:
            self.g_code = random.choice(Gene.allele[Gene.NODE_OPERAND]) # 変数名はランダム（抜け漏れ無しは保証できない）
        
    def create_arithmetic_node(self):
        """ 演算子ノードを作る """
        self.node_type = Gene.NODE_ARITHMETIC
        self.g_code = random.choice(Gene.allele[Gene.NODE_ARITHMETIC])
        # 引数としてさらに二つの遺伝子を持つ（g_idで指定する）
        self.arg1_id = None
        self.arg2_id = None
        
    def replace_gene_code(self, new_g_code):
        """ 遺伝子コードを置き換える """
        self.g_code = new_g_code
        
                