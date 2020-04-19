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

import numpy as np
from indivisual import Indivisual
from GASetting import GASetting as GA

#%% 
def create_group(group_size=0, show=False):
    """ 
    集団の生成
    """
    # 重複した個体が生まれないように集合で生成
    group_set = set()    
    i = 0
    while True:
        idv = Indivisual()
        group_set.add(idv)
        i += 1
        if group_set.__len__() == group_size: 
            break    
    
    if show is True:
        for idv in list(group_set):        
            idv.show_indivisual_info()

    # 何かと扱いやすいリストで返却する    
    return list(group_set)


#%% 
def sort_group_by_fitness(group):
    """
    現世代の集団を適応度に応じてソートする
    """
    good_group = {}
    bad_group = {}
    for idv in group:            
        ptype = idv.get_PType()
        f, c = idv.fitness_and_capacity()           
        if c > GA.capacity:
            # 上回るものは問答無用で出来損ない
            bad_group[str(ptype)] = (f, idv)
        else:
            # cが最大容量を下回るものは良い個体            
            good_group[str(ptype)] = (f, idv)
    
    #　個体を優秀な順にソートする
    good_sorted = sorted(good_group.items(), key=lambda x:x[1][0], reverse=True)
    bad_sorted = sorted(bad_group.items(), key=lambda x:x[1][0]) # badはfが小さいほど良いとする
    
    # ソート結果に応じて現在の集団（リスト）を生成する
    current_group = []
    for ptype, (f, idv) in good_sorted:
        current_group.append(idv)
    for ptype, (f, idv) in bad_sorted:
        current_group.append(idv)
        
    return current_group

#%%
def reproduction(current_group):
    next_group = [Indivisual()]
    
    """ 
    選択 selection
    ランキング方式を使用する
    ∵fitnessが大きくてもcapacityを超える個体は不良なので
      fitnessの値そのものを個体選択に影響させたくない
    """
    # ランキングテーブル生成
    all_fitness = 0
    for idv in current_group:
        all_fitness += idv.fitness
    
    selection = np.random.uniform(0, 1)
    
    
    """ 
    交叉 crossover
    """
    
    
    
    
    """ 
    突然変異 mutation
    """
    
    
    
    return next_group


#%% 収束判定
def is_converged(current_group, next_group):
    """
    適応度の前回値と変わらない、変化量が十分小さい場合は収束と判定
    """
    converged = False
    
    # いずれも先頭が最も適応度が高い個体となるようにソート済みとする
    current_fitness = current_group[0].fitness
    next_fitness = next_group[0].fitness
    
    # 絶対誤差が一定値以下？
    abs_dif = abs(current_fitness - next_fitness)    
    if abs_dif < GA.converged_dif:
        converged = True
    
    return converged


#%%
# 遺伝的アルゴリズム　メイン処理
#
if __name__ == '__main__':    
    # 初期集団を生成する
    #group = create_group(group_size=GA.GROUP_SIZE, show=True)    
    group = create_group(group_size=GA.GROUP_SIZE)        
    # 現世代で最も優れた個体
    most_valuable_idv = Indivisual() # 初期値はランダム
    
    # 世代交代ループ    
    for generation in range(1, GA.GENERATION_LOOP_NUM+1):
        print(f'===== Generation No.{generation} =====')

        """ 現世代の適応度評価 """
        current_group = sort_group_by_fitness(group)
        
        """ 選択（淘汰）・交叉・突然変異による次世代の生成 """
        next_group = reproduction(current_group)
        
        """ 収束判定 """
        most_valuable_idv = current_group[0]
        most_valuable_idv.show_indivisual_info()
        if is_converged(current_group, next_group) is True:
            # 収束なら終了           
            break
        else:
            # 収束していなければ世代交代して次のループ
            group.clear()
            for idv in next_group:
                group.append(idv)

        print('')
        
    # 解（最も優れた個体）の出力
    #most_valuable_idv.show_indivisual_info()
    print('finish')
    
# %%
