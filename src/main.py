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

・集団：　様々な個体の集まり　この中の個体が解空間を探索する

・エンコーディング：　表現型から遺伝子型への変換（符号化）
・デコーディング：　遺伝子型から表現型への変換（複合化）

"""

from indivisual import indivisual

#%%
def create_group(group_size):
    """ 集団の生成 """

    # 重複した個体が生まれないように集合で生成
    group_set = set()    
    i = 0
    while True:
        idv = indivisual()
        group_set.add(idv)
        i += 1
        if group_set.__len__() == group_size: 
            break    
    # 何かと扱いやすいリストで返却する
    return list(group_set)

#%%
# 遺伝的アルゴリズム　メイン処理
#
if __name__ == '__main__':    
    # 集団を生成する
    group_size = 10
    group = create_group(group_size)
    
    for idv in group:        
        idv.show_chromosome()

# %%
