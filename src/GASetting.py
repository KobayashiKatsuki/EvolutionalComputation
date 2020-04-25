# -*- coding: utf-8 -*-
"""
遺伝的アルゴリズムの問題設定クラス
    
"""
from collections import OrderedDict

class GASetting:
    # 何世代ループするか
    GENERATION_LOOP_NUM = 20
    # 1世代を形成する集団のサイズ
    GROUP_SIZE = 10 
    # 交叉確率
    CROSSOVER_PROB = 0.85    
    # 突然変異率(必ず 交叉率 + 突然変異率 < 1 とする)
    MUTATION_PROB = 0.01    
    # 突然変異させる割合（必ず1以上　1だとすべての遺伝子を対立遺伝子に入れ替える）
    MUTATION_RATE = 4
    # 収束判定
    converged_dif = 0.1
    
    # ランキング選択のテーブル
    rank_tbl = []

    """ ナップサック問題固有の設定 """
    """ Ei: アイテム名, (Pi, Ci): (価値, 容量) """   
    capacity = 5 # ナップサックの容量
    item = OrderedDict()
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
    
    """
    #http://ipr20.cs.ehime-u.ac.jp/column/ga/chapter4.html
    capacity = 40
    item = OrderedDict()
    item['E1'] = (21, 2)
    item['E2'] = (22, 10)
    item['E3'] = (28, 7)
    item['E4'] = (21, 2)
    item['E5'] = (12, 4)
    item['E6'] = (24, 9)
    item['E7'] = (15, 10)
    item['E8'] = (2, 7)
    item['E9'] = (25, 8)
    item['E10'] = (28, 5)
    item['E11'] = (4, 3)
    item['E12'] = (22, 10)
    item['E13'] = (36, 9)
    item['E14'] = (2, 8)
    item['E15'] = (7, 8)
    item['E16'] = (40, 5)
    item['E17'] = (14, 7)
    item['E18'] = (40, 3)
    item['E19'] = (33, 9)
    item['E20'] = (21, 7)
    item['E21'] = (28, 2)
    item['E22'] = (22, 10)
    item['E23'] = (14, 7)
    item['E24'] = (36, 9)
    item['E25'] = (28, 7)
    item['E26'] = (21, 2)
    item['E27'] = (18, 10)
    item['E28'] = (12, 4)
    item['E29'] = (24, 9)
    item['E30'] = (15, 10)
    item['E31'] = (21, 4)
    item['E32'] = (2, 7)
    item['E33'] = (25, 8)
    item['E34'] = (28, 5)
    item['E35'] = (28, 2)
    item['E36'] = (4, 3)
    item['E37'] = (22, 10)
    item['E38'] = (36, 9)
    item['E39'] = (31, 7)
    item['E40'] = (2, 8)
    item['E41'] = (7, 8)
    item['E42'] = (40, 5)
    item['E43'] = (14, 7)
    item['E44'] = (4, 5)
    item['E45'] = (28, 7)
    item['E46'] = (40, 3)
    item['E47'] = (33, 9)
    item['E48'] = (35, 7)
    item['E49'] = (21, 7)
    item['E50'] = (20, 9)    
    """
    
    
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
        
        