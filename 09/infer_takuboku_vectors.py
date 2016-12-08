# -*- coding: utf-8 -*-

import sys
import csv
import json
import gensim

# doc2vecのモデルを読み込む
model = gensim.models.doc2vec.Doc2Vec.load('aozora2vec-iter50.model')

# 標準入力からCSVを読み取る
for row in csv.reader(iter(sys.stdin.readline, '')):
    [tanka, tokens_json] = row
    tokens = list(map(lambda l:l[3], json.loads(tokens_json)))

    # doc2vecを用いて特徴ベクトルを推定する
    vector = model.infer_vector(tokens)

    print(' '.join(list(map(str, vector))))
