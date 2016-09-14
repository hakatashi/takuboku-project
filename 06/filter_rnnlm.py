# -*- coding: utf-8 -*-

import re
import sys
import csv
import json

# 引数の数をチェック
if len(sys.argv) != 2:
    print('This program must be called with 2 arguments')
    sys.exit()

# 引数からファイル名を取得
[this_file, marcov_json_file] = sys.argv

# マルコフ連鎖情報テーブルを取得
marcov = json.load(open(marcov_json_file))
token_dict = marcov['token_dict']

# 標準入力から空白区切りのテキストを読み取る
for generated_tokens in csv.reader(iter(sys.stdin.readline, ''), delimiter=' '):
    # 復元する短歌を初期トークンとして設定
    tokens = ['大跨に緣側を', '歩け', 'ば']

    clauses = []

    for next_token in generated_tokens:
        # 空文字列を読み飛ばす
        if len(next_token) == 0:
            break

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

    print(''.join(tokens))
