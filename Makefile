# PYTHON 변수 설정
ifeq ($(OS), Windows_NT)
    PYTHON=$(shell where python || where python3)
else
    PYTHON=$(shell which python || which python3)
endif
CLICMD=$(PYTHON) coursegraph

OUTDIR:=out

DATA_YAMLS=$(wildcard data/*.yaml)
OUT_YAMLS=$(DATA_YAMLS:data%=$(OUTDIR)%)

OUT_DOTS=$(OUT_YAMLS:%.yaml=%_G.dot)
OUT_GRAPHS=$(OUT_YAMLS:%.yaml=%_G.png)
OUT_TABLES=$(OUT_YAMLS:%.yaml=%_T.png)

.PHONY: test delete clean_w clean_m

# test 타겟 정의
test: $(OUTDIR) $(OUT_DOTS) $(OUT_GRAPHS) $(OUT_TABLES)

$(OUTDIR):
	mkdir $(OUTDIR)

$(OUTDIR)/%_G.dot: ./data/%.yaml
	$(CLICMD) -f dot $< -o $@ 
#	 $(CLICMD) -f dot $< -o $@ -v 1 # 아직 dot에는 verbose level 적용안됨
#	 $(CLICMD) -f dot $< -o $@ -v 2 # 아직 dot에는 verbose level 적용안됨
	- dot -Tsvg -O $@  # graphviz dot 유틸리티로 svg생성 (실패해도 넘어감)

$(OUTDIR)/%_G.png: ./data/%.yaml
	$(CLICMD) -f graph $< -o $@ 
	$(CLICMD) -f graph $< -o $@ -v 1
	$(CLICMD) -f graph $< -o $@ -v 2

$(OUTDIR)/%_T.png: ./data/%.yaml
	$(CLICMD) -f table $< -o $@
	$(CLICMD) -f table $< -o $@ -v 1
	$(CLICMD) -f table $< -o $@ -v 2

clean:
ifeq ($(OS), Windows_NT)
	rmdir /s /q $(OUTDIR)
else
	rm -rf $(OUTDIR)
endif