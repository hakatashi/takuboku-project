# -*- coding: utf-8 -*-

import sys
import csv
import json
import random

if len(sys.argv) != 4:
    print('This program must be called with 3 arguments')
    sys.exit()

[this_file, train_file, test_file, valid_file] = sys.argv

tankas = []

# 標準入力からCSVを読み取る
for row in csv.reader(iter(sys.stdin.readline, '')):
    [tanka, tokens_json] = row
    tokens = json.loads(tokens_json)

    token_texts = []
    for token in tokens:
        token_texts.append(token[0])
    delimited_tanka = ' '.join(token_texts)

    tankas.append(delimited_tanka)

random.shuffle(tankas)
tankas_len = len(tankas)
train_tankas_len = int(tankas_len * 0.8)
test_tankas_len = int(tankas_len * 0.9)
valid_tankas_len = int(tankas_len * 1.0)

train_tankas = tankas[0:train_tankas_len]
test_tankas = tankas[train_tankas_len:test_tankas_len]
valid_tankas = tankas[test_tankas_len:valid_tankas_len]

with open(train_file, 'w') as file:
    file.write('\n'.join(train_tankas))

with open(test_file, 'w') as file:
    file.write('\n'.join(test_tankas))

with open(valid_file, 'w') as file:
    file.write('\n'.join(valid_tankas))
