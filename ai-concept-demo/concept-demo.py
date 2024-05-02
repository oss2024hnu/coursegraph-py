import os
import sys
import platform
import strictyaml
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# 시스템 확인 후 폰트 지정 함수
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
            data = strictyaml.load(yaml_data)
            return data['과목']
    except FileNotFoundError:
        print("해당하는 파일이 없습니다.", file=sys.stderr)
        return None
    except strictyaml.YAMLValidationError as e:
        print(f"YAML 데이터가 잘못되어있습니다: {e}", file=sys.stderr)
        return None

# 학년과 학기가 같은 강좌에 대한 좌표 조정 함수
def adjust_coordinates(subjects):
    adjusted_pos = {}
    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        pos_key = (grade, semester)
        if pos_key in adjusted_pos:
            adjusted_pos[pos_key].append(0)
        else:
            adjusted_pos[pos_key] = [0]
    # 겹치는 노드중 하나만 이동하도록 조정 하는 함수
    for pos_key, positions in adjusted_pos.items():
        num_positions = len(positions)
        if num_positions > 1:
            spacing = 0.4
            for i in range(num_positions):
                adjusted_pos[pos_key][i] = (i - (num_positions - 1) / 2) * spacing
    return adjusted_pos

def draw_course_structure(subjects):
    system_fonts = get_system_font()
    if system_fonts:
        font_path = system_fonts[0]
        font_name = font_manager.FontProperties(fname=font_path).get_name()
    else:
        # 무조건 NanumGothic 시도하도록 임시로
        # path를 하드코딩 해놔서 리눅스에서 돌아가지 않음 배포판마다 다른데 ... 빨리 개선 필요
        # # print("시스템 폰트를 찾을 수 없습니다.", file=sys.stderr)
        # # sys.exit(1)
        font_name = "NanumGothic"
        
    G = nx.DiGraph()
    adjusted_pos = adjust_coordinates(subjects)
    plt.figure(figsize=(10,10)) # figure 사이즈 조정
    
    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        #x,y 좌표 조정
        x = grade + adjusted_pos[(grade, semester)].pop(0)  
        y = semester
        G.add_node(subject['과목명'], pos=(x, y))
        if '선수과목' in subject:
            for prereq in subject['선수과목']:
                G.add_edge(prereq, subject['과목명'])

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue",  font_family=font_name, font_size=10, font_weight="bold")
        for edge in G.edges():
            nx.draw_networkx_edges(G, pos, edgelist=[edge], arrowstyle='->', arrowsize=10)
   
    plt.rc('font', family=font_name)
    plt.title("과목 이수 체계도")
    plt.xlabel('학년')
    plt.ylabel('학기')
    plt.xticks(range(1, 5))  # 학년
    plt.yticks(range(1, 3))  # 학기
    plt.grid(True)  # 그리드 표시
    plt.show()

if __name__ == "__main__":
    filename = os.path.join(script_dir, './input.yaml')
    subjects = read_subjects(filename)
    subjects = None
    while subjects is None:
        subjects = read_subjects(filename)
        if subjects is None:
            response = input("다시 시도하시겠습니까? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
            filename = input("파일 경로를 입력하세요: ")
    draw_course_structure(subjects)
