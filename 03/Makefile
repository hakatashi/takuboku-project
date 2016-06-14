ICHIAKU_URL = http://www.aozora.gr.jp/cards/000153/files/816_ruby_5621.zip
KANASHIKI_URL = http://www.aozora.gr.jp/cards/000153/files/815_ruby_20543.zip
UNIDIC_URL = https://dl.dropboxusercontent.com/u/134600/unidic-MLJ_14.zip

PYTHON = python3

tanka-tokenized.csv: tanka.csv unidic-mecab
	$(PYTHON) tokenize_tanka.py < "$<" > "$@"

unidic-mecab: unidic.zip
	unzip -j "$<" "unidic-MLJ_14/Files/dic/unidic-mecab/*" -d "$@"

unidic.zip:
	wget "$(UNIDIC_URL)" -O "$@" || (rm -f "$@"; return 1)

tanka.csv: ichiaku.csv kanashiki.csv
	cat $^ > "$@"

%.csv: %.txt parse_aozora_text.py
	$(PYTHON) parse_aozora_text.py < "$<" > "$@"

ichiaku.zip:
	wget "$(ICHIAKU_URL)" -O "$@" || (rm -f "$@"; return 1)

kanashiki.zip:
	wget "$(KANASHIKI_URL)" -O "$@" || (rm -f "$@"; return 1)

%.txt: %.zip
	unzip -p "$<" | iconv -f SJIS -t UTF8 > "$@"

.PHONY: clean
clean:
	git clean -Xf
