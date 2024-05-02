import argparse
import fontutil
import sys
import os
import strictyaml
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)



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
        font_name = "NanumGothic"

    G = nx.DiGraph()
    adjusted_pos = adjust_coordinates(subjects)
    plt.figure(figsize=(10, 10))  # figure 사이즈 조정

    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        # x,y 좌표 조정
        x = grade + adjusted_pos[(grade, semester)].pop(0)
        y = semester
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
    plt.xlabel('학년')
    plt.ylabel('학기')
    plt.xticks(range(1, 5))  # 학년
    plt.yticks(range(1, 3))  # 학기
    plt.grid(True)  # 그리드 표시
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='A CLI utility for processing data.',
        epilog='Enjoy using the CLI utility!'
    )

    # Adding command line options
    parser.add_argument('-i', '--input', type=str, help='Specify the input file path.')
    parser.add_argument('-o', '--output', type=str, help='Specify the output file path.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')
    args = parser.parse_args()

    # Accessing the command line options
    input_file = args.input
    output_file = args.output
    verbose_mode = args.verbose
    # Perform actions based on options
    if verbose_mode:
        print("Verbose mode enabled.")

    if output_file:
        print(f"Output file path: {output_file}")

    if input_file:
        print(f"Output file path: {output_file}")

    if image_mode:
        print("Image mode enabled.")
    # Add more functionality based on your application needs
    filename = os.path.join(script_dir, '../data/ce.yaml') # 파일 경로설정
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

if __name__ == '__main__':
    main()
