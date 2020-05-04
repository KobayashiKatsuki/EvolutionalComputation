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
    GENERATION_LOOP_NUM = 1
    # 1世代を形成する集団のサイズ
    GROUP_SIZE = 2
    # 交叉確率
    CROSSOVER_PROB = 0.8    
    # 突然変異率(必ず 交叉率 + 突然変異率 < 1 とする)
    MUTATION_PROB = 0.15   
    # 収束判定
    converged_dif = 0.1
    # 遺伝子数（ツリーのノード数）の上限
    MAX_NODE_NUM = 100
    # 最大深さ
    MAX_DEPTH = 5 
    
    # ランキング選択のテーブル
    rank_tbl = []
 
    """
     テストデータセット
     このデータに合わせて計算ツリーを生成する
     値自体は評価で使用 
    """
    df_testdata = pd.read_excel('dataset.xlsx')
    var_list = [col for col in df_testdata.columns.values if col != 'answer']
        
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
        
        