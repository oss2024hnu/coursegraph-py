
# 폰트 관련 파일 모듈화
import pandas as pd
import strictyaml as syaml
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform


def get_system_font():
    system = platform.system()
    if system == 'Windows':
        # Windows의 경우, 시스템 폰트 경로로 설정
        return ['C:/Windows/Fonts/malgun.ttf']
    elif system == 'Darwin':
        # macOS의 경우, 기본 시스템 폰트 경로 설정 (MacOS 애플고딕의 정확한 이름 표기가 필요함)
        return ['/System/Library/Fonts/AppleSDGothicNeo.ttc']
    else:
        # 기타 운영 체제의 경우, 적절한 시스템 폰트 경로를 설정해야 합니다. (현재 리눅스의 파일 경로에 맞춰 설정되어있음) ===> 리눅스에 맞지 않음!! 배포판마다 위치 다름 이런 하드코딩 정말 안좋습니다
        # return ['/usr/share/fonts/truetype/NanumGothic.ttf']
        return None

