import pandas as pd
import sys
import strictyaml as syaml
import os
import platform
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc


script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# 파일 경로 설정
#파일의 이름을 받아서 파일의 정보 출력하기
#inpuy.yaml은 출력이 가능하나 다른 파일들은 경로가 달라 경로 지정하고 filename입력
def input_filename():

    input_filename = input("yaml파일을 입력하세요(ex -> me.yaml은 me만 입력)")
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    #input.yaml은 그대로 입력
    #다른 파일들은 경로가 다르기 떄문에 다른 주소로 이동
    if input_filename == 'input':
            filename = os.path.join(script_dir, 'input.yaml')
            
    else:
        filename = os.path.join(script_dir, '../data/' + input_filename + '.yaml')

    font_dir = os.path.join(script_dir, './data')
    font_path = os.path.join(font_dir, 'malgun.ttf')
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    # 폰트 설정
    plt.rcParams['font.family'] = font_name
    return filename

def get_system_font():
    system = platform.system()
    if system == 'Windows':
        # Windows의 경우, 시스템 폰트 경로로 설정
        return ['C:/Windows/Fonts/malgun.ttf']
    elif system == 'Darwin':
        # macOS의 경우, 기본 시스템 폰트 경로 설정 (MacOS 애플고딕의 정확한 이름 표기가 필요함)
        return ['/System/Library/Fonts/AppleGothic.ttf']  
    else:
        # 기타 운영 체제의 경우, 적절한 시스템 폰트 경로를 설정해야 합니다. (현재 리눅스의 파일 경로에 맞춰 설정되어있음) ===> 리눅스에 맞지 않음!! 배포판마다 위치 다름 이런 하드코딩 정말 안좋습니다
        # return ['/usr/share/fonts/truetype/NanumGothic.ttf'] 
        return None

def read_subjects(filename):
    try:
        with open(filename, 'r', encoding='UTF8') as file:
            yaml_data = file.read()
            data = syaml.load(yaml_data).data
            return data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return None
        exit(1)

# 파일 읽기


def make_data(data):
    # 데이터 가공
    df = pd.DataFrame(data['과목'])
    try:
        df['과목명'] = df['과목명']
        df['학년'] = df['학년']
        df['학기'] = df['학기']
        df['트랙'] = df['트랙']
        df['마이크로디그리'] = df['마이크로디그리']
        df['실습여부'] = df['실습여부']
        df['선수과목'] = df['선수과목'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')  # 선수과목이 리스트인 경우에만 join 적용
    except KeyError:    
        
        pass


    fig, ax = plt.subplots(figsize=(20, 10))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2]*len(df.columns))
    ax.set_title('과목 표')

    plt.show()


if __name__ == "__main__":
    filename = input_filename()
    subjects = read_subjects(filename)
    get_system_font()
    data = read_subjects(filename)
    make_data(data)
