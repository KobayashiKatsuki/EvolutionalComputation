# -*- coding: utf-8 -*-
"""
遺伝的アルゴリズムの問題設定クラス

解きたい問題に関する設定はすべてここで

"""

import numpy as np
import pandas as pd

class GPSetting:
    # 解きたい問題タイプ　いずれかのコメントアウト外す
    # 何世代ループするか
    GENERATION_LOOP_NUM = 100
    # 1世代を形成する集団のサイズ
    GROUP_SIZE = 100
    # 交叉確率
    CROSSOVER_PROB = 0.30    
    # 突然変異率(必ず 交叉率 + 突然変異率 < 1 とする)
    MUTATION_PROB = 0.1   
    # トーナメントサイズ
    TOURNAMENT_SIZE = 10
    # 収束判定
    converged_dif = 0.1    
    # 遺伝子ツリーの最小/最大深さ
    MIN_DEPTH = 3
    MAX_DEPTH = 8
    # 突然変異で単一ノードにする確率
    MUTANT_SINGLE_NODE_RATE = 0.1
    # 突然変異体の最大深さ
    MAX_MUTANT_DEPTH = 3
    # 収束判定
    converge_counter = 0
    CONVERGE_TH = 10
 
    """
     テストデータセット
     このデータに合わせて計算ツリーを生成する
     値自体は評価で使用 
    """
    df_testdata = pd.read_excel('dataset.xlsx')
    var_list = [col for col in df_testdata.columns.values if col != 'answer']
    testcase = {} # { 0: {x1: 1, x2: 3}, 1: {x1: 5, x2: -2}, ... }    
    testcase_answer = df_testdata['answer'].to_dict() # { 0: 10, 1: 15, 2: 12, ... }    
    
    # 作業用
    testdata_dict = df_testdata.loc[:, [*var_list]].to_dict() 
    for var_name, var_dict in testdata_dict.items():
        for idx, var_value in var_dict.items():
            if idx in testcase.keys():
                testcase[idx][var_name] = var_value
            else:
                tc = {}
                tc[var_name] = var_value
                testcase[idx] = tc    


#%%    
    def __init__(self):
        pass
          
        