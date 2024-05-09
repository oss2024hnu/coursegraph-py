import pandas as pd
import strictyaml as syaml
import os

import platform
import matplotlib.pyplot as plt
from fontutil import get_system_font
from matplotlib import font_manager, rc


class ShowTable:
    def __init__(self, image_mode):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_path = self.get_system_font()
        self.filename = self.input_filename()
        self.image_mode = image_mode

    def input_filename(self):
        input_filename = input("yaml 파일을 입력하세요 (예: me.yaml은 me 입력): ")
        filename = os.path.join(self.script_dir, '../data/', input_filename + '.yaml')
        return filename

    def get_system_font(self):
        try:
            return get_system_font()[1]['file']
        except:
            try:
                return get_system_font()[0]['file']
            except:
                try:
                    return get_system_font()[2]['file']
                except:
                    print("시스템내에 적합한 한글 폰트 파일을 찾을 수 없습니다.")
                    sys.exit(2)
                    
    def read_subjects(self):
        try:
            with open(self.filename, 'r', encoding='UTF8') as file:
                yaml_data = file.read()
                data = syaml.load(yaml_data).data
                return data
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
            return None
        except Exception as e:
            print("파일을 읽는 중 오류가 발생했습니다:", e)
            return None

    def make_data(self, data):
        font_name = font_manager.FontProperties(fname=self.font_path).get_name()
        rc('font', family=font_name)

        if '과목' in data:
            df = pd.DataFrame(data['과목'])
            fig, ax = plt.subplots(figsize=(20, 10))
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2]*len(df.columns))
            ax.set_title('과목 표')
            if self.image_mode:
                filename_without_ext = os.path.splitext(self.filename)[0]
                plt.savefig(filename_without_ext + '_chart_image.png')
            plt.show()
        else:
            print("데이터에 '과목' 정보가 없습니다.")

    def process_data(self):
        subjects = self.read_subjects()
        if subjects:
            self.make_data(subjects)

if __name__ == "__main__":
    data_processor = ShowTable(None)
    data_processor.process_data()
