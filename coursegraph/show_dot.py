import strictyaml
from typing import *
import gvgen

def validate_subject(subject: strictyaml.YAML) -> bool:
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
    nd = {} # dict from name to node 
    sd = {(1,1):[], (1,2):[], (2,1):[], (2,2):[], (3,1):[], (3,2):[], (4,1):[], (4,2):[]}
    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        sd[(grade, semester)].append( subject )
    
    graph = gvgen.GvGen(options="rankdir=LR;ranksep=1.25;")

    graph.styleAppend("note", "shape", "note") # node shape note

    graph.styleAppend("dashed", "color", "White")
    graph.styleAppend("dashed", "style", "dashed")

    graph.styleAppend("전선", "color", "blue")
    graph.styleAppend("전기", "color", "red")
    graph.styleAppend("교필", "color", "limegreen")

    subGitems = [((1,1), graph.newItem("1-1")), ((1,2), graph.newItem("1-2")),
                 ((2,1), graph.newItem("2-1")), ((2,2), graph.newItem("2-2")),
                 ((3,1), graph.newItem("3-1")), ((3,2), graph.newItem("3-2")),
                 ((4,1), graph.newItem("4-1")), ((4,2), graph.newItem("4-2"))]
    subGdict = dict(subGitems)
    nodedict = {(1,1):[], (1,2):[], (2,1):[], (2,2):[], (3,1):[], (3,2):[], (4,1):[], (4,2):[]}

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

    for key in sorted(nodedict.keys()):
        nodes = nodedict[key]
        if not nodes:
            node = graph.newItem("", subGdict[key])
            graph.styleApply("dashed", node)
            nodedict[key].append(node)

    # maxh = max(map(len,nodedict.values()))
    # for key, ns in nodedict.items():
    #     for _ in range(maxh - len(ns)):
    #         node = graph.newItem("\t \t", subGdict[key])
    #         graph.styleApply("dashed",node)
    #         nodedict[key].append( node )

    nodeitems = sorted(nodedict.items(), key=lambda x: x[0])
    for (_,ns1),(_,ns2) in zip(nodeitems, nodeitems[1:]):
            n1,n2 = ns1[0],ns2[0]
        # for n1,n2 in zip(ns1,ns2):
            e = graph.newLink(n1,n2)
            graph.styleApply("dashed",e)

    for subject in subjects:
        if '선수과목' not in subject:
            continue
        for prereq in subject['선수과목']:
            graph.newLink(nd[prereq], nd[subject['과목명']])

    legend = graph.newItem("Legend")
    legend_item = {
        "전선":graph.newItem("전선", legend),
        "전기":graph.newItem("전기", legend),
        "교필":graph.newItem("교필", legend)
    }

    for key, item in legend_item.items():
        graph.styleApply(key, item)

    if output_file is None:
        graph.dot()
    else:
        try:
            with open(output_file, "w", encoding= "utf-8") as outfile:
                graph.dot(outfile)
        except IOError as e:
            print(f"파일을 저장하는 중 오류가 발생했습니다: {e}")
        except Exception as e:
            print(f"예상치 못한 오류가 발생했습니다: {e}")




 
