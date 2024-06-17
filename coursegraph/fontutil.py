
# 폰트 관련 파일 모듈화
import pandas as pd
import strictyaml as syaml
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform


def get_system_font():
    flist = font_manager.findSystemFonts()
    data_list = []
    system = platform.system()
    
    font_mapping = {
        'Windows': {'name': 'Malgun Gothic'},
        'Darwin': {'name': 'Apple SD Gothic Neo'},
        'Linux': {'name': 'NanumGothic'}
    }
    
    target_font_name = font_mapping[system]['name']  # 관심 있는 폰트 이름을 설정
    
    for font_path in flist:
        if target_font_name in font_path:  # 폰트 경로에 관심 있는 폰트 이름이 포함되어 있는지 먼저 확인
            try:
                fprop = font_manager.FontProperties(fname=font_path)
                if fprop.get_name() == target_font_name:
                    data_list.append({"name": fprop.get_name(), "file": fprop.get_file()})
            except Exception as e:
                print(f"Error processing font file {font_path}: {e}")
                continue
    
    return data_list
