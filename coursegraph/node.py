import networkx as nx

def subjects_matrix_size(subjects):
    grade_semester_dict = {  # 학년과 학기별 인덱스 정의 리스트
        ('1','1'): 0,
        ('1','2'): 1,
        ('2','1'): 2,
        ('2','2'): 3,
        ('3','1'): 4,
        ('3','2'): 5,
        ('4','1'): 6,
        ('4','2'): 7,
        ('5','1'): 8,
        ('5','2'): 9,
        ('6','1'): 10,
        ('6','2'): 11,
    }
    grade = []
    for subject in subjects:
        grade.append(int(subject['학년']))
    columns = [[] for _ in range(max(grade) * 2)]  # define the columns size
    for subject in subjects:
        columns[grade_semester_dict[subject['학년'], subject['학기']]].append(subject['과목명'])
    G = nx.DiGraph()
    for idx, innerlist in enumerate(columns):
        for y, subject in enumerate(innerlist):
            G.add_node(subject, pos=(idx, y))
    return G

