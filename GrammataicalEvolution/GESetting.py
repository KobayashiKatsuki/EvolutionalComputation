# -*- coding: utf-8 -*-
"""
GEの設定

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as anm
from matplotlib.animation import PillowWriter
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

class GESetting():
    # 何世代ループするか
    GENERATION_LOOP_NUM = 200
    # 1世代を形成する集団のサイズ
    POPULATION_SIZE = 100
    # 交叉確率
    CROSSOVER_PROB = 0.8    
    # 突然変異率(必ず 交叉率 + 突然変異率 < 1 とする)
    MUTATION_PROB = 0.15   
    # 遺伝子何個に1個の割合で突然変異させるか（必ず1以上　1だとすべての遺伝子を対立遺伝子に入れ替える）
    MUTATION_RATE = 4
    # トーナメントサイズ
    TOURNAMENT_SIZE = 10
    # 最小コドン長さ
    MIN_CODON_LEN = 10
    # 最大コドン長さ
    MAX_CODON_LEN = 20
    
    
    """
    テストデータセット
    """
    df_testdata = pd.read_excel('dataset.xlsx')
    var_list = [col for col in df_testdata.columns.values if col != 'answer']
    testcase = {} # { 0: {x1: 1, x2: 3}, 1: {x1: 5, x2: -2}, ... }    
    testcase_answer = df_testdata['answer'].to_dict() # { 0: 10, 1: 15, 2: 12, ... }    
    
    testdata_dict = df_testdata.loc[:, [*var_list]].to_dict() 
    for var_name, var_dict in testdata_dict.items():
        for idx, var_value in var_dict.items():
            if idx in testcase.keys():
                testcase[idx][var_name] = var_value
            else:
                tc = {}
                tc[var_name] = var_value
                testcase[idx] = tc    

    
    def __init__(self):
        # 非終端記号
        self.non_terminal = ['<expr>', '<op>', '<var>']        
        # 終端記号
        # 0除算が発生しないように'/'は除いて0.5を追加(割り算を小数点の掛け算とみなす)
        self.terminal = ['+', '-', '*', '(', ')', 'x', '1', '2', '0.5', '0.1']        
        # 開始点        
        self.start_grammer = ['<expr>']
        # プロダクションルール        
        self.prod_rule = {
            '<expr>': [
                    ['<expr>','<op>','<expr>'],
                    ['(','<expr>','<op>','<expr>',')'],
                    ['<var>']
                ],
            '<op>': ['+', '-', '*'],
            '<var>': ['x', '1', '2', '0.5', '0.1']
            }
        
        # 最大ラッピング数
        self.max_wrapping = 10
        # ルール変更のラッピング数
        self.rule_change_wrapping = 2

#%%
    def calc_ge_formula(self, x):
        # 計算したい式をここにかけ！
        formula = "((x*1)*(((((0.1-x)*1)*(((((0.1-x)*1)*x)-x)*0.1))*0.5)*0.1))"
        ans = eval(formula)
        return ans
        

#%%
if __name__ == '__main__':
    ge = GESetting()
    #print(ge.testcase)    
    #print(ge.testcase_answer)
    
    # 計算してグラフを描画する
    x = 0
    ans_arr = []
    for i in range(100):
        ans = ge.calc_ge_formula(x)
        ans_arr.append(ans)
        x += 0.1

    x_label = [i for i in range(100)]
    plt.plot(x_label, ans_arr, marker='o', color='red', markersize=3)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.show()    