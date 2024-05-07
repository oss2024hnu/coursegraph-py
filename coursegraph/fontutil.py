
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

    if system == 'Windows':
        # Windows의 경우, 시스템 폰트 경로로 설정
        for v in flist:
            try:
                fprop = font_manager.FontProperties(fname=v)
                if fprop.get_name() == 'Malgun Gothic':
                    data_list.append({"name": fprop.get_name(), "file": fprop.get_file()})
            except:
                continue
        return data_list
    
    elif system == 'Darwin':
        for v in flist:
            try:
                fprop = font_manager.FontProperties(fname=v)
                if fprop.get_name() == 'Apple SD Gothic Neo':
                    data_list.append({"name": fprop.get_name(), "file": fprop.get_file()})
            except:
                continue
        return data_list
    
    else:
        for v in flist:
            try:
                fprop = font_manager.FontProperties(fname=v)
                if fprop.get_name() == 'NanumGothic':
                    data_list.append({"name": fprop.get_name(), "file": fprop.get_file()})
            except:
                continue
        return data_list