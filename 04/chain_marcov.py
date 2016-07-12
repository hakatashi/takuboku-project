# -*- coding: utf-8 -*-

import sys
import csv
import json
import math
from random import random

# 標準入力からマルコフ連鎖情報テーブルを取得
marcov_json = sys.stdin.read()
marcov = json.loads(marcov_json)

unigram = marcov['unigram']
bigram = marcov['bigram']

for i in range(100):
    # 復元する短歌を初期トークンとして設定
    tokens = ['大跨に緣側を', '歩け', 'ば']

    # 30形態素ぶん生成する
    for i in range(30):
        # 2-gramが利用可能な場合、70%の確率でそれを利用する
        if tokens[-2] in bigram and tokens[-1] in bigram[tokens[-2]] and random() < .7:
            next_token_dict = bigram[tokens[-2]][tokens[-1]]
        # 1-gramが利用可能な場合、それを利用する
        elif tokens[-1] in unigram:
            next_token_dict = unigram[tokens[-1]]
        # いずれも利用できない場合、そこで終了する
        else:
            break

        # 次の形態素候補からランダムに選択し、形態素列に追加する
        next_tokens = list(next_token_dict.keys())
        next_token = next_tokens[math.floor(random() * len(next_tokens))]
        tokens.append(next_token)

    print(''.join(tokens))
