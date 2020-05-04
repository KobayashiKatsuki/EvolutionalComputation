# -*- coding: utf-8 -*-
"""
遺伝子クラス
"""
import numpy as np
import GPSetting as GP
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
            NODE_OPERAND: GP.GPSetting.var_list,
            NODE_ARITHMETIC: ['add', 'sub', 'mul', 'div'],
            #NODE_BOOLEAN: ['and', 'or', 'not', 'gt', 'lt', 'eq', 'neq']
            }
    
    def __init__(self, g_id=None, is_operand=False):
        self.g_id = g_id
        # g_id=0はルートノードを表す。必ずオペランド以外
        if self.g_id == 0:
            self.create_arithmetic_node()
        
        else:        
            # オペランドと指定なら乱数ノード
            if is_operand is True:
                self.create_random_node()
                
            else:
                # ランダムに生成
                select_type = np.random.randint(2)                
                if select_type == 0:
                    self.create_random_node()

                elif select_type == 1:
                    self.create_arithmetic_node()
        
    def create_random_node(self):
        """ 乱数ノードを作る """
        self.node_type = Gene.NODE_OPERAND
        self.g_code = np.random.uniform(-10, 10)
        
    def create_arithmetic_node(self):
        """ 演算子ノードを作る """
        self.node_type = Gene.NODE_ARITHMETIC
        self.g_code = random.choice(Gene.allele[Gene.NODE_ARITHMETIC])
        # 引数としてさらに二つの遺伝子を持つ（g_idで指定する）
        self.arg1_id = None
        self.arg2_id = None
        
                