# -*- coding: utf-8 -*-

import csv
import sys
import gensim

model = gensim.models.doc2vec.Doc2Vec.load('aozora2vec-iter50.model')

# 標準入力から空白区切りのテキストを読み取る
for rows in csv.reader(iter(sys.stdin.readline, ''), delimiter=' '):
    tokens = ['大股', 'に', '縁側', 'を', '歩く', 'ば'] + rows[1:]
    vector = model.infer_vector(tokens)
    print(' '.join(rows[:1] + list(map(str, vector))))
