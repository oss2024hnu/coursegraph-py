import strictyaml
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
from matplotlib import font_manager, rc
import matplotlib.font_manager as fm

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

def get_os():
    os_name = os.name
    if os_name == 'nt':
        return "Windows"
    elif os_name == 'posix':
        return "Linux"
    else:
        return "Unknown OS"
    
if(get_os() == "Windows"):
    font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
elif(get_os() == "Linux"):
    font_name = fm.FontProperties(fname="/usr/share/fonts/truetype/nanum/NanumGothic.ttf: NanumGothic:style=Regular").get_name()
    rc('font', family=font_name)
#else: 기타 OS 폰트파일은 필요하면 추가하면 됨.

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
    G = nx.DiGraph()
    adjusted_pos = adjust_coordinates(subjects)
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
    plt.title("과목 이수 체계도")
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