# PNG 파일을 보관할 디렉터리 변수 이름
OUTDIR:=out

DATA_YAMLS=$(wildcard data/*.yaml)
OUT_YAMLS=$(DATA_YAMLS:data%=$(OUTDIR)%)

OUT_GRAPHS=$(OUT_YAMLS:%.yaml=%_G.png)
OUT_TABLES=$(OUT_YAMLS:%.yaml=%_T.png)

PYTHON=python
CLICMD=$(PYTHON) coursegraph

.PHONY: test delete

# test 타겟 정의
test: $(OUTDIR) $(OUT_GRAPHS) $(OUT_TABLES)

$(OUTDIR):
	mkdir $(OUTDIR)

$(OUTDIR)/%_G.png: ./data/%.yaml
	$(CLICMD) -f graph $< -o $@

$(OUTDIR)/%_T.png: ./data/%.yaml
	$(CLICMD) -f table $< -o $@

# clean 타겟 정의
clean_w:
	rmdir /s /q $(OUTDIR)

# delete 타겟 정의
clean_m:
	rm -rf $(OUTDIR)
