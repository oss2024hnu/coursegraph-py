import strictyaml
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rc
import sys
from fontutil import get_system_font

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

#노드&폰트 크기 비율제어
def adjust_ratio(ratio):
    circle = 1000 * ratio
    font = 1* ratio
    return circle, font

def backcolor(grade):
    for grade in range(1, 5):
        if grade % 2 == 0:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightgray', alpha=0.5)
        else:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightblue', alpha=0.5)

# 데이터 읽어와서 배열로 
# 배열안의 값 : x값 보정치
def add_array(subjects):
    adjusted_pos = {}
    #for subject in subjects:
    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        pos_key = (grade, semester)
        if pos_key in adjusted_pos:
            adjusted_pos[pos_key].append(0)
        else:
            adjusted_pos[pos_key] = [0]
    node_spreading(pos_key,adjusted_pos)
    return adjusted_pos
    #배열뱉음



#그래프 제작중 실질적인 위치값을 제어하는 함수 2개
######################################################################################
#노드 펼치는 함수
def node_spreading(pos_key,adjusted_pos):
    for pos_key, positions in adjusted_pos.items():
        num_positions = len(positions)
        if num_positions > 1:
                spacing = 0.4
                for i in range(num_positions):
                    adjusted_pos[pos_key][i] = (i - (num_positions - 1) / 2) * spacing        

#실질적인 위치를 지정하는 파트
def positioning(grade, semester, adjusted_pos):
    x = grade
    y = semester + adjusted_pos[(grade, semester)].pop(0)
    return x,y
######################################################################################


def render(subjects, output_file):
    G = nx.DiGraph()
    plt.figure(figsize=(10,10)) # figure 사이즈 조정
    font_name = get_system_font()[0]['name']
    rc('font', family = font_name)
    adjusted_pos = add_array(subjects)
    nodescale, fontscale = adjust_ratio(10) #노드와 폰트의 비율 함수 추가


    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        #x,y 좌표 조정
        x,y=positioning(grade,semester, adjusted_pos)
        G.add_node(subject['과목명'], pos=(x, y))

        if '선수과목' in subject:
            for prereq in subject['선수과목']:
                G.add_edge(prereq, subject['과목명'])
        

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, with_labels=True, node_size=nodescale, node_color="skyblue",  font_family=font_name, font_size=fontscale, font_weight="bold")
        for edge in G.edges():
            nx.draw_networkx_edges(G, pos, edgelist=[edge], arrowstyle='->', arrowsize=10)

    backcolor(grade)
    plt.rc('font', family=font_name)

    plt.title("과목 이수 체계도")
    plt.xlabel('학년')
    plt.ylabel('학기')
    plt.xticks(range(1, 5))  # 학년
    plt.yticks(range(1, 3))  # 학기
    
    # Y 축의 중간 지점에 선을 추가
    plt.axhline((max(plt.yticks()[0]) + min(plt.yticks()[0])) / 2, color='gray', linestyle='--')
    
    plt.gca().invert_yaxis()
    plt.grid(True)  # 그리드 표시

    # 학년별로 배경색 설정
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()