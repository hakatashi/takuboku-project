# -*- coding: utf-8 -*-

import sys
import csv
import json
import random

# 引数の数をチェック
if len(sys.argv) != 3:
    print('This program must be called with 2 arguments')
    sys.exit()

# 引数からファイル名を取得
[this_file, train_file, valid_file] = sys.argv

# 分かち書きされた短歌を格納する配列
tankas = []

# 標準入力からCSVを読み取る
for row in csv.reader(iter(sys.stdin.readline, '')):
    # CSVの内容をパース
    [tanka, tokens_json] = row
    tokens = json.loads(tokens_json)

    # 短歌を空白区切りの形式に変換
    token_texts = []
    for token in tokens:
        token_texts.append(token[0])
    delimited_tanka = ' '.join(token_texts)

    # 配列に短歌を追加
    tankas.append(delimited_tanka)

# 短歌データをシャッフルし、9:1の割合で訓練データと検証データに分割する
random.shuffle(tankas)
tankas_len = len(tankas)
train_tankas_len = int(tankas_len * 0.9)
train_tankas = tankas[0:train_tankas_len]
valid_tankas = tankas[train_tankas_len:tankas_len]

# 改行区切りのテキストデータとして保存
with open(train_file, 'w') as file:
    file.write('\n'.join(train_tankas))

with open(valid_file, 'w') as file:
    file.write('\n'.join(valid_tankas))
