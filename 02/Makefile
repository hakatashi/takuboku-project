ICHIAKU_URL = http://www.aozora.gr.jp/cards/000153/files/816_ruby_5621.zip
KANASHIKI_URL = http://www.aozora.gr.jp/cards/000153/files/815_ruby_20543.zip

.PHONY: texts
texts: ichiaku.txt kanashiki.txt

ichiaku.zip:
	wget "$(ICHIAKU_URL)" -O "$@"

kanashiki.zip:
	wget "$(KANASHIKI_URL)" -O "$@"

%.txt: %.zip
	unzip -p "$<" | iconv -f SJIS -t UTF8 > "$@"

.PHONY: clean
clean:
	git clean -xf
