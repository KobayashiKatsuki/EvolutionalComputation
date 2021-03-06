# -*- coding: utf-8 -*-
"""
遺伝的アルゴリズム　Genetic Algorithm

【用語の定義】

・遺伝子：　個体を形成する最小構成要素
　‐対立遺伝子：　遺伝子がとりうる値
 　（バイナリエンコーディングなら0, 1の2値）

・染色体：　遺伝子の並びで定義される個体情報
　‐遺伝子長：　染色体（配列）の長さn
　‐遺伝子座：　染色体上における各遺伝子の位置
　‐遺伝子型（GType）：　染色体を表す記号列、内部表現
　‐表現型（PType）：　染色体から個体として発現する外部表現

・個体：　1つまたは複数の染色体から生成される実体
　　　　　最適化問題の解とは最適な個体として表現される
 ★個体をどう設計するか（解くべき問題にGEをどう適用するか）が
 　遺伝的アルゴリズムでは要となる

・集団：　様々な個体の集まり　この中の個体が解空間を探索する

・エンコーディング：　表現型から遺伝子型への変換（符号化）
・デコーディング：　遺伝子型から表現型への変換（複合化）

"""
from indivisual import Indivisual
from GASetting import GASetting as GA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as anm
from matplotlib.animation import PillowWriter

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

#%% 
def sort_group_by_fitness(group):
    """
    集団を適応度に応じてソートする
    """
    good_group = []
    bad_group = []
    for idv in group:    
        if idv.capacity > GA.capacity:
            # 上回るものは問答無用で出来損ない
            bad_group.append((idv.fitness, idv))
        else:
            # cが最大容量を下回るものは良い個体            
            good_group.append((idv.fitness, idv))
    
    #　個体を優秀な順にソートする
    good_sorted = sorted(good_group, key=lambda x:x[0], reverse=True)
    bad_sorted = sorted(bad_group, key=lambda x:x[0]) # badはfが小さいほど良いとする
    
    # ソート結果に応じて現在の集団（リスト）を生成する
    sorted_group = []
    for (f, idv) in good_sorted:
        sorted_group.append(idv)
    for (f, idv) in bad_sorted:
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
        if group.__len__() == GA.GROUP_SIZE:
            break    
    
    if show is True:
        for idv in group:        
            idv.show_indivisual_info()

    return sort_group_by_fitness(group)



#%%
def select_indivisual(group, sel_num=1):
    """ 個体の選択 selection
     ランキング方式を使用する
     ∵fitnessが大きくてもcapacityを超える個体は不良なので
       fitnessの値そのものを個体選択に影響させたくない
    """
    selected_idv = []
    selected_flg = [0 for i in range(GA.rank_tbl.__len__())]
    
    # sel_num < len(rank_tbl)個の個体を選択する
    while selected_idv.__len__() < sel_num:
        # 乱数selectionがテーブルのどこに入るか確認
        selection = np.random.uniform(0, 1)
        for i in range(GA.rank_tbl.__len__()):
            if selection < GA.rank_tbl[i]:
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
    operation_tbl = [GA.CROSSOVER_PROB, 
                     GA.MUTATION_PROB + GA.CROSSOVER_PROB,
                     1.0]
    
    while next_group.__len__() < GA.GROUP_SIZE:
        # オペレーションの選択
        op = np.random.uniform(0, 1)        
        if op < operation_tbl[0]:
            # 交叉 個体を2つ選択する
            sel_idv = select_indivisual(current_group, sel_num=2)
            child_idv1, child_idv2 = sel_idv[0].crossover(sel_idv[1].chrom)

            next_group.append(child_idv1)
            if next_group.__len__() < GA.GROUP_SIZE:
                next_group.append(child_idv2)
        
        elif op < operation_tbl[1]:
            # 突然変異
            sel_idv = select_indivisual(current_group)
            mutant = sel_idv[0].mutation()
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
        GA.converge_counter += 1
    else:
        GA.converge_counter = 0
        
    if GA.converge_counter > GA.CONVERGE_TH-1:
        converged = True
    
    return converged


#%%
# 遺伝的アルゴリズム　メイン処理
#
if __name__ == '__main__':    
    # GA初期化
    GA.create_ranking_table()
    
    # 初期集団を生成する
    current_group = create_group()        
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
    for generation in range(1, GA.GENERATION_LOOP_NUM+1):
        print(f'===== Generation No.{generation} =====')
        #for c_idv in current_group:
        #    c_idv.show_GType()      
        
        most_valuable_idv = current_group[0]
        mvp_for_each_generation.append(most_valuable_idv)
        
        optimum_fitness_list.append(most_valuable_idv.fitness)
        mean_f = 0
        for idv in current_group:
            mean_f += idv.fitness
        mean_fitness_list.append(mean_f / GA.GROUP_SIZE)
        
        """ 選択（淘汰）・交叉・突然変異による次世代の生成 """
        next_group = reproduction(current_group)
        
        # 収束判定
        if is_converged(current_group, next_group) is True:
            break
        
        # 世代交代して次のループ
        current_group.clear()
        current_group.extend(next_group)

        
    # 解（最も優れた個体）の出力
    print('最強個体')
    most_valuable_idv.show_indivisual_info()
    print('finish')
    
    
    # KNAPSACKのときfitnessをプロットしてみる
    if GA.PROBLEM_TYPE == 'KNAPSACK':
        generation_label = [i for i in range(GA.GENERATION_LOOP_NUM + 1)]
        plt.plot(generation_label, mean_fitness_list, marker='o', color='red', markersize=3)
        plt.plot(generation_label, optimum_fitness_list, marker='o', color='blue', markersize=3)
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.show()    
    
    # TSPのとき描画してみる    
    elif GA.PROBLEM_TYPE == 'TSP':
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)     
        
        def update(generation):
            plt.cla()  
            plt.xlim(-1, 11)
            plt.ylim(-1, 11)
            
            mvp = mvp_for_each_generation[generation]
            city_px = []
            city_py = []           
            for (px, py) in mvp.ptype:               
                plt.plot(px, py, marker='o',color='blue', markersize=5)
                city_px.append(px)
                city_py.append(py)
                
            city_px.append(city_px[0])
            city_py.append(city_py[0])
            
            plt.title(f'第{generation+1}世代    fitness={mvp.fitness:.5f}')
            plt.plot(city_px, city_py, color='red')
            if generation == 0:
                fig.savefig(f"{generation+1}gen.png")
            elif generation == 24:
                fig.savefig(f"{generation+1}gen.png")
            elif generation == 49:
                fig.savefig(f"{generation+1}gen.png")
            elif generation == mvp_for_each_generation.__len__()-1:
                fig.savefig(f"{generation+1}gen.png")
               

        ani = anm.FuncAnimation(fig, update, interval=100, frames=mvp_for_each_generation.__len__())        
        ani.save('GA.gif', writer='pillow', fps=10) 

# %%
