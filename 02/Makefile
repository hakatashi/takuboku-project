ICHIAKU_URL = http://www.aozora.gr.jp/cards/000153/files/816_ruby_5621.zip
KANASHIKI_URL = http://www.aozora.gr.jp/cards/000153/files/815_ruby_20543.zip

PYTHON = python3

tanka.csv: ichiaku.csv kanashiki.csv
	cat $^ > "$@"

%.csv: %.txt parse_aozora_text.py
	$(PYTHON) parse_aozora_text.py < "$<" > "$@"

.PHONY: texts
texts: ichiaku.txt kanashiki.txt

ichiaku.zip:
	wget "$(ICHIAKU_URL)" -O "$@" || (rm -f "$@"; return 1)

kanashiki.zip:
	wget "$(KANASHIKI_URL)" -O "$@" || (rm -f "$@"; return 1)

%.txt: %.zip
	unzip -p "$<" | iconv -f SJIS -t UTF8 > "$@"

.PHONY: clean
clean:
	git clean -xf
