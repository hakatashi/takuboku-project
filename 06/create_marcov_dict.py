# -*- coding: utf-8 -*-

import sys
import csv
import json

# 1-gram、2-gram、形態素情報の情報を格納する変数
unigram = dict()
bigram = dict()
token_dict = dict()

# 標準入力からCSVを読み取る
for row in csv.reader(iter(sys.stdin.readline, '')):
    [tanka, tokens_json] = row
    tokens = json.loads(tokens_json)

    # 1つ前、2つ前の形態素を初期化する
    second_last_token = None
    last_token = None

    # 短歌中のすべての形態素について処理
    for token_info in tokens:
        [token, word_class, pronunciation, basic_form] = token_info
        token_dict[token] = token_info

        if last_token is not None:
            # 1-gramの単語出現情報を記録
            if last_token not in unigram:
                unigram[last_token] = dict()
            if token not in unigram[last_token]:
                unigram[last_token][token] = 0
            unigram[last_token][token] += 1

            if second_last_token is not None:
                # 2-gramの単語出現情報を記録
                if second_last_token not in bigram:
                    bigram[second_last_token] = dict()
                if last_token not in bigram[second_last_token]:
                    bigram[second_last_token][last_token] = dict()
                if token not in bigram[second_last_token][last_token]:
                    bigram[second_last_token][last_token][token] = 0
                bigram[second_last_token][last_token][token] += 1

        second_last_token = last_token
        last_token = token

# 結果をJSONとして出力
sys.stdout.write(json.dumps({
    'unigram': unigram,
    'bigram': bigram,
    'token_dict': token_dict,
}))
