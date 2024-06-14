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


def adjust_coordinates(subjects: Optional[strictyaml.YAML]) -> Dict[int, List[float]]:
    if subjects is None:
        return {}

    adjusted_pos = {}
    y_min = 0.2  # Y 좌표의 최소값
    y_max = 1.8  # Y 좌표의 최대값

    for subject in subjects:
        grade = int(subject['학년'])
        if grade not in adjusted_pos:
            adjusted_pos[grade] = []
        adjusted_pos[grade].append(0)

    for grade, positions in adjusted_pos.items():
        num_positions = len(positions)
        if num_positions > 0:
            if num_positions == 1:
                adjusted_pos[grade][0] = (y_max + y_min) / 2  # 노드가 하나일 경우 중앙에 배치
            else:
                spacing = (y_max - y_min) / (num_positions - 1) # 노드의 간격 설정
                for i in range(num_positions):
                    adjusted_pos[grade][i] = y_min + i * spacing

    return adjusted_pos

def cliprint(ref: dict):
    sorted_ref = dict(sorted(ref.items()))
    for key, value in sorted_ref.items():
        print(f"{key}: {value}")


def get_edge_color(category: str) -> str:
    colors = {
        '전기': 'red',
        '전선': 'blue',
        '교필': 'green'
    }
    return colors.get(category, 'black')


def draw_course_structure(subjects: Optional[strictyaml.YAML], output_file: str, width: int, height: int):
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
        x = grade
        y = adjusted_pos[grade].pop(0)
        ref[ind] = [(x, y)]
        ind += 1

        G.add_node(subject['과목명'], pos=(x, y))
        if '선수과목' in subject:
            for prereq in subject['선수과목']:
                G.add_edge(prereq, subject['과목명'])

    pos = nx.get_node_attributes(G, 'pos')

    edge_attrs = EdgeAttributes(edgelist=list(G.edges()))

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
        G.add_node(f"{grade}학년", pos=(grade, max_y - 0.1))

    pos = nx.get_node_attributes(G, 'pos')

    for grade in range(1, 5):
        x, y = pos[f"{grade}학년"]
        bbox_props = dict(boxstyle=f"round,pad=0.5", ec='black', lw=2, facecolor='white')
        plt.text(x, y, f"{grade}학년", fontsize=18, ha='center', va='center', fontweight='bold', bbox=bbox_props)

    # 학기 노드 추가
    max_x = max([x for x, y in pos.values()]) - 3.85
    min_y = min([y for x, y in pos.values()])
    max_y = max([y for x, y in pos.values()])
    y_range = max_y - min_y
    semester_positions = [min_y + y_range * 0.33, min_y + y_range * 0.85]

    for semester in range(1, 3):
        G.add_node(f"{semester}학기", pos=(max_x, semester_positions[semester - 1]))

    pos = nx.get_node_attributes(G, 'pos')

    for semester in range(1, 3):
        x, y = pos[f"{semester}학기"]
        bbox_props = dict(boxstyle=f"round,pad=0.5", ec='black', lw=2, facecolor='white')
        plt.text(x, y, f"{semester}학기", fontsize=18, ha='center', va='center', fontweight='bold', bbox=bbox_props)

    nx.draw_networkx_edges(G, pos, edgelist=edge_attrs.edgelist,
                           arrowstyle=edge_attrs.arrowstyle,
                           arrowsize=edge_attrs.arrowsize)

    plt.title("과목 이수 체계도")
    plt.xlabel('학년')
    plt.ylabel('학기')
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.98, top=0.9)
    plt.xticks(range(1, 5))
    plt.yticks(range(1, 3))
    plt.gca().invert_yaxis()
    plt.grid(True)

    min_y = min(y for _, y in pos.values())
    max_y = max(y for _, y in pos.values())
    center_y = (min_y + max_y) / 1.75
    plt.axhline(center_y, color='black', linestyle='-', linewidth=2)

    for grade in range(1, 5):
        if grade % 2 == 0:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightgray', alpha=0.5)
        else:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightblue', alpha=0.5)

    categories = ['전기', '전선', '교필']
    colors = ['red', 'blue', 'green']
    
    patches = []
    for category, color in zip(categories, colors):
        patch = mpatches.Patch(color=color, label=category)
        patches.append(patch)

    plt.legend(handles=patches, loc='lower right', ncol=3, bbox_to_anchor=(1, -0.05), frameon=False)

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

    return ref
