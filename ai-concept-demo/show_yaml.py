import pandas as pd
import strictyaml as syaml
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform

# 파일 경로 설정
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
filename = os.path.join(script_dir, './input.yaml')

font_dir = os.path.join(script_dir, './data')
font_path = os.path.join(font_dir, 'malgun.ttf')
font_name = font_manager.FontProperties(fname=font_path).get_name()

def get_system_font():
    flist = font_manager.findSystemFonts()
    data_list = []
    system = platform.system()

    if system == 'Windows':
        # Windows의 경우, 시스템 폰트 경로로 설정
        for v in flist:
            try:
                fprop = font_manager.FontProperties(fname=v)
                if fprop.get_name() == 'Malgun':
                    data_list.append({"name": fprop.get_name(), "file": fprop.get_file()})
            except:
                continue
        return [data_list[0]['name']]
    elif system == 'Darwin':
        for v in flist:
            try:
                fprop = font_manager.FontProperties(fname=v)
                if fprop.get_name() == 'Apple SD Gothic Neo':
                    data_list.append({"name": fprop.get_name(), "file": fprop.get_file()})
            except:
                continue
        # macOS의 경우, 기본 시스템 폰트 경로 설정 (MacOS 애플고딕의 정확한 이름 표기가 필요함)
        return [data_list[0]['name']]
    else:
        # 기타 운영 체제의 경우, 적절한 시스템 폰트 경로를 설정해야 합니다. (현재 리눅스의 파일 경로에 맞춰 설정되어있음) ===> 리눅스에 맞지 않음!! 배포판마다 위치 다름 이런 하드코딩 정말 안좋습니다
        # return ['/usr/share/fonts/truetype/NanumGothic.ttf'] 
        return None

# 폰트 설정
plt.rcParams['font.family'] = get_system_font()

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
df['학/강/실'] = df['학/강/실']
df['선수과목'] = df['선수과목'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')  # 선수과목이 리스트인 경우에만 join 적용
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2]*len(df.columns))
ax.set_title('과목 표')

plt.show()
