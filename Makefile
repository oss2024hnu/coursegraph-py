# PNG 파일을 보관할 디렉터리 변수 이름
DIR_A := A_png
DIR_G := G_png
DIR_T := T_png
# 변수 정의
PP = python
CO = coursegraph
GR = graph
TA = table
DA = data/
MD = mkdir
YY = .yaml
PG = .png
AI = ai_
ME = me_
CE = ce_
IP = input_



.PHONY: test delete

# test 타겟 정의
test: $(DIR_A) $(DIR_G) $(DIR_T) $(IP)$(GR)$(PG) $(IP)$(TA)$(PG) $(CE)$(GR)$(PG) $(CE)$(TA)$(PG) $(ME)$(GR)$(PG) $(ME)$(TA)$(PG) $(AI)$(GR)$(PG) $(AI)$(TA)$(PG)

$(DIR_A):
	$(MD) $(DIR_A)

$(DIR_G): $(DIR_A)
	$(MD) $(DIR_A)\$(DIR_G)

$(DIR_T): $(DIR_A)
	$(MD) $(DIR_A)\$(DIR_T)

$(IP)$(GR)$(PG):
	$(PP) $(CO) -f $(GR) -i $(DA)input$(YY) -o $(DIR_A)\$(DIR_G)\$(IP)$(GR)$(PG)

$(IP)$(TA)$(PG):
	$(PP) $(CO) -f $(TA) -i $(DA)input$(YY) -o $(DIR_A)\$(DIR_T)\$(IP)$(TA)$(PG)

$(CE)$(GR)$(PG):
	$(PP) $(CO) -f $(GR) -i $(DA)ce$(YY) -o $(DIR_A)\$(DIR_G)\$(CE)$(GR)$(PG)

$(CE)$(TA)$(PG):
	$(PP) $(CO) -f $(TA) -i $(DA)ce$(YY) -o $(DIR_A)\$(DIR_T)\$(CE)$(TA)$(PG)

$(ME)$(GR)$(PG):
	$(PP) $(CO) -f $(GR) -i $(DA)me$(YY) -o $(DIR_A)\$(DIR_G)\$(ME)$(GR)$(PG)

$(ME)$(TA)$(PG):
	$(PP) $(CO) -f $(TA) -i $(DA)me$(YY) -o $(DIR_A)\$(DIR_T)\$(ME)$(TA)$(PG)

$(AI)$(GR)$(PG):
	$(PP) $(CO) -f $(GR) -i $(DA)ai$(YY) -o $(DIR_A)\$(DIR_G)\$(AI)$(GR)$(PG)

$(AI)$(TA)$(PG):
	$(PP) $(CO) -f $(TA) -i $(DA)ai$(YY) -o $(DIR_A)\$(DIR_T)\$(AI)$(TA)$(PG)

# delete 타겟 정의
delete_w:
	rmdir /s /q $(DIR_A)

# delete 타겟 정의
delete_m:
	rm -rf $(DIR_A)
