# -*- coding: utf-8 -*-

import io
import re
import sys
import csv

# 段落ストック
line_stock = []
tankas = []

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
for line_number, line in enumerate(input_stream):
    # 改行を除去
    line = line.rstrip()

    # 一行目にタイトルが記されているので、取得する
    if line_number == 0:
        title = line

    # タイトルに応じて先頭の数行を読み飛ばす
    if ((title == '一握の砂'   and line_number > 29)
    or  (title == '悲しき玩具' and line_number > 13)):
        # 空行なら段落の終わりと見てストックをリセットする
        if line == '':
            # 段落が三行ならば短歌と判定して保存する
            if len(line_stock) == 3:
                tankas.append('\n'.join(line_stock))
            line_stock = []
        # 空行でないなら段落ストックに行を追加する
        else:
            line_stock.append(line)

csv_writer = csv.writer(sys.stdout, lineterminator = '\n')

for tanka in tankas:
    # 青空文庫の特殊記法を除去する
    tanka = re.sub(r'(｜|《.+?》|［.+?］)', '', tanka)

    # CSVとして書き出し
    csv_writer.writerow([tanka])
