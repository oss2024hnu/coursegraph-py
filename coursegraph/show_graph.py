import networkx as nx
import matplotlib.pyplot as plt
import sys
from show_common import read_yaml, get_system_font
from fontutil import get_system_font

 def read_subjects(self):
        subjects = read_yaml(self.filename)
        return subjects

# 학년과 학기가 같은 강좌에 대한 좌표 조정 함수
def adjust_coordinates(subjects):
    script_dir = get_script_dir()
    font_name = get_system_font()

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

def draw_course_structure(subjects, output_file):
    font_name = get_system_font()
        
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
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

