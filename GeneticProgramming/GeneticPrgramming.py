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
def reproduction(current_group):
    
    return current_group

#%%
    
if __name__ == '__main__':
    # 初期設定
    GP.create_ranking_table()
    
    # 初期集団を生成する
    current_group = create_group()        
    
    # 個体（遺伝子計算ツリーグラフ）可視化
    current_group[0].visualize_indivisual()
    print(f'fitness: {current_group[0].fitness}')
    
    """
    
    # 現世代で最も優れた個体
    most_valuable_idv = Indivisual() # 初期値はランダム
    # 適応度の変化をグラフ化するためのデータ格納領域
    optimum_fitness_list = []
    optimum_fitness_list.append(0)
    mean_fitness_list = []
    mean_fitness_list.append(0)
    
    # 各世代での歴代最適個体
    mvp_for_each_generation = []
    
    # 世代交代ループ    
    for generation in range(1, GP.GENERATION_LOOP_NUM+1):
        print(f'===== Generation No.{generation} =====')

        # 選択（淘汰）・交叉・突然変異による次世代の生成
        next_group = reproduction(current_group)
        
                
        # 世代交代して次のループ
        current_group.clear()
        current_group.extend(next_group)

    """
    print('finish')