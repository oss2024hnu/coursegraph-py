import pandas as pd
import strictyaml as syaml
import os
import sys
import platform
import matplotlib.pyplot as plt
from fontutil import get_system_font
from matplotlib import font_manager, rc
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ShowTable:
    """
    테이블을 생성하는 Class

    Attributes:
        None

    Methods:
        __init__: 클래스 생성자
        get_system_font: 시스템 폰트 확인
        read_subjects: Yaml 데이터 파싱
        make_data:
        process_data:
    """
    def __init__(self, image_mode, input_filepath, output_filename,width = None, height = None):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_path = self.get_system_font()
        self.filename = input_filepath
        self.output_filename = output_filename
        self.image_mode = image_mode
        self.width = width
        self.height = height 
        
    def get_system_font(self):
        """
        시스템 폰트의 파일 경로를 가져옵니다.
        사용 가능한 시스템 폰트를 검색하여 첫 번째로 찾은 폰트의 파일 경로를 반환합니다.

        Return:
            str: 첫 번째로 찾은 시스템 폰트의 파일 경로.

        Raises:
            SystemExit: 시스템 내에 적합한 한글 폰트 파일을 찾을 수 없는 경우, 오류 메시지를 출력하고 상태 코드 2로 프로그램이 종료됩니다.
        """
        system_fonts = get_system_font()
        try:
            for font_info in system_fonts:
                return font_info['file']
        except:
            print("시스템내에 적합한 한글 폰트 파일을 찾을 수 없습니다.")
            sys.exit(2)
                    
    def read_subjects(self):
        """
        테이블을 생성하는데 있어서 필요한 데이터를 가져옵니다.
        파일을 UTF-8로 읽고 Yaml 데이터로 파싱합니다.

        Returns:
            UTF-8로 인코딩 된 Yaml 데이터를 파싱해 반환합니다.
            오류가 발생한 경우 None 을 반환합니다.

        Raises:
            FileNotFoundError: 파일을 찾을 수 없는 경우, 오류 메시지를 출력하고 None을 반환합니다.
            Exception: 파일을 읽는 중 다른 오류가 발생한 경우, 오류 메시지와 예외 정보를 출력하고 None을 반환합니다.
        """
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
        """
        데이터로부터 테이블을 생성하거나 이미지를 저장한다.

        Args:
            data: 테이블 생성의 데이터, '과목' 키가 포함되어야함
            width: 생성될 테이블의 너비 
            height: 생성될 테이블의 높이
        """
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
                if self.output_filename.endswith('.pdf'):
                    self.create_pdf(df)
                else:
                    self.create_image(df, width, height)
           else:
                plt.show()
        else:
            print("데이터에 '과목' 정보가 없습니다.")

    def create_pdf(self, df):
        c = canvas.Canvas(self.output_filename, pagesize=letter)
        c.setFont("Helvetica", 10)
        width, height = letter

        x_offset = 50
        y_offset = height - 50
        c.drawString(x_offset, y_offset, "과목 표")
        y_offset -= 30

        for i, col in enumerate(df.columns):
            c.drawString(x_offset + i * 100, y_offset, col)

        y_offset -= 20
        for index, row in df.iterrows():
            for i, item in enumerate(row):
                c.drawString(x_offset + i * 100, y_offset, str(item))
            y_offset -= 20

        c.save()

    def process_data(self):
        """
        필요한 데이터를 가져오는 함수와 데이터로부터 테이블을 생성하는 역할을 연결한다.
        """
        subjects = self.read_subjects()
        if subjects:
            self.make_data(subjects,self.width,self.height)

if __name__ == "__main__":
    data_processor = ShowTable(None, False, False)
    data_processor.process_data()
