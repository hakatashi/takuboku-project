ICHIAKU_URL = http://www.aozora.gr.jp/cards/000153/files/816_ruby_5621.zip
KANASHIKI_URL = http://www.aozora.gr.jp/cards/000153/files/815_ruby_20543.zip
UNIDIC_URL = https://dl.dropboxusercontent.com/u/134600/unidic-MLJ_14.zip
RNNLM_URL = https://googledrive.com/host/0ByxdPXuxLPS5RFM5dVNvWVhTd0U/rnnlm-0.4b.tgz

PYTHON = python3

rnnlm/rnnlm: rnnlm
	$(MAKE) -C "$<"

rnnlm: rnnlm.tar.gz
	mkdir -p "$@"
	tar xvzf "$<" -C "$@" --strip-components 1

rnnlm.tar.gz:
	wget "$(RNNLM_URL)" -O "$@" || (rm -f "$@"; return 1)

rnnlm-train%txt rnnlm-test%txt rnnlm-valid%txt: tanka-tokenized.csv create_rnnlm_datasets.py
	$(PYTHON) create_rnnlm_datasets.py rnnlm-train.txt rnnlm-test.txt rnnlm-valid.txt < "$<"

marcov-chained.txt: marcov-dict.json chain_marcov.py
	$(PYTHON) chain_marcov.py < "$<" > "$@"

marcov-dict.json: tanka-tokenized.csv create_marcov_dict.py
	$(PYTHON) create_marcov_dict.py < "$<" > "$@"

tanka-tokenized.csv: tanka.csv unidic-mecab tokenize_tanka.py
	$(PYTHON) tokenize_tanka.py < "$<" > "$@"

unidic-mecab: unidic.zip
	unzip -j -o "$<" "unidic-MLJ_14/Files/dic/unidic-mecab/*" -d "$@"

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
	git clean -Xdf
