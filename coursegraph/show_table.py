import pandas as pd
import os
import platform
import matplotlib.pyplot as plt
from show_common import read_yaml, get_system_font, get_script_dir

class ShowTable:
    def __init__(self, image_mode, input_filepath, output_filename):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_path = self.get_system_font()
        self.filename = input_filepath
        self.output_filename = output_filename
        self.image_mode = image_mode

    def input_filename(self):
        input_filename = input("yaml 파일을 입력하세요 (예: me.yaml은 me 입력): ")
        filename = os.path.join(self.script_dir, '../data/', input_filename + '.yaml')
        return filename
                    
    def read_subjects(self):
        subjects = read_yaml(self.filename)
        return subjects

    def make_data(self, data):
        font_name = get_system_font()
        rc('font', family=font_name)

        if '과목' in data:
            df = pd.DataFrame(data['과목'])
            fig, ax = plt.subplots(figsize=(20, 10))
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2]*len(df.columns))
            ax.set_title('과목 표')
            if self.image_mode:
                if self.output_filename:
                    plt.savefig(self.output_filename)
            plt.show()
        else:
            print("데이터에 '과목' 정보가 없습니다.")

    def process_data(self):
        subjects = self.read_subjects()
        if subjects:
            self.make_data(subjects)

if __name__ == "__main__":
    data_processor = ShowTable(None, False, False)
    data_processor.process_data()
