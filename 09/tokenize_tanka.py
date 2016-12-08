# -*- coding: utf-8 -*-

import sys
import csv
import json
import MeCab

# CSV書き出しを初期化する
csv_writer = csv.writer(sys.stdout, lineterminator = '\n')

# UniDic近代文語辞書を使用する
arguments = [
    '--node-format=%m\\t%f[0]\\t%f[9]\\t%f[7]\\n',
    '--unk-format=%m\\t%f[0]\\t%m\\t%m\\n',
    '--eos-format=',
    '--dicdir=unidic-mecab',
]
mecab = MeCab.Tagger(' '.join(arguments))

# 標準入力からCSVを読み取る
for row in csv.reader(iter(sys.stdin.readline, '')):
    tanka = row[0]
    tokens = []

    # 出力を行に分割する
    lines = mecab.parse(tanka).split('\n')

    for line in lines:
        # 出力は形態素とその情報がタブで区切られている
        token_and_info = line.split('\t')

        # 空行を読み飛ばす
        if len(token_and_info) is not 4:
            continue

        # 品詞と原形を抽出する
        [token, word_class, pronunciation, basic_form] = token_and_info
        basic_form = basic_form.split('-')[0]

        # 補助記号もしくは空白の場合は読み飛ばす
        if word_class == '補助記号' or word_class == '空白':
            continue

        # 形態素・品詞・原形を保存
        tokens.append([token, word_class, pronunciation, basic_form])

    # 形態素列をJSONに変換
    tokens_json = json.dumps(tokens)

    # CSVとして書き出し
    csv_writer.writerow([tanka, tokens_json])
