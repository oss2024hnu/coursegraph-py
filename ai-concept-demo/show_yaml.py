import pandas as pd
import strictyaml as syaml
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 파일 경로 설정
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
filename = os.path.join(script_dir, './input.yaml')

font_dir = os.path.join(script_dir, './data')
font_path = os.path.join(font_dir, 'malgun.ttf')
font_name = font_manager.FontProperties(fname=font_path).get_name()

# 폰트 설정
plt.rcParams['font.family'] = font_name

# 파일 읽기
try:
    with open(filename, 'r', encoding='UTF8') as file:
        yaml_data = file.read()
        data = syaml.load(yaml_data).data
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
    exit(1)

# 데이터 가공
df = pd.DataFrame(data['과목'])
df['과목명'] = df['과목명']
df['학년'] = df['학년']
df['학기'] = df['학기']
df['선수과목'] = df['선수과목'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')  # 선수과목이 리스트인 경우에만 join 적용
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2]*len(df.columns))
ax.set_title('과목 표')

plt.show()
