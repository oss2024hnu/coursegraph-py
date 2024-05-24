import pandas as pd
import strictyaml as syaml
import os
import sys
import platform
import matplotlib.pyplot as plt
from fontutil import get_system_font
from matplotlib import font_manager, rc


class ShowTable:
    def __init__(self, image_mode, input_filepath, output_filename,width = None, height = None):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_path = self.get_system_font()
        self.filename = input_filepath
        self.output_filename = output_filename
        self.image_mode = image_mode
        self.width = width
        self.height = height 
        
    def get_system_font(self):
        system_fonts = get_system_font()
        try:
            for font_info in system_fonts:
                return font_info['file']
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

    def make_data(self, data, width, height):
        font_name = font_manager.FontProperties(fname=self.font_path).get_name()
        rc('font', family=font_name)

        if '과목' in data:
           df = pd.DataFrame(data['과목'])
           # NaN 값을 빈 문자열로 대체
           df.fillna('', inplace=True)
           fig, ax = plt.subplots(figsize=(width, height))
           ax.axis('off')
           ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2]*len(df.columns))
           ax.set_title('과목 표')
           plt.tight_layout()
           if self.image_mode:
              if self.output_filename:
                plt.savefig(self.output_filename)
           else:
                plt.show()
        else:
            print("데이터에 '과목' 정보가 없습니다.")

    def process_data(self):
        subjects = self.read_subjects()
        if subjects:
            self.make_data(subjects,self.width,self.height)

if __name__ == "__main__":
    data_processor = ShowTable(None, False, False)
    data_processor.process_data()

