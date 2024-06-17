
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
import logging
from matplotlib.patches import ArrowStyle
# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.error("해당하는 파일이 없습니다.")
        return None
    except PermissionError:
        print("파일 읽기 권한이 없습니다.", file=sys.stderr)
        return None
    except IOError:
        print("파일 읽기 중 오류가 발생했습니다.", file=sys.stderr)
        return None
    except strictyaml.YAMLValidationError as e:
        logger.error(f"YAML 데이터가 잘못되어 있습니다: {e}")
        return None
    except Exception as e:
        print(f"알 수 없는 오류가 발생했습니다: {e}", file=sys.stderr)
        return None


def adjust_coordinates(subjects: Optional[strictyaml.YAML]) -> Dict[int, List[float]]:
    """
    학년과 학기가 같은 강좌에 대한 좌표 조정 함수입니다.

    Parameter:
    subjects (Optional[strictyaml.YAML]): strictyaml.YAML 유형의 데이터를 받습니다.

    return:
    좌표가 조정되어야 할 부분이 dict 자료형으로 반환됩니다.
    """

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

    """
    CLI 상에서 ref 의 값을 출력해주는 함수입니다.
    
    Parameter:
    ref (dict) : 키값이 과목, 학기 들로 구성되어 있는 딕셔너리입니다.

    return:
    해당 함수는 반환값이 없습니다.
    """
    
    sorted_ref = dict(sorted(ref.items()))
    for key, value in sorted_ref.items():
        print(f"{key}: {value}")


def get_edge_color(category: str) -> str:

    """
    각 edge 의 컬러를 결정해주는 함수입니다. category 값을 기반으로 컬러를 결정합니다.

    Parameters:
    category (str) : 과목이 전선, 전기, 교필 중에 무엇인지 알려주는 문자열입니다.

    return:
    colors 에서 알맞은 값을 찾아 해당 컬러의 문자열을 반환해줍니다. 아무것도 해당하지 않는다면 black을 반환합니다.
    """

    colors = {
        '전기': 'red',
        '전선': 'blue'
    }
    return colors.get(category, 'black')


def draw_course_structure(subjects: Optional[strictyaml.YAML], output_file: str, width: int, height: int):
    
    """
    파싱된 데이터를 기반으로, 과목의 위치를 조정하고, matplotlib로 데이터를 그린 후 output_file 경로로 파일을 저장하는 함수입니다.

    Parameters:
    subjects (Optional[strictyaml.YAML]) : 파싱된 과목 부분의 strictyaml.YAML 유형 데이터를 받습니다.
    output_file (str) : 출력 데이터를 저장할 경로와 이름입니다.
    width (int) : 사용자 임의 너비값입니다.
    height (int) : 사용자 임의 높이값입니다.

    return:
    키값쌍이 과목, 학기 로 구성되어 있는 dict 자료형을 반환합니다.
    """

    font_name = get_system_font()[0]['name']

    rc('font', family=font_name)
    G = nx.DiGraph()
    adjusted_pos = adjust_coordinates(subjects)
    plt.figure(figsize=(width, height))  # 사용자가 지정한 이미지 크기로 설정
    ref = {}
    ind = 0

    if subjects is None:
        logger.error("과목 데이터가 없습니다.")
        return
    
    adjusted_pos_1st_semester = {}  # 1학기 과목의 위치를 저장하는 딕셔너리
    adjusted_pos_2nd_semester = {}  # 2학기 과목의 위치를 저장하는 딕셔너리

    # 1학기 과목의 위치 조정
    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        x = grade
        if semester == 1:
            y = adjusted_pos[grade].pop(0) - 0.12 # 1학기 과목의 위치를 조정
            adjusted_pos_1st_semester[subject['과목명']] = (x, y)
        elif semester == 2:
            y = adjusted_pos[grade].pop(0) + 0.12 # 2학기 과목의 위치를 조정
            adjusted_pos_2nd_semester[subject['과목명']] = (x, y)

        G.add_node(subject['과목명'], pos=(x, y))
        if '선수과목' in subject:
            for prereq in subject['선수과목']:
                G.add_edge(prereq, subject['과목명'])

    pos = nx.get_node_attributes(G, 'pos')

    edge_attrs = EdgeAttributes(edgelist=list(G.edges()), arrowsize=20, arrowstyle='->')

    for subject in subjects:
        node = subject['과목명']
        x, y = pos[node]
        plt.text(x, y, node, fontsize=15, ha='center', va='center',
                 bbox=dict(facecolor='white', edgecolor=get_edge_color(subject['구분']), boxstyle='round,pad=0.5',
                           linewidth=3))


    #학년 노드 최상단
    bbox_props = dict(boxstyle=f"round,pad=0.5", ec='black', lw=2, facecolor='white')
    for x in range(1,5):
        plt.text(x,-0.18, f"{x}학년", fontsize=18, ha='center', va='center', fontweight='bold', bbox=bbox_props)
    for y in range(1,3):
        plt.text(0.6,(y-1)+0.5, f"{y}학기", fontsize=18, ha='center', va='center', fontweight='bold', bbox=bbox_props)

    nx.draw_networkx_edges(G, pos, edgelist=edge_attrs.edgelist,
                       arrowstyle=edge_attrs.arrowstyle,
                       connectionstyle='arc3,rad=0',
                       arrowsize=50,
                       min_source_margin=20,
                       min_target_margin=70,
                       width=2.0)

    plt.title("과목 이수 체계도")
    plt.xlabel('학년')
    plt.ylabel('학기')
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.98, top=0.9)
    plt.xticks(range(1, 5)) # 학년
    plt.yticks(range(1, 3)) # 학기
    plt.gca().invert_yaxis()
    plt.grid(True) # 그리드 표시


    plt.axhline(1, color='black', linestyle='-', linewidth=2)


    # 학년별로 배경색 설정
    for grade in range(1, 5):
        if grade % 2 == 0:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightgray', alpha=0.5)
        else:
            plt.axvspan(grade - 0.5, grade + 0.5, color='lightblue', alpha=0.5)

    categories = ['전기', '전선']
    colors = ['red', 'blue']
    
    patches = [] # Patch 객체들을 담을 리스트 초기화

    # 각 범주와 색상 쌍을 처리하여 Patch 객체 생성
    for category, color in zip(categories, colors):
        patch = mpatches.Patch(color=color, label=category)
        patches.append(patch)

    plt.legend(handles=patches, loc='lower right', ncol=3, bbox_to_anchor=(1, -0.05), frameon=False)

    if output_file:
        plt.savefig(output_file)
        print(f"파일이 저장되었습니다: {output_file}")
    else:
        plt.show()

    return ref

