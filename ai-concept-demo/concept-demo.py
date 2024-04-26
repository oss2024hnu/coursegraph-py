import yaml
import networkx as nx
import matplotlib.pyplot as plt
import os
from matplotlib import font_manager, rc

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

font_dir = os.path.join(script_dir, './data')
font_path = os.path.join(font_dir, 'malgun.ttf')
font_name = font_manager.FontProperties(fname=font_path).get_name()

def read_subjects(filename):
    with open(filename, 'rt', encoding='UTF8') as file:
        data = yaml.safe_load(file)
    return data.get('과목', [])

def draw_course_structure(subjects):
    G = nx.DiGraph()
    for subject in subjects:
        G.add_node(subject['과목명'], pos=(subject['학년'], subject['학기']))
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
    filename = './ai-concept-demo/input.yaml'
    subjects = read_subjects(filename)
    draw_course_structure(subjects)
