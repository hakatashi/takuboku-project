# -*- coding: utf-8 -*-

import csv
import sys
import gensim

# doc2vecのモデルを読み込む
model = gensim.models.doc2vec.Doc2Vec.load('aozora2vec-iter50.model')

# 標準入力から空白区切りのテキストを読み取る
for tokens in csv.reader(iter(sys.stdin.readline, ''), delimiter=' '):
    # doc2vecを用いて特徴ベクトルを推定する
    vector = model.infer_vector(tokens)

    # 出力
    print(' '.join(list(map(str, vector))))
