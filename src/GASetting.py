# -*- coding: utf-8 -*-
"""
遺伝的アルゴリズムの問題設定クラス

解きたい問題に関する設定はすべてここで

"""
from collections import OrderedDict
import numpy as np

class GASetting:
    # 解きたい問題タイプ　いずれかのコメントアウト外す
    #PROBLEM_TYPE = 'KNAPSACK'
    PROBLEM_TYPE = 'TSP'
    
    # 何世代ループするか
    GENERATION_LOOP_NUM = 1000
    # 1世代を形成する集団のサイズ
    GROUP_SIZE = 1000 
    # 交叉確率
    CROSSOVER_PROB = 0.9    
    # 突然変異率(必ず 交叉率 + 突然変異率 < 1 とする)
    MUTATION_PROB = 0.2   
    # 突然変異させる割合（必ず1以上　1だとすべての遺伝子を対立遺伝子に入れ替える）
    MUTATION_RATE = 4
    # 収束判定
    converged_dif = 0.1
    # ランキング選択のテーブル
    rank_tbl = []
    # 探索する要素を格納する領域
    item = OrderedDict()
    
    # 問題ごとの設定
    if PROBLEM_TYPE == 'KNAPSACK':
        """ ナップサック問題の設定 """
        """ Ei: アイテム名, (Pi, Ci): (価値, 容量) """   
        capacity = 5 # ナップサックの容量
        item['E1'] = (1.0, 0.9)
        item['E2'] = (1.1, 1.2)
        item['E3'] = (0.8, 0.9)
        item['E4'] = (1.4, 1.5)
        item['E5'] = (0.6, 0.5)
        item['E6'] = (1.3, 0.7)
        item['E7'] = (0.9, 1.2)
        item['E8'] = (0.5, 1.6)
        item['E9'] = (1.2, 1.5)
        item['E10'] = (0.3, 0.1)
        
    elif PROBLEM_TYPE == 'TSP':
        """ 巡回セールスマン問題 """
        """ Ci: 都市名, (Px, Py): (x座標, y座標) """
        capacity = 1 # 便宜的に…
        city_num = 100 # 都市の数
        for i in range(city_num):
            px = np.random.uniform(0, 10)
            py = np.random.uniform(0, 10)
            item[f'C{i+1}'] = (px, py)
        cities = item.keys()
        
#%%    
    def __init__(self):
        pass
    
    def create_ranking_table():
        """ ランキング選択のテーブルを生成する """
        # テーブルは先頭からランキングが高いものとする（先頭は1位、末尾は最下位）
        # 確率は上位10%～30%を高めに設定、30%より下位は同確率とする
        best_size = round(GASetting.GROUP_SIZE * 0.1)
        rank_prob_tbl = [] # 確率テーブル
        for i in range(GASetting.GROUP_SIZE):
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
        for i in range(GASetting.GROUP_SIZE):
            if i > 0:
                GASetting.rank_tbl.append(rank_prob_tbl[i] + GASetting.rank_tbl[i-1])
            else:
                GASetting.rank_tbl.append(rank_prob_tbl[i])
                
        return
        
        