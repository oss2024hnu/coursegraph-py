import strictyaml
from typing import Optional
import gvgen
import sys

def validate_subject(subject: strictyaml.YAML) -> bool:
    """
    주어진 과목 정보가 유효한지 검증합니다.

    Args:
        subject (strictyaml.YAML): 검증할 과목 정보.

    Returns:
        bool: 과목 정보가 유효하면 True, 그렇지 않으면 False.
    """
    required_fields = {'학년', '학기', '과목명', '구분'}
    if not all(field in subject for field in required_fields):
        return False
    if not subject['학년'].isdigit() or not subject['학기'].isdigit():
        return False
    if not isinstance(subject['과목명'], str) or not isinstance(subject['구분'], str):
        return False
    if '선수과목' in subject and not isinstance(subject['선수과목'], list):
        return False
    return True

def print_dot(subjects: strictyaml.YAML, output_file: Optional[str]) -> None:
    """
    주어진 과목 리스트를 DOT 형식으로 출력합니다.

    Args:
        subjects (strictyaml.YAML): 과목 리스트.
        output_file (Optional[str]): DOT 출력을 저장할 파일 경로. None인 경우 콘솔에 출력.
    """
    try:
        # 과목을 학년과 학기에 따라 분류
        nd = {}  # 과목명에서 노드로의 딕셔너리
        sd = {(1,1):[], (1,2):[], (2,1):[], (2,2):[], (3,1):[], (3,2):[], (4,1):[], (4,2):[]}
        for subject in subjects:
            grade = int(subject['학년'])
            semester = int(subject['학기'])
            sd[(grade, semester)].append(subject)
        
        # 그래프 생성
        graph = gvgen.GvGen(options="rankdir=LR;ranksep=1.25;")

        # 노드 스타일 설정
        graph.styleAppend("note", "shape", "note")
        graph.styleAppend("dashed", "style", "invis")

        graph.styleAppend("전선", "color", "blue")
        graph.styleAppend("전기", "color", "red")
        graph.styleAppend("교필", "color", "limegreen")

        # 학기별 서브그래프 생성
        subGitems = [((1,1), graph.newItem("1-1")), ((1,2), graph.newItem("1-2")),
                     ((2,1), graph.newItem("2-1")), ((2,2), graph.newItem("2-2")),
                     ((3,1), graph.newItem("3-1")), ((3,2), graph.newItem("3-2")),
                     ((4,1), graph.newItem("4-1")), ((4,2), graph.newItem("4-2"))]
        subGdict = dict(subGitems)
        nodedict = {(1,1):[], (1,2):[], (2,1):[], (2,2):[], (3,1):[], (3,2):[], (4,1):[], (4,2):[]}

        # 과목 노드 추가
        for key, subG in sorted(subGdict.items(), key=lambda x: x[0], reverse=True):
            for subject in sd[key]:
                node = graph.newItem(subject['과목명'], subG)

                course_type = subject['구분'].data
                if course_type in ["전선", "전기", "교필"]:
                    graph.styleApply(course_type, node)
                else:
                    graph.styleApply("note", node)

                nd[subject['과목명']] = node
                nodedict[key].append(node)

        # 학기별로 연결 노드 추가
        for key, ns in nodedict.items():
            node = graph.newItem("", subGdict[key])
            graph.styleApply("dashed", node)
            nodedict[key].insert(0, node)

        # 학기 사이의 연결 추가
        nodeitems = sorted(nodedict.items(), key=lambda x: x[0])
        for (_, ns1), (_, ns2) in zip(nodeitems, nodeitems[1:]):
            n1, n2 = ns1[0], ns2[0]
            e = graph.newLink(n1, n2)
            graph.styleApply("dashed", e)

        # 선수 과목 연결 추가
        for subject in subjects:
            if '선수과목' not in subject:
                continue
            for prereq in subject['선수과목']:
                graph.newLink(nd[prereq], nd[subject['과목명']])

        # 레전드 추가
        legend = graph.newItem("Legend")
        legend_item = {
            "전선": graph.newItem("전선", legend),
            "전기": graph.newItem("전기", legend),
            "교필": graph.newItem("교필", legend)
        }

        for key, item in legend_item.items():
            graph.styleApply(key, item)

        # DOT 출력
        if output_file is None:
            graph.dot()
        else:
            try:
                with open(output_file, "w", encoding="utf-8") as outfile:
                    graph.dot(outfile)
            except PermissionError:
                print("파일 읽기 권한이 없습니다.", file=sys.stderr)
                return None
            except IOError:
                print("파일 읽기 중 오류가 발생했습니다.", file=sys.stderr)
                return None
            except Exception as e:
                print(f"알 수 없는 오류가 발생했습니다: {e}", file=sys.stderr)
                return None

    except PermissionError:
        print("파일 읽기 권한이 없습니다.", file=sys.stderr)
        return None
    except IOError:
        print("파일 읽기 중 오류가 발생했습니다.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"알 수 없는 오류가 발생했습니다: {e}", file=sys.stderr)
        return None
