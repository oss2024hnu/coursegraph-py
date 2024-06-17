
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
    
    for v in flist:
        try:
            fprop = font_manager.FontProperties(fname=v)
            if fprop.get_name() == font_mapping[system]['name']:
                data_list.append({"name": fprop.get_name(), "file": fprop.get_file()})
        except:
            continue
    
    return data_list
