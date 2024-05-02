import pandas as pd
import strictyaml as syaml
import os
import platform
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

def input_filename():
    input_filename = input("yaml 파일을 입력하세요 (예: me.yaml은 me 입력): ")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if input_filename == 'input':
        filename = os.path.join(script_dir, '../ai-concept-demo/data', input_filename + '.yaml')         
    else:
        filename = os.path.join(script_dir, '../data/', input_filename + '.yaml')

    return filename

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
            data = syaml.load(yaml_data).data
            return data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print("파일을 읽는 중 오류가 발생했습니다:", e)
        return None

def make_data(data):

    font_path = get_system_font()[0]
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)


    df = pd.DataFrame(data['과목'])
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2]*len(df.columns))
    ax.set_title('과목 표')
    plt.show()

if __name__ == "__main__":
    filename = input_filename()
    subjects = read_subjects(filename)
    if subjects:
        get_system_font()
        make_data(subjects)
