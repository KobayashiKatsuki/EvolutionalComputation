# -*- coding: utf-8 -*-
"""
Genetic Programming

遺伝的プログラミング
・遺伝的アルゴリズムによる演算ツリー生成
・木構造エンコーディングにより遺伝子型を表現した
　遺伝的アルゴリズム

ビヘイビアツリー
・エージェントの動作をaction, selector, sequencer, conditionなどを
　各ノードとするツリーで表現したモデル
・入力値に対して条件を満たせば実行しSuccess、満たさなければFailure
　を繰り返していくかんじ
　つまり入力に対する行動のセット（仕様書）が定義されているので
 適応度評価は可能
 　ステップ数を少なくするとか到達できたところまで累積するとか

"""

from GPSetting import GPSetting as GP
from Indivisual import Indivisual
import numpy as np

#%% 
def sort_group_by_fitness(group):
    """
    集団を適応度に応じてソートする
    """
    idv_list = []
    for idv in group:    
        idv_list.append((idv.fitness, idv))
    
    #　個体を適応度の順にソートする
    idv_sorted = sorted(idv_list, key=lambda x:x[0], reverse=True)
    
    # ソート結果に応じて現在の集団（リスト）を生成する
    sorted_group = []
    for (f, idv) in idv_sorted:
        sorted_group.append(idv)
        
    return sorted_group

#%% 
def create_group(show=False):
    """ 
    集団の生成
    """
    group = []
    gene_set = set() # 初期集団は重複した個体が生まれないように集合を利用

    while True:
        idv = Indivisual()        
        before_gene_set_len = gene_set.__len__()        
        gene_set.add(str(idv.gtype))
        if gene_set.__len__() > before_gene_set_len:
            group.append(idv)
        if group.__len__() == GP.GROUP_SIZE:
            break    
    
    if show is True:
        for idv in group:        
            idv.show_indivisual_info()

    return sort_group_by_fitness(group)

#%%
def select_indivisual(group, sel_num=1):
    """ 個体の選択 selection
     ランキング方式を使用する
    """
    selected_idv = []
    selected_flg = [0 for i in range(GP.rank_tbl.__len__())]
    
    # sel_num < len(rank_tbl)個の個体を選択する
    while selected_idv.__len__() < sel_num:
        # 乱数selectionがテーブルのどこに入るか確認
        selection = np.random.uniform(0, 1)
        for i in range(GP.rank_tbl.__len__()):
            if selection < GP.rank_tbl[i]:
                if selected_flg[i] == 0:
                    selected_flg[i] = 1
                    selected_idv.append(group[i])
                    break

    return selected_idv


#%%
def reproduction(current_group):
    """ 選択・交叉・突然変異で次世代を生成する """
    next_group = []
    
    # 個体の遺伝子操作を選択するテーブル（各操作の選択確率で生成した累積度数分布）
    operation_tbl = [GP.CROSSOVER_PROB, 
                     GP.MUTATION_PROB + GP.CROSSOVER_PROB,
                     1.0]
    
    while next_group.__len__() < GP.GROUP_SIZE:
        # オペレーションの選択
        op = np.random.uniform(0, 1)        
        if op < operation_tbl[0]:
            # 交叉 個体を2つ選択する
            sel_idv = select_indivisual(current_group, sel_num=2)
            
            # 交差前
            #sel_idv[0].visualize_indivisual()
            #sel_idv[1].visualize_indivisual()
            
            child_idv1, child_idv2 = sel_idv[0].crossover(sel_idv[1].chrom)
                        
            # 交叉によって生まれた個体
            child_idv1.visualize_indivisual()
            #child_idv2.visualize_indivisual()
            

            next_group.append(child_idv1)
            if next_group.__len__() < GP.GROUP_SIZE:
                next_group.append(child_idv2)

        """
        elif op < operation_tbl[1]:
            # 突然変異
            sel_idv = select_indivisual(current_group)
            mutant = sel_idv[0].mutation()
            next_group.append(mutant)

        else:
            # 再生 次世代にそのままコピー
            sel_idv = select_indivisual(current_group)            
            next_group.append(sel_idv[0])
        """
        
    return sort_group_by_fitness(next_group)


#%%
    
if __name__ == '__main__':
    # 初期設定
    GP.create_ranking_table()
    
    # 初期集団を生成する
    current_group = create_group()            
    # 現世代で最も優れた個体
    most_valuable_idv = current_group[0] # 初期値は現世代の先頭
    #most_valuable_idv.visualize_indivisual()
    
    # 世代交代ループ    
    for generation in range(1, GP.GENERATION_LOOP_NUM+1):
        print(f'===== Generation No.{generation} =====')
                
        # 選択（淘汰）・交叉・突然変異による次世代の生成
        next_group = reproduction(current_group)
                        
        # 世代交代して次のループ
        current_group.clear()
        current_group.extend(next_group)


    
    # 最強個体（遺伝子計算ツリーグラフ）可視化
    #most_valuable_idv.visualize_indivisual()

    print('finish')