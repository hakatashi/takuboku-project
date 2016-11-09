# -*- coding: utf-8 -*-

import csv
import sys
import gensim

# doc2vecのモデルを読み込む
model = gensim.models.doc2vec.Doc2Vec.load('aozora2vec-iter50.model')

# 標準入力から空白区切りのテキストを読み取る
for rows in csv.reader(iter(sys.stdin.readline, ''), delimiter=' '):
    # 入力から単語列を復元する
    tokens = ['大股', 'に', '縁側', 'を', '歩く', 'ば'] + rows[1:]

    # doc2vecを用いて特徴ベクトルを推定する
    vector = model.infer_vector(tokens)

    print(' '.join(rows[:1] + list(map(str, vector))))
