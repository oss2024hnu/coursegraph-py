import strictyaml
from typing import *
import gvgen

def print_dot(subjects: strictyaml.YAML, output_file: Optional[str]) -> None:
    nd = {} # dict from name to node 
    sd = {(1,1):[], (1,2):[], (2,1):[], (2,2):[], (3,1):[], (3,2):[], (4,1):[], (4,2):[]}
    for subject in subjects:
        grade = int(subject['학년'])
        semester = int(subject['학기'])
        sd[(grade, semester)].append( subject )
    
    graph = gvgen.GvGen(options="rankdir=TB;ranksep=1.25;")

    graph.styleAppend("note", "shape", "note") # node shape note

    graph.styleAppend("dashed", "color", "White")
    graph.styleAppend("dashed", "style", "dashed")

    subGitems = [((1,1), graph.newItem("1-1")), ((1,2), graph.newItem("1-2")),
                 ((2,1), graph.newItem("2-1")), ((2,2), graph.newItem("2-2")),
                 ((3,1), graph.newItem("3-1")), ((3,2), graph.newItem("3-2")),
                 ((4,1), graph.newItem("4-1")), ((4,2), graph.newItem("4-2"))]
    subGdict = dict(subGitems)
    nodedict = {(1,1):[], (1,2):[], (2,1):[], (2,2):[], (3,1):[], (3,2):[], (4,1):[], (4,2):[]}
    for key, subG in sorted(subGdict.items(), key=lambda x: x[0], reverse=True):
        for subject in sd[key]:
            node = graph.newItem(subject['과목명'], subG)
            graph.styleApply("note",node)
            nd[subject['과목명']] = node
            nodedict[key].append(node)

    for key, ns in nodedict.items():
        # if len(ns)==0:
             node = graph.newItem("", subGdict[key])
             graph.styleApply("dashed",node)
             nodedict[key].insert(0, node)

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

    if output_file is None:
        graph.dot()
    else:
        with open(output_file, "w", encoding= "utf-8") as outfile:
            graph.dot(outfile)

 
