# PNG 파일을 보관할 디렉터리 변수 이름
OUTDIR:=out

DATA_YAMLS=$(wildcard data/*.yaml)
OUT_YAMLS=$(DATA_YAMLS:data%=$(OUTDIR)%)

OUT_DOTS=$(OUT_YAMLS:%.yaml=%_G.dot)
OUT_GRAPHS=$(OUT_YAMLS:%.yaml=%_G.png)
OUT_TABLES=$(OUT_YAMLS:%.yaml=%_T.png)

PYTHON := $(shell \
  if command -v python3 > /dev/null 2>&1; then \
    echo python3; \
  elif command -v python > /dev/null 2>&1; then \
    echo python; \
  elif where python3 > nul 2>&1; then \
    echo python3; \
  elif where python > nul 2>&1; then \
    echo python; \
  else \
    echo ""; \
  fi \
)
CLICMD=$(PYTHON) coursegraph

.PHONY: test delete

# test 타겟 정의
test: $(OUTDIR) $(OUT_DOTS) $(OUT_GRAPHS) $(OUT_TABLES)

$(OUTDIR):
	mkdir $(OUTDIR)

$(OUTDIR)/%_G.dot: ./data/%.yaml
	$(CLICMD) -f dot $< -o $@ 
	# $(CLICMD) -f dot $< -o $@ -v 1 # 아직 dot에는 verbose level 적용안됨
	# $(CLICMD) -f dot $< -o $@ -v 2 # 아직 dot에는 verbose level 적용안됨
	- dot -Tsvg -O $@  # graphviz dot 유틸리티로 svg생성 (실패해도 넘어감)

$(OUTDIR)/%_G.png: ./data/%.yaml
	$(CLICMD) -f graph $< -o $@ 
	$(CLICMD) -f graph $< -o $@ -v 1
	$(CLICMD) -f graph $< -o $@ -v 2


$(OUTDIR)/%_T.png: ./data/%.yaml
	$(CLICMD) -f table $< -o $@
	$(CLICMD) -f table $< -o $@ -v 1
	$(CLICMD) -f table $< -o $@ -v 2

# clean 타겟 정의
clean_w:
	rmdir /s /q $(OUTDIR)

# delete 타겟 정의
clean_m:
	rm -rf $(OUTDIR)
