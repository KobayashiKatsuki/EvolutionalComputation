# -*- coding: utf-8 -*-
"""
GEの設定

"""

class GESetting():
    
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
