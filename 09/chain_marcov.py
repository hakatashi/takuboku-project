# -*- coding: utf-8 -*-

import re
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
token_dict = marcov['token_dict']

tankas = 0

# 短歌が100個たまるまで実行する
while tankas < 1000:
    # 復元する短歌を初期トークンとして設定
    tokens = ['大跨に緣側を', '歩け', 'ば']

    clauses = []

    # 最大で30形態素ぶん生成する
    for i in range(30):
        # 2-gramが利用可能な場合、70%の確率でそれを利用する
        if (tokens[-2] in bigram and
            tokens[-1] in bigram[tokens[-2]] and
            random() < .7):
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

        # 形態素の品詞情報などを取得する
        next_token_speech = token_dict[next_token][1]
        previous_token_speech = token_dict[tokens[-2]][1]
        next_token_pronounce = token_dict[next_token][2]
        next_token_length = len(re.sub(r'[ァィゥェォャュョ]', r'', next_token_pronounce))

        if (
            # 付属語を前の文節に追い込む
            next_token_speech in ['助詞', '助動詞'] or
            # 前の形態素が接頭辞の場合は前の文節に追い込む
            previous_token_speech == '接頭辞' or
            # 動詞が連続する場合は前の文節に追い込む
            (previous_token_speech == '動詞' and next_token_speech == '動詞')):

            if len(clauses) == 0:
                clauses.append(0)

            clauses[-1] += next_token_length
        else:
            clauses.append(next_token_length)


    # 文節分けしたデータを57577の形に合うように当てはめていく
    target_regions = [5, 7, 7]
    generated_regions = [0]

    for clause in clauses:
        if (len(generated_regions) == 3 or
            generated_regions[-1] < target_regions[len(generated_regions) - 1]):
            generated_regions[-1] += clause
        else:
            generated_regions.append(clause)

    if len(generated_regions) != 3:
        continue

    # 字余りと字足らずの量を計算する
    jitarazu = 0
    jiamari = 0

    for (region, target_region) in zip(generated_regions, target_regions):
        if region < target_region:
            jitarazu += target_region - region
        if region > target_region:
            jiamari += region - target_region

    # 字余りが1以内でない場合は切り捨てる
    if jitarazu > 0 or jiamari > 1:
        continue

    rows = [''.join(tokens)]
    for token in tokens[3:]:
        rows.append(token_dict[token][3])

    print(' '.join(rows))

    tankas += 1
