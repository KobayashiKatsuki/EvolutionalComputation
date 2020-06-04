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

必要なライブラリ(含むGA)
pillow -> pip install pillow
Graphviz ->インストールしてパス通す　そのあと pip install graphviz
dtreeviz -> pip install dtreeviz

"""

from GPSetting import GPSetting as GP
from Indivisual import Indivisual
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as anm
from matplotlib.animation import PillowWriter


#%% 
def sort_group_by_fitness(group):
    """
    集団を適応度に応じてソートする
    """
    idv_list = []
    for idv in group:    
        idv_list.append((idv.fitness, idv))
    
    #　個体を適応度の順にソートする
    # 今回は適応度が小さいほど優良（誤差が小さい）
    idv_sorted = sorted(idv_list, key=lambda x:x[0], reverse=False)
    
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
    
    while selected_idv.__len__() < sel_num:
       # トーナメントサイズの分ランダムに集団から取得
        tornament_idvs = random.sample(group, GP.TOURNAMENT_SIZE)
        # 最大個体を取得
        sorted_tornament_idvs = sort_group_by_fitness(tornament_idvs)
        selected_idv.append(sorted_tornament_idvs[0])

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
            #child_idv1.visualize_indivisual()
            #child_idv2.visualize_indivisual()            

            next_group.append(child_idv1)
            if next_group.__len__() < GP.GROUP_SIZE:
                next_group.append(child_idv2)

        elif op < operation_tbl[1]:
            # 突然変異
            sel_idv = select_indivisual(current_group)            
            # 変異前
            #sel_idv[0].visualize_indivisual()
            mutant = sel_idv[0].mutation()            
            # 変異後
            #mutant.visualize_indivisual()
            
            next_group.append(mutant)

        else:
            # 再生 次世代にそのままコピー
            sel_idv = select_indivisual(current_group)            
            next_group.append(sel_idv[0])
            
        
    return sort_group_by_fitness(next_group)


#%% 収束判定
def is_converged(current_group, next_group):
    """
    集団全体の平均適応度増加率が一定期間一定値以下なら収束
    """
    converged = False
    
    # 現世代のmvpの適応度
    current_fitness = current_group[0].fitness
    # 次世代のmvpの適応度
    next_fitness = next_group[0].fitness
    
    # 誤差が10000分の1以下が一定世代以上続けば収束
    diff = np.abs(current_fitness - next_fitness)
    if diff < 0.0001:
        GP.converge_counter += 1
    else:
        GP.converge_counter = 0
        
    if GP.converge_counter > GP.CONVERGE_TH-1:
        converged = True
    
    return converged

#%% 遺伝的プログラミングメイン処理
    
if __name__ == '__main__':
    # 初期集団を生成する
    current_group = create_group()            
    # 現世代で最も優れた個体
    most_valuable_idv = current_group[0] # 初期値は現世代の先頭
    #most_valuable_idv.visualize_indivisual()

    # 各世代での歴代最適個体
    mvp_for_each_generation = []
    
    # 世代交代ループ    
    for generation in range(1, GP.GENERATION_LOOP_NUM+1):
        print(f'===== Generation No.{generation} =====')
        
        # そのGenerationでの最強個体
        most_valuable_idv = current_group[0]
        mvp_for_each_generation.append(most_valuable_idv)
        
        # 選択（淘汰）・交叉・突然変異による次世代の生成
        next_group = reproduction(current_group)
                
        # 収束判定
        """
        if is_converged(current_group, next_group) is True:
            most_valuable_idv = next_group[0]
            mvp_for_each_generation.append(most_valuable_idv)
            break
        """
        
        # 世代交代して次のループ
        current_group.clear()
        current_group.extend(next_group)


    
    # 最強個体（遺伝子計算ツリーグラフ）可視化
    #most_valuable_idv.show_indivisual_info()
    most_valuable_idv.fitness
    most_valuable_idv.visualize_indivisual()

    print('finish')
    
    
    # fitnessの変化
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)  
    generation_label = [i for i in range(len(mvp_for_each_generation))]
    fitness_list = []
    for idv in mvp_for_each_generation:
        fitness_list.append(idv.fitness)

    plt.plot(generation_label, fitness_list, marker='o', color='red', markersize=3)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()    

    