# -*- coding: utf-8 -*-
"""
Grammatical Evolution

"""

from GESetting import GESetting as GE
from Indivisual import Indivisual
import random
import numpy as np
import pandas as pd
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as anm
from matplotlib.animation import PillowWriter
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']


#%% 
def sort_population_by_fitness(population):
    """
    集団を適応度に応じてソートする
    """
    idv_list = []
    for idv in population:    
        idv_list.append((idv.fitness, idv))
    
    #　個体を適応度の順にソートする
    idv_sorted = sorted(idv_list, key=lambda x:x[0], reverse=True)
    
    # ソート結果に応じて現在の集団（リスト）を生成する
    sorted_population = []
    for (f, idv) in idv_sorted:
        sorted_population.append(idv)
        
    return sorted_population


#%% 
def create_population(show=False):
    """ 
    集団の生成
    """
    population = []
    gene_set = set() # 初期集団は重複した個体が生まれないように集合を利用

    while True:
        idv = Indivisual()        
        before_gene_set_len = gene_set.__len__()        
        gene_set.add(str(idv.gtype))
        if gene_set.__len__() > before_gene_set_len:
            population.append(idv)
        if population.__len__() == GE.POPULATION_SIZE:
            break    
    
    if show is True:
        for idv in population:        
            idv.show_chrom_info()

    return sort_population_by_fitness(population)


#%%
def select_indivisual(population, sel_num=1):
    """ 個体の選択 selection
     トーナメント方式を使用する
    """
    selected_idv = []
    
    while selected_idv.__len__() < sel_num:
       # トーナメントサイズの分ランダムに集団から取得
        tornament_idvs = random.sample(population, GE.TOURNAMENT_SIZE)
        # 最大個体を取得
        sorted_tornament_idvs = sort_population_by_fitness(tornament_idvs)
        selected_idv.append(sorted_tornament_idvs[0])

    return selected_idv


#%%
def reproduction(cur_pop):
    """ 選択・交叉・突然変異で次世代を生成する """
    next_pop = []
    
    # 個体の遺伝子操作を選択するテーブル（各操作の選択確率で生成した累積度数分布）
    operation_tbl = [GE.CROSSOVER_PROB, 
                     GE.MUTATION_PROB + GE.CROSSOVER_PROB,
                     1.0]
    
    while next_pop.__len__() < GE.POPULATION_SIZE:
        # オペレーションの選択
        op = np.random.uniform(0, 1)        
        if op < operation_tbl[0]:
            # 交叉 個体を2つ選択する
            sel_idv = select_indivisual(cur_pop, sel_num=2)
            child_idv1, child_idv2 = sel_idv[0].crossover(sel_idv[1].chrom)

            next_pop.append(child_idv1)
            if next_pop.__len__() < GE.POPULATION_SIZE:
                next_pop.append(child_idv2)
        
        elif op < operation_tbl[1]:
            # 突然変異
            sel_idv = select_indivisual(cur_pop)
            mutant = sel_idv[0].mutation()
            next_pop.append(mutant)
            
        else:
            # 再生 次世代にそのままコピー
            sel_idv = select_indivisual(cur_pop)            
            next_pop.append(sel_idv[0])
    
    return sort_population_by_fitness(next_pop)


#%% 収束判定
def is_converged(current_group, next_group):
    """
    集団全体の平均適応度増加率が一定期間一定値以下なら収束
    """
    converged = False
    
    # み じ っ そ う
    
    """
    # 現世代のmvpの適応度
    current_fitness = current_group[0].fitness
    # 次世代のmvpの適応度
    next_fitness = next_group[0].fitness
    
    # 誤差が10000分の1以下が一定世代以上続けば収束
    diff = np.abs(current_fitness - next_fitness)
    if diff < 0.0001:
        GA.converge_counter += 1
    else:
        GA.converge_counter = 0
        
    if GA.converge_counter > GA.CONVERGE_TH-1:
        converged = True
    """
    
    return converged


#%%
# Grammatical Evolution　メイン処理
#
if __name__ == '__main__':    
    # GE設定クラスオブジェクト
    ge = GE()
    # 初期集団
    cur_pop = create_population()

    # 各世代での歴代最適個体
    mvp_for_each_generation = []
    mvp_fitness = []    
    
    # 最初の
    prim = copy.deepcopy(cur_pop[0])
    
    # 世代交代ループ    
    for generation in range(1, GE.GENERATION_LOOP_NUM+1):
        print(f'===== Generation No.{generation} =====')
        
        # そのGenerationでの最強個体
        mvp = cur_pop[0]
        mvp_for_each_generation.append(mvp)
        
        mvp_fitness.append(mvp.fitness)
        
        # 選択（淘汰）・交叉・突然変異による次世代の生成
        next_pop = reproduction(cur_pop)
                
        # 収束判定
        """
        if is_converged(current_group, next_group) is True:
            most_valuable_idv = next_group[0]
            mvp_for_each_generation.append(most_valuable_idv)
            break
        """
        
        # 世代交代して次のループ
        cur_pop.clear()
        cur_pop.extend(next_pop)


    # 最強個体
    mvp = next_pop[0]
    
    # 比較
    print(prim.formula)
    print('↓')
    print(mvp.formula)

    generation_label = [i for i in range(GE.GENERATION_LOOP_NUM)]
    plt.plot(generation_label, mvp_fitness, marker='o', color='red', markersize=3)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()    

    print('finish')
    
    
    
    
    
    