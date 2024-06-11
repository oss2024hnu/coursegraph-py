import pandas as pd
import strictyaml as syaml
import os
import sys
import platform
import matplotlib.pyplot as plt
from fontutil import get_system_font
from matplotlib import font_manager, rc


class ShowTable:
    """
    테이블을 생성하는 Class

    Attributes:
        None

    Methods:
        __init__: 클래스 생성자
        get_system_font: 시스템 폰트 확인
        read_subjects: Yaml 데이터 파싱
        make_data: 테이블 생성
        process_data: 데이터를 처리하고 테이블 생성
    """
    def __init__(self, image_mode, input_filepath, output_filename, width=None, height=None):
        self.font_path = self.get_system_font()
        self.filename = input_filepath
        self.output_filename = output_filename
        self.image_mode = image_mode
        self.width = width or 10  # 기본 너비 설정
        self.height = height or 6  # 기본 높이 설정

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
        except Exception:
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

    def dpi_ratio(self, width, height):
        dpi = width * height
        # if (dpi > 350 or dpi <= 100):
        #     dpi = 350  # 렌더링이 컴퓨터 부하가 걸리면 주석을 풀고 아래의 코드줄을 지울 것.
        dpi = 350
        return dpi

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
            res = self.dpi_ratio(width, height)
            fig, ax = plt.subplots(figsize=(width, height), dpi=res)
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2] * len(df.columns))
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
        """
        필요한 데이터를 가져오는 함수와 데이터로부터 테이블을 생성하는 역할을 연결한다.
        """
        subjects = self.read_subjects()
        if subjects:
            self.make_data(subjects, self.width, self.height)


if __name__ == "__main__":
    # 필요한 인자를 전달하여 객체 생성
    data_processor = ShowTable(image_mode=True, input_filepath="input.yaml", output_filename="output.png", width=10, height=6)
    data_processor.process_data()
