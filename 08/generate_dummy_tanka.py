# -*- coding: utf-8 -*-

import sys
import json
import random

# 標準入力から単語データを読み取る
marcov_json = sys.stdin.read()
marcov = json.loads(marcov_json)

token_dict = marcov['token_dict']
tokens = list(token_dict.keys())

# 1000個のダミーデータを生成する
for i in range(1000):
    # 1データに含まれる単語の数は12個から23個
    token_count = random.randint(12, 23)
    base_forms = []

    # 単語をランダムに選択
    for j in range(token_count):
        token = random.choice(tokens)
        base_form = token_dict[token][3]
        base_forms.append(base_form)

    # 出力
    print(' '.join(base_forms))
