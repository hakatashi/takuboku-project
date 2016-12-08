# -*- coding: utf-8 -*-

import sys
import csv
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import numpy as np

# 引数の数をチェック
if len(sys.argv) != 4:
    print('This program must be called with 4 arguments')
    sys.exit()

# 引数からファイル名を取得
[this_file, dummy_vectors_file, takuboku_vectors_file, tanka_vectors_file] = sys.argv

# ファイルから短歌のベクトルデータを読み取る
dummy_vectors = np.loadtxt(dummy_vectors_file, delimiter=' ')
takuboku_vectors = np.loadtxt(takuboku_vectors_file, delimiter=' ')
tanka_vectors = np.genfromtxt(tanka_vectors_file, delimiter=' ', dtype=None)

# ダミーの短歌と啄木の短歌を結合して入力データとして整形
X = np.concatenate((dummy_vectors, takuboku_vectors))
y = np.concatenate((np.zeros(len(dummy_vectors)), np.ones(len(takuboku_vectors))))

# 学習精度を測るための事前分類機を用意
pre_classifier = SVC(kernel='linear')

# 5分割交差検定で入力データを分割する
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 学習用データで事前分類機を学習
pre_classifier.fit(X_train, y_train)

# テスト用データに対して事前分類機を適用しスコアを報告
print('SVM Score:', pre_classifier.score(X_test, y_test))

# 同じパラメータで今度はすべての入力データを用いて学習を行う
classifier = SVC(kernel='linear', probability=True)
classifier.fit(X, y)

# 「最後の一首」候補の短歌をラベルデータとベクトルデータに分割
tanka_vectors_labels = np.array([list(row)[0] for row in tanka_vectors])
tanka_vectors_data = np.array([list(row)[1:] for row in tanka_vectors])

# 分類機を用いて学習し、それぞれの「啄木の短歌らしさ」を計測する
proba = classifier.predict_log_proba(tanka_vectors_data)

# 「啄木の短歌らしさ」の高い順に並べる
sorted_proba = np.array(sorted(zip(proba, tanka_vectors_labels), key=lambda r:r[0][1]))

# 上位30件を報告
print('\n'.join(['{0:>2}. {1}'.format(i + 1, p[1].decode("utf-8")) for i, p in enumerate(sorted_proba[:30])]))
