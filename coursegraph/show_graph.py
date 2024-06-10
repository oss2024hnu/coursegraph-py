import strictyaml
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rc
import sys
from fontutil import get_system_font
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
import matplotlib.patches as mpatches
from schema_checker import schema


@dataclass
class EdgeAttributes:
    edgelist: List[Tuple[str, str]]
    arrowstyle: str = '->'
    arrowsize: int = 10


def read_subjects(filename: str) -> Optional[strictyaml.YAML]:
    """
    파일의 경로로 파일 열기를 시도합니다. 그리고 데이터 파일의 유효성을 검사하여, 에러를 처리하는 함수입니다.

    Parameter:
    filename (str) : 파일의 경로

    return:
    유효한 경우 '과목' 의 키값들을 strictyaml.YAML 유형으로 리턴합니다. 유효하지 않은 경우 None 을 반환합니다.
    """
    try:
        with open(filename, 'r', encoding='UTF8') as file:
            yaml_data = file.read()
            data = strictyaml.load(yaml_data, schema)
            return data['과목']
    except FileNotFoundError:
        print("해당하는 파일이 없습니다.", file=sys.stderr)
        return None
    except strictyaml.YAMLValidationError as e:
        print(f"YAML 데이터가 잘못되어있습니다: {e}", file=sys.stderr)
        return None


def adjust_coordinates(subjects: Optional[strictyaml.YAML]) -> Dict[Tuple[int, int], List[float]]:
    """
    학년과 학기가 같은 강좌에 대한 좌표 조정 함수입니다.

    Parameter:
    subjects (Optional[strictyaml.YAML]): strictyaml.YAML 유형의 데이터를 받습니다.

    return:
    좌표가 조정되어야 할 부분이 dict 자료형으로 반환됩니다.
    """
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
        if num_positions > 0:
            spacing = 0.5
            init = 0

            for i in range(num_positions):
                # 6/3변경점 1
                adjusted_pos[pos_key][i] = init + spacing
                init = adjusted_pos[pos_key][i]

    return adjusted_pos


def cliprint(ref):
    sorted_ref = dict(sorted(ref.items()))
    for key, value in sorted_ref.items():
        print(f"{key}: {value}")


def get_edge_color(category: str):
    colors = {
        '전기': 'red',
        '전선': 'blue',
        '교필': 'green'
    }
    return colors.get(category, 'black')


def draw_course_structure(subjects: Optional[strictyaml.YAML], output_file: str, width: int, height: int):
    """
    파싱된 데이터를 기반으로, 과목의 위치를 조정하고, matplotlib로 데이터를 그린 후 output_file 경로로 파일을 저장하는 함수입니다.

    Parameters:
    subjects (Optional[strictyaml.YAML]) : 파싱된 과목 부분의 strictyaml.YAML 유형 데이터를 받습니다.
    output_file (str) : 출력 데이터를 저장할 경로와 이름입니다.

    return:
    이 함수는 반환값이 없습니다.
    """

    font_name = get_system_font()[0]['name']

    rc('font', family=font_name)
    G = nx.DiGraph()
    adjusted_pos = adjust_coordinates(subjects)
    plt.figure(figsize=(width, height))  # 사용자가 지정한 이미지 크기로 설정
    ref = {}
    ind = 0

    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        # x, y 좌표 조정
        x = grade
        y = adjusted_pos[grade].pop(0)  # + semester : 학기간 간격을 주고싶다면 주석을 풀것.
        ref[ind] = [(x, y)]
        ind += 1

        # print(ref)
        G.add_node(subject['과목명'], pos=(x, y))
        if '선수과목' in subject:
            for prereq in subject['선수과목']:
                G.add_edge(prereq, subject['과목명'])

    pos = nx.get_node_attributes(G, 'pos')

    # 엣지 속성 설정
    edge_attrs = EdgeAttributes(edgelist=list(G.edges()))

    # 노드 라벨 그리기
    for subject in subjects:
        node = subject['과목명']
        x, y = pos[node]
        plt.text(x, y, node, fontsize=15, ha='center', va='center',
                 bbox=dict(facecolor='white', edgecolor=get_edge_color(subject['구분']), boxstyle='round,pad=0.5',
                           linewidth=3))

    # 학년 노드 추가
    non_empty_positions = [max(y_values) for y_values in adjusted_pos.values() if y_values]
    max_y = max(non_empty_positions) if non_empty_positions else 0

    for grade in range(1, 5):
        G.add_node(f"{grade}학년", pos=(grade, max_y - 0.3))

    pos = nx.get_node_attributes(G, 'pos')

    for grade in range(1, 5):
        x, y = pos[f"{grade}학년"]
        bbox_props = dict(boxstyle=f"round,pad=0.5", ec='black', lw=2, facecolor='white')
        plt.text(x, y, f"{grade}학년", fontsize=18, ha='center', va='center', fontweight='bold', bbox=bbox_props)

    # 학기 노드 추가
    max_x = max([x for x, y in pos.values()]) + 0.3  # x 좌표의 최대값
    semester_positions = [1.5, 4.5] # 각 학기의 y 좌표 
    for semester in range(1, 3):  # 1학기, 2학기
        G.add_node(f"{semester}학기", pos=(max_x - 4.15, semester_positions[semester-1]))

    pos = nx.get_node_attributes(G, 'pos')

    for semester in range(1, 3):  # 1학기, 2학기
        x, y = pos[f"{semester}학기"]
        bbox_props = dict(boxstyle=f"round,pad=0.5", ec='black', lw=2, facecolor='white')
        plt.text(x, y, f"{semester}학기", fontsize=18, ha='center', va='center', fontweight='bold', bbox=bbox_props)

    nx.draw_networkx_edges(G, pos, edgelist=edge_attrs.edgelist,
                           arrowstyle=edge_attrs.arrowstyle,
                           arrowsize=edge_attrs.arrowsize)

    plt.title("과목 이수 체계도")
    plt.xlabel('학년')
    plt.ylabel('학기')
    plt.xticks(range(1, 5))  # 학년
    plt.yticks(range(1, 3))  # 학기
    plt.gca().invert_yaxis()
    plt.grid(True)  # 그리드 표시

    min_y = min(y for _, y in pos.values())
    max_y = max(y for _, y in pos.values())
    center_y = (min_y + max_y) / 1.75
    plt.axhline(center_y, color='black', linestyle='-', linewidth=2)

    # 학년별로 배경색 설정
    for grade in range(1, 5):
        if grade % 2 == 0:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightgray', alpha=0.5)
        else:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightblue', alpha=0.5)

    categories = ['전기', '전선', '교필']
    colors = ['red', 'blue', 'green']
    patches = [mpatches.Patch(color=color, label=category) for category, color in zip(categories, colors)]
    plt.legend(handles=patches, loc='lower right', ncol=3, bbox_to_anchor=(1, -0.05), frameon=False)

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

    return ref
