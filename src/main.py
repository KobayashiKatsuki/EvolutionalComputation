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

from indivisual import indivisual
from collections import OrderedDict
import GASetting as GA

def CreateGroup(group_size=0, show=False):
    """ 
    集団の生成
    """
    # 重複した個体が生まれないように集合で生成
    group_set = set()    
    i = 0
    while True:
        idv = indivisual()
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
# 遺伝的アルゴリズム　メイン処理
#
if __name__ == '__main__':    
    # 問題設定を取り込む
    ga_setting = GA.GASetting()
    
    # 初期集団を生成する
    group = CreateGroup(group_size=10, show=False)    
    
    # 世代交代ループ
    for generation in range(ga_setting.GENERATION_LOOP_NUM):

        """ 現世代の適応度評価 """
        cur_group_good = {}
        cur_group_bad = {}
        for idv in group:            
            ptype = idv.get_PType()
            f, c = idv.fitness()           
            if c > ga_setting.capacity:
                # 上回るものは問答無用で出来損ない
                cur_group_bad[str(ptype)] = f
            else:
                # cが最大容量を下回るものは良い個体            
                cur_group_good[str(ptype)] = f
        
        #　個体を優秀な順にソートする
        cur_good_sorted = sorted(cur_group_good.items(), key=lambda x:x[1])
        cur_bad_sorted = sorted(cur_group_bad.items(), key=lambda x:x[1])        

        """ 収束判定 """
        # 適応度の前回値と変わらない、変化量が十分小さい、一定世代終えたら
        #　終了してその世代の最も適応度の高い個体を出力
        
        
        
        # 交叉・淘汰・突然変異による次世代の生成
    
    

# %%
