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
    MUTATION_PROB = 0.15   
    # 収束判定
    converged_dif = 0.1    
    # 遺伝子ツリーの最小/最大深さ
    MIN_DEPTH = 3
    MAX_DEPTH = 8
    # 突然変異で単一ノードにする確率
    MUTANT_SINGLE_NODE_RATE = 0.1
    # 突然変異体の最大深さ
    MAX_MUTANT_DEPTH = 4
    # 収束判定
    converge_counter = 0
    CONVERGE_TH = 10
    
    # ランキング選択のテーブル
    rank_tbl = []
 
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
    
    def create_ranking_table():
        """ ランキング選択のテーブルを生成する """
        # テーブルは先頭からランキングが高いものとする（先頭は1位、末尾は最下位）
        # 確率は上位10%～30%を高めに設定、30%より下位は同確率とする
        best_size = round(GPSetting.GROUP_SIZE * 0.1)
        rank_prob_tbl = [] # 確率テーブル
        for i in range(GPSetting.GROUP_SIZE):
            if i < best_size*3:
                if i < best_size*2:
                    if i < best_size:
                        # 上位10%
                        rank_prob_tbl.append(12)
                    else:
                        # 上位20%
                        rank_prob_tbl.append(8)
                else:
                    # 上位30%
                    rank_prob_tbl.append(5)
            else:
                # 30%より下位
                rank_prob_tbl.append(1)
        
        # テーブルの各要素を合計で割って確率にする
        sum_of_tbl = sum(rank_prob_tbl)
        rank_prob_tbl = [x/sum_of_tbl for x in rank_prob_tbl]
        # 累積度数分布に変換する
        for i in range(GPSetting.GROUP_SIZE):
            if i > 0:
                GPSetting.rank_tbl.append(rank_prob_tbl[i] + GPSetting.rank_tbl[i-1])
            else:
                GPSetting.rank_tbl.append(rank_prob_tbl[i])
                
        return
        
        