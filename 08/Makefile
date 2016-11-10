ICHIAKU_URL = http://www.aozora.gr.jp/cards/000153/files/816_ruby_5621.zip
KANASHIKI_URL = http://www.aozora.gr.jp/cards/000153/files/815_ruby_20543.zip
UNIDIC_URL = https://dl.dropboxusercontent.com/u/134600/unidic-MLJ_14.zip
RNNLM_URL = http://www.fit.vutbr.cz/~imikolov/rnnlm/rnnlm-0.3e.tgz
AOZORA2VEC_URL = https://github.com/hakatashi/aozora2vec/releases/download/20161013/

AOZORA2VEC_MODELS = aozora2vec-iter50.model aozora2vec-iter50.model.syn0.npy aozora2vec-iter50.model.syn1.npy

PYTHON = python3

tanka-takuboku-vectors.txt: infer_takuboku_vectors.py tanka-tokenized.csv $(AOZORA2VEC_MODELS)
	$(PYTHON) infer_takuboku_vectors.py < tanka-tokenized.csv > "$@"

tanka-dummy-vectors.txt: infer_dummy_vectors.py dummy-tanka.txt $(AOZORA2VEC_MODELS)
	$(PYTHON) infer_dummy_vectors.py < dummy-tanka.txt > "$@"

dummy-tanka.txt: marcov-dict.json generate_dummy_tanka.py
	$(PYTHON) generate_dummy_tanka.py < marcov-dict.json > "$@"

tanka-vectors.txt: infer_vectors.py rnnlm-tanka.txt marcov-chained.txt $(AOZORA2VEC_MODELS)
	cat marcov-chained.txt rnnlm-tanka.txt | $(PYTHON) infer_vectors.py > "$@"

$(AOZORA2VEC_MODELS):
	wget "$(AOZORA2VEC_URL)$@" -O "$@" || (rm -f "$@"; return 1)

rnnlm-tanka.txt: filter_rnnlm.py marcov-dict.json rnnlm-generated.txt
	$(PYTHON) filter_rnnlm.py marcov-dict.json < rnnlm-generated.txt > "$@"

rnnlm-generated.txt: rnnlm.model rnnlm/rnnlm
	rnnlm/rnnlm -rnnlm "$<" -gen 100000 -debug 0 > "$@"

rnnlm.model: rnnlm/rnnlm rnnlm-train.txt rnnlm-valid.txt
	rnnlm/rnnlm -train rnnlm-train.txt -valid rnnlm-valid.txt -rnnlm "$@" -debug 2 -hidden 200 -class 100 -bptt 5 -bptt-block 10 -min-improvement 1.001
	touch "$@"

rnnlm/rnnlm: rnnlm
	$(MAKE) -C "$<"

rnnlm: rnnlm.tar.gz
	mkdir -p "$@"
	tar xvzf "$<" -C "$@"
	echo "CC = g++" >> rnnlm/makefile

rnnlm.tar.gz:
	wget "$(RNNLM_URL)" -O "$@" || (rm -f "$@"; return 1)

rnnlm-train%txt rnnlm-valid%txt: tanka-tokenized.csv create_rnnlm_datasets.py
	$(PYTHON) create_rnnlm_datasets.py rnnlm-train.txt rnnlm-valid.txt < "$<"

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
