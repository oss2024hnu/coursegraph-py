import strictyaml
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rc
import sys
from fontutil import get_system_font
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass

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
            data = strictyaml.load(yaml_data)
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
        semester = int(subject['학기'])
        pos_key = (grade, semester)
        if pos_key in adjusted_pos:
            adjusted_pos[pos_key].append(0)
        else:
            adjusted_pos[pos_key] = [0]
    # 겹치는 노드 중 하나만 이동하도록 조정하는 함수
    for pos_key, positions in adjusted_pos.items():
        num_positions = len(positions)
        if num_positions > 1:
            spacing = 0.4
            for i in range(num_positions):
                adjusted_pos[pos_key][i] = (i - (num_positions - 1) / 2) * spacing
    return adjusted_pos

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

    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        # x, y 좌표 조정
        x = grade
        y = semester + adjusted_pos[(grade, semester)].pop(0)

        G.add_node(subject['과목명'], pos=(x, y))
        if '선수과목' in subject:
            for prereq in subject['선수과목']:
                G.add_edge(prereq, subject['과목명'])

    pos = nx.get_node_attributes(G, 'pos')

    # 엣지 속성 설정
    edge_attrs = EdgeAttributes(edgelist=list(G.edges()))

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_family=font_name, font_size=10, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edgelist=edge_attrs.edgelist, arrowstyle=edge_attrs.arrowstyle, arrowsize=edge_attrs.arrowsize)

    plt.title("과목 이수 체계도")
    plt.xlabel('학년')
    plt.ylabel('학기')
    plt.xticks(range(1, 5))  # 학년
    plt.yticks(range(1, 3))  # 학기
    plt.gca().invert_yaxis()
    plt.grid(True)  # 그리드 표시

    # 학년별로 배경색 설정
    for grade in range(1, 5):
        if grade % 2 == 0:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightgray', alpha=0.5)
        else:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightblue', alpha=0.5)

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
