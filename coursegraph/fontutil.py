# 한글 폰트 정보를 가져오는 모듈
# 제발 ttf 파일 path를 하드코딩하지 말 것!!!
<<<<<<< HEAD
=======
import os
import platform
from matplotlib import font_manager
def get_system_font(): # 시스템 확인 후 폰트 지정 함수
    system = platform.system()
    if system == 'Windows':
        font_list = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        font_path= [font for font in font_list if 'malgun.ttf' in font]
        return font_path
    elif system == 'Darwin':
        font_list = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        font_path = [font for font in font_list if 'AppleGothic.ttf' in font]
        if font_path:
            return font_path
        else:
            return None
    elif system == 'Linux':
        font_list = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        font_path = [font for font in font_list if 'NanumGothic.ttf' in font]
        if font_path:
            return font_path
        else:
            return None
    else:
        # 기타 운영 체제의 경우, 적절한 시스템 폰트 경로를 설정해야 합니다. (현재 리눅스의 파일 경로에 맞춰 설정되어있음) ===> 리눅스에 맞지 않음!! 배포판마다 위치 다름 이런 하드코딩 정말 안좋습니다
        # return ['/usr/share/fonts/truetype/NanumGothic.ttf']
        return None
>>>>>>> fontpath_and_img
