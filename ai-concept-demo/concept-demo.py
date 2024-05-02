import os
import sys
import platform
import strictyaml
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)


def get_system_font():
    system = platform.system()
    if system == 'Windows':
        return ['C:/Windows/Fonts/malgun.ttf']
    elif system == 'Darwin':
        return ['/System/Library/Fonts/AppleGothic.ttf']
    else:
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


def adjust_coordinates(subjects):
    adjusted_pos = {}
    for subject in subjects:
        grade = int(subject['학년'])
        pos_key = grade
        if pos_key in adjusted_pos:
            adjusted_pos[pos_key].append(0)
        else:
            adjusted_pos[pos_key] = [0]
    for pos_key, positions in adjusted_pos.items():
        num_positions = len(positions)
        if num_positions > 1:
            spacing = 0.4
            base_pos = 0.1

            for i in range(num_positions):
                adjusted_pos[pos_key][i] = (i - (num_positions - 1) / 2)-0.5 * spacing
    return adjusted_pos


def draw_course_structure(subjects):
    system_fonts = get_system_font()
    if system_fonts:
        font_path = system_fonts[0]
        font_name = font_manager.FontProperties(fname=font_path).get_name()
    else:
        font_name = "NanumGothic"

    G = nx.DiGraph()
    adjusted_pos = adjust_coordinates(subjects)
    plt.figure(figsize=(10, 10))

    # 학년별로 다른 배경 색상 지정
    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink']

    for i, grade in enumerate(range(1, 5)):  # 학년 범위에 따라 반복
        plt.axhspan(grade - 0.5, grade + 0.5, facecolor=colors[i], alpha=0.3)  # 학년별로 배경 레이어를 그립니다.

    num_semesters = 1  #구분선
    for semester in range(num_semesters):
        plt.axvline(x=semester * 0.4, color='gray', linestyle='--', linewidth=0.5)  # 학기 수에 따라 조정해야 할 수 있습니다.

    for subject in subjects:
        grade = int(subject['학년'])
        y = grade  # y축에 학년 배치
        x = adjusted_pos[grade].pop(0)  # x축에 학기 배치는 고려하지 않습니다.
        G.add_node(subject['과목명'], pos=(x, y))
        if '선수과목' in subject:
            for prereq in subject['선수과목']:
                G.add_edge(prereq, subject['과목명'])

    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_family=font_name, font_size=10,
            font_weight="bold")
    for edge in G.edges():
        nx.draw_networkx_edges(G, pos, edgelist=[edge], arrowstyle='->', arrowsize=10)

    plt.rc('font', family=font_name)
    plt.title("과목 이수 체계도")
    plt.xlabel('학기')
    plt.ylabel('학년')
    plt.xticks([])  # x축 눈금을 제거합니다.
    plt.yticks(range(1, 5))  # y축 눈금을 학년에 맞게 조정
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    filename = os.path.join(script_dir, './input.yaml')
    subjects = read_subjects(filename)
    draw_course_structure(subjects)
    subjects = None
    while subjects is None:
        subjects = read_subjects(filename)
        if subjects is None:
            response = input("다시 시도하시겠습니까? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
            filename = input("파일 경로를 입력하세요: ")
    draw_course_structure(subjects)
